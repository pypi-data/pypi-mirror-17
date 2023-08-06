from os.path import join, dirname
import setuptools


def read(fname):
    with open(join(dirname(__file__), fname)) as f:
        return f.read()
from distutils.core import setup, Command
# you can also import from setuptools


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess
        errno = subprocess.call([sys.executable, 'runtest.py'])
        raise SystemExit(errno)

setuptools.setup(
    name="harness-it",
    version="0.1.3",
    author="Tony Fast",
    author_email="tony.fast@continuum.io",
    description="A Test Harness in a DataFrame",
    license="BSD-3-Clause",
    keywords="IPython Magic Jupyter",
    url="http://github.com/tonyfast/harness-it",
    packages=setuptools.find_packages(),
    long_description=read("readme.rst"),
    classifiers=[
        "Topic :: Utilities",
        "Framework :: IPython",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Testing",
    ],
    install_requires=[
        "sklearn", "pandas", "whatever-forever",
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest', 'pytest-ipynb'
    ],
    cmdclass={
        'test': PyTest
    },
)
