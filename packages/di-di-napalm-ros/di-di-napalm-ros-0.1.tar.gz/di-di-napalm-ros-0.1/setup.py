from setuptools import find_packages, setup

list_packages = ['napalm', 'librouteros']

setup(
    name='di-di-napalm-ros',
    version='0.1',
    description='functionality for mikrotik devices, via netmiko connection for netbox',
    url='',
    author='Ilya Gulin',
    license='Apache 2.0',
    install_requires=[*list_packages],
    packages=find_packages(),
    include_package_data=True,
)
