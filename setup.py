from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


install_requires = [
    "numpy"
]


setup(name='pycascades', 
        version='1.0.0',
        url = 'wwww.pik-potsdam.de',
        author = 'Nico Wunderling',
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
