from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


install_requires = [
    "numpy",
    "scipy",
    "matplotlib",
    "cartopy",
    "seaborn",
    "netCDF4",
    "networkx",
    "ipykernel",
    "pyDOE",
    "PyPDF2",
    "numba"
]


setup(name='pycascades', 
        version='1.0.2',
        url = 'https://github.com/pik-copan/pycascades',
        author = 'Nico Wunderling, Jonathan Krönke, Vitus Benson, Dorothea Kistinger, Jan Kohler, Benedikt Stumpf, Valentin Wohlfarth, Jonathan F. Donges',
        author_email = 'nico.wunderling@pik-potsdam.de',
        long_description=long_description,
        long_description_content_type="text/markdown",
        classifiers=[
                "Intended Audience :: Science/Research",
                "License :: Other/Proprietary License",
                "Programming Language :: Python :: 3"
                 ],
        packages=find_packages(),
        install_requires=install_requires,
        )
