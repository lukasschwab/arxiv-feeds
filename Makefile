# Dev utilities. Not meaningful for deployment.

install:
	pip3 install -r requirements.txt

run:
	python3 main.py

watch:
	cork-make -p */** -r 'touch main.py'

