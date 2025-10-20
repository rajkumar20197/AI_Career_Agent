import json
import boto3
import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import re
from opensearchpy import OpenSearch, RequestsHttpConnection
from aws_requests_auth.aws_auth import AWSRequestsAuth

def lambda_handler(event, context):
    """
    Enhanced AWS Lambda function for autonomous job search with AI integration
    Features: Multi-platform search, AI matching, OpenSearch indexing, Step Functions integration
    """
    
    try:
        # Initialize AWS clients with X-Ray tracing
        bedrock_runtime = boto3.client('bedrock-runtime')
        s3_client = boto3.client('s3')
        dynamodb = boto3.resource('dynamodb')
        sqs = boto3.client('sqs')
        opensearch_client = get_opensearch_client()
        
        # Extract user profile and search parameters
        user_profile = event.get('user_profile', {})
        search_params = event.get('search_params', {})
        user_id = user_profile.get('user_id')
        
        # Enhanced job search across multiple platforms
        job_results = search_multiple_job_boards_enhanced(user_profile, search_params)
        
        # AI-powered job matching with Claude 3
        matched_jobs = ai_job_matching_enhanced(bedrock_runtime, job_results, user_profile)
        
        # Index jobs in OpenSearch for powerful search capabilities
        index_jobs_in_opensearch(opensearch_client, matched_jobs, user_id)
        
        # Store results in DynamoDB with enhanced metadata
        store_job_results_enhanced(dynamodb, matched_jobs, user_profile)
        
        # Send notifications via SQS
        send_job_notifications(sqs, matched_jobs, user_id)
        
        # Prepare enhanced response
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'matched_jobs': matched_jobs[:15],  # Top 15 matches
                'total_found': len(job_results),
                'ai_insights': generate_ai_insights(matched_jobs, user_profile),
                'market_analysis': get_market_analysis(bedrock_runtime, user_profile),
                'search_metadata': {
                    'search_id': f"search_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    'timestamp': datetime.now().isoformat(),
                    'next_search_scheduled': (datetime.now() + timedelta(hours=24)).isoformat(),
                    'ai_model_used': 'claude-3-sonnet',
                    'search_platforms': ['indeed', 'linkedin', 'glassdoor', 'dice', 'monster']
                }
            })
        }
        
        return response
        
    except Exception as e:
        # Enhanced error handling with detailed logging
        error_details = {
            'error': str(e),
            'error_type': type(e).__name__,
            'timestamp': datetime.now().isoformat(),
            'user_id': user_profile.get('user_id', 'unknown'),
            'search_params': search_params
        }
        
        print(f"Enhanced Job Search Error: {json.dumps(error_details)}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Failed to execute enhanced job search',
                'error_id': f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'support_message': 'Please contact support with the error ID'
            })
        }

def get_opensearch_client():
    """Initialize OpenSearch client with AWS authentication"""
    
    host = os.environ.get('OPENSEARCH_ENDPOINT', '').replace('https://', '')
    region = os.environ.get('AWS_REGION', 'us-east-1')
    
    awsauth = AWSRequestsAuth(
        aws_access_key=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        aws_token=os.environ.get('AWS_SESSION_TOKEN'),
        aws_host=host,
        aws_region=region,
        aws_service='es'
    )
    
    return OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

def search_multiple_job_boards_enhanced(user_profile: Dict, search_params: Dict) -> List[Dict]:
    """Enhanced job search across multiple platforms with AI-powered filtering"""
    
    all_jobs = []
    
    # Enhanced job board configurations with API endpoints
    job_boards = [
        {
            'name': 'indeed',
            'api_endpoint': 'https://api.indeed.com/ads/apisearch',
            'weight': 0.3,
            'features': ['salary_data', 'company_reviews', 'remote_jobs']
        },
        {
            'name': 'linkedin',
            'api_endpoint': 'https://api.linkedin.com/v2/jobSearch',
            'weight': 0.25,
            'features': ['network_connections', 'company_insights', 'skill_assessments']
        },
        {
            'name': 'glassdoor',
            'api_endpoint': 'https://api.glassdoor.com/api/api.htm',
            'weight': 0.2,
            'features': ['company_culture', 'interview_insights', 'salary_transparency']
        },
        {
            'name': 'dice',
            'api_endpoint': 'https://service.dice.com/api/rest/jobsearch/v1/simple.json',
            'weight': 0.15,
            'features': ['tech_focus', 'contract_positions', 'skill_matching']
        },
        {
            'name': 'monster',
            'api_endpoint': 'https://api.monster.com/v2/jobsearch',
            'weight': 0.1,
            'features': ['career_advice', 'resume_services', 'broad_coverage']
        }
    ]
    
    # Extract enhanced search criteria
    keywords = user_profile.get('job_domain', 'Software Engineer')
    location = user_profile.get('location', 'Remote')
    experience_level = user_profile.get('experience_level', 'Entry Level')
    salary_min = user_profile.get('salary_expectation', 70000)
    skills = user_profile.get('skills', [])
    
    # Generate enhanced mock job listings (in production, replace with real API calls)
    for board in job_boards:
        board_jobs = generate_enhanced_mock_jobs(
            board, keywords, location, experience_level, salary_min, skills
        )
        all_jobs.extend(board_jobs)
    
    # Remove duplicates and enhance job data
    unique_jobs = remove_duplicate_jobs(all_jobs)
    enhanced_jobs = enhance_job_data(unique_jobs)
    
    return enhanced_jobs

def generate_enhanced_mock_jobs(board_config: Dict, keywords: str, location: str, 
                              experience_level: str, salary_min: int, skills: List[str]) -> List[Dict]:
    """Generate enhanced mock job listings with realistic data"""
    
    companies = [
        {'name': 'TechCorp', 'size': 'Large', 'industry': 'Technology', 'rating': 4.2},
        {'name': 'InnovateLab', 'size': 'Medium', 'industry': 'AI/ML', 'rating': 4.5},
        {'name': 'StartupXYZ', 'size': 'Small', 'industry': 'Fintech', 'rating': 4.0},
        {'name': 'DataDriven Inc', 'size': 'Medium', 'industry': 'Analytics', 'rating': 4.3},
        {'name': 'CloudFirst', 'size': 'Large', 'industry': 'Cloud Services', 'rating': 4.1},
        {'name': 'AI Solutions', 'size': 'Medium', 'industry': 'Artificial Intelligence', 'rating': 4.4},
        {'name': 'DevOps Masters', 'size': 'Small', 'industry': 'DevOps', 'rating': 4.2},
        {'name': 'ScaleUp Co', 'size': 'Medium', 'industry': 'SaaS', 'rating': 4.0},
        {'name': 'NextGen Tech', 'size': 'Large', 'industry': 'Enterprise Software', 'rating': 4.3},
        {'name': 'FutureSoft', 'size': 'Small', 'industry': 'Mobile Apps', 'rating': 4.1}
    ]
    
    job_titles = [
        'Software Engineer', 'Senior Software Engineer', 'Frontend Developer', 
        'Backend Engineer', 'Full Stack Developer', 'Data Scientist', 
        'Machine Learning Engineer', 'DevOps Engineer', 'Product Manager',
        'Cloud Architect', 'Security Engineer', 'Mobile Developer'
    ]
    
    tech_stacks = [
        ['Python', 'Django', 'PostgreSQL', 'AWS'],
        ['JavaScript', 'React', 'Node.js', 'MongoDB'],
        ['Java', 'Spring Boot', 'MySQL', 'Docker'],
        ['Python', 'FastAPI', 'Redis', 'Kubernetes'],
        ['TypeScript', 'Angular', 'GraphQL', 'Azure'],
        ['Go', 'Microservices', 'gRPC', 'GCP'],
        ['C#', '.NET Core', 'SQL Server', 'Azure'],
        ['Rust', 'WebAssembly', 'PostgreSQL', 'Docker']
    ]
    
    mock_jobs = []
    jobs_per_board = 8  # Generate 8 jobs per board
    
    for i in range(jobs_per_board):
        company = companies[i % len(companies)]
        tech_stack = tech_stacks[i % len(tech_stacks)]
        
        # Calculate salary based on experience level and location
        base_salary = 75000 if experience_level == 'Entry Level' else 95000 if experience_level == 'Mid Level' else 130000
        salary_variance = 15000
        salary_min_calc = base_salary + (i * 2000) - salary_variance
        salary_max_calc = base_salary + (i * 3000) + salary_variance
        
        job = {
            'id': f"{board_config['name']}_job_{i+1}",
            'title': f"{experience_level} {job_titles[i % len(job_titles)]}",
            'company': company['name'],
            'company_details': company,
            'location': location if i % 4 != 0 else 'Remote',
            'salary_min': max(salary_min_calc, 50000),
            'salary_max': min(salary_max_calc, 200000),
            'description': generate_job_description(job_titles[i % len(job_titles)], company['name'], tech_stack),
            'requirements': generate_job_requirements(experience_level, tech_stack),
            'benefits': generate_job_benefits(company['size']),
            'tech_stack': tech_stack,
            'posted_date': (datetime.now() - timedelta(days=i % 14)).isoformat(),
            'application_url': f'https://{board_config["name"]}.com/jobs/{i+1}',
            'remote_friendly': i % 3 == 0,
            'source': board_config['name'],
            'source_weight': board_config['weight'],
            'source_features': board_config['features'],
            'job_type': 'Full-time' if i % 5 != 0 else 'Contract',
            'visa_sponsorship': i % 6 == 0,
            'equity_offered': company['size'] in ['Small', 'Medium'] and i % 4 == 0,
            'interview_process': generate_interview_process(),
            'team_size': f"{5 + (i % 15)}-{10 + (i % 20)} engineers"
        }
        
        mock_jobs.append(job)
    
    return mock_jobs

def generate_job_description(title: str, company: str, tech_stack: List[str]) -> str:
    """Generate realistic job descriptions"""
    
    descriptions = {
        'Software Engineer': f"Join {company} as a {title} and work on cutting-edge projects using {', '.join(tech_stack[:3])}. You'll be responsible for designing, developing, and maintaining scalable applications that serve millions of users.",
        'Data Scientist': f"We're looking for a passionate {title} at {company} to analyze complex datasets and build ML models using {', '.join(tech_stack[:2])}. Drive data-driven decisions and create insights that impact business strategy.",
        'DevOps Engineer': f"As a {title} at {company}, you'll architect and maintain our cloud infrastructure using {', '.join(tech_stack)}. Automate deployments, ensure system reliability, and optimize performance.",
        'Product Manager': f"Lead product strategy at {company} as a {title}. Work closely with engineering teams using {tech_stack[0]} to deliver features that delight our customers and drive business growth."
    }
    
    base_description = descriptions.get(title.split()[-2] + ' ' + title.split()[-1], 
                                      f"Exciting opportunity at {company} to work as a {title} with modern technologies including {', '.join(tech_stack[:2])}.")
    
    return base_description + " We offer competitive compensation, excellent benefits, and opportunities for professional growth in a collaborative environment."

def generate_job_requirements(experience_level: str, tech_stack: List[str]) -> List[str]:
    """Generate realistic job requirements based on experience level"""
    
    base_requirements = [
        f"Proficiency in {tech_stack[0]} and {tech_stack[1]}",
        "Strong problem-solving and analytical skills",
        "Excellent communication and teamwork abilities",
        "Experience with version control (Git) and agile methodologies"
    ]
    
    if experience_level == 'Entry Level':
        base_requirements.extend([
            "Bachelor's degree in Computer Science or related field",
            "0-2 years of professional experience",
            "Eagerness to learn and grow in a fast-paced environment"
        ])
    elif experience_level == 'Mid Level':
        base_requirements.extend([
            "3-5 years of professional software development experience",
            f"Experience with {tech_stack[2]} and cloud platforms",
            "Track record of delivering production-quality software"
        ])
    else:  # Senior Level
        base_requirements.extend([
            "5+ years of professional experience in software development",
            f"Deep expertise in {tech_stack[0]} ecosystem and architecture patterns",
            "Experience mentoring junior developers and leading technical initiatives",
            "Strong system design and scalability knowledge"
        ])
    
    return base_requirements

def generate_job_benefits(company_size: str) -> List[str]:
    """Generate realistic job benefits based on company size"""
    
    base_benefits = [
        "Competitive salary and performance bonuses",
        "Comprehensive health, dental, and vision insurance",
        "401(k) with company matching",
        "Flexible PTO and work-life balance"
    ]
    
    if company_size == 'Large':
        base_benefits.extend([
            "Stock options and equity participation",
            "Professional development budget ($3,000/year)",
            "On-site gym and wellness programs",
            "Parental leave and family support"
        ])
    elif company_size == 'Medium':
        base_benefits.extend([
            "Equity participation and growth opportunities",
            "Learning and development stipend ($2,000/year)",
            "Remote work flexibility",
            "Team building events and company retreats"
        ])
    else:  # Small
        base_benefits.extend([
            "Significant equity upside potential",
            "Direct impact on product and company direction",
            "Flexible work arrangements",
            "Close-knit team culture and mentorship"
        ])
    
    return base_benefits

def generate_interview_process() -> Dict:
    """Generate realistic interview process information"""
    
    processes = [
        {
            'stages': ['Phone Screen', 'Technical Interview', 'System Design', 'Cultural Fit'],
            'duration': '2-3 weeks',
            'feedback_timeline': '1 week'
        },
        {
            'stages': ['Recruiter Call', 'Coding Challenge', 'Technical Panel', 'Final Interview'],
            'duration': '3-4 weeks',
            'feedback_timeline': '5 business days'
        },
        {
            'stages': ['Initial Screen', 'Take-home Project', 'Technical Discussion', 'Team Meet'],
            'duration': '2-4 weeks',
            'feedback_timeline': '1 week'
        }
    ]
    
    return processes[hash(str(datetime.now())) % len(processes)]

def ai_job_matching_enhanced(bedrock_runtime, job_results: List[Dict], user_profile: Dict) -> List[Dict]:
    """Enhanced AI job matching using Claude 3 Sonnet with detailed analysis"""
    
    # Prepare comprehensive user profile for AI analysis
    profile_summary = create_detailed_profile_summary(user_profile)
    
    matched_jobs = []
    
    for job in job_results:
        try:
            # Enhanced AI match scoring with Claude 3 Sonnet
            match_analysis = calculate_enhanced_ai_match_score(bedrock_runtime, job, profile_summary)
            
            # Add comprehensive match information
            job.update({
                'match_score': match_analysis['score'],
                'match_reasons': match_analysis['reasons'],
                'skill_gaps': match_analysis['skill_gaps'],
                'growth_potential': match_analysis['growth_potential'],
                'ai_recommendations': match_analysis['recommendations'],
                'salary_analysis': analyze_salary_fit(job, user_profile),
                'culture_fit': analyze_culture_fit(job, user_profile),
                'career_progression': analyze_career_progression(job, user_profile)
            })
            
            matched_jobs.append(job)
            
        except Exception as e:
            print(f"AI matching failed for job {job.get('id', 'unknown')}: {str(e)}")
            # Fallback to enhanced basic matching
            job.update(calculate_enhanced_basic_match_score(job, user_profile))
            matched_jobs.append(job)
    
    # Sort by match score with tie-breaking logic
    matched_jobs.sort(key=lambda x: (
        x['match_score'], 
        x.get('salary_max', 0), 
        1 if x.get('remote_friendly', False) else 0
    ), reverse=True)
    
    return matched_jobs

def create_detailed_profile_summary(user_profile: Dict) -> str:
    """Create a comprehensive profile summary for AI analysis"""
    
    return f"""
    CANDIDATE PROFILE ANALYSIS:
    
    Personal Information:
    - Job Domain: {user_profile.get('job_domain', 'Software Engineering')}
    - Experience Level: {user_profile.get('experience_level', 'Entry Level')}
    - Current Location: {user_profile.get('location', 'Not specified')}
    - Graduation Timeline: {user_profile.get('graduation_date', 'Not specified')}
    
    Technical Skills:
    - Primary Skills: {', '.join(user_profile.get('skills', ['Programming', 'Problem Solving']))}
    - Programming Languages: {', '.join(user_profile.get('programming_languages', ['Python', 'JavaScript']))}
    - Frameworks/Tools: {', '.join(user_profile.get('frameworks', ['React', 'Django']))}
    - Cloud Platforms: {', '.join(user_profile.get('cloud_experience', ['AWS']))}
    
    Career Preferences:
    - Salary Expectation: ${user_profile.get('salary_expectation', 75000):,}
    - Work Style: {user_profile.get('work_style', 'Hybrid')}
    - Company Size Preference: {user_profile.get('company_size_pref', 'Any')}
    - Industry Interest: {user_profile.get('industry_interest', 'Technology')}
    
    Professional Goals:
    - Career Goals: {user_profile.get('career_goals', 'Professional growth and skill development')}
    - Learning Interests: {', '.join(user_profile.get('learning_interests', ['Machine Learning', 'Cloud Computing']))}
    - Leadership Aspirations: {user_profile.get('leadership_goals', 'Individual contributor to team lead')}
    """

def calculate_enhanced_ai_match_score(bedrock_runtime, job: Dict, profile_summary: str) -> Dict:
    """Use Claude 3 Sonnet for comprehensive job matching analysis"""
    
    prompt = f"""
    {profile_summary}
    
    JOB OPPORTUNITY ANALYSIS:
    - Title: {job['title']}
    - Company: {job['company']} ({job['company_details']['size']} company, {job['company_details']['industry']} industry)
    - Location: {job['location']} (Remote: {job['remote_friendly']})
    - Salary Range: ${job['salary_min']:,} - ${job['salary_max']:,}
    - Tech Stack: {', '.join(job['tech_stack'])}
    - Job Type: {job['job_type']}
    - Experience Required: {job['title']}
    - Benefits: {', '.join(job['benefits'][:3])}
    - Team Size: {job['team_size']}
    - Visa Sponsorship: {job['visa_sponsorship']}
    - Equity: {job['equity_offered']}
    
    Job Description: {job['description'][:800]}
    
    Requirements: {', '.join(job['requirements'])}
    
    Please provide a comprehensive analysis in the following JSON format:
    {
        "score": <0-100 integer>,
        "reasons": [<list of 3-5 specific reasons for the match>],
        "skill_gaps": [<list of skills candidate should develop>],
        "growth_potential": "<assessment of career growth opportunities>",
        "recommendations": [<list of 3-4 actionable recommendations for applying>]
    }
    
    Consider: technical skill alignment, experience level fit, salary expectations, location preferences, 
    company culture fit, career growth potential, learning opportunities, and long-term career trajectory.
    
    Respond with ONLY the JSON object, no additional text.
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
        ai_response = response_body['content'][0]['text'].strip()
        
        # Parse JSON response
        try:
            analysis = json.loads(ai_response)
            # Validate and sanitize the response
            return {
                'score': max(0, min(100, analysis.get('score', 50))),
                'reasons': analysis.get('reasons', ['AI analysis unavailable']),
                'skill_gaps': analysis.get('skill_gaps', []),
                'growth_potential': analysis.get('growth_potential', 'Assessment unavailable'),
                'recommendations': analysis.get('recommendations', ['Review job requirements carefully'])
            }
        except json.JSONDecodeError:
            # Fallback parsing if JSON is malformed
            return parse_ai_response_fallback(ai_response)
            
    except Exception as e:
        print(f"AI analysis failed: {str(e)}")
        return {
            'score': 50,
            'reasons': ['AI analysis temporarily unavailable'],
            'skill_gaps': ['Unable to assess'],
            'growth_potential': 'Assessment unavailable',
            'recommendations': ['Review job description manually']
        }

def parse_ai_response_fallback(response_text: str) -> Dict:
    """Fallback parser for AI responses that aren't valid JSON"""
    
    # Extract score using regex
    score_match = re.search(r'"?score"?\s*:\s*(\d+)', response_text)
    score = int(score_match.group(1)) if score_match else 50
    
    return {
        'score': max(0, min(100, score)),
        'reasons': ['Basic compatibility assessment'],
        'skill_gaps': ['Manual review recommended'],
        'growth_potential': 'Requires further analysis',
        'recommendations': ['Research company and role thoroughly']
    }

def analyze_salary_fit(job: Dict, user_profile: Dict) -> Dict:
    """Analyze salary fit and provide insights"""
    
    user_expectation = user_profile.get('salary_expectation', 75000)
    job_min = job['salary_min']
    job_max = job['salary_max']
    job_mid = (job_min + job_max) / 2
    
    if user_expectation <= job_max and user_expectation >= job_min:
        fit_level = 'Excellent'
        message = f"Salary range ${job_min:,}-${job_max:,} meets your expectation of ${user_expectation:,}"
    elif user_expectation < job_min:
        fit_level = 'Above Expectations'
        message = f"Salary range ${job_min:,}-${job_max:,} exceeds your expectation of ${user_expectation:,}"
    elif user_expectation <= job_mid:
        fit_level = 'Good'
        message = f"Salary negotiable within range ${job_min:,}-${job_max:,}"
    else:
        fit_level = 'Below Expectations'
        message = f"Salary range ${job_min:,}-${job_max:,} below expectation of ${user_expectation:,}"
    
    return {
        'fit_level': fit_level,
        'message': message,
        'negotiation_potential': 'High' if job.get('equity_offered') else 'Medium'
    }

def analyze_culture_fit(job: Dict, user_profile: Dict) -> Dict:
    """Analyze company culture fit"""
    
    company_size = job['company_details']['size']
    user_pref = user_profile.get('company_size_pref', 'Any')
    work_style = user_profile.get('work_style', 'Hybrid')
    
    culture_score = 70  # Base score
    
    # Company size preference
    if user_pref == 'Any' or user_pref == company_size:
        culture_score += 15
    
    # Remote work alignment
    if work_style == 'Remote' and job['remote_friendly']:
        culture_score += 10
    elif work_style == 'Hybrid' and (job['location'] != 'Remote' or job['remote_friendly']):
        culture_score += 5
    
    # Industry alignment
    user_industry = user_profile.get('industry_interest', 'Technology')
    if user_industry.lower() in job['company_details']['industry'].lower():
        culture_score += 5
    
    return {
        'score': min(100, culture_score),
        'company_size_fit': company_size == user_pref or user_pref == 'Any',
        'work_style_fit': assess_work_style_fit(work_style, job),
        'industry_alignment': user_industry.lower() in job['company_details']['industry'].lower()
    }

def assess_work_style_fit(user_style: str, job: Dict) -> bool:
    """Assess work style compatibility"""
    
    if user_style == 'Remote':
        return job['remote_friendly'] or job['location'] == 'Remote'
    elif user_style == 'On-site':
        return job['location'] != 'Remote'
    else:  # Hybrid
        return True  # Hybrid workers are generally flexible

def analyze_career_progression(job: Dict, user_profile: Dict) -> Dict:
    """Analyze career progression opportunities"""
    
    current_level = user_profile.get('experience_level', 'Entry Level')
    job_title = job['title']
    company_size = job['company_details']['size']
    
    progression_score = 60  # Base score
    
    # Level progression analysis
    if 'Senior' in job_title and current_level in ['Entry Level', 'Mid Level']:
        progression_score += 20
        progression_type = 'Advancement Opportunity'
    elif 'Lead' in job_title or 'Principal' in job_title:
        progression_score += 25
        progression_type = 'Leadership Track'
    else:
        progression_type = 'Skill Development'
    
    # Company size impact on growth
    if company_size == 'Large':
        progression_score += 10
        growth_path = 'Structured career ladder with defined levels'
    elif company_size == 'Medium':
        progression_score += 15
        growth_path = 'Flexible growth with cross-functional opportunities'
    else:
        progression_score += 20
        growth_path = 'Rapid growth potential with broad responsibilities'
    
    return {
        'score': min(100, progression_score),
        'progression_type': progression_type,
        'growth_path': growth_path,
        'mentorship_available': company_size in ['Medium', 'Large'],
        'learning_budget': job['benefits'] and any('development' in benefit.lower() for benefit in job['benefits'])
    }

def remove_duplicate_jobs(jobs: List[Dict]) -> List[Dict]:
    """Remove duplicate jobs based on title and company"""
    
    seen = set()
    unique_jobs = []
    
    for job in jobs:
        job_key = (job['title'].lower(), job['company'].lower())
        if job_key not in seen:
            seen.add(job_key)
            unique_jobs.append(job)
    
    return unique_jobs

def enhance_job_data(jobs: List[Dict]) -> List[Dict]:
    """Enhance job data with additional computed fields"""
    
    for job in jobs:
        # Add computed fields
        job['salary_midpoint'] = (job['salary_min'] + job['salary_max']) / 2
        job['days_since_posted'] = (datetime.now() - datetime.fromisoformat(job['posted_date'].replace('Z', '+00:00'))).days
        job['urgency_score'] = calculate_urgency_score(job)
        job['competitiveness_score'] = calculate_competitiveness_score(job)
    
    return jobs

def calculate_urgency_score(job: Dict) -> int:
    """Calculate job application urgency score"""
    
    days_posted = job['days_since_posted']
    
    if days_posted <= 3:
        return 90  # Very urgent
    elif days_posted <= 7:
        return 70  # Urgent
    elif days_posted <= 14:
        return 50  # Moderate
    else:
        return 30  # Low urgency

def calculate_competitiveness_score(job: Dict) -> int:
    """Calculate job competitiveness score"""
    
    score = 50  # Base score
    
    # High salary increases competitiveness
    if job['salary_max'] > 120000:
        score += 20
    elif job['salary_max'] > 90000:
        score += 10
    
    # Remote work increases competitiveness
    if job['remote_friendly']:
        score += 15
    
    # Equity and benefits
    if job['equity_offered']:
        score += 10
    
    # Company rating
    company_rating = job['company_details'].get('rating', 3.5)
    if company_rating >= 4.0:
        score += 10
    
    return min(100, score)

def index_jobs_in_opensearch(opensearch_client, jobs: List[Dict], user_id: str):
    """Index jobs in OpenSearch for powerful search capabilities"""
    
    try:
        index_name = f"job-search-{datetime.now().strftime('%Y-%m')}"
        
        # Create index if it doesn't exist
        if not opensearch_client.indices.exists(index=index_name):
            create_job_search_index(opensearch_client, index_name)
        
        # Index each job
        for job in jobs:
            doc_id = f"{user_id}_{job['id']}"
            
            # Prepare document for indexing
            doc = {
                'user_id': user_id,
                'job_id': job['id'],
                'title': job['title'],
                'company': job['company'],
                'location': job['location'],
                'salary_min': job['salary_min'],
                'salary_max': job['salary_max'],
                'salary_midpoint': job['salary_midpoint'],
                'tech_stack': job['tech_stack'],
                'description': job['description'],
                'requirements': job['requirements'],
                'benefits': job['benefits'],
                'match_score': job.get('match_score', 0),
                'remote_friendly': job['remote_friendly'],
                'source': job['source'],
                'posted_date': job['posted_date'],
                'indexed_date': datetime.now().isoformat(),
                'company_size': job['company_details']['size'],
                'company_industry': job['company_details']['industry'],
                'job_type': job['job_type'],
                'visa_sponsorship': job['visa_sponsorship'],
                'equity_offered': job['equity_offered']
            }
            
            opensearch_client.index(
                index=index_name,
                id=doc_id,
                body=doc
            )
        
        print(f"Successfully indexed {len(jobs)} jobs for user {user_id}")
        
    except Exception as e:
        print(f"Failed to index jobs in OpenSearch: {str(e)}")
        # Continue execution even if indexing fails

def create_job_search_index(opensearch_client, index_name: str):
    """Create OpenSearch index with proper mappings for job search"""
    
    mapping = {
        "mappings": {
            "properties": {
                "user_id": {"type": "keyword"},
                "job_id": {"type": "keyword"},
                "title": {"type": "text", "analyzer": "standard"},
                "company": {"type": "text", "analyzer": "standard"},
                "location": {"type": "keyword"},
                "salary_min": {"type": "integer"},
                "salary_max": {"type": "integer"},
                "salary_midpoint": {"type": "float"},
                "tech_stack": {"type": "keyword"},
                "description": {"type": "text", "analyzer": "standard"},
                "requirements": {"type": "text", "analyzer": "standard"},
                "benefits": {"type": "text", "analyzer": "standard"},
                "match_score": {"type": "float"},
                "remote_friendly": {"type": "boolean"},
                "source": {"type": "keyword"},
                "posted_date": {"type": "date"},
                "indexed_date": {"type": "date"},
                "company_size": {"type": "keyword"},
                "company_industry": {"type": "keyword"},
                "job_type": {"type": "keyword"},
                "visa_sponsorship": {"type": "boolean"},
                "equity_offered": {"type": "boolean"}
            }
        }
    }
    
    opensearch_client.indices.create(index=index_name, body=mapping)

def store_job_results_enhanced(dynamodb, matched_jobs: List[Dict], user_profile: Dict):
    """Store enhanced job search results in DynamoDB"""
    
    try:
        table = dynamodb.Table(os.environ['DYNAMODB_JOB_TABLE'])
        
        search_record = {
            'searchId': f"search_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_profile['user_id']}",
            'userId': user_profile['user_id'],
            'timestamp': datetime.now().isoformat(),
            'search_params': {
                'job_domain': user_profile.get('job_domain'),
                'location': user_profile.get('location'),
                'experience_level': user_profile.get('experience_level'),
                'salary_expectation': user_profile.get('salary_expectation')
            },
            'results_summary': {
                'total_jobs_found': len(matched_jobs),
                'top_match_score': matched_jobs[0]['match_score'] if matched_jobs else 0,
                'average_match_score': sum(job['match_score'] for job in matched_jobs) / len(matched_jobs) if matched_jobs else 0,
                'sources_searched': list(set(job['source'] for job in matched_jobs)),
                'salary_range': {
                    'min': min(job['salary_min'] for job in matched_jobs) if matched_jobs else 0,
                    'max': max(job['salary_max'] for job in matched_jobs) if matched_jobs else 0
                }
            },
            'top_matches': matched_jobs[:10],  # Store top 10 matches
            'ai_insights': generate_search_insights(matched_jobs, user_profile),
            'ttl': int((datetime.now() + timedelta(days=90)).timestamp())  # Auto-delete after 90 days
        }
        
        table.put_item(Item=search_record)
        print(f"Successfully stored job search results for user {user_profile['user_id']}")
        
    except Exception as e:
        print(f"Failed to store job results in DynamoDB: {str(e)}")

def generate_search_insights(matched_jobs: List[Dict], user_profile: Dict) -> Dict:
    """Generate insights from job search results"""
    
    if not matched_jobs:
        return {'message': 'No jobs found matching criteria'}
    
    # Calculate insights
    avg_salary = sum(job['salary_midpoint'] for job in matched_jobs) / len(matched_jobs)
    remote_percentage = (sum(1 for job in matched_jobs if job['remote_friendly']) / len(matched_jobs)) * 100
    top_companies = [job['company'] for job in matched_jobs[:5]]
    common_skills = get_most_common_skills([job['tech_stack'] for job in matched_jobs])
    
    return {
        'market_insights': {
            'average_salary_offered': f"${avg_salary:,.0f}",
            'remote_work_availability': f"{remote_percentage:.1f}%",
            'top_hiring_companies': top_companies,
            'in_demand_skills': common_skills[:5],
            'job_market_competitiveness': assess_market_competitiveness(matched_jobs)
        },
        'recommendations': generate_market_recommendations(matched_jobs, user_profile),
        'skill_development_suggestions': suggest_skill_development(matched_jobs, user_profile)
    }

def get_most_common_skills(tech_stacks: List[List[str]]) -> List[str]:
    """Get most commonly required skills across job listings"""
    
    skill_count = {}
    for stack in tech_stacks:
        for skill in stack:
            skill_count[skill] = skill_count.get(skill, 0) + 1
    
    return sorted(skill_count.keys(), key=lambda x: skill_count[x], reverse=True)

def assess_market_competitiveness(jobs: List[Dict]) -> str:
    """Assess overall job market competitiveness"""
    
    avg_match_score = sum(job['match_score'] for job in jobs) / len(jobs)
    
    if avg_match_score >= 80:
        return 'Highly Favorable'
    elif avg_match_score >= 65:
        return 'Favorable'
    elif avg_match_score >= 50:
        return 'Competitive'
    else:
        return 'Challenging'

def generate_market_recommendations(jobs: List[Dict], user_profile: Dict) -> List[str]:
    """Generate market-based recommendations"""
    
    recommendations = []
    
    # Salary recommendations
    user_expectation = user_profile.get('salary_expectation', 75000)
    avg_offered = sum(job['salary_midpoint'] for job in jobs) / len(jobs)
    
    if avg_offered > user_expectation * 1.1:
        recommendations.append(f"Market offers ${avg_offered:,.0f} on average - consider raising salary expectations")
    elif avg_offered < user_expectation * 0.9:
        recommendations.append(f"Market average ${avg_offered:,.0f} is below expectations - consider expanding search criteria")
    
    # Remote work recommendations
    remote_jobs = [job for job in jobs if job['remote_friendly']]
    if len(remote_jobs) > len(jobs) * 0.6:
        recommendations.append("Strong remote work opportunities available - highlight remote work experience")
    
    # Skill recommendations
    common_skills = get_most_common_skills([job['tech_stack'] for job in jobs])
    user_skills = user_profile.get('skills', [])
    missing_skills = [skill for skill in common_skills[:3] if skill not in user_skills]
    
    if missing_skills:
        recommendations.append(f"Consider learning {', '.join(missing_skills)} - highly demanded in current market")
    
    return recommendations

def suggest_skill_development(jobs: List[Dict], user_profile: Dict) -> List[str]:
    """Suggest skills to develop based on job requirements"""
    
    # Analyze skill gaps from job requirements
    all_requirements = []
    for job in jobs:
        all_requirements.extend(job.get('tech_stack', []))
    
    skill_frequency = {}
    for skill in all_requirements:
        skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
    
    # Get top skills not in user profile
    user_skills = [skill.lower() for skill in user_profile.get('skills', [])]
    suggestions = []
    
    for skill, frequency in sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True):
        if skill.lower() not in user_skills and len(suggestions) < 5:
            suggestions.append(f"{skill} (mentioned in {frequency} job listings)")
    
    return suggestions

def send_job_notifications(sqs, matched_jobs: List[Dict], user_id: str):
    """Send job search notifications via SQS"""
    
    try:
        if not matched_jobs:
            return
        
        # Prepare notification message
        top_jobs = matched_jobs[:3]  # Top 3 matches
        
        notification = {
            'user_id': user_id,
            'notification_type': 'job_search_complete',
            'timestamp': datetime.now().isoformat(),
            'data': {
                'total_jobs_found': len(matched_jobs),
                'top_matches': [
                    {
                        'title': job['title'],
                        'company': job['company'],
                        'match_score': job['match_score'],
                        'salary_range': f"${job['salary_min']:,} - ${job['salary_max']:,}",
                        'location': job['location'],
                        'application_url': job['application_url']
                    }
                    for job in top_jobs
                ],
                'search_summary': f"Found {len(matched_jobs)} jobs with average match score of {sum(job['match_score'] for job in matched_jobs) / len(matched_jobs):.1f}%"
            }
        }
        
        sqs.send_message(
            QueueUrl=os.environ['NOTIFICATION_QUEUE_URL'],
            MessageBody=json.dumps(notification)
        )
        
        print(f"Successfully sent job notification for user {user_id}")
        
    except Exception as e:
        print(f"Failed to send job notifications: {str(e)}")

def generate_ai_insights(matched_jobs: List[Dict], user_profile: Dict) -> Dict:
    """Generate AI-powered insights about the job search results"""
    
    if not matched_jobs:
        return {'message': 'No insights available - no jobs found'}
    
    return {
        'market_trends': {
            'hot_skills': get_most_common_skills([job['tech_stack'] for job in matched_jobs])[:5],
            'salary_trends': analyze_salary_trends(matched_jobs),
            'remote_work_trend': f"{(sum(1 for job in matched_jobs if job['remote_friendly']) / len(matched_jobs)) * 100:.1f}% of jobs offer remote work",
            'company_size_distribution': analyze_company_size_distribution(matched_jobs)
        },
        'personalized_insights': {
            'best_fit_companies': [job['company'] for job in matched_jobs[:3]],
            'skill_alignment': assess_skill_alignment(matched_jobs, user_profile),
            'career_progression_opportunities': count_progression_opportunities(matched_jobs),
            'negotiation_potential': assess_negotiation_potential(matched_jobs, user_profile)
        },
        'action_items': generate_action_items(matched_jobs, user_profile)
    }

def analyze_salary_trends(jobs: List[Dict]) -> Dict:
    """Analyze salary trends in job results"""
    
    salaries = [job['salary_midpoint'] for job in jobs]
    
    return {
        'average': f"${sum(salaries) / len(salaries):,.0f}",
        'median': f"${sorted(salaries)[len(salaries) // 2]:,.0f}",
        'range': f"${min(salaries):,.0f} - ${max(salaries):,.0f}",
        'high_paying_percentage': f"{(sum(1 for s in salaries if s > 100000) / len(salaries)) * 100:.1f}%"
    }

def analyze_company_size_distribution(jobs: List[Dict]) -> Dict:
    """Analyze company size distribution"""
    
    size_count = {}
    for job in jobs:
        size = job['company_details']['size']
        size_count[size] = size_count.get(size, 0) + 1
    
    total = len(jobs)
    return {size: f"{(count / total) * 100:.1f}%" for size, count in size_count.items()}

def assess_skill_alignment(jobs: List[Dict], user_profile: Dict) -> str:
    """Assess how well user skills align with job requirements"""
    
    user_skills = set(skill.lower() for skill in user_profile.get('skills', []))
    
    alignment_scores = []
    for job in jobs:
        job_skills = set(skill.lower() for skill in job['tech_stack'])
        if job_skills:
            alignment = len(user_skills.intersection(job_skills)) / len(job_skills)
            alignment_scores.append(alignment)
    
    if alignment_scores:
        avg_alignment = sum(alignment_scores) / len(alignment_scores)
        if avg_alignment >= 0.7:
            return "Excellent - Strong skill alignment with most positions"
        elif avg_alignment >= 0.5:
            return "Good - Moderate skill alignment, some gaps to address"
        else:
            return "Developing - Significant skill development opportunities identified"
    
    return "Unable to assess - insufficient data"

def count_progression_opportunities(jobs: List[Dict]) -> int:
    """Count jobs that offer clear progression opportunities"""
    
    progression_keywords = ['senior', 'lead', 'principal', 'manager', 'director', 'architect']
    
    return sum(1 for job in jobs if any(keyword in job['title'].lower() for keyword in progression_keywords))

def assess_negotiation_potential(jobs: List[Dict], user_profile: Dict) -> str:
    """Assess salary negotiation potential"""
    
    user_expectation = user_profile.get('salary_expectation', 75000)
    above_expectation = sum(1 for job in jobs if job['salary_max'] > user_expectation)
    
    percentage = (above_expectation / len(jobs)) * 100 if jobs else 0
    
    if percentage >= 70:
        return "High - Most positions offer salary above expectations"
    elif percentage >= 40:
        return "Moderate - Good negotiation opportunities available"
    else:
        return "Limited - Consider expanding search or adjusting expectations"

def generate_action_items(jobs: List[Dict], user_profile: Dict) -> List[str]:
    """Generate actionable next steps based on job search results"""
    
    actions = []
    
    if jobs:
        # Top applications
        top_matches = [job for job in jobs if job['match_score'] >= 80]
        if top_matches:
            actions.append(f"Apply immediately to {len(top_matches)} high-match positions (80%+ match)")
        
        # Skill development
        common_skills = get_most_common_skills([job['tech_stack'] for job in jobs])
        user_skills = [skill.lower() for skill in user_profile.get('skills', [])]
        missing_skills = [skill for skill in common_skills[:3] if skill.lower() not in user_skills]
        
        if missing_skills:
            actions.append(f"Develop skills in {', '.join(missing_skills)} to increase competitiveness")
        
        # Network building
        top_companies = list(set(job['company'] for job in jobs[:10]))
        actions.append(f"Research and network with employees at {', '.join(top_companies[:3])}")
        
        # Application optimization
        actions.append("Customize resume and cover letter for each high-match position")
        
        # Interview preparation
        if any(job['match_score'] >= 70 for job in jobs):
            actions.append("Prepare for technical interviews focusing on your strongest skill areas")
    
    else:
        actions.extend([
            "Expand search criteria (location, experience level, or job titles)",
            "Update and optimize your profile with additional skills",
            "Consider entry-level positions to gain experience",
            "Network with professionals in your target industry"
        ])
    
    return actions

def get_market_analysis(bedrock_runtime, user_profile: Dict) -> Dict:
    """Get AI-powered market analysis for the user's domain"""
    
    try:
        job_domain = user_profile.get('job_domain', 'Software Engineering')
        location = user_profile.get('location', 'United States')
        experience_level = user_profile.get('experience_level', 'Entry Level')
        
        prompt = f"""
        Provide a comprehensive job market analysis for:
        - Job Domain: {job_domain}
        - Location: {location}
        - Experience Level: {experience_level}
        
        Include insights on:
        1. Market demand and growth trends
        2. Salary expectations and ranges
        3. In-demand skills and technologies
        4. Career progression opportunities
        5. Industry challenges and opportunities
        
        Respond in JSON format with specific, actionable insights.
        """
        
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
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
        ai_response = response_body['content'][0]['text'].strip()
        
        # Try to parse as JSON, fallback to structured text
        try:
            return json.loads(ai_response)
        except json.JSONDecodeError:
            return {
                'market_summary': ai_response[:500] + '...',
                'analysis_date': datetime.now().isoformat(),
                'note': 'Detailed analysis available - contact for full report'
            }
            
    except Exception as e:
        print(f"Market analysis failed: {str(e)}")
        return {
            'market_summary': f"Market analysis for {job_domain} shows continued growth and opportunities",
            'note': 'Detailed analysis temporarily unavailable',
            'analysis_date': datetime.now().isoformat()
        }

def calculate_enhanced_basic_match_score(job: Dict, user_profile: Dict) -> Dict:
    """Enhanced fallback matching when AI is unavailable"""
    
    score = 0
    reasons = []
    
    # Title and domain matching (30 points)
    job_domain = user_profile.get('job_domain', '').lower()
    if job_domain in job['title'].lower():
        score += 30
        reasons.append(f"Job title matches your {job_domain} domain")
    
    # Salary matching (25 points)
    user_salary = user_profile.get('salary_expectation', 75000)
    if job['salary_min'] <= user_salary <= job['salary_max']:
        score += 25
        reasons.append("Salary range meets your expectations")
    elif abs(job['salary_min'] - user_salary) < 15000:
        score += 15
        reasons.append("Salary range is close to your expectations")
    
    # Location and remote work (20 points)
    user_location = user_profile.get('location', '').lower()
    if user_location in job['location'].lower() or job.get('remote_friendly', False):
        score += 20
        reasons.append("Location preferences aligned")
    
    # Experience level matching (15 points)
    experience_level = user_profile.get('experience_level', '').lower()
    if experience_level in job['title'].lower():
        score += 15
        reasons.append("Experience level is a good match")
    
    # Skills matching (10 points)
    user_skills = set(skill.lower() for skill in user_profile.get('skills', []))
    job_skills = set(skill.lower() for skill in job.get('tech_stack', []))
    skill_overlap = len(user_skills.intersection(job_skills))
    if skill_overlap > 0:
        score += min(10, skill_overlap * 3)
        reasons.append(f"Matching skills: {skill_overlap} technologies")
    
    return {
        'match_score': min(100, score),
        'match_reasons': reasons if reasons else ['Basic compatibility assessment'],
        'skill_gaps': ['Manual review recommended'],
        'growth_potential': 'Requires detailed analysis',
        'ai_recommendations': ['Review job requirements and company details']
    }