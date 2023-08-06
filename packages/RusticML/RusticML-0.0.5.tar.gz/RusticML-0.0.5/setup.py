import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RusticML",                     # This is the name of the package
    version="0.0.5",                     # The initial release version
    author="yaegerknight, ani_ash",      # Full name of the author
    description="A simple machine learning framework",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.8',                # Minimum version requirement of the package
    py_modules=["RusticML"],             # Name of the python package
    package_dir={'':'RusticML/src'},     # Directory of the source code of the package
    install_requires=['numpy==1.23.4','dill==0.3.6']                     # Install other dependencies if any
)