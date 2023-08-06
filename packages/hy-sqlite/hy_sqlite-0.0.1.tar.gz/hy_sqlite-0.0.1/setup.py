import setuptools

with open("README.md","r") as fh:
    long_description=fh.read()


setuptools.setup(
    name="hy_sqlite",
    version="0.0.1",
    author="Hypo",
    description="Module de requettes sqlite sans sql",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
    py_modules=["hy_sqlite"],
    package_dir={'':'hy_sqlite/src'},
    install_requires=[]
)