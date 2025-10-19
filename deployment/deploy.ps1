# AI Career Agent - Windows PowerShell Deployment Script
# Full production deployment to AWS

param(
    [string]$ProjectName = "ai-career-agent",
    [string]$Environment = "prod",
    [string]$Region = "us-east-1"
)

$StackName = "$ProjectName-$Environment"

Write-Host "🚀 Starting AI Career Agent Production Deployment" -ForegroundColor Green
Write-Host "Project: $ProjectName" -ForegroundColor Cyan
Write-Host "Environment: $Environment" -ForegroundColor Cyan
Write-Host "Region: $Region" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

# Check AWS CLI
try {
    $awsVersion = aws --version
    Write-Host "✅ AWS CLI: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS CLI not found. Please install AWS CLI first." -ForegroundColor Red
    exit 1
}

# Check AWS credentials
try {
    $identity = aws sts get-caller-identity --output json | ConvertFrom-Json
    Write-Host "✅ AWS Account: $($identity.Account)" -ForegroundColor Green
    Write-Host "✅ AWS User: $($identity.Arn)" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS credentials not configured. Please run 'aws configure' first." -ForegroundColor Red
    exit 1
}

# Create deployment packages directory
Write-Host "📦 Creating deployment packages..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "deployment\packages" | Out-Null

# Package Lambda functions
$lambdaFunctions = @("market_intelligence", "job_search_agent", "resume_optimizer")

foreach ($function in $lambdaFunctions) {
    Write-Host "📦 Packaging $function..." -ForegroundColor Cyan
    
    $tempDir = New-TemporaryFile | ForEach-Object { Remove-Item $_; New-Item -ItemType Directory -Path $_ }
    
    # Copy function code
    Copy-Item "lambda_functions\$function.py" -Destination $tempDir
    
    # Install dependencies if requirements exist
    if (Test-Path "lambda_functions\requirements.txt") {
        Set-Location $tempDir
        pip install -r "..\lambda_functions\requirements.txt" -t . --quiet
        Set-Location $PSScriptRoot\..
    }
    
    # Create ZIP package
    $zipPath = "deployment\packages\$function.zip"
    Compress-Archive -Path "$tempDir\*" -DestinationPath $zipPath -Force
    
    # Cleanup
    Remove-Item $tempDir -Recurse -Force
    
    Write-Host "✅ Created $zipPath" -ForegroundColor Green
}

# Deploy CloudFormation stack
Write-Host "☁️ Deploying CloudFormation stack: $StackName..." -ForegroundColor Yellow

try {
    # Check if stack exists
    $stackExists = $false
    try {
        aws cloudformation describe-stacks --stack-name $StackName --region $Region --output json | Out-Null
        $stackExists = $true
        Write-Host "📝 Stack exists. Updating..." -ForegroundColor Cyan
    } catch {
        Write-Host "📝 Creating new stack..." -ForegroundColor Cyan
    }
    
    if ($stackExists) {
        aws cloudformation update-stack `
            --stack-name $StackName `
            --template-body file://deployment/cloudformation_template.yaml `
            --parameters ParameterKey=ProjectName,ParameterValue=$ProjectName ParameterKey=Environment,ParameterValue=$Environment `
            --capabilities CAPABILITY_NAMED_IAM `
            --region $Region
        
        Write-Host "⏳ Waiting for stack update to complete..." -ForegroundColor Yellow
        aws cloudformation wait stack-update-complete --stack-name $StackName --region $Region
    } else {
        aws cloudformation create-stack `
            --stack-name $StackName `
            --template-body file://deployment/cloudformation_template.yaml `
            --parameters ParameterKey=ProjectName,ParameterValue=$ProjectName ParameterKey=Environment,ParameterValue=$Environment `
            --capabilities CAPABILITY_NAMED_IAM `
            --region $Region
        
        Write-Host "⏳ Waiting for stack creation to complete..." -ForegroundColor Yellow
        aws cloudformation wait stack-create-complete --stack-name $StackName --region $Region
    }
    
    Write-Host "✅ CloudFormation stack deployed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ CloudFormation deployment failed: $_" -ForegroundColor Red
    exit 1
}

# Update Lambda function code
Write-Host "🔄 Updating Lambda function code..." -ForegroundColor Yellow

$functionMappings = @{
    "market_intelligence" = "$ProjectName-market-intelligence"
    "job_search_agent" = "$ProjectName-job-search"
    "resume_optimizer" = "$ProjectName-resume-optimizer"
}

foreach ($mapping in $functionMappings.GetEnumerator()) {
    $localName = $mapping.Key
    $awsName = $mapping.Value
    $zipFile = "deployment\packages\$localName.zip"
    
    if (Test-Path $zipFile) {
        Write-Host "🔄 Updating $awsName..." -ForegroundColor Cyan
        
        aws lambda update-function-code `
            --function-name $awsName `
            --zip-file "fileb://$zipFile" `
            --region $Region
        
        Write-Host "✅ Updated $awsName" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Package not found for $localName" -ForegroundColor Yellow
    }
}

# Get deployment information
Write-Host "📊 Deployment Information:" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green

aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region `
    --query "Stacks[0].Outputs[*].[OutputKey,OutputValue]" `
    --output table

Write-Host ""
Write-Host "🎉 Production Deployment Completed Successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Create Bedrock Agent using AWS Console and bedrock_agent_config.json"
Write-Host "2. Test Lambda functions individually"
Write-Host "3. Deploy Streamlit app to AWS App Runner or ECS"
Write-Host "4. Configure domain and SSL certificate"
Write-Host ""
Write-Host "🔗 Access your resources in AWS Console:" -ForegroundColor Yellow
Write-Host "- CloudFormation: https://console.aws.amazon.com/cloudformation/"
Write-Host "- Lambda Functions: https://console.aws.amazon.com/lambda/"
Write-Host "- S3 Buckets: https://console.aws.amazon.com/s3/"
Write-Host "- Bedrock: https://console.aws.amazon.com/bedrock/"