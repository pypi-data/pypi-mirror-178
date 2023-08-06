from setuptools import setup

setup(
    name='trackcalc',
    version='1.0.0',
    author='github.com/charmparticle',
    scripts=['bin/trackcalc'],
    url='https://github.com/charmparticle/trackcalc',
    license='BSD 3-Clause License',
    description='An album track calculator',
    long_description=open('README.md').read(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

