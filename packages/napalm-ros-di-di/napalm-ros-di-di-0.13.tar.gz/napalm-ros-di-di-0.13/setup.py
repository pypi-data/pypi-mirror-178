from setuptools import find_packages, setup

list_packages = ['napalm', 'librouteros']

setup(
    name='napalm-ros-di-di',
    version='0.13',
    description='driver napalm functionality for mikrotik devices',
    url='',
    author='Ilya Gulin',
    license='Apache 2.0',
    install_requires=[*list_packages],
    packages=find_packages(),
    include_package_data=True,
)
