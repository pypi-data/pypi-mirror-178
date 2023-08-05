__author__ = 'Jordi Arellano'
__copyright__ = 'Copyleft 2021'
__date__ = '05/04/22'
__credits__ = ['Jordi Arellano', ]
__license__ = 'CC0 1.0 Universal'
__version__ = '0.1.0'
__maintainer__ = 'Jordi Arellano'
__email__ = 'jordiarellano1996@gmail.com'

from setuptools import setup
import os

# Read README and CHANGES files for the long description
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as fh:
    long_description = fh.read()

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirementPath = lib_folder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(name="DDExcelAccesslib",
      version=__version__,
      description="This lib controls Excel files for ProbeCard project",
      long_description_content_type="text/markdown",
      long_description=long_description,
      python_requires='>=3',
      packages=["ExcelAccesslib"],
      license="CC0 1.0 Universal",
      zip_safe=False,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Programming Language :: Python :: 3",
      ],
      setup_requires=['wheel'],
      install_requires=["et-xmlfile==1.1.0", "numpy==1.23.4", "openpyxl==3.0.10"],
      )
