import setuptools

with open("README.md","r") as fh:
    long_description=fh.read()


setuptools.setup(
    name="nic_finance",
    version="0.0.1",
    author="Nicolas-ngeleza",
    description="Librarie pour le calcul financiers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
    py_modules=["nic_finance"],
    package_dir={'':'nic_finance/src'},
    install_requires=[]
)