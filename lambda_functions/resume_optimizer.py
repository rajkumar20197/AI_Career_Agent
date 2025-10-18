import json
import boto3
from datetime import datetime
from typing import Dict, List, Any
import re

def lambda_handler(event, context):
    """
    AWS Lambda function for AI-powered resume optimization
    Tailors resumes and cover letters for specific job applications
    """
    
    try:
        # Extract parameters from event
        user_resume = event.get('user_resume', '')
        job_description = event.get('job_description', '')
        job_title = event.get('job_title', '')
        company_name = event.get('company_name', '')
        user_profile = event.get('user_profile', {})
        
        # Initialize AWS clients
        bedrock_runtime = boto3.client('bedrock-runtime')
        s3_client = boto3.client('s3')
        
        # Generate optimized resume
        optimized_resume = optimize_resume_with_ai(
            bedrock_runtime, user_resume, job_description, job_title, company_name
        )
        
        # Generate tailored cover letter
        cover_letter = generate_cover_letter(
            bedrock_runtime, user_profile, job_description, job_title, company_name
        )
        
        # Generate application insights
        application_insights = analyze_application_strategy(
            bedrock_runtime, job_description, user_profile
        )
        
        # Store optimized documents in S3
        document_urls = store_documents(
            s3_client, optimized_resume, cover_letter, 
            user_profile.get('user_id'), job_title, company_name
        )
        
        # Prepare response
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'optimized_resume': optimized_resume,
                'cover_letter': cover_letter,
                'application_insights': application_insights,
                'document_urls': document_urls,
                'optimization_timestamp': datetime.now().isoformat()
            })
        }
        
        return response
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Failed to optimize resume and cover letter'
            })
        }

def optimize_resume_with_ai(bedrock_runtime, user_resume: str, job_description: str, 
                           job_title: str, company_name: str) -> Dict[str, Any]:
    """Use Claude to optimize resume for specific job application"""
    
    prompt = f"""
    You are an expert resume writer and career coach. Please optimize the following resume for a specific job application.

    ORIGINAL RESUME:
    {user_resume}

    JOB DETAILS:
    - Position: {job_title}
    - Company: {company_name}
    - Job Description: {job_description}

    OPTIMIZATION REQUIREMENTS:
    1. Tailor the resume to match the job requirements
    2. Highlight relevant skills and experiences
    3. Use keywords from the job description naturally
    4. Quantify achievements where possible
    5. Ensure ATS (Applicant Tracking System) compatibility
    6. Maintain professional formatting and structure
    7. Keep the resume concise and impactful

    Please provide:
    1. The optimized resume content
    2. A summary of key changes made
    3. ATS optimization score (1-10)
    4. Specific recommendations for this application

    Format your response as JSON with the following structure:
    {{
        "optimized_content": "...",
        "changes_summary": ["change1", "change2", ...],
        "ats_score": 8,
        "recommendations": ["rec1", "rec2", ...]
    }}
    """
    
    try:
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
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
        ai_response = response_body['content'][0]['text']
        
        # Parse JSON response
        try:
            optimization_result = json.loads(ai_response)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            optimization_result = {
                "optimized_content": ai_response,
                "changes_summary": ["AI optimization applied"],
                "ats_score": 7,
                "recommendations": ["Review the optimized content carefully"]
            }
        
        return optimization_result
        
    except Exception as e:
        # Fallback optimization
        return {
            "optimized_content": user_resume,
            "changes_summary": ["Optimization temporarily unavailable"],
            "ats_score": 5,
            "recommendations": ["Manual review recommended"],
            "error": str(e)
        }

def generate_cover_letter(bedrock_runtime, user_profile: Dict, job_description: str, 
                         job_title: str, company_name: str) -> Dict[str, Any]:
    """Generate personalized cover letter using AI"""
    
    prompt = f"""
    Write a compelling, personalized cover letter for the following job application:

    APPLICANT PROFILE:
    - Name: {user_profile.get('name', '[Your Name]')}
    - Job Domain: {user_profile.get('job_domain', 'Software Engineering')}
    - Experience Level: {user_profile.get('experience_level', 'Entry Level')}
    - Skills: {user_profile.get('skills', 'Programming, Problem Solving')}
    - Education: {user_profile.get('education', 'Bachelor\'s Degree')}

    JOB DETAILS:
    - Position: {job_title}
    - Company: {company_name}
    - Job Description: {job_description[:1000]}...

    COVER LETTER REQUIREMENTS:
    1. Professional and engaging tone
    2. Highlight relevant skills and experiences
    3. Show genuine interest in the company and role
    4. Demonstrate knowledge of the company's mission/values
    5. Include specific examples of achievements
    6. Strong opening and closing paragraphs
    7. Keep it concise (3-4 paragraphs)

    Please provide:
    1. The complete cover letter
    2. Key selling points highlighted
    3. Personalization score (1-10)

    Format as JSON:
    {{
        "cover_letter": "...",
        "key_selling_points": ["point1", "point2", ...],
        "personalization_score": 8
    }}
    """
    
    try:
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 1500,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            })
        )
        
        response_body = json.loads(response['body'].read())
        ai_response = response_body['content'][0]['text']
        
        # Parse JSON response
        try:
            cover_letter_result = json.loads(ai_response)
        except json.JSONDecodeError:
            cover_letter_result = {
                "cover_letter": ai_response,
                "key_selling_points": ["Relevant experience", "Strong skills match"],
                "personalization_score": 7
            }
        
        return cover_letter_result
        
    except Exception as e:
        # Fallback cover letter template
        return {
            "cover_letter": generate_fallback_cover_letter(user_profile, job_title, company_name),
            "key_selling_points": ["Template-based content"],
            "personalization_score": 4,
            "error": str(e)
        }

def analyze_application_strategy(bedrock_runtime, job_description: str, user_profile: Dict) -> Dict[str, Any]:
    """Analyze and provide strategic insights for the job application"""
    
    prompt = f"""
    Analyze this job application opportunity and provide strategic insights:

    USER PROFILE:
    - Job Domain: {user_profile.get('job_domain')}
    - Experience Level: {user_profile.get('experience_level')}
    - Skills: {user_profile.get('skills')}
    - Salary Expectation: ${user_profile.get('salary_expectation', 75000):,}

    JOB DESCRIPTION:
    {job_description[:1500]}...

    Please analyze:
    1. Strengths of the candidate for this role
    2. Potential gaps or weaknesses
    3. Interview preparation recommendations
    4. Salary negotiation insights
    5. Application timing strategy
    6. Follow-up recommendations

    Provide actionable insights in JSON format:
    {{
        "strengths": ["strength1", "strength2", ...],
        "gaps": ["gap1", "gap2", ...],
        "interview_prep": ["prep1", "prep2", ...],
        "salary_insights": "...",
        "timing_strategy": "...",
        "follow_up_plan": ["step1", "step2", ...]
    }}
    """
    
    try:
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 1000,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            })
        )
        
        response_body = json.loads(response['body'].read())
        ai_response = response_body['content'][0]['text']
        
        # Parse JSON response
        try:
            strategy_insights = json.loads(ai_response)
        except json.JSONDecodeError:
            strategy_insights = generate_fallback_insights(user_profile)
        
        return strategy_insights
        
    except Exception as e:
        return generate_fallback_insights(user_profile)

def generate_fallback_cover_letter(user_profile: Dict, job_title: str, company_name: str) -> str:
    """Generate basic cover letter template when AI is unavailable"""
    
    return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. As a {user_profile.get('experience_level', 'motivated')} professional in {user_profile.get('job_domain', 'technology')}, I am excited about the opportunity to contribute to your team.

My background in {user_profile.get('skills', 'relevant technologies')} aligns well with the requirements for this role. I am particularly drawn to {company_name} because of your reputation for innovation and excellence in the industry.

I would welcome the opportunity to discuss how my skills and enthusiasm can contribute to your team's success. Thank you for considering my application.

Sincerely,
{user_profile.get('name', '[Your Name]')}"""

def generate_fallback_insights(user_profile: Dict) -> Dict[str, Any]:
    """Generate basic application insights when AI is unavailable"""
    
    return {
        "strengths": [
            f"Strong background in {user_profile.get('job_domain', 'technology')}",
            "Relevant educational background",
            "Motivated and eager to learn"
        ],
        "gaps": [
            "May need to highlight specific technical skills",
            "Consider gaining additional industry experience"
        ],
        "interview_prep": [
            "Research the company thoroughly",
            "Prepare specific examples of your work",
            "Practice common technical questions"
        ],
        "salary_insights": "Research market rates for similar positions in your area",
        "timing_strategy": "Apply within 24-48 hours for best visibility",
        "follow_up_plan": [
            "Send application immediately",
            "Follow up after 1 week if no response",
            "Connect with hiring manager on LinkedIn"
        ]
    }

def store_documents(s3_client, optimized_resume: Dict, cover_letter: Dict, 
                   user_id: str, job_title: str, company_name: str) -> Dict[str, str]:
    """Store optimized documents in S3"""
    
    try:
        bucket_name = 'ai-career-agent-documents'  # Configure your S3 bucket
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Clean company name for filename
        clean_company = re.sub(r'[^\w\s-]', '', company_name).strip()
        clean_company = re.sub(r'[-\s]+', '_', clean_company)
        
        # Store resume
        resume_key = f'resumes/{user_id}/{clean_company}_{timestamp}_resume.json'
        s3_client.put_object(
            Bucket=bucket_name,
            Key=resume_key,
            Body=json.dumps(optimized_resume),
            ContentType='application/json'
        )
        
        # Store cover letter
        cover_letter_key = f'cover_letters/{user_id}/{clean_company}_{timestamp}_cover_letter.json'
        s3_client.put_object(
            Bucket=bucket_name,
            Key=cover_letter_key,
            Body=json.dumps(cover_letter),
            ContentType='application/json'
        )
        
        return {
            'resume_url': f's3://{bucket_name}/{resume_key}',
            'cover_letter_url': f's3://{bucket_name}/{cover_letter_key}'
        }
        
    except Exception as e:
        print(f"Failed to store documents in S3: {str(e)}")
        return {
            'resume_url': 'Storage failed',
            'cover_letter_url': 'Storage failed'
        }