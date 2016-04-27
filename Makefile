

pyedf: clean
	python setup.py install --prefix $(HOME)

	echo '###################'
	echo 'Add to your pythonpath variable, located in $(HOME)/.bashrc, the line:'
	echo '>export PYTHONPATH=S(PYTHONPATH):$(HOME)/lib/python2.7/site-packages:'

clean:
	rm -rf build dist pyedf.egg-info tmp
