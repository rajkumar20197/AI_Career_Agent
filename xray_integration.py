# Add these imports to your Lambda function
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import boto3

# Patch AWS SDK calls for X-Ray tracing
patch_all()

@xray_recorder.capture('lambda_handler')
def lambda_handler(event, context):
    """
    Lambda handler with X-Ray tracing
    """
    
    # Add custom annotations for filtering traces
    xray_recorder.put_annotation("function_name", "ai-career-agent-demo")
    xray_recorder.put_annotation("version", "2.0")
    
    # Add metadata for additional context
    xray_recorder.put_metadata("event_source", determine_event_source(event))
    
    try:
        # Your existing function logic here
        result = process_request(event, context)
        
        # Add success metadata
        xray_recorder.put_annotation("status", "success")
        return result
        
    except Exception as e:
        # Add error metadata
        xray_recorder.put_annotation("status", "error")
        xray_recorder.put_metadata("error_details", {
            "error_type": type(e).__name__,
            "error_message": str(e)
        })
        raise

@xray_recorder.capture('bedrock_ai_call')
def call_bedrock_ai(prompt, model_id):
    """
    Bedrock AI call with X-Ray tracing
    """
    
    # Add AI-specific annotations
    xray_recorder.put_annotation("ai_model", model_id)
    xray_recorder.put_annotation("prompt_length", len(prompt))
    
    bedrock_runtime = boto3.client('bedrock-runtime')
    
    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 1000,
                'messages': [{'role': 'user', 'content': prompt}]
            })
        )
        
        # Add success metadata
        xray_recorder.put_metadata("ai_response_size", len(response['body'].read()))
        return response
        
    except Exception as e:
        xray_recorder.put_annotation("ai_error", str(e))
        raise

@xray_recorder.capture('database_operation')
def store_in_dynamodb(table_name, item):
    """
    DynamoDB operation with X-Ray tracing
    """
    
    xray_recorder.put_annotation("table_name", table_name)
    xray_recorder.put_annotation("operation", "put_item")
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    return table.put_item(Item=item)

def determine_event_source(event):
    """Determine the source of the Lambda trigger"""
    
    if 'httpMethod' in event:
        return 'api_gateway'
    elif 'Records' in event:
        if 's3' in event['Records'][0]:
            return 's3'
        elif 'dynamodb' in event['Records'][0]:
            return 'dynamodb_stream'
        elif 'Sns' in event['Records'][0]:
            return 'sns'
        elif 'eventSource' in event['Records'][0] and 'sqs' in event['Records'][0]['eventSource']:
            return 'sqs'
    elif 'source' in event and event['source'] == 'aws.events':
        return 'eventbridge'
    else:
        return 'unknown'

# Example of how to use X-Ray subsegments for detailed tracing
@xray_recorder.capture('process_job_search')
def process_job_search(user_profile):
    """
    Process job search with detailed X-Ray tracing
    """
    
    # Create subsegment for AI processing
    with xray_recorder.in_subsegment('ai_job_matching'):
        xray_recorder.put_metadata("user_skills", user_profile.get('skills', []))
        ai_recommendations = call_bedrock_ai(
            f"Find jobs for: {user_profile}",
            'anthropic.claude-3-haiku-20240307-v1:0'
        )
    
    # Create subsegment for database storage
    with xray_recorder.in_subsegment('store_results'):
        store_in_dynamodb('job_searches', {
            'user_id': user_profile.get('user_id'),
            'recommendations': ai_recommendations,
            'timestamp': datetime.now().isoformat()
        })
    
    return ai_recommendations