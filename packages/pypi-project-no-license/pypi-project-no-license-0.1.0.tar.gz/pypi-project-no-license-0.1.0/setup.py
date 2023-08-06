from setuptools import setup
from pathlib import Path

current_dir = Path(__file__).resolve().parent

try:
    readme = current_dir.joinpath("README.md").read_text()
except FileNotFoundError:
    readme = "PyPI minimal project with no"

setup(
    name="pypi-project-no-license",
    version="0.1.0",
    author="pilosus",
    author_email="vrs@pilosus.org",
    packages=["pypi_project_no_license"],
    package_dir={"pypi_project_no_license": "./src/pypi_project_no_license"},
    url="https://github.com/pilosus/pypi-project-no-license",
    description="PyPI minimal project with no license",
    long_description=readme,
    zip_safe=False,
)
