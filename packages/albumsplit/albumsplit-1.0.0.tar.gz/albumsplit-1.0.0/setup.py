from setuptools import setup

setup(
    name='albumsplit',
    version='1.0.0',
    author='github.com/charmparticle',
    scripts=['bin/albumsplit'],
    url='https://github.com/charmparticle/albumsplit',
    license='BSD 3-Clause License',
    description='An album splitter',
    long_description=open('README.md').read(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

