ifndef ENV
    ENV=$(USER)
endif

STACK_NAME=runs-to-gadgetfund-$(ENV)
DEPLOYMENTS_BUCKET=kees-deployments

ifeq ($(ENV),production)
	Environment=Production
else
	Environment=Staging
endif

build:
	mkdir -p _build
	pip install -r requirements.txt --target _build --upgrade

package:
	cp -R src/* _build/
	aws cloudformation package \
		--template-file cloudformation/runs-to-gadgetfund.yaml \
		--s3-bucket $(DEPLOYMENTS_BUCKET) \
		--output-template-file _build/packaged-cloudformation-template.yaml

deploy:
	aws cloudformation deploy \
		--template-file _build/packaged-cloudformation-template.yaml \
		--stack-name $(STACK_NAME) \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides Environment=$(Environment)

clean:
	find . -name \*.pyc -exec rm -rf {} \;
	find src/ test* -name "__pycache__" -exec rm -rf {} \;
	
test:
	PYTHONPATH=./src py.test tests

test-v:
	PYTHONPATH=./src py.test tests -vv

test-integration:
	STACK_NAME=$(STACK_NAME) PYTHONPATH=./src py.test tests_integration --fulltrace