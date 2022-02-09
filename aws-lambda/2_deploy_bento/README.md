## Deploy bento to Lambda

Time to complete: 15-20 minutes(depends on your internet speed and the model
you chose).


### What are we building?

We are going to deploy our bento to AWS Lambda.


### Deploy to AWS Lambda 

1. Creation of Deployment Configuration file
 
The Deployment Configuration file is a YAML file that configures the
deployment. bentoctl refers to this file to perform its operations.

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

2. Deploy the `sentiment_analysis` service

With the `deployment_config.yaml` file generated we can now deploy the service 
using 
```
bentoctl deploy -f ./deployment_config.yaml
```
This will create the AWS resources required for creating our endpoint. This
step might take a while depending on your internet speeds. Once the deployment
is completed it will print out a description of the deployment.

3. Verify the deployment

In order to check the status of the deployment, we can use the `describe` command.
```
bentoctl describe -f ./deployment_config.yaml

# sample output
{
  "StackId": "arn:aws:cloudformation:us-east-1:213386773652:stack/sentiment-analysis-stack/ba6fac50-87f9-11ec-8ccc-0e92b8ecbd8f",
  "StackName": "sentiment-analysis-stack",
  "StackStatus": "CREATE_COMPLETE",
  "CreationTime": "02/07/2022, 09:38:38",
  "LastUpdatedTime": "02/07/2022, 09:38:51",
  "EndpointUrl": "https://99i8raooj6.execute-api.us-east-1.amazonaws.com/Prod"
}
```
This will show releavent information like the EndpointUrl, StackStatus,
LastUpdatedTime etc. Make sure the StackStatus is in the `CREATE_COMPLETE`
state, which implies a successfull deployment.


4. Test the endpoint

Now that our model is running successfully on the cloud, lets make some
requests to the endpoint. The URL for the lambda service is given by the `EndpointUrl`.
We can use curl to sent the exact same request used in the previous step.
```
curl \
-X POST \
-H "content-type: application/json" \
--data "This is a test." \
https://99i8raooj6.execute-api.us-east-1.amazonaws.com/Prod/predict

# sample output
{"label":"NEUTRAL","score":0.612240731716156}% 
```

And that is it, we have successfully deployed the bentoml service to AWS Lambda.


**Q: My request returns a 504 with the message "Endpoint request timed out" ?**
Incase your request times out, it is most likely due to the lambda not having enought
memory to load the model and perform the inference. You should increase the 
memory allocated and try again.


**Q: How do I see the logs for the deployment?**
All the logs for the deployment are logged into the AWS CloudWatch service. You
can checkout the logs at CloudWatch -> Logs -> Log groups ->
sentiment_analysis-predict and you can see all the log streams.
