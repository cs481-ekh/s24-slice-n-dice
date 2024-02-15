import numpy as np
from ase import Atoms
from ase.neighborlist import NeighborList, natural_cutoffs, neighbor_list


class Graph:
    """
    Class with methods for generating simple graph represtations of an atomic
    configuration stored as an adjacency matrix in a np.ndarray.
    """

    def __init__(self, atoms: Atoms):

        self._atoms = atoms
        self.graph = None

    def gen_adj_matrix(self, scaling_factor: float = 1.05, do_mic: bool = False) -> np.ndarray:
        """
        Returns an adjacency matrix representation of bonds within a system. Bond distances are
        based on sets of natural cutoffs provided by ASE. Optionally, bonds across periodic
        boundaries can be determined using the minimum image convetion.

        Parameters
        ----------
        scaling_factor (float, optional): Scalar for natural cutoff distances
        do_mic (bool, optional): Compute bonds 

        Returns
        -------
        graph (np.ndarray, shape=NxN): Graph representation of bonds within a unit
        cell stored as a symmetric adjacency matrix, where N = # of atoms in the
        system.

        This method uses numpy broadcasting to accelerate the following loop:

            for i in range(nat):
                tmp = []
                ri = fpos[i, :]
                for j in range(nat):
                    dx = ri - fpos[j, :]
                    dx = dx - np.rint(dx)
                    dr = np.matmul(cell, dx)
                    dr_ = np.linalg.norm(dr)
                    tmp.append(np.linalg.norm(dr_))
                d.append(tuple(tmp))
            d = np.array(d)
        """

        # -- Construct a symmetric NxN matrix of natural cutoffs for atom pairs
        nat_cut = natural_cutoffs(self._atoms, mult=scaling_factor)
        mask = np.array([[a+b for a in nat_cut] for b in nat_cut])

        # -- Construct a symmetric NxN matrix of atom pair distances
        if do_mic:
            # Compute r[i, :] - r[j, :]
            fpos = self._atoms.get_scaled_positions()
            x = fpos[:, np.newaxis, :] - fpos[np.newaxis, :, :]
            # Minimum image convention in fractional coordinates
            x = x - np.rint(x)
            # Convert back to cartesian coordinates
            cell = np.array(self._atoms.get_cell())
            x = x @ cell
        else:
            # Compute r[i, :] - r[j, :]
            pos = self._atoms.get_positions()
            x = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]

        # -- Compute the distances
        d = np.linalg.norm(x, axis=2)

        # -- Build the adjaceny matrix graph representation
        N = len(nat_cut)
        self.graph = (d < mask).astype(np.int8) - np.eye(N, dtype=np.int8)
