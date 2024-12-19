from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "mlops",
    version = "0.1",
    author = "Parshuram",
    author_email = "parshuramsingh433@gmail.com",
    description = "MlOps Project",

    packages = find_packages(),
    
    install_requires = requirements,
    python_requires =">=3.7"

)