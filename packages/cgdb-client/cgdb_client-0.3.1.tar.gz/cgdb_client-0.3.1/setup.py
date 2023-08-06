from setuptools import find_packages, setup

setup(
    name='cgdb_client',
    packages=find_packages(include=["cgdb", "cgdb.exceptions", "cgdb.managers", "cgdb.resources", "cgdb.utils"]),
    version='0.3.1',
    install_requires=["pandas==1.1.5"],
    description='CGDB Client',
    author='CzechGlobe',
    license='MIT',
)
