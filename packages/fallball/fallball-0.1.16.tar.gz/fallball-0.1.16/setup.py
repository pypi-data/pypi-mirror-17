import os
import time
from os.path import join, dirname, abspath
from setuptools import find_packages, setup

PACKAGE_VERSION = '0.1'


def version():
    path_version = join(dirname(abspath(__file__)), 'version.txt')

    def version_file(mode='r'):
        return open(path_version, mode)

    if os.path.exists(path_version):
        with version_file() as verfile:
            return verfile.readline().strip()

    if os.getenv('TRAVIS'):
        build_version = os.getenv('TRAVIS_BUILD_NUMBER')
    elif os.getenv('JENKINS_HOME'):
        build_version = 'jenkins{}'.format(os.getenv('BUILD_NUMBER'))
    else:
        build_version = 'dev{}'.format(int(time.time()))

    with version_file('w') as verfile:
        verfile.write('{0}.{1}'.format(PACKAGE_VERSION, build_version))

    with version_file() as verfile:
        return verfile.readline().strip()

setup(
    name='fallball',
    version=version(),
    author='APS Lite team',
    author_email='apslite@odin.com',
    packages=find_packages('fallball'),
    package_dir={'': 'fallball'},
    include_package_data=True,
    test_suite="fallball.runtests",
    url='https://fallball.io',
    license='Apache License',
    description='Dummy file sharing service available by REST api.',
    long_description=open('README.md').read(),
)
