all:

flake8:
	flake8


clean:
	find -name "__pycache__" | xargs rm -rf
	find -name "*.pyc" | xargs rm -f
	find -name "*.pyd" | xargs rm -f
	find -name "*.pyo" | xargs rm -f
	find -name "*.orig" | xargs rm -f
	find -name "*.so" | xargs rm -f
	find -name "*.c" | xargs rm -f
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	rm -rf .tox


release_check: clean
	pandoc README.md -o README.rst
	python setup.py sdist
	tox
	@echo version `python -c "import doing; print(doing.__version__)"`


upload: release_check
	python setup.py sdist --formats=gztar,zip
	python setup.py bdist_wheel --universal
	twine upload dist/*

