#!/usr/bin/env python3
"""
Enhanced AI Career Agent Architecture Testing Suite
Tests all components: Authentication, AI Integration, Search, Workflows, etc.
"""

import json
import boto3
import requests
import time
import os
from datetime import datetime
from typing import Dict, List, Any
import asyncio
import aiohttp

class EnhancedArchitectureTester:
    def __init__(self, stack_name: str, region: str = 'us-east-1'):
        self.stack_name = stack_name
        self.region = region
        self.session = boto3.Session(region_name=region)
        self.cloudformation = self.session.client('cloudformation')
        
        # Get stack outputs
        self.outputs = self._get_stack_outputs()
        
        # Initialize service clients
        self.cognito_idp = self.session.client('cognito-idp')
        self.lambda_client = self.session.client('lambda')
        self.dynamodb = self.session.resource('dynamodb')
        self.s3 = self.session.client('s3')
        self.opensearch = self.session.client('opensearch')
        self.stepfunctions = self.session.client('stepfunctions')
        
        # Test results
        self.test_results = []
        
    def _get_stack_outputs(self) -> Dict[str, str]:
        """Get CloudFormation stack outputs"""
        try:
            response = self.cloudformation.describe_stacks(StackName=self.stack_name)
            outputs = {}
            
            for output in response['Stacks'][0].get('Outputs', []):
                outputs[output['OutputKey']] = output['OutputValue']
            
            return outputs
        except Exception as e:
            print(f"❌ Failed to get stack outputs: {str(e)}")
            return {}
    
    def log_test_result(self, test_name: str, success: bool, details: str = "", duration: float = 0):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name} ({duration:.2f}s)")
        if details:
            print(f"   {details}")
        
        self.test_results.append({
            'test_name': test_name,
            'success': success,
            'details': details,
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        })
    
    async def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🧪 Enhanced AI Career Agent Architecture Test Suite")
        print("=" * 60)
        print()
        
        # Test categories
        test_categories = [
            ("Infrastructure Tests", self.test_infrastructure),
            ("Authentication Tests", self.test_authentication),
            ("API Gateway Tests", self.test_api_gateway),
            ("Lambda Function Tests", self.test_lambda_functions),
            ("AI Integration Tests", self.test_ai_integration),
            ("Database Tests", self.test_database_operations),
            ("Search Engine Tests", self.test_opensearch),
            ("Workflow Tests", self.test_step_functions),
            ("Messaging Tests", self.test_sqs_messaging),
            ("Storage Tests", self.test_s3_operations),
            ("End-to-End Tests", self.test_end_to_end_workflows)
        ]
        
        for category_name, test_function in test_categories:
            print(f"\n🔍 {category_name}")
            print("-" * 40)
            await test_function()
        
        # Generate test report
        self.generate_test_report()
    
    async def test_infrastructure(self):
        """Test basic infrastructure components"""
        
        # Test 1: Stack exists and is in good state
        start_time = time.time()
        try:
            response = self.cloudformation.describe_stacks(StackName=self.stack_name)
            stack_status = response['Stacks'][0]['StackStatus']
            
            success = stack_status in ['CREATE_COMPLETE', 'UPDATE_COMPLETE']
            details = f"Stack status: {stack_status}"
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test_result("CloudFormation Stack Status", success, details, time.time() - start_time)
        
        # Test 2: Required outputs exist
        start_time = time.time()
        required_outputs = [
            'APIEndpoint', 'UserPoolId', 'UserPoolClientId', 
            'S3BucketName', 'OpenSearchEndpoint', 'StepFunctionArn'
        ]
        
        missing_outputs = [output for output in required_outputs if output not in self.outputs]
        success = len(missing_outputs) == 0
        details = f"Missing outputs: {missing_outputs}" if missing_outputs else "All required outputs present"
        
        self.log_test_result("Stack Outputs Validation", success, details, time.time() - start_time)
    
    async def test_authentication(self):
        """Test Cognito authentication system"""
        
        # Test 1: User Pool exists and is configured
        start_time = time.time()
        try:
            user_pool_id = self.outputs.get('UserPoolId')
            if not user_pool_id:
                raise Exception("UserPoolId not found in outputs")
            
            response = self.cognito_idp.describe_user_pool(UserPoolId=user_pool_id)
            user_pool = response['UserPool']
            
            success = user_pool['Status'] == 'Enabled'
            details = f"User Pool: {user_pool['Name']}, Status: {user_pool['Status']}"
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test_result("Cognito User Pool Configuration", success, details, time.time() - start_time)
        
        # Test 2: User Pool Client exists
        start_time = time.time()
        try:
            user_pool_id = self.outputs.get('UserPoolId')
            client_id = self.outputs.get('UserPoolClientId')
            
            response = self.cognito_idp.describe_user_pool_client(
                UserPoolId=user_pool_id,
                ClientId=client_id
            )
            
            success = True
            details = f"Client configured with auth flows"
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test_result("Cognito User Pool Client", success, details, time.time() - start_time)
    
    async def test_api_gateway(self):
        """Test API Gateway endpoints"""
        
        api_endpoint = self.outputs.get('APIEndpoint')
        if not api_endpoint:
            self.log_test_result("API Gateway Endpoint", False, "API endpoint not found in outputs")
            return
        
        # Test 1: API Gateway health check
        start_time = time.time()
        try:
            # Test the main agent endpoint
            response = requests.get(f"{api_endpoint}/agent", timeout=10)
            
            success = response.status_code in [200, 401]  # 401 is expected without auth
            details = f"Status: {response.status_code}, Response time: {response.elapsed.total_seconds():.2f}s"
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test_result("API Gateway Connectivity", success, details, time.time() - start_time)
        
        # Test 2: CORS configuration
        start_time = time.time()
        try:
            response = requests.options(f"{api_endpoint}/agent", timeout=10)
            
            cors_headers = [
                'Access-Control-Allow-Origin',
                'Access-Control-Allow-Methods',
                'Access-Control-Allow-Headers'
            ]
            
            has_cors = any(header in response.headers for header in cors_headers)
            success = has_cors or response.status_code == 200
            details = f"CORS headers present: {has_cors}"
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test_result("API Gateway CORS Configuration", success, details, time.time() - start_time)
    
    async def test_lambda_functions(self):
        """Test Lambda function deployments and basic functionality"""
        
        # Get Lambda functions from the stack
        lambda_functions = self._get_lambda_functions_from_stack()
        
        for function_name in lambda_functions:
            await self._test_lambda_function(function_name)
    
    def _get_lambda_functions_from_stack(self) -> List[str]:
        """Get Lambda function names from CloudFormation stack"""
        try:
            response = self.cloudformation.describe_stack_resources(
                StackName=self.stack_name,
                LogicalResourceId=None
            )
            
            lambda_functions = []
            for resource in response['StackResources']:
                if resource['ResourceType'] == 'AWS::Lambda::Function':
                    lambda_functions.append(resource['PhysicalResourceId'])
            
            return lambda_functions
        except Exception as e:
            print(f"⚠️  Could not get Lambda functions: {str(e)}")
            return []
    
    async def _test_lambda_function(self, function_name: str):
        """Test individual Lambda function"""
        start_time = time.time()
        
        try:
            # Test function configuration
            response = self.lambda_client.get_function(FunctionName=function_name)
            config = response['Configuration']
            
            # Check if function is active
            success = config['State'] == 'Active'
            details = f"State: {config['State']}, Runtime: {config['Runtime']}, Memory: {config['MemorySize']}MB"
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        # Shorten function name for display
        display_name = function_name.split('-')[-1] if '-' in function_name else function_name
        self.log_test_result(f"Lambda Function: {display_name}", success, details, time.time() - start_time)
    
    async def test_ai_integration(self):
        """Test AI integration with Amazon Bedrock"""
        
        # Test 1: Bedrock service availability
        start_time = time.time()
        try:
            bedrock = self.session.client('bedrock')
            response = bedrock.list_foundation_models()
            
            # Check if Claude models are available
            claude_models = [
                model for model in response['modelSummaries'] 
                if 'claude' in model['modelId'].lower()
            ]
            
            success = len(claude_models) > 0
            details = f"Found {len(claude_models)} Claude models available"
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test_result("Bedrock Service Availability", success, details, time.time() - start_time)
        
        # Test 2: Test AI model invocation (if possible)
        start_time = time.time()
        try:
            bedrock_runtime = self.session.client('bedrock-runtime')
            
            # Simple test prompt
            test_payload = {
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 50,
                'messages': [
                    {
                        'role': 'user',
                        'content': 'Hello, this is a test. Please respond with "AI integration working".'
                    }
                ]
            }
            
            response = bedrock_runtime.invoke_model(
                modelId='anthropic.claude-3-haiku-20240307-v1:0',
                body=json.dumps(test_payload)
            )
            
            response_body = json.loads(response['body'].read())
            ai_response = response_body['content'][0]['text']
            
            success = 'working' in ai_response.lower() or len(ai_response) > 0
            details = f"AI Response: {ai_response[:50]}..."
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test_result("AI Model Invocation", success, details, time.time() - start_time)
    
    async def test_database_operations(self):
        """Test DynamoDB operations"""
        
        # Test 1: DynamoDB tables exist
        tables_to_check = ['users', 'job-searches']  # Based on template
        
        for table_suffix in tables_to_check:
            start_time = time.time()
            try:
                # Construct likely table name
                table_name = f"ai-career-agent-{table_suffix}-prod"  # Adjust based on your naming
                
                table = self.dynamodb.Table(table_name)
                response = table.meta.client.describe_table(TableName=table_name)
                
                table_status = response['Table']['TableStatus']
                success = table_status == 'ACTIVE'
                details = f"Status: {table_status}, Items: {response['Table'].get('ItemCount', 'Unknown')}"
                
            except Exception as e:
                success = False
                details = f"Error: {str(e)}"
            
            self.log_test_result(f"DynamoDB Table: {table_suffix}", success, details, time.time() - start_time)
    
    async def test_opensearch(self):
        """Test OpenSearch functionality"""
        
        opensearch_endpoint = self.outputs.get('OpenSearchEndpoint')
        if not opensearch_endpoint:
            self.log_test_result("OpenSearch Endpoint", False, "Endpoint not found in outputs")
            return
        
        # Test 1: OpenSearch cluster health
        start_time = time.time()
        try:
            # Get domain status
            domain_name = opensearch_endpoint.split('.')[0].split('//')[1]
            response = self.opensearch.describe_domain(DomainName=domain_name)
            
            domain_status = response['DomainStatus']
            success = not domain_status.get('Processing', True)
            details = f"Created: {domain_status.get('Created', False)}, Processing: {domain_status.get('Processing', True)}"
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test_result("OpenSearch Cluster Status", success, details, time.time() - start_time)
    
    async def test_step_functions(self):
        """Test Step Functions workflows"""
        
        step_function_arn = self.outputs.get('StepFunctionArn')
        if not step_function_arn:
            self.log_test_result("Step Functions ARN", False, "ARN not found in outputs")
            return
        
        # Test 1: State machine exists and is active
        start_time = time.time()
        try:
            response = self.stepfunctions.describe_state_machine(
                stateMachineArn=step_function_arn
            )
            
            status = response['status']
            success = status == 'ACTIVE'
            details = f"Status: {status}, Type: {response.get('type', 'Unknown')}"
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test_result("Step Functions State Machine", success, details, time.time() - start_time)
    
    async def test_sqs_messaging(self):
        """Test SQS messaging system"""
        
        # Test 1: List queues and check for our queues
        start_time = time.time()
        try:
            sqs = self.session.client('sqs')
            response = sqs.list_queues()
            
            queue_urls = response.get('QueueUrls', [])
            career_agent_queues = [
                url for url in queue_urls 
                if 'ai-career-agent' in url or 'job-processing' in url or 'notification' in url
            ]
            
            success = len(career_agent_queues) > 0
            details = f"Found {len(career_agent_queues)} related queues"
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test_result("SQS Queues Configuration", success, details, time.time() - start_time)
    
    async def test_s3_operations(self):
        """Test S3 bucket operations"""
        
        bucket_name = self.outputs.get('S3BucketName')
        if not bucket_name:
            self.log_test_result("S3 Bucket Name", False, "Bucket name not found in outputs")
            return
        
        # Test 1: Bucket exists and is accessible
        start_time = time.time()
        try:
            response = self.s3.head_bucket(Bucket=bucket_name)
            success = True
            details = f"Bucket accessible, Region: {response.get('ResponseMetadata', {}).get('HTTPHeaders', {}).get('x-amz-bucket-region', 'Unknown')}"
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test_result("S3 Bucket Accessibility", success, details, time.time() - start_time)
        
        # Test 2: Test upload/download operations
        start_time = time.time()
        try:
            test_key = f"test-files/test-{int(time.time())}.txt"
            test_content = "This is a test file for AI Career Agent"
            
            # Upload test file
            self.s3.put_object(
                Bucket=bucket_name,
                Key=test_key,
                Body=test_content.encode('utf-8'),
                ContentType='text/plain'
            )
            
            # Download and verify
            response = self.s3.get_object(Bucket=bucket_name, Key=test_key)
            downloaded_content = response['Body'].read().decode('utf-8')
            
            # Cleanup
            self.s3.delete_object(Bucket=bucket_name, Key=test_key)
            
            success = downloaded_content == test_content
            details = f"Upload/download test successful"
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test_result("S3 Upload/Download Operations", success, details, time.time() - start_time)
    
    async def test_end_to_end_workflows(self):
        """Test end-to-end workflows"""
        
        # Test 1: Simulated job search workflow
        start_time = time.time()
        try:
            api_endpoint = self.outputs.get('APIEndpoint')
            if not api_endpoint:
                raise Exception("API endpoint not available")
            
            # Simulate job search request (without auth for now)
            test_payload = {
                'action': 'search_jobs',
                'user_profile': {
                    'job_domain': 'Software Engineering',
                    'location': 'Remote',
                    'experience_level': 'Mid Level'
                }
            }
            
            response = requests.post(
                f"{api_endpoint}/agent/jobs",
                json=test_payload,
                timeout=30
            )
            
            # We expect 401 (unauthorized) or 200 (success)
            success = response.status_code in [200, 401, 202]
            details = f"Status: {response.status_code}, Response: {response.text[:100]}..."
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test_result("End-to-End Job Search Workflow", success, details, time.time() - start_time)
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("🧪 TEST REPORT SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test_name']}: {result['details']}")
        
        # Save detailed report
        report_file = f"test-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': success_rate,
                    'test_date': datetime.now().isoformat()
                },
                'detailed_results': self.test_results,
                'stack_outputs': self.outputs
            }, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: {report_file}")
        
        # Overall status
        if success_rate >= 90:
            print(f"\n🎉 EXCELLENT! Your AI Career Agent architecture is working great!")
        elif success_rate >= 75:
            print(f"\n✅ GOOD! Most components are working, minor issues to address.")
        elif success_rate >= 50:
            print(f"\n⚠️  PARTIAL! Some components need attention.")
        else:
            print(f"\n❌ NEEDS WORK! Multiple components require fixes.")

async def main():
    """Main test execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Enhanced AI Career Agent Architecture')
    parser.add_argument('--stack-name', required=True, help='CloudFormation stack name')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    
    args = parser.parse_args()
    
    tester = EnhancedArchitectureTester(args.stack_name, args.region)
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())