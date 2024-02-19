from setuptools import setup

setup(name='cube_viskit',
      version='0.1',
      description='Utilities for visualizing scalar data stored in Gaussian format cube files.',
      url='https://github.com/sweitzner/cube_viskit',
      author='Stephen Weitzner',
      author_email='stephen.weitzner@gmail.com',
      license='MIT',
      packages=['cube_viskit'],
      include_package_data=True,
#      scripts=['bin/convert_cube.py', 
#               'bin/extract_pw_coord.py', 
#               'bin/extract_xyz_traj.py'
#               'bin/planar_average.py'],
      install_requires=['numpy', 'scipy', 'msgpack', 'future'],
      zip_safe=False)
