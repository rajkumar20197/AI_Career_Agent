import streamlit as st
import boto3
import requests
import json
from datetime import datetime
import base64
import hmac
import hashlib

# Cognito Configuration (replace with your actual values)
COGNITO_USER_POOL_ID = "us-east-1_tCWj764JJ"
COGNITO_CLIENT_ID = "45ilt1o3uebk3elkgjevgsru9n"
COGNITO_CLIENT_SECRET = "your_client_secret_here"  # Get this from AWS Console
COGNITO_REGION = "us-east-1"
API_GATEWAY_URL = "https://your-api-gateway-url.amazonaws.com/prod"

class CognitoAuth:
    def __init__(self):
        self.cognito_client = boto3.client('cognito-idp', region_name=COGNITO_REGION)
    
    def calculate_secret_hash(self, username):
        """Calculate secret hash for Cognito authentication"""
        message = username + COGNITO_CLIENT_ID
        dig = hmac.new(
            COGNITO_CLIENT_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()
    
    def sign_up(self, email, password, given_name, family_name):
        """Sign up a new user"""
        try:
            response = self.cognito_client.sign_up(
                ClientId=COGNITO_CLIENT_ID,
                Username=email,
                Password=password,
                SecretHash=self.calculate_secret_hash(email),
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'given_name', 'Value': given_name},
                    {'Name': 'family_name', 'Value': family_name}
                ]
            )
            return True, "Sign up successful! Please check your email for verification."
        except Exception as e:
            return False, str(e)
    
    def confirm_sign_up(self, email, confirmation_code):
        """Confirm user sign up with verification code"""
        try:
            response = self.cognito_client.confirm_sign_up(
                ClientId=COGNITO_CLIENT_ID,
                Username=email,
                ConfirmationCode=confirmation_code,
                SecretHash=self.calculate_secret_hash(email)
            )
            return True, "Email confirmed successfully!"
        except Exception as e:
            return False, str(e)
    
    def sign_in(self, email, password):
        """Sign in user and get JWT tokens"""
        try:
            response = self.cognito_client.initiate_auth(
                ClientId=COGNITO_CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password,
                    'SECRET_HASH': self.calculate_secret_hash(email)
                }
            )
            
            tokens = response['AuthenticationResult']
            return True, tokens
        except Exception as e:
            return False, str(e)
    
    def get_user_info(self, access_token):
        """Get user information from access token"""
        try:
            response = self.cognito_client.get_user(AccessToken=access_token)
            
            user_info = {}
            for attr in response['UserAttributes']:
                user_info[attr['Name']] = attr['Value']
            
            return True, user_info
        except Exception as e:
            return False, str(e)

def main():
    st.set_page_config(
        page_title="AI Career Agent",
        page_icon="🤖",
        layout="wide"
    )
    
    # Initialize Cognito auth
    auth = CognitoAuth()
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}
    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
    
    # Main app logic
    if not st.session_state.authenticated:
        show_auth_page(auth)
    else:
        show_main_app()

def show_auth_page(auth):
    """Show authentication page"""
    
    st.title("🤖 AI Career Agent")
    st.subheader("Secure Login with Amazon Cognito")
    
    tab1, tab2, tab3 = st.tabs(["Sign In", "Sign Up", "Confirm Email"])
    
    with tab1:
        st.header("Sign In")
        with st.form("signin_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")
            
            if submit and email and password:
                success, result = auth.sign_in(email, password)
                
                if success:
                    st.session_state.access_token = result['AccessToken']
                    st.session_state.id_token = result['IdToken']
                    st.session_state.refresh_token = result['RefreshToken']
                    
                    # Get user info
                    user_success, user_info = auth.get_user_info(result['AccessToken'])
                    if user_success:
                        st.session_state.user_info = user_info
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("Failed to get user information")
                else:
                    st.error(f"Sign in failed: {result}")
    
    with tab2:
        st.header("Sign Up")
        with st.form("signup_form"):
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            given_name = st.text_input("First Name")
            family_name = st.text_input("Last Name")
            submit = st.form_submit_button("Sign Up")
            
            if submit and email and password and given_name and family_name:
                success, message = auth.sign_up(email, password, given_name, family_name)
                
                if success:
                    st.success(message)
                    st.info("Please check your email and use the 'Confirm Email' tab to verify your account.")
                else:
                    st.error(f"Sign up failed: {message}")
    
    with tab3:
        st.header("Confirm Email")
        with st.form("confirm_form"):
            email = st.text_input("Email", key="confirm_email")
            code = st.text_input("Verification Code")
            submit = st.form_submit_button("Confirm")
            
            if submit and email and code:
                success, message = auth.confirm_sign_up(email, code)
                
                if success:
                    st.success(message)
                    st.info("You can now sign in using the 'Sign In' tab.")
                else:
                    st.error(f"Confirmation failed: {message}")

def show_main_app():
    """Show main AI Career Agent application"""
    
    st.title("🤖 AI Career Agent Dashboard")
    
    # Sidebar with user info
    with st.sidebar:
        st.header("👤 User Profile")
        st.write(f"**Name:** {st.session_state.user_info.get('given_name', '')} {st.session_state.user_info.get('family_name', '')}")
        st.write(f"**Email:** {st.session_state.user_info.get('email', '')}")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_info = {}
            st.session_state.access_token = None
            st.rerun()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Job Search", "📄 Resume Optimizer", "📊 Market Intelligence", "⚙️ Settings"])
    
    with tab1:
        show_job_search_tab()
    
    with tab2:
        show_resume_optimizer_tab()
    
    with tab3:
        show_market_intelligence_tab()
    
    with tab4:
        show_settings_tab()

def show_job_search_tab():
    """Job search functionality with AI"""
    
    st.header("🔍 AI-Powered Job Search")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Search Criteria")
        job_domain = st.selectbox("Job Domain", [
            "Software Engineering", "Data Science", "Product Management", 
            "DevOps Engineering", "UX/UI Design", "Cybersecurity"
        ])
        location = st.text_input("Location", value="Remote")
        experience_level = st.selectbox("Experience Level", [
            "Entry Level", "Mid Level", "Senior Level"
        ])
        skills = st.text_area("Skills (comma-separated)", 
                             value="Python, AWS, React")
    
    with col2:
        st.subheader("Preferences")
        salary_min = st.number_input("Minimum Salary", value=70000, step=5000)
        salary_max = st.number_input("Maximum Salary", value=150000, step=5000)
        remote_only = st.checkbox("Remote Only")
        company_size = st.selectbox("Company Size", ["Any", "Startup", "Medium", "Large"])
    
    if st.button("🚀 Search Jobs with AI", type="primary"):
        with st.spinner("AI is analyzing the job market for you..."):
            # Prepare request data
            search_data = {
                "user_profile": {
                    "user_id": st.session_state.user_info.get('sub'),
                    "job_domain": job_domain,
                    "location": location,
                    "experience_level": experience_level,
                    "skills": [skill.strip() for skill in skills.split(",")],
                    "salary_expectation": salary_min
                },
                "preferences": {
                    "salary_min": salary_min,
                    "salary_max": salary_max,
                    "remote_only": remote_only,
                    "company_size": company_size
                }
            }
            
            # Call your Lambda function
            success, results = call_lambda_api("/job-search", search_data, "POST")
            
            if success:
                st.success("✅ AI Job Search Completed!")
                
                # Display results
                if 'recommendations' in results:
                    try:
                        recommendations = json.loads(results['recommendations'])
                        
                        st.subheader("🎯 Top Job Recommendations")
                        for i, job in enumerate(recommendations[:5], 1):
                            with st.expander(f"{i}. {job.get('title', 'Job Title')} at {job.get('company', 'Company')}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"**Location:** {job.get('location', 'N/A')}")
                                    st.write(f"**Salary:** {job.get('salary_range', 'N/A')}")
                                with col2:
                                    st.write(f"**Match Score:** {job.get('match_score', 'N/A')}%")
                                    st.write(f"**Why it's a match:** {job.get('match_reason', 'N/A')}")
                    except:
                        st.write(results.get('recommendations', 'No recommendations available'))
                else:
                    st.info("No job recommendations found. Try adjusting your search criteria.")
            else:
                st.error(f"Job search failed: {results}")

def show_resume_optimizer_tab():
    """Resume optimization with AI"""
    
    st.header("📄 AI Resume Optimizer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Your Resume")
        resume_text = st.text_area("Paste your resume text here", height=300)
        
        st.subheader("Target Job (Optional)")
        job_description = st.text_area("Paste job description for targeted optimization", height=150)
    
    with col2:
        if st.button("🤖 Optimize Resume with AI", type="primary"):
            if resume_text:
                with st.spinner("AI is analyzing and optimizing your resume..."):
                    optimization_data = {
                        "resume_text": resume_text,
                        "job_description": job_description
                    }
                    
                    success, results = call_lambda_api("/resume-analyze", optimization_data, "POST")
                    
                    if success:
                        st.success("✅ Resume Analysis Complete!")
                        
                        if 'analysis' in results:
                            try:
                                analysis = json.loads(results['analysis'])
                                
                                # Display analysis results
                                st.subheader("📊 Resume Analysis")
                                
                                if 'overall_score' in analysis:
                                    score = analysis['overall_score']
                                    st.metric("Overall Score", f"{score}/100")
                                
                                if 'strengths' in analysis:
                                    st.subheader("💪 Strengths")
                                    for strength in analysis['strengths']:
                                        st.write(f"✅ {strength}")
                                
                                if 'suggestions' in analysis:
                                    st.subheader("🎯 Improvement Suggestions")
                                    for suggestion in analysis['suggestions']:
                                        st.write(f"💡 {suggestion}")
                                        
                            except:
                                st.write(results.get('analysis', 'Analysis not available'))
                    else:
                        st.error(f"Resume analysis failed: {results}")
            else:
                st.warning("Please paste your resume text first.")

def show_market_intelligence_tab():
    """Market intelligence with AI"""
    
    st.header("📊 AI Market Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        domain = st.selectbox("Job Domain", [
            "Software Engineering", "Data Science", "Product Management"
        ], key="market_domain")
        location = st.text_input("Location", value="United States", key="market_location")
        level = st.selectbox("Experience Level", [
            "Entry Level", "Mid Level", "Senior Level"
        ], key="market_level")
    
    with col2:
        if st.button("📈 Get Market Intelligence", type="primary"):
            with st.spinner("AI is analyzing market trends..."):
                params = f"?domain={domain}&location={location}&level={level}"
                success, results = call_lambda_api(f"/market-intel{params}", {}, "GET")
                
                if success:
                    st.success("✅ Market Analysis Complete!")
                    
                    if 'intelligence' in results:
                        try:
                            intel = json.loads(results['intelligence'])
                            
                            # Display market intelligence
                            st.subheader("💰 Salary Information")
                            if 'salary_range' in intel:
                                salary_info = intel['salary_range']
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Min Salary", f"${salary_info.get('min', 'N/A'):,}")
                                with col2:
                                    st.metric("Median Salary", f"${salary_info.get('median', 'N/A'):,}")
                                with col3:
                                    st.metric("Max Salary", f"${salary_info.get('max', 'N/A'):,}")
                            
                            if 'in_demand_skills' in intel:
                                st.subheader("🔥 In-Demand Skills")
                                skills = intel['in_demand_skills']
                                for i, skill in enumerate(skills[:5], 1):
                                    st.write(f"{i}. {skill}")
                                    
                        except:
                            st.write(results.get('intelligence', 'Intelligence not available'))
                else:
                    st.error(f"Market analysis failed: {results}")

def show_settings_tab():
    """User settings and preferences"""
    
    st.header("⚙️ Settings")
    
    st.subheader("👤 Profile Information")
    
    # Display current user info
    user_info = st.session_state.user_info
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("First Name", value=user_info.get('given_name', ''), disabled=True)
        st.text_input("Email", value=user_info.get('email', ''), disabled=True)
    
    with col2:
        st.text_input("Last Name", value=user_info.get('family_name', ''), disabled=True)
        st.text_input("User ID", value=user_info.get('sub', ''), disabled=True)
    
    st.subheader("🔧 API Configuration")
    st.code(f"API Gateway URL: {API_GATEWAY_URL}")
    st.code(f"Cognito User Pool: {COGNITO_USER_POOL_ID}")
    
    st.subheader("🔑 Access Token")
    if st.checkbox("Show Access Token"):
        st.code(st.session_state.access_token)

def call_lambda_api(endpoint, data, method="POST"):
    """Call your Lambda function via API Gateway"""
    
    try:
        url = f"{API_GATEWAY_URL}{endpoint}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {st.session_state.access_token}'
        }
        
        if method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=30)
        else:
            response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API call failed: {response.status_code} - {response.text}"
            
    except Exception as e:
        return False, f"API call error: {str(e)}"

if __name__ == "__main__":
    main()