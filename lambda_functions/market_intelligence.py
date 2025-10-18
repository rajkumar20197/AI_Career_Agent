import json
import boto3
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any

def lambda_handler(event, context):
    """
    AWS Lambda function for market intelligence analysis
    Provides job market insights, salary data, and AI impact analysis
    """
    
    try:
        # Extract parameters from event
        job_domain = event.get('job_domain', 'Software Engineering')
        location = event.get('location', 'San Francisco')
        experience_level = event.get('experience_level', 'Entry Level')
        
        # Initialize AWS clients
        bedrock_runtime = boto3.client('bedrock-runtime')
        
        # Gather market data
        market_data = gather_market_intelligence(job_domain, location, experience_level)
        
        # Analyze with AI
        ai_insights = generate_ai_insights(bedrock_runtime, market_data, job_domain)
        
        # Prepare response
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'market_data': market_data,
                'ai_insights': ai_insights,
                'timestamp': datetime.now().isoformat()
            })
        }
        
        return response
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Failed to generate market intelligence'
            })
        }

def gather_market_intelligence(job_domain: str, location: str, experience_level: str) -> Dict[str, Any]:
    """Gather comprehensive market intelligence data"""
    
    # In a real implementation, this would integrate with:
    # - Job board APIs (Indeed, LinkedIn, Glassdoor)
    # - Salary databases
    # - Labor statistics APIs
    
    # Mock data structure for demonstration
    market_data = {
        'salary_ranges': {
            'entry_level': {'min': 65000, 'max': 85000, 'median': 75000},
            'mid_level': {'min': 85000, 'max': 120000, 'median': 102500},
            'senior_level': {'min': 120000, 'max': 180000, 'median': 150000}
        },
        'job_availability': {
            'total_openings': 1250,
            'new_this_week': 85,
            'competition_ratio': 3.2  # applications per opening
        },
        'location_insights': {
            'cost_of_living_index': 1.8,  # relative to national average
            'remote_percentage': 65,
            'top_companies': ['Google', 'Meta', 'Apple', 'Salesforce', 'Uber']
        },
        'skill_demand': {
            'hot_skills': ['Python', 'React', 'AWS', 'Machine Learning', 'Docker'],
            'emerging_skills': ['Kubernetes', 'GraphQL', 'Rust', 'WebAssembly'],
            'declining_skills': ['jQuery', 'Flash', 'Perl']
        },
        'growth_projections': {
            'job_growth_5yr': 15.2,  # percentage
            'salary_growth_5yr': 8.5,
            'automation_risk': 'Low'  # Low, Medium, High
        }
    }
    
    return market_data

def generate_ai_insights(bedrock_runtime, market_data: Dict, job_domain: str) -> Dict[str, Any]:
    """Generate AI-powered insights using Amazon Bedrock"""
    
    # Prepare prompt for Claude
    prompt = f"""
    Analyze the following job market data for {job_domain} and provide strategic insights:
    
    Market Data: {json.dumps(market_data, indent=2)}
    
    Please provide:
    1. Key market trends and opportunities
    2. Salary negotiation strategies
    3. Skills to prioritize for career growth
    4. Timeline recommendations for job search
    5. Risk assessment and mitigation strategies
    
    Format your response as structured JSON with clear recommendations.
    """
    
    try:
        # Call Claude via Bedrock
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
        
        # Parse response
        response_body = json.loads(response['body'].read())
        ai_analysis = response_body['content'][0]['text']
        
        # Structure the insights
        insights = {
            'analysis': ai_analysis,
            'confidence_score': 0.85,
            'last_updated': datetime.now().isoformat(),
            'recommendations': extract_recommendations(ai_analysis)
        }
        
        return insights
        
    except Exception as e:
        # Fallback insights if Bedrock call fails
        return {
            'analysis': 'Market analysis temporarily unavailable',
            'confidence_score': 0.0,
            'last_updated': datetime.now().isoformat(),
            'recommendations': generate_fallback_recommendations(job_domain)
        }

def extract_recommendations(ai_analysis: str) -> List[str]:
    """Extract actionable recommendations from AI analysis"""
    # In a real implementation, this would parse the AI response more intelligently
    return [
        "Focus on cloud computing skills (AWS, Azure, GCP)",
        "Build a strong portfolio with 3-5 diverse projects",
        "Network actively through tech meetups and LinkedIn",
        "Consider remote opportunities to expand job market",
        "Prepare for technical interviews with coding practice"
    ]

def generate_fallback_recommendations(job_domain: str) -> List[str]:
    """Generate basic recommendations when AI analysis fails"""
    return [
        f"Stay updated with latest trends in {job_domain}",
        "Build a strong professional network",
        "Create a compelling portfolio",
        "Practice interview skills regularly",
        "Consider additional certifications"
    ]