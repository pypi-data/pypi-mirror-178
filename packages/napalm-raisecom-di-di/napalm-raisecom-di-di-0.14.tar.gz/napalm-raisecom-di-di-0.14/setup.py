from setuptools import find_packages, setup

list_packages = ['napalm', 'raisecom-netmiko', 'librouteros']

setup(
    name='napalm-raisecom-di-di',
    version='0.14',
    description='functionality for raisecom devices, via netmiko connection for netbox',
    url='',
    author='Ilya Gulin',
    license='Apache 2.0',
    install_requires=[*list_packages],
    packages=find_packages(),
    include_package_data=True,
)
