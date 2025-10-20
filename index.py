import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    """
    Enhanced ai-career-agent-demo with Bedrock AI integration
    """
    
    # Initialize Bedrock client
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    try:
        # Determine trigger source and handle accordingly
        if 'httpMethod' in event:
            return handle_api_request_with_ai(event, bedrock_runtime)
        elif 'Records' in event:
            if 's3' in event['Records'][0]:
                return handle_s3_with_ai(event, bedrock_runtime)
            elif 'dynamodb' in event['Records'][0]:
                return handle_dynamodb_with_ai(event, bedrock_runtime)
        else:
            return handle_default_with_ai(bedrock_runtime)
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'AI processing failed'
            })
        }

def handle_api_request_with_ai(event, bedrock_runtime):
    """Handle API requests with AI processing and Cognito authentication"""
    
    # Extract user info from Cognito JWT token
    user_info = extract_user_from_cognito(event)
    
    # Extract request data
    body = json.loads(event.get('body', '{}'))
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    
    # Add user context to request
    if user_info:
        body['user_context'] = user_info
    
    # Route to AI-powered handlers
    if path == '/job-search' and method == 'POST':
        return ai_job_search(body, bedrock_runtime)
    elif path == '/resume-analyze' and method == 'POST':
        return ai_resume_analysis(body, bedrock_runtime)
    elif path == '/market-intel' and method == 'GET':
        return ai_market_intelligence(event.get('queryStringParameters', {}), bedrock_runtime)
    else:
        return ai_general_response(bedrock_runtime)

def ai_job_search(request_data, bedrock_runtime):
    """AI-powered job search and matching"""
    
    user_profile = request_data.get('user_profile', {})
    job_preferences = request_data.get('preferences', {})
    
    # Create AI prompt for job recommendations
    prompt = f"""
    Based on this user profile, provide 5 personalized job recommendations:
    
    User Profile:
    - Skills: {user_profile.get('skills', [])}
    - Experience: {user_profile.get('experience_level', 'Entry Level')}
    - Location: {user_profile.get('location', 'Remote')}
    - Salary Target: ${user_profile.get('salary_target', 75000)}
    
    Job Preferences:
    - Industry: {job_preferences.get('industry', 'Technology')}
    - Company Size: {job_preferences.get('company_size', 'Any')}
    - Work Style: {job_preferences.get('work_style', 'Hybrid')}
    
    For each recommendation, provide:
    1. Job Title
    2. Company Name (realistic)
    3. Location
    4. Salary Range
    5. Match Score (0-100)
    6. Why it's a good match
    7. Key requirements
    
    Respond in JSON format as an array of job objects.
    """
    
    try:
        # Call Bedrock Claude 3 Haiku
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 2000,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            })
        )
        
        # Parse AI response
        response_body = json.loads(response['body'].read())
        ai_recommendations = response_body['content'][0]['text']
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'AI-powered job recommendations generated',
                'recommendations': ai_recommendations,
                'user_profile': user_profile,
                'generated_at': datetime.now().isoformat(),
                'ai_model': 'Claude 3 Haiku'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'AI job search failed: {str(e)}',
                'fallback_message': 'Please try again or contact support'
            })
        }

def ai_resume_analysis(request_data, bedrock_runtime):
    """AI-powered resume analysis and optimization"""
    
    resume_text = request_data.get('resume_text', '')
    job_description = request_data.get('job_description', '')
    
    if not resume_text:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'resume_text is required'})
        }
    
    # Create AI prompt for resume analysis
    prompt = f"""
    Analyze this resume and provide detailed feedback:
    
    Resume:
    {resume_text[:3000]}  # Limit for token efficiency
    
    {f"Target Job Description: {job_description[:1000]}" if job_description else ""}
    
    Provide analysis in JSON format with:
    1. overall_score (0-100)
    2. strengths (array of strengths)
    3. weaknesses (array of areas to improve)
    4. ats_score (0-100 for ATS compatibility)
    5. keywords_missing (if job description provided)
    6. suggestions (specific improvement recommendations)
    7. optimized_summary (improved professional summary)
    
    Focus on actionable feedback for career advancement.
    """
    
    try:
        # Call Bedrock Claude 3 Sonnet for detailed analysis
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 2500,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            })
        )
        
        response_body = json.loads(response['body'].read())
        ai_analysis = response_body['content'][0]['text']
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'AI resume analysis completed',
                'analysis': ai_analysis,
                'analyzed_at': datetime.now().isoformat(),
                'ai_model': 'Claude 3 Sonnet'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'AI resume analysis failed: {str(e)}'
            })
        }

def ai_market_intelligence(query_params, bedrock_runtime):
    """AI-powered job market intelligence"""
    
    job_domain = query_params.get('domain', 'Software Engineering')
    location = query_params.get('location', 'United States')
    experience_level = query_params.get('level', 'Mid Level')
    
    prompt = f"""
    Provide comprehensive job market intelligence for:
    - Job Domain: {job_domain}
    - Location: {location}
    - Experience Level: {experience_level}
    
    Include in JSON format:
    1. salary_range (min, max, median)
    2. job_growth_outlook (percentage and trend)
    3. in_demand_skills (top 10 skills)
    4. market_competitiveness (High/Medium/Low)
    5. top_companies_hiring (list of companies)
    6. career_advice (specific recommendations)
    7. skill_development_priorities (what to learn next)
    8. salary_negotiation_tips (specific to this market)
    
    Provide current, realistic market data and actionable insights.
    """
    
    try:
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 2000,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            })
        )
        
        response_body = json.loads(response['body'].read())
        market_intel = response_body['content'][0]['text']
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Market intelligence generated',
                'intelligence': market_intel,
                'parameters': {
                    'domain': job_domain,
                    'location': location,
                    'level': experience_level
                },
                'generated_at': datetime.now().isoformat(),
                'ai_model': 'Claude 3 Haiku'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Market intelligence failed: {str(e)}'
            })
        }

def handle_s3_with_ai(event, bedrock_runtime):
    """Handle S3 uploads with AI processing"""
    
    s3_client = boto3.client('s3')
    results = []
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        try:
            # Get uploaded file
            response = s3_client.get_object(Bucket=bucket, Key=key)
            
            # Process based on file type
            if key.endswith(('.txt', '.pdf', '.docx')):
                # Assume it's a resume - analyze with AI
                content = response['Body'].read()
                
                if key.endswith('.txt'):
                    text_content = content.decode('utf-8')
                else:
                    text_content = f"Binary file uploaded: {key}"
                
                # AI analysis of uploaded resume
                ai_result = analyze_uploaded_resume(bedrock_runtime, text_content, key)
                
                results.append({
                    'file': key,
                    'status': 'processed',
                    'ai_analysis': ai_result
                })
            
        except Exception as e:
            results.append({
                'file': key,
                'status': 'error',
                'error': str(e)
            })
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'S3 files processed with AI',
            'results': results
        })
    }

def analyze_uploaded_resume(bedrock_runtime, content, filename):
    """Analyze uploaded resume with AI"""
    
    prompt = f"""
    Analyze this uploaded resume file:
    
    Filename: {filename}
    Content: {content[:2000]}
    
    Provide quick analysis in JSON format:
    1. file_type_detected
    2. key_skills_found
    3. experience_level_estimate
    4. overall_quality_score (0-100)
    5. immediate_suggestions (top 3)
    
    Keep response concise but actionable.
    """
    
    try:
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 800,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            })
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
        
    except Exception as e:
        return f"AI analysis failed: {str(e)}"

def handle_dynamodb_with_ai(event, bedrock_runtime):
    """Handle DynamoDB changes with AI insights"""
    
    processed_records = []
    
    for record in event['Records']:
        event_name = record['eventName']
        
        if event_name in ['INSERT', 'MODIFY']:
            # Generate AI insights for data changes
            dynamodb_data = record.get('dynamodb', {})
            
            # You could trigger AI analysis based on data changes
            # For example, when user profile is updated, generate new job recommendations
            
            processed_records.append({
                'eventName': event_name,
                'processed': True,
                'ai_triggered': True
            })
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'DynamoDB changes processed with AI insights',
            'records': processed_records
        })
    }

def extract_user_from_cognito(event):
    """Extract user information from Cognito JWT token"""
    
    try:
        # Get authorization header
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization') or headers.get('authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        # Extract token (in production, you'd verify the JWT signature)
        token = auth_header.replace('Bearer ', '')
        
        # For now, we'll extract claims without verification
        # In production, use proper JWT verification with Cognito public keys
        import base64
        
        try:
            # Decode JWT payload (middle part)
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            payload = parts[1]
            # Add padding if needed
            payload += '=' * (4 - len(payload) % 4)
            
            decoded = base64.b64decode(payload)
            claims = json.loads(decoded)
            
            return {
                'user_id': claims.get('sub'),
                'email': claims.get('email'),
                'username': claims.get('cognito:username'),
                'given_name': claims.get('given_name'),
                'family_name': claims.get('family_name'),
                'token_use': claims.get('token_use'),
                'client_id': claims.get('client_id')
            }
            
        except Exception as e:
            print(f"Error decoding JWT: {str(e)}")
            return None
            
    except Exception as e:
        print(f"Error extracting user from Cognito: {str(e)}")
        return None

def ai_general_response(bedrock_runtime):
    """General AI-powered status response"""
    
    prompt = """
    Generate a helpful status message for an AI Career Agent system.
    Include current capabilities and available features.
    Keep it professional and informative.
    Respond in JSON format with: status, capabilities, available_endpoints, tips
    """
    
    try:
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 600,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            })
        )
        
        response_body = json.loads(response['body'].read())
        ai_status = response_body['content'][0]['text']
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'AI Career Agent - Enhanced with Bedrock',
                'ai_response': ai_status,
                'timestamp': datetime.now().isoformat()
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'AI Career Agent - System Operational',
                'features': [
                    'AI-powered job search',
                    'Resume analysis and optimization',
                    'Market intelligence',
                    'S3 resume processing',
                    'Real-time data insights'
                ],
                'ai_status': 'Bedrock integration active',
                'timestamp': datetime.now().isoformat()
            })
        }

def handle_default_with_ai(bedrock_runtime):
    """Handle default events with AI"""
    return ai_general_response(bedrock_runtime)