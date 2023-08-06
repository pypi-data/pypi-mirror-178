import io
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup


# Read in the README for the long description on PyPI
def long_description():
	with io.open('README.md', 'r', encoding='utf-8') as f:
		readme = f.read()
	return readme


setup(
	name="DHpyutils",
	version="0.0.2",
	long_description=long_description(),
	url="https://github.com/skdkfk8758/C-PyUtils.git",
	author="CarpDm",
	author_email="skdkfk8758@gmail.com",
	license="CarpDm",
	packages=find_packages(where='src'),
	package_dir={'': 'src'},
	py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
	install_requires=[

	]
)
