import setuptools

with open("README.md","r") as fh:
    long_description=fh.read()


setuptools.setup(
    name="tk_inter_fr",
    version="0.0.1",
    author="Jospin kahereni",
    description="Librarie pour le calcul statistique",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
    py_modules=["tk_inter_fr"],
    package_dir={'':'tk_inter_fr/src'},
    install_requires=[]
)