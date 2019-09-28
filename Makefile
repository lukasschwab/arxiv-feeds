# Dev utilities. Not meaningful for deployment.

install:
	pip3 install -r requirements.txt

run:
	dev_appserver.py app.yaml

watch:
	cork-make -p */** -r 'touch main.py'

open:
	open http://localhost:8080/

deploy:
	gcloud app deploy

open-prod:
	gcloud app browse
