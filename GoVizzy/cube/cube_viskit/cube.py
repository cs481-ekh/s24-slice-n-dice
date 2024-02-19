import numpy as np
from ase import Atoms
from ase.units import Bohr
from scipy.interpolate import RegularGridInterpolator
from itertools import product
from dataclasses import dataclass, field, fields
from struct import pack, error as struct_error
from .graph import Graph


@dataclass
class Cube:
    """
    A data class for storing and manipulating cube files. Contains cell basis,
    atomic basis, and scalar field data.

    atoms: ase.Atoms
        Atoms object constructed from cell and atomic positions in cube file.

    bonds: tuple, shape(M,2)
        Pairs of indices that are first nearest neighbors in self.atoms

    grid: np.ndarray, shape [3, Nx, Ny, Nz]
        Rank 4 array that contains the cartesian coordinates of the numerical
        grid in units of Bohr.

    data3D: np.ndarray, shape [Nx, Ny, Nz]
        Rank 3 array that contains scalar field data on the corresponding grid.

        If charge data, in units of 'e'.
        If potential data, in units of 'Ry/e'.

    cell: np.ndarray, shape [3, 3]
        Each column contains a basis vector of the supercell in units of Bohr.

    origin: np.ndarray, shape[1, 3]
        origin of the supercell / atoms.

    TODO
    ----
    + Add a method for adding, subtracting, scaling cube files
      -> e.g., Allow for density difference plots
    + Add method for getting polyhedra
    + Test the interpolator method and save the output to a new cube object
    + Add method to write cube files (or other file formats?)
    """

    fname: str = ''
    scaling_factor: float = 1.1
    units: str = 'Bohr'
    atoms: list[tuple] = field(default_factory=list, repr=False)
    bonds: list[tuple] = field(default_factory=list, repr=False)
    cell: list[tuple] = field(default_factory=list, repr=False)
    data3D: list[tuple] = field(default_factory=list, repr=False)
    grid: list[tuple] = field(default_factory=list, repr=False)
    origin: list[tuple] = field(default_factory=list, repr=False)
    prefix: str = field(default_factory=str, repr=False)

    def load_cube(self, fname='', units='Bohr'):
        """
        load_cube(cube_file)

        Extracts numerical data from Gaussian *.cube files. Atomic units are assume

        Parameters
        ----------
        units: string, optional (default='Bohr')

        Returns
        -------
        None

        References
        ----------
        [1] http://www.gaussian.com/g_tech/g_ur/u_cubegen.htm

        To Do
        -----
        -> Nothing for the moment.
        """

        if fname:
            self.fname = fname
        assert self.fname, "No filename provided."

        print(f"Loading {self.fname} ...")

        self.prefix = self.fname.split('.')[0]
        self.units = units

        with open(self.fname, 'r') as f:
            contents = f.readlines()

        # -- Parse the header of the cube file
        del contents[0:2]  # remove first 2 comment lines
        tmp = contents[0].split()
        num_atoms, origin = int(tmp[0]), np.array(list(map(float, tmp[1:])))
        self.origin = origin
        header = contents[1:num_atoms+4]
        N1 = int(header[0].split()[0])
        N2 = int(header[1].split()[0])
        N3 = int(header[2].split()[0])
        R1 = list(map(float, header[0].split()[1:4]))
        R2 = list(map(float, header[1].split()[1:4]))
        R3 = list(map(float, header[2].split()[1:4]))

        # -- Get supercell dimensions
        basis = np.array([R1, R2, R3], dtype='d').T  # store vectors as columns
        scalars = np.array([N1, N2, N3], dtype='d')
        self.cell = basis * scalars  # broadcasting

        # -- Create an ASE Atoms object
        tmp = np.array([line.split() for line in header[3:]], dtype='d')
        numbers = tmp[:, 0].astype(int)
        positions = tmp[:, 2:] * Bohr
        self.atoms = Atoms(
            numbers=numbers, positions=positions, cell=self.cell.T)

        # -- Construct the grid
        mesh = np.mgrid[0:N3, 0:N2, 0:N1]
        self.grid = np.einsum('ij,jklm->imlk', basis, mesh) + \
            origin[:, None, None, None]

        # -- Isolate scalar field data
        del contents[0:num_atoms+4]
        data1D = np.array([float(val)
                          for line in contents for val in line.split()])
        self.data3D = data1D.reshape((N3, N2, N1), order='F')

        print("Done.")

    def create_interpolator(self):
        # Extract the grid points along each axis
        x = np.linspace(self.origin[0], self.origin[0] +
                        self.cell[0, 0], self.data3D.shape[0])
        y = np.linspace(self.origin[1], self.origin[1] +
                        self.cell[1, 1], self.data3D.shape[1])
        z = np.linspace(self.origin[2], self.origin[2] +
                        self.cell[2, 2], self.data3D.shape[2])
        interpolator = RegularGridInterpolator(
            (x, y, z), self.data3D, method='linear', bounds_error=False, fill_value=None)
        return interpolator

    def get_bonds(self, do_mic=True):
        """
        Constructs an adjacency matrix describing the connectivity
        within the system.

        Parameters
        ----------
        do_mic: bool, optional (default=True)
        """

        g = Graph(self.atoms)
        g.gen_adj_matrix(do_mic=do_mic)
        nat = len(self.atoms)
        self.bonds = tuple([(i, j) for i in range(nat)
                           for j in range(i) if g.graph[i, j] == 1])

    def get_polyhedra(self, do_mic=True):
        """
        Identifies polyhedra within the stucture
        """
        pass

    def repeat(self, N1, N2, N3):
        """
        Repeats the supercell by factors N1, N2, N3 in the A, B, C directions,
        respectively.

        fname: str = ''
        scaling_factor: float = 1.1
        units: str = 'Bohr'
        atoms: list[tuple] = field(default_factory=list, repr=False)
        bonds: list[tuple] = field(default_factory=list, repr=False)
        cell: list[tuple] = field(default_factory=list, repr=False)
        data3D: list[tuple] = field(default_factory=list, repr=False)
        grid: list[tuple] = field(default_factory=list, repr=False)
        origin: list[tuple] = field(default_factory=list, repr=False)
        prefix: str = field(default_factory=str, repr=False)

        """

        # -- Make a copy of the object
        new_cube = Cube()
        for field in fields(Cube):
            setattr(new_cube, field.name, getattr(self, field.name))

        # -- Scale the atoms
        new_cube.atoms *= (N1, N2, N3)

        # -- Repeat the density data
        s = new_cube.data3D.shape
        new_s = (N1 * s[0], N2 * s[1], N3 * s[2])
        new_data3D = np.empty(new_s)
        for i, j, k in product(range(N1), range(N2), range(N3)):
            imin, imax = i * s[0], (i+1) * s[0]
            jmin, jmax = j * s[1], (j+1) * s[1]
            kmin, kmax = k * s[2], (k+1) * s[2]
            new_data3D[imin:imax, jmin:jmax, kmin:kmax] = self.data3D[:, :, :]

        new_cube.data3D = new_data3D

        # -- Generate the new grid
        N1_ = N1 * s[0]
        N2_ = N2 * s[1]
        N3_ = N3 * s[2]
        origin = self.origin
        basis = self.cell / np.array([N1, N2, N3])

        mesh = np.mgrid[0:N3_, 0:N2_, 0:N1_]
        new_cube.grid = np.einsum('ij,jklm->imlk', basis, mesh) + \
            origin[:, None, None, None]

        return new_cube

    def write_df3(self, df3_file=None, log_scale=False, do_abs=False,
                  eps=1.E-6
                  ):
        """
        Extracts 3D scalar field data from an array and writes
        a 3D bitmap file in the POVRAY *.df3 format.

        Parameters
        ----------
        df3_file: string, optional
           The name of the *.df3 file. If None, self.prefix.df3 is used.

        log_scale: boolean, optional
            Write the logarithm (base 10) of the data to the bitmap file.
            If negative values are present, the code exits without Writing
            the bitmap file.

        eps : float, optional
            Numerical tolerance for converting a strictly positive
            scalar quantity (e.g., an electron density) to a positive value.
            Used when log_scale = True.

        Returns
        -------
        <None>

        References
        ----------
        [1] http://www.povray.org/documentation/view/3.6.1/374/
        [2] http://paulbourke.net/miscellaneous/povexamples/
        [3] https://en.wikipedia.org/wiki/Integer_(computer_science)

        To Do
        -----
        [1]  Could be a problem for users on 32 bit systems, currently using
             64 bit integrs for the bitmap by default.
        [2]  For large data sets it could be faster to write in chunks.

        NOTE:
        -----
        Old version of code transposed data3D when reading the file. Here we do it in the beginning.
        """

        # df3 files expect inner loop on x, middle loop on y, and outer loop on z
        data3D = self.data3D.copy()
        data3D = np.ascontiguousarray(data3D.T)

        if df3_file is None:
            df3_file = self.prefix + ".df3"

        if do_abs:
            data3D = np.abs(data3D)

        if log_scale:
            idx = np.where(np.abs(data3D) < eps)
            data3D[idx] = np.abs(data3D[idx])
            assert np.all(data3D > 0), "log_scale: data3D <= 0 (must be >0)"
            data3D = np.log10(data3D)

        # -- Get grid information
        nx, ny, nz = data3D.shape
        lmin = np.amin(data3D)
        lmax = np.amax(data3D)

        # -- If minimum of density data is < 0, shift data by abs(lmin)
        if lmin < 0:
            data3D += np.abs(lmin)
            # -- get new lmin, lmax
            lmin = np.amin(data3D)  # should be 0.00 now.
            lmax = np.amax(data3D)

        # -- scale data to a 4-byte [32-bit] (unsigned long) int
        data3D = (data3D / lmax * 4294967295.).astype(int)

        with open(df3_file, 'wb') as df3:
            # NOTE: Mac OS X uses the LP64 data model for which integers
            # are 32-bit (4 bytes) and longs and pointers are 64-bit (8 bytes).
            # Machines which use the ILP32 data model set integers, long
            # integers, and pointers to be 32-bit quantities.
            #
            # The density data in df3 files can be 8-, 16- or 32-bit integers.
            # Therefore, struct format on Mac OS X: use '>I' for big endian
            # 32 bit integer (unsigned long int).  On machines which use ILP32
            # data models, use '>L' format string in struct.pack().
            #
            # This may need to be tested before using.
            #
            # 6 byte header of 3 16-bit integers
            df3.write(pack('>HHH', nx, ny, nz))
            for k, j, i in product(range(nz), range(ny), range(nx)):
                val = data3D[i, j, k]
                try:
                    df3.write(pack('>I', val))
                except struct_error:
                    print("In write_df3(): val = {} out of range".format(val))
                    print("Exiting now.")
                    return

    # def write_cube(self, fname, grid, scalar_data, atom_data, cell_data, origin,
    #             use_ff=False
    #             ):
    #     """
    #     Writes a Gaussian cube file.
    #     """

    #     # -- Prepare the cube file header
    #     nat, _ = atom_data.shape
    #     nx, ny, nz = scalar_data.shape
    #     header = "Cubefile created from cube_viskit"
    #     header += "Contains the selected quantity on a FFT grid\n"

    #     # -- Write the cell geometry
    #     format_string = "{:>5d}{:>12.6f}{:>12.6f}{:>12.6f}\n"
    #     header += format_string.format(nat, *origin)
    #     header += format_string.format(nx, *(cell_data[0, :] / nx))
    #     header += format_string.format(ny, *(cell_data[1, :] / ny))
    #     header += format_string.format(nz, *(cell_data[2, :] / nz))

    #     # -- Write the atom data
    #     format_string = "{:>5d}{:>12.6f}{:>12.6f}{:>12.6f}{:>12.6f}\n"
    #     for i in range(nat):
    #         header += format_string.format(int(atom_data[i, 0]), *atom_data[i, 1:])

    #     # -- Prepare the cube file scalar data block
    #     block = ""
    #     scalar_data = np.asfortranarray(scalar_data)

    #     if use_ff:
    #         # -- Use Fortran's scientific notation
    #         # NOTE: THIS IS SLOW! and probably not necessary
    #         import fortranformat as ff

    #         x = ff.FortranRecordWriter('(1E13.5)')
    #         for ix in range(nx):
    #             for iy in range(ny):
    #                 for iz in range(nz):
    #                     block += x.write([scalar_data[ix, iy, iz]])
    #                     if iz % 6 == 5:
    #                         block += "\n"
    #                 block += "\n"
    #     else:
    #         # -- Use python's scientific notation
    #         for ix in range(nx):
    #             for iy in range(ny):
    #                 for iz in range(nz):
    #                     block += " {:>12.5E}".format(scalar_data[ix, iy, iz])
    #                     if iz % 6 == 5:
    #                         block += "\n"
    #                 block += "\n"

    #     with open(fname, 'w') as f:
    #         f.write(header)
    #         f.write(block)

    #     return
