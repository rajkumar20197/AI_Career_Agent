import json
import boto3
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
import re

def lambda_handler(event, context):
    """
    AWS Lambda function for autonomous job search
    Searches multiple job boards and matches opportunities to user profile
    """
    
    try:
        # Extract user profile from event
        user_profile = event.get('user_profile', {})
        search_params = event.get('search_params', {})
        
        # Initialize AWS clients
        bedrock_runtime = boto3.client('bedrock-runtime')
        s3_client = boto3.client('s3')
        
        # Search for jobs across multiple platforms
        job_results = search_multiple_job_boards(user_profile, search_params)
        
        # AI-powered job matching and ranking
        matched_jobs = ai_job_matching(bedrock_runtime, job_results, user_profile)
        
        # Store results in S3 for persistence
        store_job_results(s3_client, matched_jobs, user_profile.get('user_id'))
        
        # Prepare response
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'matched_jobs': matched_jobs[:10],  # Return top 10 matches
                'total_found': len(job_results),
                'search_timestamp': datetime.now().isoformat(),
                'next_search_scheduled': (datetime.now() + timedelta(hours=24)).isoformat()
            })
        }
        
        return response
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Failed to execute job search'
            })
        }

def search_multiple_job_boards(user_profile: Dict, search_params: Dict) -> List[Dict]:
    """Search multiple job boards for relevant opportunities"""
    
    all_jobs = []
    
    # Job board configurations
    job_boards = [
        {'name': 'indeed', 'api_endpoint': 'https://api.indeed.com/ads/apisearch'},
        {'name': 'linkedin', 'api_endpoint': 'https://api.linkedin.com/v2/jobSearch'},
        {'name': 'glassdoor', 'api_endpoint': 'https://api.glassdoor.com/api/api.htm'}
    ]
    
    # Extract search criteria
    keywords = user_profile.get('job_domain', 'Software Engineer')
    location = user_profile.get('location', 'San Francisco')
    experience_level = user_profile.get('experience_level', 'Entry Level')
    
    # For demonstration, we'll use mock data
    # In production, this would make actual API calls to job boards
    mock_jobs = generate_mock_job_listings(keywords, location, experience_level)
    all_jobs.extend(mock_jobs)
    
    return all_jobs

def generate_mock_job_listings(keywords: str, location: str, experience_level: str) -> List[Dict]:
    """Generate mock job listings for demonstration"""
    
    companies = [
        'TechCorp', 'InnovateLab', 'StartupXYZ', 'DataDriven Inc', 'CloudFirst',
        'AI Solutions', 'DevOps Masters', 'ScaleUp Co', 'NextGen Tech', 'FutureSoft'
    ]
    
    job_titles = [
        'Software Engineer', 'Frontend Developer', 'Backend Engineer', 'Full Stack Developer',
        'Data Scientist', 'Machine Learning Engineer', 'DevOps Engineer', 'Product Manager'
    ]
    
    mock_jobs = []
    
    for i in range(25):  # Generate 25 mock jobs
        job = {
            'id': f'job_{i+1}',
            'title': f"{experience_level} {job_titles[i % len(job_titles)]}",
            'company': companies[i % len(companies)],
            'location': location,
            'salary_min': 70000 + (i * 2000),
            'salary_max': 95000 + (i * 3000),
            'description': f"Exciting opportunity for a {experience_level} {job_titles[i % len(job_titles)]} to join our growing team...",
            'requirements': [
                'Bachelor\'s degree in Computer Science or related field',
                'Strong programming skills',
                'Experience with modern frameworks',
                'Excellent communication skills'
            ],
            'posted_date': (datetime.now() - timedelta(days=i % 7)).isoformat(),
            'application_url': f'https://example.com/jobs/{i+1}',
            'remote_friendly': i % 3 == 0,
            'source': 'indeed' if i % 3 == 0 else 'linkedin' if i % 3 == 1 else 'glassdoor'
        }
        mock_jobs.append(job)
    
    return mock_jobs

def ai_job_matching(bedrock_runtime, job_results: List[Dict], user_profile: Dict) -> List[Dict]:
    """Use AI to match and rank jobs based on user profile"""
    
    # Prepare user profile summary for AI
    profile_summary = f"""
    User Profile:
    - Job Domain: {user_profile.get('job_domain', 'Software Engineering')}
    - Experience Level: {user_profile.get('experience_level', 'Entry Level')}
    - Skills: {user_profile.get('skills', 'Programming, Problem Solving')}
    - Location Preference: {user_profile.get('location', 'San Francisco')}
    - Salary Expectation: ${user_profile.get('salary_expectation', 75000):,}
    """
    
    matched_jobs = []
    
    for job in job_results:
        try:
            # Calculate match score using AI
            match_score = calculate_ai_match_score(bedrock_runtime, job, profile_summary)
            
            # Add match information to job
            job['match_score'] = match_score
            job['match_reasons'] = generate_match_reasons(job, user_profile)
            job['ai_recommendations'] = generate_application_recommendations(job, user_profile)
            
            matched_jobs.append(job)
            
        except Exception as e:
            # Fallback to basic matching if AI fails
            job['match_score'] = calculate_basic_match_score(job, user_profile)
            job['match_reasons'] = ['Basic keyword matching']
            job['ai_recommendations'] = ['Review job description carefully']
            matched_jobs.append(job)
    
    # Sort by match score (highest first)
    matched_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    
    return matched_jobs

def calculate_ai_match_score(bedrock_runtime, job: Dict, profile_summary: str) -> float:
    """Use Claude to calculate intelligent job match score"""
    
    prompt = f"""
    {profile_summary}
    
    Job Details:
    - Title: {job['title']}
    - Company: {job['company']}
    - Location: {job['location']}
    - Salary: ${job['salary_min']:,} - ${job['salary_max']:,}
    - Description: {job['description'][:500]}...
    - Requirements: {', '.join(job['requirements'])}
    
    Please analyze how well this job matches the user profile and provide a match score from 0-100.
    Consider: skills alignment, experience level fit, location preference, salary expectations, and career growth potential.
    
    Respond with just the numeric score (0-100).
    """
    
    try:
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 50,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            })
        )
        
        response_body = json.loads(response['body'].read())
        score_text = response_body['content'][0]['text'].strip()
        
        # Extract numeric score
        score_match = re.search(r'\d+', score_text)
        if score_match:
            return min(100, max(0, int(score_match.group())))
        else:
            return 50  # Default score if parsing fails
            
    except Exception:
        return 50  # Fallback score

def calculate_basic_match_score(job: Dict, user_profile: Dict) -> float:
    """Calculate basic match score without AI"""
    
    score = 0
    
    # Title matching
    job_domain = user_profile.get('job_domain', '').lower()
    if job_domain in job['title'].lower():
        score += 30
    
    # Salary matching
    user_salary = user_profile.get('salary_expectation', 75000)
    if job['salary_min'] <= user_salary <= job['salary_max']:
        score += 25
    elif abs(job['salary_min'] - user_salary) < 10000:
        score += 15
    
    # Location matching
    user_location = user_profile.get('location', '').lower()
    if user_location in job['location'].lower() or job.get('remote_friendly', False):
        score += 20
    
    # Experience level matching
    experience_level = user_profile.get('experience_level', '').lower()
    if experience_level in job['title'].lower():
        score += 25
    
    return min(100, score)

def generate_match_reasons(job: Dict, user_profile: Dict) -> List[str]:
    """Generate reasons why this job is a good match"""
    
    reasons = []
    
    if job['match_score'] > 80:
        reasons.append("Excellent skills and experience alignment")
    elif job['match_score'] > 60:
        reasons.append("Good overall fit for your profile")
    
    if job.get('remote_friendly'):
        reasons.append("Offers remote work flexibility")
    
    user_salary = user_profile.get('salary_expectation', 75000)
    if job['salary_max'] >= user_salary:
        reasons.append("Meets salary expectations")
    
    return reasons

def generate_application_recommendations(job: Dict, user_profile: Dict) -> List[str]:
    """Generate AI recommendations for applying to this job"""
    
    recommendations = [
        "Tailor your resume to highlight relevant experience",
        "Research the company culture and values",
        "Prepare specific examples of your technical skills"
    ]
    
    if job['match_score'] > 85:
        recommendations.append("High match - apply immediately!")
    elif job['match_score'] < 60:
        recommendations.append("Consider gaining additional skills before applying")
    
    return recommendations

def store_job_results(s3_client, matched_jobs: List[Dict], user_id: str):
    """Store job search results in S3 for persistence"""
    
    try:
        bucket_name = 'ai-career-agent-data'  # Configure your S3 bucket
        key = f'job_searches/{user_id}/{datetime.now().strftime("%Y-%m-%d")}.json'
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps({
                'jobs': matched_jobs,
                'search_date': datetime.now().isoformat(),
                'user_id': user_id
            }),
            ContentType='application/json'
        )
        
    except Exception as e:
        print(f"Failed to store job results in S3: {str(e)}")
        # Continue execution even if S3 storage fails