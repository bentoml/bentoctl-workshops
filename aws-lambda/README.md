## AWS Lambda Workshop

### Goals

After the workshop, you should have a ML service hosted on AWS Lambda that
accepts HTTP requests.


### Workshop walkthrough

In this workshop, we will be deploying an ML service for online serving with
AWS Lambda. We will first build a [sentiment
analysis](https://en.wikipedia.org/wiki/Sentiment_analysis) service with
BentoML and Hugging Face transformers model and then deploy it to AWS Lambda
using bentoctl. Finally we will run an inference against the deployed Lambda
function.



#### AWS services will be used

Lambda, API Gateway, ECR, CloudFormation, CloudWatch.

### Prerequisites

Make sure you have the the following prerequisites setup before moving on.

- An active AWS account with permissions to access the AWS services mentioned
  above and AWS CLI installed and configured on your system with that account
    - Install instruction:
      https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
    - Configure AWS account instruction:
      https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
- AWS SAM CLI (>=1.27). Installation instructions
  https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html
- Docker is installed and running on the machine.
    - Install instruction: https://docs.docker.com/install

