from setuptools import setup

setup(name='gv_ui',
      version='0.1',
      description='GoVizzy user interface package.',
      url='https://github.com/cs481-ekh/s24-slice-n-dice',
      author='Team Slice \'n Dice',
      author_email='ehenderson@boisestate.edu',
      license='MIT',
      packages=['gv_ui'],
      include_package_data=True,
      install_requires=['numpy', 'matplotlib', 'ipywidgets', 'ipyvolume'],
      zip_safe=False)
