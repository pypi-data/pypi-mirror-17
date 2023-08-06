clean:
	rm -rf *.py[co] __pycache__ .*.sw?

test:
	pep8 --ignore=E241,E501,E731 *.py
	PYTHONPATH=../../lrparsing ./lrparsing-expr.py "1 + 1"
	PYTHONPATH=../../lrparsing ./lrparsing-lua.py --quiet
	PYTHONPATH=../../lrparsing ./lrparsing-sqlite.py --quiet
