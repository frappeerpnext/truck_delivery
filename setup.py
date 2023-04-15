from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in truck_delivery/__init__.py
from truck_delivery import __version__ as version

setup(
	name="truck_delivery",
	version=version,
	description="truck deliver",
	author="tes pheakdey",
	author_email="pheakdey.micronet@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
