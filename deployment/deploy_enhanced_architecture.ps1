# Enhanced AI Career Agent Deployment Script
# Deploys the complete serverless architecture with all power features

param(
    [Parameter(Mandatory=$false)]
    [string]$Environment = "prod",
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-east-1",
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectName = "ai-career-agent",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipConfirmation
)

Write-Host "🚀 AI Career Agent Enhanced Architecture Deployment" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$StackName = "$ProjectName-enhanced-$Environment"
$TemplateFile = "enhanced_production_template.yaml"
$Region = $Region
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

Write-Host "📋 Deployment Configuration:" -ForegroundColor Yellow
Write-Host "   Stack Name: $StackName" -ForegroundColor White
Write-Host "   Environment: $Environment" -ForegroundColor White
Write-Host "   Region: $Region" -ForegroundColor White
Write-Host "   Template: $TemplateFile" -ForegroundColor White
Write-Host ""

# Validate AWS CLI and credentials
Write-Host "🔍 Validating AWS Configuration..." -ForegroundColor Yellow
try {
    $awsIdentity = aws sts get-caller-identity --output json | ConvertFrom-Json
    Write-Host "   ✅ AWS Account: $($awsIdentity.Account)" -ForegroundColor Green
    Write-Host "   ✅ User/Role: $($awsIdentity.Arn)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ AWS CLI not configured or credentials invalid" -ForegroundColor Red
    Write-Host "   Please run 'aws configure' to set up your credentials" -ForegroundColor Red
    exit 1
}

# Check if template file exists
if (-not (Test-Path $TemplateFile)) {
    Write-Host "❌ Template file not found: $TemplateFile" -ForegroundColor Red
    exit 1
}

Write-Host "   ✅ Template file found" -ForegroundColor Green
Write-Host ""

# Validate CloudFormation template
Write-Host "🔍 Validating CloudFormation Template..." -ForegroundColor Yellow
try {
    aws cloudformation validate-template --template-body file://$TemplateFile --region $Region | Out-Null
    Write-Host "   ✅ Template validation successful" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Template validation failed" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Show what will be deployed
Write-Host "🏗️  Architecture Components to Deploy:" -ForegroundColor Yellow
Write-Host "   🔐 Authentication: Amazon Cognito User Pool + Identity Pool" -ForegroundColor White
Write-Host "   💾 Storage: DynamoDB Tables with Streams + S3 Bucket" -ForegroundColor White
Write-Host "   🔍 Search: Amazon OpenSearch Service" -ForegroundColor White
Write-Host "   📨 Messaging: SQS Queues with Dead Letter Queues" -ForegroundColor White
Write-Host "   🤖 AI Integration: Amazon Bedrock (Claude 3 Sonnet)" -ForegroundColor White
Write-Host "   ⚡ Compute: Lambda Functions with X-Ray Tracing" -ForegroundColor White
Write-Host "   🔄 Orchestration: Step Functions Workflows" -ForegroundColor White
Write-Host "   🌐 API: API Gateway with Cognito Authorization" -ForegroundColor White
Write-Host "   📊 Monitoring: CloudWatch + X-Ray" -ForegroundColor White
Write-Host "   🔔 Notifications: SNS Topics" -ForegroundColor White
Write-Host "   ⏰ Scheduling: EventBridge Rules" -ForegroundColor White
Write-Host ""

# Confirmation prompt
if (-not $SkipConfirmation) {
    $confirmation = Read-Host "Do you want to proceed with deployment? (y/N)"
    if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
        Write-Host "Deployment cancelled by user" -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""
Write-Host "🚀 Starting Deployment..." -ForegroundColor Cyan
Write-Host ""

# Create deployment parameters
$Parameters = @(
    "ParameterKey=ProjectName,ParameterValue=$ProjectName",
    "ParameterKey=Environment,ParameterValue=$Environment"
)

# Check if stack exists
Write-Host "🔍 Checking if stack exists..." -ForegroundColor Yellow
$stackExists = $false
try {
    aws cloudformation describe-stacks --stack-name $StackName --region $Region | Out-Null
    $stackExists = $true
    Write-Host "   ✅ Stack exists - will update" -ForegroundColor Green
} catch {
    Write-Host "   ℹ️  Stack does not exist - will create" -ForegroundColor Blue
}

# Deploy the stack
$deploymentStartTime = Get-Date
Write-Host ""
Write-Host "⏳ Deploying CloudFormation Stack..." -ForegroundColor Yellow
Write-Host "   This may take 15-20 minutes for initial deployment" -ForegroundColor Gray

try {
    if ($stackExists) {
        # Update existing stack
        Write-Host "   📝 Updating existing stack..." -ForegroundColor Blue
        aws cloudformation update-stack `
            --stack-name $StackName `
            --template-body file://$TemplateFile `
            --parameters $Parameters `
            --capabilities CAPABILITY_NAMED_IAM `
            --region $Region
        
        Write-Host "   ⏳ Waiting for stack update to complete..." -ForegroundColor Yellow
        aws cloudformation wait stack-update-complete --stack-name $StackName --region $Region
    } else {
        # Create new stack
        Write-Host "   🆕 Creating new stack..." -ForegroundColor Blue
        aws cloudformation create-stack `
            --stack-name $StackName `
            --template-body file://$TemplateFile `
            --parameters $Parameters `
            --capabilities CAPABILITY_NAMED_IAM `
            --region $Region
        
        Write-Host "   ⏳ Waiting for stack creation to complete..." -ForegroundColor Yellow
        aws cloudformation wait stack-create-complete --stack-name $StackName --region $Region
    }
    
    $deploymentEndTime = Get-Date
    $deploymentDuration = $deploymentEndTime - $deploymentStartTime
    
    Write-Host ""
    Write-Host "✅ Stack deployment completed successfully!" -ForegroundColor Green
    Write-Host "   Duration: $($deploymentDuration.Minutes) minutes $($deploymentDuration.Seconds) seconds" -ForegroundColor Green
    
} catch {
    Write-Host ""
    Write-Host "❌ Stack deployment failed!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    
    # Get stack events for debugging
    Write-Host ""
    Write-Host "📋 Recent Stack Events:" -ForegroundColor Yellow
    aws cloudformation describe-stack-events --stack-name $StackName --region $Region --max-items 10 --query 'StackEvents[?ResourceStatus==`CREATE_FAILED` || ResourceStatus==`UPDATE_FAILED`].[Timestamp,ResourceType,LogicalResourceId,ResourceStatusReason]' --output table
    
    exit 1
}

# Get stack outputs
Write-Host ""
Write-Host "📊 Retrieving Stack Outputs..." -ForegroundColor Yellow

try {
    $outputs = aws cloudformation describe-stacks --stack-name $StackName --region $Region --query 'Stacks[0].Outputs' --output json | ConvertFrom-Json
    
    Write-Host ""
    Write-Host "🎉 Deployment Complete! Here are your endpoints:" -ForegroundColor Green
    Write-Host "=============================================" -ForegroundColor Green
    
    foreach ($output in $outputs) {
        switch ($output.OutputKey) {
            "APIEndpoint" {
                Write-Host "🌐 API Gateway Endpoint:" -ForegroundColor Cyan
                Write-Host "   $($output.OutputValue)" -ForegroundColor White
            }
            "UserPoolId" {
                Write-Host "🔐 Cognito User Pool ID:" -ForegroundColor Cyan
                Write-Host "   $($output.OutputValue)" -ForegroundColor White
            }
            "UserPoolClientId" {
                Write-Host "🔑 Cognito Client ID:" -ForegroundColor Cyan
                Write-Host "   $($output.OutputValue)" -ForegroundColor White
            }
            "S3BucketName" {
                Write-Host "💾 S3 Bucket:" -ForegroundColor Cyan
                Write-Host "   $($output.OutputValue)" -ForegroundColor White
            }
            "OpenSearchEndpoint" {
                Write-Host "🔍 OpenSearch Endpoint:" -ForegroundColor Cyan
                Write-Host "   $($output.OutputValue)" -ForegroundColor White
            }
            "StepFunctionArn" {
                Write-Host "🔄 Step Functions ARN:" -ForegroundColor Cyan
                Write-Host "   $($output.OutputValue)" -ForegroundColor White
            }
        }
    }
    
} catch {
    Write-Host "⚠️  Could not retrieve stack outputs" -ForegroundColor Yellow
    Write-Host "   You can view them in the AWS Console CloudFormation section" -ForegroundColor Gray
}

Write-Host ""
Write-Host "🔧 Next Steps:" -ForegroundColor Yellow
Write-Host "1. 📱 Test the API endpoints using the provided URLs" -ForegroundColor White
Write-Host "2. 👤 Create test users in Cognito User Pool" -ForegroundColor White
Write-Host "3. 📄 Upload test resumes to S3 bucket" -ForegroundColor White
Write-Host "4. 🔍 Verify OpenSearch indexing is working" -ForegroundColor White
Write-Host "5. 📊 Check CloudWatch logs and X-Ray traces" -ForegroundColor White
Write-Host "6. 🧪 Run end-to-end tests with the Streamlit app" -ForegroundColor White

Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "   • API Documentation: Check API Gateway console" -ForegroundColor White
Write-Host "   • Authentication: Use Cognito User Pool credentials" -ForegroundColor White
Write-Host "   • Monitoring: CloudWatch dashboards and X-Ray service map" -ForegroundColor White
Write-Host "   • Troubleshooting: Check Lambda function logs in CloudWatch" -ForegroundColor White

Write-Host ""
Write-Host "🎯 Architecture Features Deployed:" -ForegroundColor Green
Write-Host "   ✅ Cognito Authentication & Authorization" -ForegroundColor White
Write-Host "   ✅ AI-Powered Job Search with Claude 3 Sonnet" -ForegroundColor White
Write-Host "   ✅ Resume Optimization with ATS Analysis" -ForegroundColor White
Write-Host "   ✅ Market Intelligence & Salary Benchmarking" -ForegroundColor White
Write-Host "   ✅ OpenSearch for Powerful Job Search" -ForegroundColor White
Write-Host "   ✅ Step Functions for Complex Workflows" -ForegroundColor White
Write-Host "   ✅ SQS with Dead Letter Queues for Resilience" -ForegroundColor White
Write-Host "   ✅ X-Ray Tracing for Monitoring & Debugging" -ForegroundColor White
Write-Host "   ✅ EventBridge for Event-Driven Architecture" -ForegroundColor White
Write-Host "   ✅ SNS for Notifications" -ForegroundColor White

Write-Host ""
Write-Host "🚀 Your AI Career Agent is now live and ready!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Save deployment info to file
$deploymentInfo = @{
    StackName = $StackName
    Environment = $Environment
    Region = $Region
    DeploymentTime = $deploymentEndTime.ToString("yyyy-MM-dd HH:mm:ss")
    Duration = "$($deploymentDuration.Minutes)m $($deploymentDuration.Seconds)s"
    Outputs = $outputs
}

$deploymentInfoJson = $deploymentInfo | ConvertTo-Json -Depth 3
$deploymentInfoFile = "deployment-info-$Environment-$Timestamp.json"
$deploymentInfoJson | Out-File -FilePath $deploymentInfoFile -Encoding UTF8

Write-Host ""
Write-Host "💾 Deployment information saved to: $deploymentInfoFile" -ForegroundColor Blue
Write-Host ""