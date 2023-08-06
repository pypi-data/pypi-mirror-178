from setuptools import setup
from setuptools import find_packages

# Import the version
from extradtypes import __version__

setup(name = "extradtypes",\
      version = __version__,\
      author = 'Stephen Maldonado',\
      author_email = 'Maldonado527@knights.ucf.edu',\
      description = ('Contains extra data types / containers'),\
      license='MIT',\
      keywords = ['datatypes','containers','tools','utilities'],\
      url = 'https://github.com/StephenMal/ExtraDtypes',\
      packages = find_packages(),\
      include_package_data=True)
