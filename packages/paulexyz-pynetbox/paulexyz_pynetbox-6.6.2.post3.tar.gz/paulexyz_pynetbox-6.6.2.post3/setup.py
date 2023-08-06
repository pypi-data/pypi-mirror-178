from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="paulexyz_pynetbox",
    description="NetBox API client library",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Zach Moody",
    author_email="zmoody@do.co",
    license="Apache2",
    include_package_data=True,
    version="6.6.2.post3",
    setup_requires=["setuptools_scm"],
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "requests>=2.20.0,<3.0",
    ],
    zip_safe=False,
    keywords=["netbox"],
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
