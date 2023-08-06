import setuptools


setuptools.setup(
    name="myPackagesQJ1204",
    version="0.1.0",
    author="xiaoxin",
    description="edited by myself",
    py_modules=["myPackagesQJ1204.aaa"],
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent"],
    packages=setuptools.find_packages(),
    install_requires=['pandas'],
    python_requires=">=3"
)