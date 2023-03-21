from setuptools import setup, find_packages
# List of requirements
requirements = []  # This could be retrieved from requirements.txt
# Package (minimal) configuration
setup(
    name="ksp-kspi",
    version="2023.3a1",
    description="KSPI, a Kerbal Space Program Python remote automation plugin",
    packages=find_packages(),  # __init__.py folders search
    install_requires=requirements
)