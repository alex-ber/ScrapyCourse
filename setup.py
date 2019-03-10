import setuptools
from setuptools import setup
import os

print(__file__)
print(os.path.abspath(__file__))
print(setuptools.find_packages(exclude=('tests*',)))

#print(os.path.realpath(__file__))

base_dir = os.path.dirname(os.path.abspath(__file__))

def get_content(filename):
    with open(os.path.join(base_dir, filename)) as f:
        content = f.read().splitlines()
    return content

install_requires = get_content('requirements.txt')
tests_require = []#get_content('requirements-test.txt')



setup(
    name='rocket-paper-scissors-gmae',
    version='0.0.1',
    url='https://github.com/alex-ber/RocketPaperScissorsGame',
    author='Alexander Berkovich',
    description='Rock-Paper-Scissors game',
    long_description="\n\n".join([
        open(os.path.join(base_dir, "README.rst"), "r").read(),
        open(os.path.join(base_dir, "CHANGELOG.rst"), "r").read()
    ]),
    packages=setuptools.find_packages(exclude=('tests*',)),
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite = "tests",
    namespace_packages=('alexber',),
    license='Apache 2.0',
    keywords='game engine player rock papaer scissors',
    classifiers=[
        # See: https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 1 - Planning',
        'Environment :: Console'
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',

        # List of python versions and their support status:
        # https://en.wikipedia.org/wiki/CPython#Version_history
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython'
        "Topic :: Utilities",
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe = False,
    include_package_data=True
)