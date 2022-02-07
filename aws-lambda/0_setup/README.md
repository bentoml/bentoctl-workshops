## Set up your development environment

Time to complete: 5 - 10 minutes.


### What are we building?

* We are setting up the AWS credential with the permissions to different services.
* Install bentoctl and the `aws-lambda` operator required to deploy to AWS Lambda.


### Setup AWS account

1. Download and Install AWS CLI tool

2. Configure AWS CLI tool

3. Run generate_iam.sh to create the AWS user for deployment



### Setup development environment

1. Download bentoctl 

| Because BentoML is still in pre release, we will use the `--pre` flag for pip to install the pre-release version.

```
pip install --pre bentoctl
```

2. Install the Hugging Face transformers library along with pytorch since we
   will be using pytorch based models for building our service.

```
pip install transformers[torch]
```

3. Add the `aws-lambda` operator
