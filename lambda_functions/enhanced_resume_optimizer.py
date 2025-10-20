import json
import boto3
import os
from datetime import datetime
from typing import Dict, List, Any
import re
from io import BytesIO
import PyPDF2
import docx

def lambda_handler(event, context):
    """
    Enhanced Resume Optimizer with AI-powered customization
    Features: ATS optimization, job-specific tailoring, skill gap analysis, format optimization
    """
    
    try:
        # Initialize AWS clients
        bedrock_runtime = boto3.client('bedrock-runtime')
        s3_client = boto3.client('s3')
        dynamodb = boto3.resource('dynamodb')
        
        # Extract request data
        if 'Records' in event:
            # S3 trigger - process uploaded resume
            return process_s3_resume_upload(event, bedrock_runtime, s3_client, dynamodb)
        else:
            # API call - optimize resume for specific job
            return optimize_resume_for_job(event, bedrock_runtime, s3_client, dynamodb)
            
    except Exception as e:
        error_details = {
            'error': str(e),
            'error_type': type(e).__name__,
            'timestamp': datetime.now().isoformat(),
            'event_type': 'S3' if 'Records' in event else 'API'
        }
        
        print(f"Resume Optimizer Error: {json.dumps(error_details)}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Failed to optimize resume',
                'error_id': f"resume_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'support_message': 'Please check resume format and try again'
            })
        }

def process_s3_resume_upload(event, bedrock_runtime, s3_client, dynamodb):
    """Process resume uploaded to S3 bucket"""
    
    results = []
    
    for record in event['Records']:
        try:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            
            # Extract resume content
            resume_content = extract_resume_content(s3_client, bucket, key)
            
            # AI-powered resume analysis
            analysis = analyze_resume_with_ai(bedrock_runtime, resume_content, key)
            
            # Store analysis results
            store_resume_analysis(dynamodb, analysis, key)
            
            # Generate improvement suggestions
            suggestions = generate_resume_improvements(bedrock_runtime, resume_content, analysis)
            
            results.append({
                'file': key,
                'analysis': analysis,
                'suggestions': suggestions,
                'status': 'processed'
            })
            
        except Exception as e:
            print(f"Failed to process resume {key}: {str(e)}")
            results.append({
                'file': key,
                'status': 'failed',
                'error': str(e)
            })
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Resume processing completed',
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
    }

def optimize_resume_for_job(event, bedrock_runtime, s3_client, dynamodb):
    """Optimize resume for specific job application"""
    
    body = json.loads(event.get('body', '{}'))
    
    # Extract parameters
    user_resume = body.get('user_resume', '')
    job_description = body.get('job_description', '')
    job_title = body.get('job_title', '')
    company_name = body.get('company_name', '')
    user_profile = body.get('user_profile', {})
    
    # AI-powered resume optimization
    optimized_resume = optimize_resume_with_ai(
        bedrock_runtime, user_resume, job_description, job_title, company_name
    )
    
    # Generate tailored cover letter
    cover_letter = generate_cover_letter(
        bedrock_runtime, user_profile, job_description, job_title, company_name
    )
    
    # ATS optimization analysis
    ats_analysis = analyze_ats_compatibility(bedrock_runtime, optimized_resume, job_description)
    
    # Application insights and recommendations
    application_insights = generate_application_insights(
        bedrock_runtime, optimized_resume, job_description, user_profile
    )
    
    # Store optimization results
    optimization_id = store_optimization_results(
        dynamodb, optimized_resume, cover_letter, ats_analysis, 
        application_insights, user_profile.get('user_id')
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'optimization_id': optimization_id,
            'optimized_resume': optimized_resume,
            'cover_letter': cover_letter,
            'ats_analysis': ats_analysis,
            'application_insights': application_insights,
            'timestamp': datetime.now().isoformat()
        })
    }

def extract_resume_content(s3_client, bucket: str, key: str) -> str:
    """Extract text content from resume file (PDF, DOCX, or TXT)"""
    
    try:
        # Download file from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read()
        
        # Determine file type and extract content
        if key.lower().endswith('.pdf'):
            return extract_pdf_content(file_content)
        elif key.lower().endswith('.docx'):
            return extract_docx_content(file_content)
        elif key.lower().endswith('.txt'):
            return file_content.decode('utf-8')
        else:
            # Try to decode as text
            return file_content.decode('utf-8', errors='ignore')
            
    except Exception as e:
        print(f"Failed to extract content from {key}: {str(e)}")
        return f"Error extracting content from {key}"

def extract_pdf_content(file_content: bytes) -> str:
    """Extract text from PDF file"""
    
    try:
        pdf_file = BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text_content = []
        for page in pdf_reader.pages:
            text_content.append(page.extract_text())
        
        return '\n'.join(text_content)
        
    except Exception as e:
        print(f"Failed to extract PDF content: {str(e)}")
        return "Error: Could not extract PDF content"

def extract_docx_content(file_content: bytes) -> str:
    """Extract text from DOCX file"""
    
    try:
        docx_file = BytesIO(file_content)
        doc = docx.Document(docx_file)
        
        text_content = []
        for paragraph in doc.paragraphs:
            text_content.append(paragraph.text)
        
        return '\n'.join(text_content)
        
    except Exception as e:
        print(f"Failed to extract DOCX content: {str(e)}")
        return "Error: Could not extract DOCX content"

def analyze_resume_with_ai(bedrock_runtime, resume_content: str, filename: str) -> Dict:
    """Comprehensive AI analysis of resume content"""
    
    prompt = f"""
    Analyze the following resume and provide a comprehensive assessment:
    
    RESUME CONTENT:
    {resume_content[:3000]}  # Limit content for token efficiency
    
    Please provide analysis in the following JSON format:
    {{
        "overall_score": <0-100 integer>,
        "strengths": [<list of 3-5 key strengths>],
        "weaknesses": [<list of 3-5 areas for improvement>],
        "extracted_info": {{
            "name": "<candidate name>",
            "email": "<email address>",
            "phone": "<phone number>",
            "location": "<location>",
            "experience_years": <estimated years of experience>,
            "education": [<list of education entries>],
            "skills": [<list of technical skills>],
            "work_experience": [<list of job titles and companies>],
            "certifications": [<list of certifications>]
        }},
        "ats_readiness": {{
            "score": <0-100 integer>,
            "issues": [<list of ATS compatibility issues>],
            "recommendations": [<list of ATS optimization suggestions>]
        }},
        "content_analysis": {{
            "keyword_density": "<assessment of keyword usage>",
            "quantified_achievements": <number of quantified achievements found>,
            "action_verbs_usage": "<assessment of action verb usage>",
            "formatting_quality": "<assessment of formatting and structure>"
        }},
        "improvement_priority": [<ordered list of top 5 improvements needed>]
    }}
    
    Focus on actionable insights and specific recommendations.
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
        ai_response = response_body['content'][0]['text'].strip()
        
        try:
            analysis = json.loads(ai_response)
            analysis['filename'] = filename
            analysis['analysis_date'] = datetime.now().isoformat()
            return analysis
        except json.JSONDecodeError:
            return create_fallback_analysis(resume_content, filename)
            
    except Exception as e:
        print(f"AI resume analysis failed: {str(e)}")
        return create_fallback_analysis(resume_content, filename)

def create_fallback_analysis(resume_content: str, filename: str) -> Dict:
    """Create basic analysis when AI fails"""
    
    # Basic text analysis
    word_count = len(resume_content.split())
    has_email = '@' in resume_content
    has_phone = bool(re.search(r'\d{3}[-.]?\d{3}[-.]?\d{4}', resume_content))
    
    return {
        'overall_score': 60,
        'strengths': ['Resume uploaded successfully', 'Content detected'],
        'weaknesses': ['AI analysis unavailable', 'Manual review recommended'],
        'extracted_info': {
            'name': 'Not extracted',
            'email': 'Found' if has_email else 'Not found',
            'phone': 'Found' if has_phone else 'Not found',
            'location': 'Not extracted',
            'experience_years': 0,
            'education': [],
            'skills': [],
            'work_experience': [],
            'certifications': []
        },
        'ats_readiness': {
            'score': 50,
            'issues': ['Unable to analyze ATS compatibility'],
            'recommendations': ['Manual ATS review recommended']
        },
        'content_analysis': {
            'keyword_density': 'Unable to analyze',
            'quantified_achievements': 0,
            'action_verbs_usage': 'Unable to analyze',
            'formatting_quality': 'Unable to analyze'
        },
        'improvement_priority': ['Get professional resume review'],
        'filename': filename,
        'analysis_date': datetime.now().isoformat(),
        'word_count': word_count
    }

def optimize_resume_with_ai(bedrock_runtime, user_resume: str, job_description: str, 
                           job_title: str, company_name: str) -> Dict:
    """AI-powered resume optimization for specific job"""
    
    prompt = f"""
    Optimize the following resume for this specific job application:
    
    JOB DETAILS:
    - Title: {job_title}
    - Company: {company_name}
    - Description: {job_description[:2000]}
    
    CURRENT RESUME:
    {user_resume[:2500]}
    
    Please provide optimized resume in JSON format:
    {{
        "optimized_sections": {{
            "professional_summary": "<tailored 3-4 sentence summary>",
            "key_skills": [<list of relevant skills to highlight>],
            "work_experience": [
                {{
                    "position": "<job title>",
                    "company": "<company name>",
                    "duration": "<time period>",
                    "achievements": [<list of tailored, quantified achievements>]
                }}
            ],
            "education": [<relevant education entries>],
            "additional_sections": {{
                "certifications": [<relevant certifications>],
                "projects": [<relevant projects>],
                "technical_skills": [<categorized technical skills>]
            }}
        }},
        "optimization_notes": {{
            "keywords_added": [<list of job-relevant keywords incorporated>],
            "achievements_enhanced": [<list of achievements that were improved>],
            "skills_prioritized": [<list of skills moved to prominence>],
            "content_tailored": [<list of content specifically tailored for this role>]
        }},
        "ats_optimization": {{
            "keyword_density": "<assessment>",
            "format_compatibility": "<assessment>",
            "section_organization": "<assessment>"
        }},
        "match_score": <0-100 integer representing how well optimized resume matches job>
    }}
    
    Focus on:
    1. Incorporating job-specific keywords naturally
    2. Highlighting relevant experience and achievements
    3. Quantifying accomplishments with metrics
    4. Ensuring ATS compatibility
    5. Tailoring professional summary to the role
    """
    
    try:
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
        ai_response = response_body['content'][0]['text'].strip()
        
        try:
            optimized = json.loads(ai_response)
            optimized['optimization_date'] = datetime.now().isoformat()
            optimized['job_title'] = job_title
            optimized['company_name'] = company_name
            return optimized
        except json.JSONDecodeError:
            return create_fallback_optimization(user_resume, job_title, company_name)
            
    except Exception as e:
        print(f"AI resume optimization failed: {str(e)}")
        return create_fallback_optimization(user_resume, job_title, company_name)

def create_fallback_optimization(user_resume: str, job_title: str, company_name: str) -> Dict:
    """Create basic optimization when AI fails"""
    
    return {
        'optimized_sections': {
            'professional_summary': f'Experienced professional seeking {job_title} position at {company_name}',
            'key_skills': ['Communication', 'Problem Solving', 'Teamwork'],
            'work_experience': [{'note': 'Original experience maintained - manual optimization recommended'}],
            'education': [{'note': 'Original education maintained'}],
            'additional_sections': {
                'certifications': [],
                'projects': [],
                'technical_skills': []
            }
        },
        'optimization_notes': {
            'keywords_added': ['Manual keyword optimization recommended'],
            'achievements_enhanced': ['Manual enhancement recommended'],
            'skills_prioritized': ['Manual prioritization recommended'],
            'content_tailored': ['Manual tailoring recommended']
        },
        'ats_optimization': {
            'keyword_density': 'Manual review needed',
            'format_compatibility': 'Manual review needed',
            'section_organization': 'Manual review needed'
        },
        'match_score': 50,
        'optimization_date': datetime.now().isoformat(),
        'job_title': job_title,
        'company_name': company_name,
        'note': 'AI optimization unavailable - manual review recommended'
    }

def generate_cover_letter(bedrock_runtime, user_profile: Dict, job_description: str, 
                         job_title: str, company_name: str) -> Dict:
    """Generate tailored cover letter using AI"""
    
    prompt = f"""
    Generate a professional, tailored cover letter for this job application:
    
    CANDIDATE PROFILE:
    - Name: {user_profile.get('name', 'Candidate')}
    - Experience Level: {user_profile.get('experience_level', 'Entry Level')}
    - Skills: {', '.join(user_profile.get('skills', []))}
    - Career Goals: {user_profile.get('career_goals', 'Professional growth')}
    
    JOB DETAILS:
    - Position: {job_title}
    - Company: {company_name}
    - Description: {job_description[:1500]}
    
    Generate a cover letter with these sections:
    {{
        "header": {{
            "date": "<current date>",
            "recipient": "<hiring manager address>",
            "subject": "<subject line>"
        }},
        "opening_paragraph": "<engaging opening that mentions specific role and company>",
        "body_paragraphs": [
            "<paragraph highlighting relevant experience and achievements>",
            "<paragraph demonstrating knowledge of company and role fit>",
            "<paragraph showcasing specific skills and value proposition>"
        ],
        "closing_paragraph": "<professional closing with call to action>",
        "signature": "<professional signature>",
        "key_points": [<list of key selling points emphasized>],
        "personalization_elements": [<list of company-specific elements included>]
    }}
    
    Make it professional, engaging, and specifically tailored to this opportunity.
    Avoid generic language and focus on specific value the candidate brings.
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
        ai_response = response_body['content'][0]['text'].strip()
        
        try:
            cover_letter = json.loads(ai_response)
            cover_letter['generation_date'] = datetime.now().isoformat()
            cover_letter['job_title'] = job_title
            cover_letter['company_name'] = company_name
            return cover_letter
        except json.JSONDecodeError:
            return create_fallback_cover_letter(user_profile, job_title, company_name)
            
    except Exception as e:
        print(f"AI cover letter generation failed: {str(e)}")
        return create_fallback_cover_letter(user_profile, job_title, company_name)

def create_fallback_cover_letter(user_profile: Dict, job_title: str, company_name: str) -> Dict:
    """Create basic cover letter when AI fails"""
    
    candidate_name = user_profile.get('name', 'Candidate')
    
    return {
        'header': {
            'date': datetime.now().strftime('%B %d, %Y'),
            'recipient': f'{company_name} Hiring Team',
            'subject': f'Application for {job_title} Position'
        },
        'opening_paragraph': f'Dear Hiring Manager, I am writing to express my interest in the {job_title} position at {company_name}.',
        'body_paragraphs': [
            f'As a {user_profile.get("experience_level", "motivated")} professional, I am excited about the opportunity to contribute to your team.',
            f'My background in {", ".join(user_profile.get("skills", ["various technologies"]))} aligns well with your requirements.',
            f'I am particularly drawn to {company_name} because of your reputation for innovation and excellence.'
        ],
        'closing_paragraph': 'I would welcome the opportunity to discuss how my skills and enthusiasm can contribute to your team. Thank you for your consideration.',
        'signature': f'Sincerely,\n{candidate_name}',
        'key_points': ['Relevant experience', 'Technical skills', 'Company interest'],
        'personalization_elements': [f'Company name: {company_name}', f'Position: {job_title}'],
        'generation_date': datetime.now().isoformat(),
        'job_title': job_title,
        'company_name': company_name,
        'note': 'AI generation unavailable - template provided'
    }

def analyze_ats_compatibility(bedrock_runtime, resume_content: Dict, job_description: str) -> Dict:
    """Analyze ATS (Applicant Tracking System) compatibility"""
    
    prompt = f"""
    Analyze ATS compatibility for this resume against the job description:
    
    JOB DESCRIPTION:
    {job_description[:1500]}
    
    RESUME CONTENT (key sections):
    - Skills: {resume_content.get('optimized_sections', {}).get('key_skills', [])}
    - Experience: {len(resume_content.get('optimized_sections', {}).get('work_experience', []))} positions
    - Keywords: {resume_content.get('optimization_notes', {}).get('keywords_added', [])}
    
    Provide ATS analysis in JSON format:
    {{
        "overall_ats_score": <0-100 integer>,
        "keyword_analysis": {{
            "matched_keywords": [<list of job keywords found in resume>],
            "missing_keywords": [<list of important job keywords missing>],
            "keyword_density": "<assessment of keyword usage>",
            "natural_integration": "<assessment of how naturally keywords are integrated>"
        }},
        "format_analysis": {{
            "structure_score": <0-100 integer>,
            "readability_score": <0-100 integer>,
            "section_organization": "<assessment>",
            "formatting_issues": [<list of potential formatting problems>]
        }},
        "content_optimization": {{
            "quantified_achievements": <number found>,
            "action_verbs": [<list of strong action verbs used>],
            "skills_placement": "<assessment of skills section placement and content>",
            "experience_relevance": "<assessment of experience relevance>"
        }},
        "recommendations": [<list of specific ATS optimization recommendations>],
        "pass_probability": "<High/Medium/Low assessment of ATS screening success>"
    }}
    """
    
    try:
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 1200,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            })
        )
        
        response_body = json.loads(response['body'].read())
        ai_response = response_body['content'][0]['text'].strip()
        
        try:
            ats_analysis = json.loads(ai_response)
            ats_analysis['analysis_date'] = datetime.now().isoformat()
            return ats_analysis
        except json.JSONDecodeError:
            return create_fallback_ats_analysis()
            
    except Exception as e:
        print(f"ATS analysis failed: {str(e)}")
        return create_fallback_ats_analysis()

def create_fallback_ats_analysis() -> Dict:
    """Create basic ATS analysis when AI fails"""
    
    return {
        'overall_ats_score': 70,
        'keyword_analysis': {
            'matched_keywords': ['Manual analysis required'],
            'missing_keywords': ['Manual analysis required'],
            'keyword_density': 'Unable to analyze',
            'natural_integration': 'Manual review needed'
        },
        'format_analysis': {
            'structure_score': 70,
            'readability_score': 70,
            'section_organization': 'Standard format detected',
            'formatting_issues': ['Manual review recommended']
        },
        'content_optimization': {
            'quantified_achievements': 0,
            'action_verbs': ['Manual analysis required'],
            'skills_placement': 'Manual review needed',
            'experience_relevance': 'Manual assessment required'
        },
        'recommendations': [
            'Conduct manual ATS compatibility review',
            'Ensure keywords from job description are included',
            'Use standard section headings',
            'Include quantified achievements'
        ],
        'pass_probability': 'Medium',
        'analysis_date': datetime.now().isoformat(),
        'note': 'AI analysis unavailable - manual review recommended'
    }

def generate_application_insights(bedrock_runtime, optimized_resume: Dict, 
                                job_description: str, user_profile: Dict) -> Dict:
    """Generate comprehensive application insights and recommendations"""
    
    prompt = f"""
    Provide comprehensive application insights for this job opportunity:
    
    CANDIDATE PROFILE:
    - Experience Level: {user_profile.get('experience_level')}
    - Skills: {user_profile.get('skills', [])}
    - Career Goals: {user_profile.get('career_goals')}
    
    OPTIMIZED RESUME MATCH SCORE: {optimized_resume.get('match_score', 'N/A')}
    
    JOB DESCRIPTION:
    {job_description[:1500]}
    
    Provide insights in JSON format:
    {{
        "application_strategy": {{
            "timing_recommendation": "<best time to apply>",
            "application_priority": "<High/Medium/Low>",
            "success_probability": "<percentage estimate>",
            "competitive_advantage": [<list of candidate's key advantages>]
        }},
        "interview_preparation": {{
            "likely_questions": [<list of 5 probable interview questions>],
            "technical_topics": [<list of technical areas to review>],
            "behavioral_scenarios": [<list of behavioral questions to prepare>],
            "company_research_points": [<list of company aspects to research>]
        }},
        "skill_development": {{
            "immediate_improvements": [<skills to develop before applying>],
            "long_term_growth": [<skills for career advancement>],
            "learning_resources": [<specific resources or courses to consider>]
        }},
        "negotiation_insights": {{
            "salary_range_estimate": "<estimated range for this role>",
            "negotiation_leverage": [<factors that strengthen negotiation position>],
            "benefits_to_consider": [<non-salary benefits to negotiate>]
        }},
        "application_checklist": [<list of items to complete before applying>]
    }}
    """
    
    try:
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 1800,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            })
        )
        
        response_body = json.loads(response['body'].read())
        ai_response = response_body['content'][0]['text'].strip()
        
        try:
            insights = json.loads(ai_response)
            insights['generation_date'] = datetime.now().isoformat()
            return insights
        except json.JSONDecodeError:
            return create_fallback_insights(user_profile)
            
    except Exception as e:
        print(f"Application insights generation failed: {str(e)}")
        return create_fallback_insights(user_profile)

def create_fallback_insights(user_profile: Dict) -> Dict:
    """Create basic insights when AI fails"""
    
    return {
        'application_strategy': {
            'timing_recommendation': 'Apply within 1-2 weeks of job posting',
            'application_priority': 'Medium',
            'success_probability': 'Requires detailed analysis',
            'competitive_advantage': ['Manual assessment needed']
        },
        'interview_preparation': {
            'likely_questions': [
                'Tell me about yourself',
                'Why are you interested in this role?',
                'What are your greatest strengths?',
                'Describe a challenging project you worked on',
                'Where do you see yourself in 5 years?'
            ],
            'technical_topics': ['Manual assessment based on job requirements'],
            'behavioral_scenarios': ['STAR method preparation recommended'],
            'company_research_points': ['Company mission, values, recent news, culture']
        },
        'skill_development': {
            'immediate_improvements': ['Review job requirements for specific skills'],
            'long_term_growth': ['Industry trends and emerging technologies'],
            'learning_resources': ['Online courses, certifications, practice projects']
        },
        'negotiation_insights': {
            'salary_range_estimate': 'Research market rates for similar positions',
            'negotiation_leverage': ['Relevant experience', 'In-demand skills', 'Market conditions'],
            'benefits_to_consider': ['Health insurance', 'PTO', 'Professional development', 'Remote work']
        },
        'application_checklist': [
            'Customize resume for this specific role',
            'Write tailored cover letter',
            'Research company thoroughly',
            'Prepare portfolio or work samples',
            'Practice interview questions',
            'Prepare thoughtful questions to ask interviewer'
        ],
        'generation_date': datetime.now().isoformat(),
        'note': 'AI insights unavailable - general guidance provided'
    }

def store_resume_analysis(dynamodb, analysis: Dict, filename: str):
    """Store resume analysis results in DynamoDB"""
    
    try:
        table = dynamodb.Table(os.environ.get('DYNAMODB_USER_TABLE', 'ai-career-agent-users'))
        
        # Extract user ID from filename or generate one
        user_id = extract_user_id_from_filename(filename)
        
        analysis_record = {
            'userId': user_id,
            'analysisId': f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'analysisType': 'resume_upload',
            'filename': filename,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat(),
            'ttl': int((datetime.now().timestamp()) + (90 * 24 * 60 * 60))  # 90 days TTL
        }
        
        table.put_item(Item=analysis_record)
        print(f"Successfully stored resume analysis for {filename}")
        
    except Exception as e:
        print(f"Failed to store resume analysis: {str(e)}")

def store_optimization_results(dynamodb, optimized_resume: Dict, cover_letter: Dict, 
                             ats_analysis: Dict, application_insights: Dict, user_id: str) -> str:
    """Store resume optimization results in DynamoDB"""
    
    try:
        table = dynamodb.Table(os.environ.get('DYNAMODB_USER_TABLE', 'ai-career-agent-users'))
        
        optimization_id = f"optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
        
        optimization_record = {
            'userId': user_id,
            'optimizationId': optimization_id,
            'optimizationType': 'job_specific',
            'optimizedResume': optimized_resume,
            'coverLetter': cover_letter,
            'atsAnalysis': ats_analysis,
            'applicationInsights': application_insights,
            'timestamp': datetime.now().isoformat(),
            'ttl': int((datetime.now().timestamp()) + (180 * 24 * 60 * 60))  # 180 days TTL
        }
        
        table.put_item(Item=optimization_record)
        print(f"Successfully stored optimization results: {optimization_id}")
        
        return optimization_id
        
    except Exception as e:
        print(f"Failed to store optimization results: {str(e)}")
        return f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def extract_user_id_from_filename(filename: str) -> str:
    """Extract user ID from filename or generate a default"""
    
    # Try to extract user ID from filename pattern like "user123_resume.pdf"
    match = re.search(r'user(\w+)_', filename)
    if match:
        return f"user{match.group(1)}"
    
    # Try to extract from path like "users/user123/resume.pdf"
    match = re.search(r'users?/(\w+)/', filename)
    if match:
        return match.group(1)
    
    # Generate default user ID based on filename
    return f"user_{hash(filename) % 100000}"

def generate_resume_improvements(bedrock_runtime, resume_content: str, analysis: Dict) -> Dict:
    """Generate specific improvement suggestions for the resume"""
    
    prompt = f"""
    Based on this resume analysis, provide specific improvement suggestions:
    
    CURRENT ANALYSIS:
    - Overall Score: {analysis.get('overall_score', 'N/A')}
    - Strengths: {analysis.get('strengths', [])}
    - Weaknesses: {analysis.get('weaknesses', [])}
    - ATS Score: {analysis.get('ats_readiness', {}).get('score', 'N/A')}
    
    RESUME CONTENT (first 1000 chars):
    {resume_content[:1000]}
    
    Provide improvement suggestions in JSON format:
    {{
        "immediate_fixes": [<list of quick fixes that can be implemented right away>],
        "content_improvements": [<list of content-related improvements>],
        "formatting_suggestions": [<list of formatting and structure improvements>],
        "ats_optimizations": [<list of ATS-specific improvements>],
        "skill_enhancements": [<list of ways to better showcase skills>],
        "achievement_improvements": [<list of ways to better quantify and present achievements>],
        "priority_order": [<ordered list of improvements by priority>],
        "estimated_impact": {{
            "score_improvement": "<estimated points improvement>",
            "ats_improvement": "<estimated ATS score improvement>",
            "overall_effectiveness": "<assessment of overall improvement potential>"
        }}
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
        ai_response = response_body['content'][0]['text'].strip()
        
        try:
            suggestions = json.loads(ai_response)
            suggestions['generation_date'] = datetime.now().isoformat()
            return suggestions
        except json.JSONDecodeError:
            return create_fallback_suggestions(analysis)
            
    except Exception as e:
        print(f"Resume improvement suggestions failed: {str(e)}")
        return create_fallback_suggestions(analysis)

def create_fallback_suggestions(analysis: Dict) -> Dict:
    """Create basic suggestions when AI fails"""
    
    return {
        'immediate_fixes': [
            'Ensure contact information is complete and professional',
            'Use consistent formatting throughout',
            'Check for spelling and grammar errors',
            'Use standard section headings'
        ],
        'content_improvements': [
            'Add quantified achievements with specific metrics',
            'Include relevant keywords from target job descriptions',
            'Strengthen professional summary',
            'Highlight most relevant experience first'
        ],
        'formatting_suggestions': [
            'Use clean, professional font (Arial, Calibri, or similar)',
            'Maintain consistent spacing and margins',
            'Use bullet points for easy scanning',
            'Keep to 1-2 pages maximum'
        ],
        'ats_optimizations': [
            'Include keywords from job descriptions',
            'Use standard section headings',
            'Avoid graphics, tables, and complex formatting',
            'Save in both PDF and Word formats'
        ],
        'skill_enhancements': [
            'Organize skills by category (technical, soft skills, etc.)',
            'Include proficiency levels where appropriate',
            'Add relevant certifications and training',
            'Showcase skills through specific examples'
        ],
        'achievement_improvements': [
            'Use action verbs to start bullet points',
            'Include specific numbers, percentages, and metrics',
            'Focus on results and impact, not just responsibilities',
            'Use the STAR method for complex achievements'
        ],
        'priority_order': [
            'Fix formatting and consistency issues',
            'Add quantified achievements',
            'Optimize for ATS compatibility',
            'Strengthen professional summary',
            'Enhance skills section'
        ],
        'estimated_impact': {
            'score_improvement': '10-20 points',
            'ats_improvement': '15-25 points',
            'overall_effectiveness': 'Moderate to significant improvement expected'
        },
        'generation_date': datetime.now().isoformat(),
        'note': 'AI suggestions unavailable - general best practices provided'
    }