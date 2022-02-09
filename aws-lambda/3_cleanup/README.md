## Clean up Lambda deployment

You can delete all the resources created using the `delete` command for
bentoctl.
```
bentoctl delete deployment_config.yaml
```

This will remove
1. Lambda Function
2. ECR repository and all the images pushed
3. API Gateway
4. any IAM roles generated.
