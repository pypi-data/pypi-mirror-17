from setuptools import setup

with open("README.rst") as f:
    readme = f.read()

setup(
    name="oommfc",
    version="0.5.1",
    description="A Python-based OOMMF calculator.",
    long_description=readme,
    author="Computational Modelling Group",
    author_email="fangohr@soton.ac.uk",
    url="https://github.com/joommf/oommfc",
    download_url="https://github.com/joommf/oommfc/tarball/0.5.1",
    packages=["oommfc",
              "oommfc.tests"],
    install_requires=["discretisedfield",
                      "micromagneticmodel",
                      "oommfodt"],
    classifiers=["License :: OSI Approved :: BSD License",
                 "Programming Language :: Python :: 3"]
)
