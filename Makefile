ifndef ENV
    ENV=$(USER)
endif

STACK_NAME=runs-to-gadgetfund-$(ENV)
DEPLOYMENTS_BUCKET=kees-deployments
AWS_PROFILE=$(AWS_DEFAULT_PROFILE)

ifeq ($(ENV),production)
	Environment=Production
else
	Environment=Staging
endif

build:
	mkdir -p _build
	pip install -r requirements.txt --target _build --upgrade

package:
	cp -R src/* _build
	echo $(STACK_NAME) > _build/STACK_NAME
	aws cloudformation package \
		--template-file cloudformation/runs-to-gadgetfund.yaml \
		--s3-bucket $(DEPLOYMENTS_BUCKET) \
		--output-template-file _build/packaged-cloudformation-template.yaml

deploy:
	aws cloudformation deploy \
		--template-file _build/packaged-cloudformation-template.yaml \
		--stack-name $(STACK_NAME) \
		--capabilities CAPABILITY_IAM \

deploy-docker:
	docker build -t runs-to-gadgetfund .
	docker run \
		-e "ENV=$(ENV)" \
		-e "AWS_DEFAULT_PROFILE=$(AWS_PROFILE)" \
		-v $(HOME)/.aws:/root/.aws \
		--rm \
		-it runs-to-gadgetfund make package deploy

clean:
	find . -name "__pycache__" -exec rm -rf {} \;