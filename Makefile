.phony: install test uninstall clean

install:
	@echo 'Installing'
	@pip3 install ./

uninstall:
	@echo 'Uninstalling'
	pip3 uninstall rpncalc

test:
	@echo 'Testing'
	python3 -m unittest discover -v

clean:
	@echo 'Cleaning __pycache__'
	find . -regex '^.*\(__pycache__\|\.py[co]\)' -delete
