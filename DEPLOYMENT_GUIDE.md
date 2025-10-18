# AI Career Agent - Deployment Guide

## Quick Start Deployment

### Prerequisites

- AWS Account with Bedrock access in us-east-1
- AWS CLI configured with appropriate permissions
- Python 3.11+ installed
- Git installed

### One-Command Deployment

```bash
git clone https://github.com/YourUsername/ai-career-agent.git
cd ai-career-agent
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

## Manual Deployment Steps

### 1. Deploy Infrastructure

```bash
aws cloudformation create-stack \
  --stack-name ai-career-agent-prod \
  --template-body file://deployment/cloudformation_template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1
```

### 2. Update Lambda Functions

After CloudFormation completes, update the Lambda functions with actual code:

```bash
# Package and deploy each function
zip -r market_intelligence.zip lambda_functions/market_intelligence.py
aws lambda update-function-code \
  --function-name ai-career-agent-market-intelligence \
  --zip-file fileb://market_intelligence.zip
```

### 3. Create Bedrock Agent

Use the AWS Console to create a Bedrock Agent with the configuration in `bedrock_agent_config.json`

### 4. Run Streamlit App

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and update with your values:

- AWS credentials and region
- Bedrock Agent ID and Alias ID
- S3 bucket names (created by CloudFormation)

### AWS Permissions Required

- Bedrock: InvokeModel, CreateAgent, UpdateAgent
- Lambda: CreateFunction, UpdateFunctionCode, InvokeFunction
- S3: CreateBucket, GetObject, PutObject
- CloudFormation: CreateStack, UpdateStack
- IAM: CreateRole, AttachRolePolicy

## Testing

### Test Lambda Functions

```bash
# Test market intelligence
aws lambda invoke \
  --function-name ai-career-agent-market-intelligence \
  --payload '{"job_domain":"Software Engineering"}' \
  response.json
```

### Test Bedrock Agent

Use the AWS Console Bedrock Agent test interface or integrate with your Streamlit app.

## Troubleshooting

### Common Issues

1. **Bedrock Access**: Ensure your region supports Bedrock and you have model access
2. **Lambda Timeouts**: Increase timeout if functions take longer than 300 seconds
3. **S3 Permissions**: Verify Lambda execution role has S3 access
4. **Agent Creation**: Use AWS Console for Bedrock Agent creation (CLI support limited)

### Support

- Check CloudFormation events for deployment issues
- Review Lambda logs in CloudWatch
- Verify IAM permissions for all services
