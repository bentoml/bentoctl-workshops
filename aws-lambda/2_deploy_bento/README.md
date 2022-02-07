## Deploy bento to Lambda

Time to complete: 15-20 minutes(depends on your internet speed and the model
you chose).


### What are we building?

We are going to deploy our bento to AWS Lambda.


### Deploy to AWS Lambda 

This is where you get to see bentoctl in action. The first step for deploying is
to create the deployment configuration file

1. Creation of Deployment Configuration file
| Deployments in bentoctl are defined by the deployment configuration. This YAML file specifies everything bentoctl needs to carry out the deployment and represents the configuration for the cloud service.
| (refer to the Core Concepts page to know more)

This is the deployment configuration we can use to deploy the sentiment_analysis
service into lambda.
```yaml
# deployment_config.yaml
api_version: v1
metadata:
  name: sentiment_analysis
  operator: aws-lambda
spec:
  bento: sentiment_analysis:latest
  region: us-east-1
  timeout: 180
  memory_size: 10240

```

You can checkout the Deployment Configuration section(link here) of the docs if
you want a clear understanding of what this file means but there are a few important
options we have to keep in mind.

1. `memory_size` - The amount of memory(in MBs) the lambda function can use.
   Since we are using a fairly heavy model we will need more RAM than usual. If
   you are using the dummy model 3Gigs should be fine but incase us want to
   experiment with the full model set aside 10Gigs, which is the maximum.

2. `region` - The AWS region in which the lambda function and other resources
   will be created. Keep in mind that in most regions the limit for available
   memory is ~= 3Gigs hence make sure to use a region that has no such limits

There is also an interactive mode inside bentoctl that will guide you through each
of the configurable options and provide help messages for the various fields.
You can start it by running
```
bentoctl generate
```
and follow the prompts to create a similar deployment configuration. 

2. Deploy the sentiment_analysis service

3. Verify the Endpoint


### How does it work?
