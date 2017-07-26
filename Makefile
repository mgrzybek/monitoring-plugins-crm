# Make a distribution package
all: deb rpm

build: doc
	python setup.py build

clean:
	rm -rf build
	rm -rf deb_dist
	rm -rf dist
	rm -rf *.egg-info

sdist: doc
	python setup.py sdist

# Documentation is written using Markdown (Github-compatible) 
# then translated into RST to be pypi-compatible
# Pandoc is used
doc:
	pandoc -f markdown_github -t rst README.md > README.rst

install:
	python setup.py install

# Packaging

deb: doc
	which apt-get && python setup.py --command-packages=stdeb.command bdist_deb || exit 0

rpm: doc
	which rpm && python setup.py bdist_rpm || exit 0

