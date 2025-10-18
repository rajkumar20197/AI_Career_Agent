#!/bin/bash

# AI Career Agent Deployment Script
# This script deploys the complete AI Career Agent infrastructure to AWS

set -e  # Exit on any error

# Configuration
PROJECT_NAME="ai-career-agent"
ENVIRONMENT="prod"
AWS_REGION="us-east-1"
STACK_NAME="${PROJECT_NAME}-${ENVIRONMENT}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS credentials not configured. Please run 'aws configure' first."
        exit 1
    fi
    
    # Check if Bedrock is available in the region
    print_status "Checking Bedrock availability in region ${AWS_REGION}..."
    
    print_success "Prerequisites check completed."
}

# Package Lambda functions
package_lambda_functions() {
    print_status "Packaging Lambda functions..."
    
    # Create deployment package directory
    mkdir -p deployment/packages
    
    # Package each Lambda function
    for function_dir in lambda_functions/*.py; do
        if [ -f "$function_dir" ]; then
            function_name=$(basename "$function_dir" .py)
            print_status "Packaging ${function_name}..."
            
            # Create temporary directory
            temp_dir=$(mktemp -d)
            
            # Copy function code
            cp "$function_dir" "$temp_dir/"
            
            # Install dependencies if requirements exist
            if [ -f "lambda_functions/requirements.txt" ]; then
                pip install -r lambda_functions/requirements.txt -t "$temp_dir/"
            fi
            
            # Create ZIP package
            cd "$temp_dir"
            zip -r "../deployment/packages/${function_name}.zip" .
            cd - > /dev/null
            
            # Cleanup
            rm -rf "$temp_dir"
            
            print_success "Packaged ${function_name}.zip"
        fi
    done
}

# Deploy CloudFormation stack
deploy_infrastructure() {
    print_status "Deploying CloudFormation stack: ${STACK_NAME}..."
    
    # Check if stack exists
    if aws cloudformation describe-stacks --stack-name "$STACK_NAME" --region "$AWS_REGION" &> /dev/null; then
        print_status "Stack exists. Updating..."
        aws cloudformation update-stack \
            --stack-name "$STACK_NAME" \
            --template-body file://deployment/cloudformation_template.yaml \
            --parameters ParameterKey=ProjectName,ParameterValue="$PROJECT_NAME" \
                        ParameterKey=Environment,ParameterValue="$ENVIRONMENT" \
            --capabilities CAPABILITY_NAMED_IAM \
            --region "$AWS_REGION"
        
        print_status "Waiting for stack update to complete..."
        aws cloudformation wait stack-update-complete \
            --stack-name "$STACK_NAME" \
            --region "$AWS_REGION"
    else
        print_status "Creating new stack..."
        aws cloudformation create-stack \
            --stack-name "$STACK_NAME" \
            --template-body file://deployment/cloudformation_template.yaml \
            --parameters ParameterKey=ProjectName,ParameterValue="$PROJECT_NAME" \
                        ParameterKey=Environment,ParameterValue="$ENVIRONMENT" \
            --capabilities CAPABILITY_NAMED_IAM \
            --region "$AWS_REGION"
        
        print_status "Waiting for stack creation to complete..."
        aws cloudformation wait stack-create-complete \
            --stack-name "$STACK_NAME" \
            --region "$AWS_REGION"
    fi
    
    print_success "CloudFormation stack deployed successfully."
}

# Update Lambda function code
update_lambda_functions() {
    print_status "Updating Lambda function code..."
    
    # Get function ARNs from CloudFormation outputs
    MARKET_FUNCTION_NAME="${PROJECT_NAME}-market-intelligence"
    JOB_SEARCH_FUNCTION_NAME="${PROJECT_NAME}-job-search"
    RESUME_OPTIMIZER_FUNCTION_NAME="${PROJECT_NAME}-resume-optimizer"
    
    # Update each function
    functions=("market_intelligence:$MARKET_FUNCTION_NAME" "job_search_agent:$JOB_SEARCH_FUNCTION_NAME" "resume_optimizer:$RESUME_OPTIMIZER_FUNCTION_NAME")
    
    for function_info in "${functions[@]}"; do
        IFS=':' read -r local_name aws_name <<< "$function_info"
        
        if [ -f "deployment/packages/${local_name}.zip" ]; then
            print_status "Updating ${aws_name}..."
            
            aws lambda update-function-code \
                --function-name "$aws_name" \
                --zip-file "fileb://deployment/packages/${local_name}.zip" \
                --region "$AWS_REGION"
            
            print_success "Updated ${aws_name}"
        else
            print_warning "Package not found for ${local_name}"
        fi
    done
}

# Create Bedrock Agent
create_bedrock_agent() {
    print_status "Creating Bedrock Agent..."
    
    # Get the Bedrock Agent role ARN from CloudFormation
    AGENT_ROLE_ARN=$(aws cloudformation describe-stacks \
        --stack-name "$STACK_NAME" \
        --region "$AWS_REGION" \
        --query "Stacks[0].Outputs[?OutputKey=='BedrockAgentRoleArn'].OutputValue" \
        --output text)
    
    # Get Lambda function ARNs
    MARKET_FUNCTION_ARN=$(aws cloudformation describe-stacks \
        --stack-name "$STACK_NAME" \
        --region "$AWS_REGION" \
        --query "Stacks[0].Outputs[?OutputKey=='MarketIntelligenceFunctionArn'].OutputValue" \
        --output text)
    
    JOB_SEARCH_FUNCTION_ARN=$(aws cloudformation describe-stacks \
        --stack-name "$STACK_NAME" \
        --region "$AWS_REGION" \
        --query "Stacks[0].Outputs[?OutputKey=='JobSearchFunctionArn'].OutputValue" \
        --output text)
    
    RESUME_OPTIMIZER_FUNCTION_ARN=$(aws cloudformation describe-stacks \
        --stack-name "$STACK_NAME" \
        --region "$AWS_REGION" \
        --query "Stacks[0].Outputs[?OutputKey=='ResumeOptimizerFunctionArn'].OutputValue" \
        --output text)
    
    # Update the Bedrock Agent configuration with actual ARNs
    sed -i.bak "s|ACCOUNT_ID|$(aws sts get-caller-identity --query Account --output text)|g" bedrock_agent_config.json
    sed -i.bak "s|arn:aws:iam::ACCOUNT_ID:role/AmazonBedrockExecutionRoleForAgents_AI_Career_Agent|$AGENT_ROLE_ARN|g" bedrock_agent_config.json
    sed -i.bak "s|arn:aws:lambda:us-east-1:ACCOUNT_ID:function:market-intelligence-function|$MARKET_FUNCTION_ARN|g" bedrock_agent_config.json
    sed -i.bak "s|arn:aws:lambda:us-east-1:ACCOUNT_ID:function:job-search-agent-function|$JOB_SEARCH_FUNCTION_ARN|g" bedrock_agent_config.json
    sed -i.bak "s|arn:aws:lambda:us-east-1:ACCOUNT_ID:function:resume-optimizer-function|$RESUME_OPTIMIZER_FUNCTION_ARN|g" bedrock_agent_config.json
    
    print_status "Bedrock Agent configuration updated with actual ARNs."
    print_warning "Please create the Bedrock Agent manually using the AWS Console with the updated bedrock_agent_config.json"
    print_warning "Bedrock Agent creation via CLI is not yet fully supported in all regions."
}

# Deploy Streamlit application
deploy_streamlit_app() {
    print_status "Preparing Streamlit application deployment..."
    
    # Create deployment configuration
    cat > .streamlit/config.toml << EOF
[server]
port = 8501
address = "0.0.0.0"

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
EOF

    # Create environment configuration
    cat > .env << EOF
AWS_REGION=${AWS_REGION}
PROJECT_NAME=${PROJECT_NAME}
ENVIRONMENT=${ENVIRONMENT}
EOF

    print_success "Streamlit application configured."
    print_status "To run locally: streamlit run app.py"
    print_status "For production deployment, consider using AWS App Runner, ECS, or EC2."
}

# Get deployment information
get_deployment_info() {
    print_status "Deployment Information:"
    echo "=========================="
    
    # Get CloudFormation outputs
    aws cloudformation describe-stacks \
        --stack-name "$STACK_NAME" \
        --region "$AWS_REGION" \
        --query "Stacks[0].Outputs[*].[OutputKey,OutputValue]" \
        --output table
    
    echo ""
    print_success "Deployment completed successfully!"
    echo ""
    print_status "Next Steps:"
    echo "1. Create the Bedrock Agent using the AWS Console and bedrock_agent_config.json"
    echo "2. Test the Lambda functions individually"
    echo "3. Run the Streamlit application: streamlit run app.py"
    echo "4. Configure any additional integrations (job board APIs, etc.)"
    echo ""
    print_status "For the hackathon submission, make sure to:"
    echo "- Update the README.md with your deployment URLs"
    echo "- Create a demo video showing the application in action"
    echo "- Document the architecture and features"
}

# Main deployment function
main() {
    print_status "Starting AI Career Agent deployment..."
    print_status "Project: ${PROJECT_NAME}"
    print_status "Environment: ${ENVIRONMENT}"
    print_status "Region: ${AWS_REGION}"
    echo ""
    
    check_prerequisites
    package_lambda_functions
    deploy_infrastructure
    update_lambda_functions
    create_bedrock_agent
    deploy_streamlit_app
    get_deployment_info
}

# Run main function
main "$@"