import streamlit as st
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional
import time

# Configure Streamlit page
st.set_page_config(
    page_title="AI Career Agent - Land Your Dream Job",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional landing page
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        padding: 0 !important;
    }
    
    /* Color Variables */
    :root {
        --primary-blue: #103778;
        --primary-teal: #0593A2;
        --accent-orange: #FF7A48;
        --accent-yellow: #FFD700;
        --text-dark: #1a1a1a;
        --text-gray: #666666;
        --bg-light: #f8fafc;
        --white: #ffffff;
    }
    
    /* Header Navigation */
    .header-nav {
        background: var(--white);
        padding: 1rem 2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .nav-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-blue);
    }
    
    .nav-menu {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-item {
        color: var(--text-dark);
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        color: var(--primary-teal);
    }
    
    .cta-button {
        background: linear-gradient(135deg, var(--accent-yellow) 0%, #FFA500 100%);
        color: var(--text-dark);
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: none;
        cursor: pointer;
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 4rem 2rem;
        min-height: 80vh;
        display: flex;
        align-items: center;
    }
    
    .hero-container {
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4rem;
        align-items: center;
    }
    
    .hero-content {
        padding-right: 2rem;
    }
    
    .hero-tagline {
        color: var(--primary-teal);
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
        position: relative;
    }
    
    .hero-tagline::before {
        content: '';
        position: absolute;
        left: -3rem;
        top: 50%;
        width: 2rem;
        height: 2px;
        background: var(--accent-orange);
        transform: translateY(-50%);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: var(--text-dark);
        line-height: 1.1;
        margin-bottom: 1.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: var(--text-gray);
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    .hero-features {
        list-style: none;
        margin-bottom: 2rem;
    }
    
    .hero-features li {
        color: var(--text-gray);
        margin-bottom: 0.5rem;
        position: relative;
        padding-left: 1.5rem;
    }
    
    .hero-features li::before {
        content: '✓';
        position: absolute;
        left: 0;
        color: var(--primary-teal);
        font-weight: bold;
    }
    
    .hero-actions {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .primary-cta {
        background: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-blue) 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 30px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .primary-cta:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(5, 147, 162, 0.4);
    }
    
    .social-links {
        display: flex;
        gap: 1rem;
    }
    
    .social-link {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: var(--white);
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        color: var(--primary-teal);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .social-link:hover {
        transform: translateY(-2px);
    }
    
    /* Hero Visual */
    .hero-visual {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 500px;
    }
    
    /* Main AI Dashboard Mockup */
    .ai-dashboard {
        background: var(--white);
        border-radius: 20px;
        box-shadow: 0 25px 80px rgba(0,0,0,0.15);
        width: 400px;
        height: 300px;
        transform: rotate(-8deg);
        transition: transform 0.3s ease;
        position: relative;
        z-index: 10;
    }
    
    .ai-dashboard:hover {
        transform: rotate(-3deg) scale(1.02);
    }
    
    .dashboard-header {
        background: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-blue) 100%);
        height: 50px;
        border-radius: 20px 20px 0 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 1rem;
        color: white;
    }
    
    .dashboard-title {
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .ai-status {
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: #00ff88;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .dashboard-content {
        padding: 1rem;
        height: 250px;
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
    }
    
    .ai-metric {
        background: var(--bg-light);
        padding: 0.8rem;
        border-radius: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.85rem;
    }
    
    .metric-value {
        font-weight: 600;
        color: var(--primary-teal);
    }
    
    /* Floating AI Action Cards */
    .ai-action-card {
        position: absolute;
        background: var(--white);
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        border-left: 4px solid var(--primary-teal);
        min-width: 200px;
        animation: float 4s ease-in-out infinite;
    }
    
    .ai-action-card.card-1 {
        top: 50px;
        right: -50px;
        animation-delay: 0s;
        transform: rotate(5deg);
    }
    
    .ai-action-card.card-2 {
        bottom: 80px;
        left: -80px;
        animation-delay: 2s;
        transform: rotate(-3deg);
    }
    
    .ai-action-card.card-3 {
        top: 20px;
        left: -20px;
        animation-delay: 1s;
        transform: rotate(8deg);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .card-icon {
        width: 30px;
        height: 30px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
    }
    
    .card-title {
        font-weight: 600;
        font-size: 0.9rem;
        color: var(--text-dark);
    }
    
    .card-content {
        font-size: 0.8rem;
        color: var(--text-gray);
        line-height: 1.4;
    }
    
    .card-progress {
        margin-top: 0.5rem;
        height: 4px;
        background: var(--bg-light);
        border-radius: 2px;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-teal), var(--primary-blue));
        border-radius: 2px;
        animation: progress 3s ease-in-out infinite;
    }
    
    @keyframes progress {
        0% { width: 0%; }
        50% { width: 100%; }
        100% { width: 100%; }
    }
    
    /* User Avatar */
    .user-avatar {
        position: absolute;
        bottom: 150px;
        right: 50px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ff6b6b, #ffa500);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: float 3s ease-in-out infinite;
        animation-delay: 0.5s;
    }
    
    /* Notification Badges */
    .notification-badge {
        position: absolute;
        background: var(--accent-orange);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(255, 122, 72, 0.4);
        animation: bounce 2s ease-in-out infinite;
    }
    
    .notification-badge.badge-1 {
        top: 100px;
        right: 20px;
        animation-delay: 0s;
    }
    
    .notification-badge.badge-2 {
        bottom: 200px;
        left: 20px;
        animation-delay: 1s;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(var(--rotation, 0deg)); }
        50% { transform: translateY(-15px) rotate(var(--rotation, 0deg)); }
    }
    
    /* Features Section */
    .features-section {
        padding: 4rem 2rem;
        background: var(--white);
    }
    
    .features-container {
        max-width: 1200px;
        margin: 0 auto;
        text-align: center;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-dark);
        margin-bottom: 1rem;
    }
    
    .section-subtitle {
        font-size: 1.2rem;
        color: var(--text-gray);
        margin-bottom: 3rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
    }
    
    .feature-card {
        background: var(--white);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: left;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-blue) 100%);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
        margin-bottom: 1.5rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--text-dark);
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: var(--text-gray);
        line-height: 1.6;
    }
    
    /* Stats Section */
    .stats-section {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-teal) 100%);
        padding: 4rem 2rem;
        color: white;
    }
    
    .stats-container {
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        text-align: center;
    }
    
    .stat-item {
        padding: 1rem;
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        color: var(--accent-yellow);
    }
    
    .stat-label {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* CTA Section */
    .cta-section {
        background: var(--bg-light);
        padding: 4rem 2rem;
        text-align: center;
    }
    
    .cta-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-dark);
        margin-bottom: 1rem;
    }
    
    .cta-description {
        font-size: 1.2rem;
        color: var(--text-gray);
        margin-bottom: 2rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-container {
            grid-template-columns: 1fr;
            text-align: center;
        }
        
        .hero-title {
            font-size: 2.5rem;
        }
        
        .nav-menu {
            display: none;
        }
    }
</style>
""", unsafe_allow_html=True)

def render_onboarding_flow():
    """Show what happens after clicking START FREE TRIAL"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0593A2 0%, #103778 100%); padding: 2rem; border-radius: 15px; margin: 2rem 0; color: white; text-align: center;">
        <h1>🎉 Welcome to AI Career Agent!</h1>
        <p style="font-size: 1.2rem; margin-bottom: 2rem;">Your AI-powered career journey starts now</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Onboarding steps
    st.markdown("## 🚀 Let's Get You Started")
    
    # Step 1: Basic Info
    with st.form("onboarding_form"):
        st.markdown("### 📋 Step 1: Tell us about yourself")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email Address", placeholder="john@example.com")
            
        with col2:
            status = st.selectbox("Current Status", 
                ["Current Student", "Recent Graduate", "Active Job Seeker", "Career Changer"])
            graduation_date = st.date_input("Graduation Date (Expected/Actual)")
        
        st.markdown("### 💼 Step 2: Your Dream Job")
        dream_job = st.text_area("Describe your dream job", 
            placeholder="e.g., Software Engineer at a tech company in San Francisco, working on AI/ML projects...")
        
        col3, col4 = st.columns(2)
        with col3:
            experience_level = st.selectbox("Experience Level", 
                ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior Level (6+ years)"])
        with col4:
            preferred_location = st.selectbox("Preferred Location", 
                ["Remote", "San Francisco", "New York", "Seattle", "Austin", "Boston", "Other"])
        
        st.markdown("### 🎯 Step 3: AI Preferences")
        col5, col6 = st.columns(2)
        with col5:
            job_search_frequency = st.selectbox("Job Search Frequency", 
                ["Daily", "Every 2 days", "Weekly", "Bi-weekly"])
            notification_preference = st.selectbox("Notification Preference", 
                ["Email + SMS", "Email Only", "SMS Only", "In-App Only"])
        
        with col6:
            auto_apply = st.checkbox("Enable Auto-Apply (AI applies to jobs for you)", value=True)
            resume_optimization = st.checkbox("Enable Resume Optimization", value=True)
        
        # Submit button
        submitted = st.form_submit_button("🤖 ACTIVATE MY AI CAREER AGENT", use_container_width=True)
        
        if submitted and name and email and dream_job:
            # Store user data temporarily
            st.session_state.temp_profile = {
                'name': name,
                'email': email,
                'status': status,
                'graduation_date': graduation_date,
                'dream_job': dream_job,
                'experience_level': experience_level,
                'preferred_location': preferred_location,
                'auto_apply': auto_apply,
                'resume_optimization': resume_optimization
            }
            st.session_state.onboarding_completed = True
            
            # Show success and AI activation
            st.balloons()
            st.success("🎉 Congratulations! Your AI Career Agent is now active!")
            
            # Show what the AI will do
            st.markdown("## 🤖 Your AI Agent is Now Working...")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("🔍 **Scanning Job Boards**\nSearching 50+ platforms for matches...")
            with col2:
                st.info("📝 **Optimizing Resume**\nTailoring your resume for top matches...")
            with col3:
                st.info("📊 **Market Analysis**\nAnalyzing salary trends and requirements...")
            
            # Simulate AI progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            import time
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("🔍 Scanning job boards...")
                elif i < 60:
                    status_text.text("📝 Optimizing your resume...")
                elif i < 90:
                    status_text.text("📊 Analyzing market data...")
                else:
                    status_text.text("✅ Setup complete!")
                time.sleep(0.05)
            
            # Show results
            st.markdown("## 🎯 Initial Results")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Jobs Found", "47", "+47")
            with col2:
                st.metric("Perfect Matches", "12", "+12")
            with col3:
                st.metric("Resume Score", "85/100", "+15")
            with col4:
                st.metric("Avg Salary", "$125K", "Market Rate")
            
            # Next steps
            st.markdown("## 🚀 What Happens Next?")
            
            st.info("""
            **Your AI Career Agent will now:**
            - 🔄 **Monitor job boards 24/7** and find new opportunities daily
            - 📧 **Send you daily updates** with new job matches and applications sent
            - 📞 **Schedule interviews** automatically when you get responses
            - 📈 **Track your progress** and optimize your job search strategy
            - 🎯 **Provide career guidance** based on market trends and your goals
            """)
            
        elif submitted:
            st.error("Please fill in all required fields (Name, Email, Dream Job)")
    
    # CTA to main app - Outside the form
    if st.session_state.get('onboarding_completed', False):
        if st.button("🎯 GO TO MY AI CAREER DASHBOARD", use_container_width=True, type="primary"):
            # Store user data and redirect to main app
            profile_data = st.session_state.get('temp_profile', {})
            st.session_state.user_profile = profile_data
            st.session_state.show_main_app = True
            st.session_state.show_onboarding = False
            st.rerun()
    
    # Back to landing page
    if st.button("← Back to Landing Page"):
        st.session_state.show_onboarding = False
        st.rerun()

def render_navigation():
    """Render the navigation header with functional buttons"""
    # Header Navigation
    st.markdown("""
    <div class="header-nav">
        <div class="nav-container">
            <div class="logo">
                🎓 AI Career Agent
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Functional navigation buttons in same positions
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1, 1, 1, 1, 1, 1, 0.5, 1.5])
    
    with col1:
        if st.button("🏠 Home", use_container_width=True, key="nav_home_1"):
            st.session_state.current_nav_page = 'home'
            st.rerun()
    
    with col2:
        if st.button("⚡ Features", use_container_width=True):
            st.session_state.current_nav_page = 'features'
            st.rerun()
    
    with col3:
        if st.button("🔄 How It Works", use_container_width=True):
            st.session_state.current_nav_page = 'how_it_works'
            st.rerun()
    
    with col4:
        if st.button("🏆 Success Stories", use_container_width=True):
            st.session_state.current_nav_page = 'success_stories'
            st.rerun()
    
    with col5:
        if st.button("💰 Pricing", use_container_width=True):
            st.session_state.current_nav_page = 'pricing'
            st.rerun()
    
    with col6:
        if st.button("👥 About Us", use_container_width=True):
            st.session_state.current_nav_page = 'about'
            st.rerun()
    
    with col7:
        st.write("")  # Spacer
    
    with col8:
        if st.button("🚀 START FREE TRIAL", type="primary", use_container_width=True):
            st.session_state.show_onboarding = True
            st.rerun()

def render_home_page():
    """Render the main landing page content"""
    
    # Hero Section - Complete layout in one markdown block
    st.markdown("""
    <div class="hero-section">
        <div class="hero-container">
            <div class="hero-content">
                <div class="hero-tagline">YOUR AI-POWERED CAREER PARTNER</div>
                <h1 class="hero-title">Land Your Dream Job Without Limits</h1>
                <p class="hero-subtitle">
                    AI-powered career acceleration for students and graduates. 
                    We handle job search, applications, and interview prep automatically.
                </p>
                <ul class="hero-features">
                    <li>Automated job discovery across 50+ platforms daily</li>
                    <li>AI-optimized resumes tailored for each application</li>
                    <li>Smart interview scheduling and preparation</li>
                    <li>Real-time market intelligence and salary insights</li>
                </ul>
                <div class="hero-actions">
                    <button class="primary-cta">🚀 START YOUR CAREER JOURNEY</button>
                    <div class="social-links">
                        <a href="#" class="social-link">📧</a>
                        <a href="#" class="social-link">💼</a>
                        <a href="#" class="social-link">🐦</a>
                        <a href="#" class="social-link">📱</a>
                    </div>
                </div>
            </div>
            <div class="hero-visual">
                <div class="ai-dashboard">
                    <div class="dashboard-header">
                        <div class="dashboard-title">🤖 AI Career Agent</div>
                        <div class="ai-status">
                            <div class="status-dot"></div>
                            AI Working
                        </div>
                    </div>
                    <div class="dashboard-content">
                        <div class="ai-metric">
                            <span>🎯 Jobs Found Today</span>
                            <span class="metric-value">23</span>
                        </div>
                        <div class="ai-metric">
                            <span>📝 Applications Sent</span>
                            <span class="metric-value">12</span>
                        </div>
                        <div class="ai-metric">
                            <span>📞 Interviews Scheduled</span>
                            <span class="metric-value">4</span>
                        </div>
                        <div class="ai-metric">
                            <span>✅ Response Rate</span>
                            <span class="metric-value">34%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive CTA Buttons
    # Professional call-to-action section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🚀 Ready to Transform Your Career?")
        
        # Main CTA button
        if st.button("🚀 START FREE TRIAL", use_container_width=True, type="primary"):
            st.session_state.show_onboarding = True
            st.success("✅ Button clicked! Loading onboarding...")
            st.rerun()
    
    # Debug info
    st.write(f"Debug: show_onboarding = {st.session_state.get('show_onboarding', False)}")
    
    # Show onboarding flow when button is clicked
    if st.session_state.get('show_onboarding', False):
        st.markdown("---")
        st.markdown("## 🎯 ONBOARDING FLOW ACTIVATED")
        render_onboarding_flow()
    
    # Features Section
    st.markdown("""
    <div class="features-section">
        <div class="features-container">
            <h2 class="section-title">Why Choose AI Career Agent?</h2>
            <p class="section-subtitle">
                We combine cutting-edge AI with deep career expertise to give you an unfair advantage in today's competitive job market.
            </p>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🤖</div>
                    <h3 class="feature-title">AI-Powered Automation</h3>
                    <p class="feature-description">
                        Our AI agent works 24/7 to find jobs, optimize your resume, and apply to positions while you focus on interview prep.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <h3 class="feature-title">Smart Job Matching</h3>
                    <p class="feature-description">
                        Advanced algorithms analyze your skills, preferences, and career goals to find the perfect job matches across 50+ platforms.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3 class="feature-title">Market Intelligence</h3>
                    <p class="feature-description">
                        Real-time salary data, skill demand trends, and AI impact analysis to help you make informed career decisions.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📝</div>
                    <h3 class="feature-title">Resume Optimization</h3>
                    <p class="feature-description">
                        AI tailors your resume for each application, ensuring maximum ATS compatibility and recruiter appeal.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📞</div>
                    <h3 class="feature-title">Interview Preparation</h3>
                    <p class="feature-description">
                        Personalized interview questions, company research, and practice sessions to boost your confidence.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📈</div>
                    <h3 class="feature-title">Career Planning</h3>
                    <p class="feature-description">
                        Strategic roadmaps based on your graduation timeline, from skill development to job search acceleration.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("""
    <div class="stats-section">
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">95%</div>
                <div class="stat-label">Job Match Accuracy</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">3x</div>
                <div class="stat-label">Faster Job Placement</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">50+</div>
                <div class="stat-label">Job Boards Monitored</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">24/7</div>
                <div class="stat-label">AI Agent Working</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Final CTA Section
    st.markdown("""
    <div class="cta-section">
        <div class="cta-container">
            <h2 class="cta-title">Ready to Land Your Dream Job?</h2>
            <p class="cta-description">
                Join thousands of students and graduates who are already using AI to accelerate their careers. 
                Start your free trial today and see the difference AI can make.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Final CTA Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎓 START YOUR SUCCESS STORY", use_container_width=True, type="primary"):
            st.session_state.show_onboarding = True
            st.rerun()

# Import main app functions
def create_sample_data():
    """Generate sample career data for visualization"""
    # Job market trends data
    job_trends = pd.DataFrame({
        'Month': pd.date_range('2024-01-01', periods=12, freq='ME'),
        'Software Engineer': [850, 920, 1100, 1250, 1180, 1300, 1450, 1380, 1520, 1600, 1750, 1800],
        'Data Scientist': [420, 480, 550, 620, 580, 650, 720, 680, 750, 800, 850, 900],
        'Product Manager': [320, 350, 400, 450, 430, 480, 520, 500, 550, 580, 620, 650],
        'DevOps Engineer': [280, 320, 380, 420, 400, 450, 490, 470, 520, 550, 580, 600]
    })
    
    # Salary ranges by experience
    salary_data = pd.DataFrame({
        'Experience': ['0-2 years', '3-5 years', '6-10 years', '10+ years'],
        'Software Engineer': [75000, 105000, 140000, 180000],
        'Data Scientist': [80000, 110000, 145000, 185000],
        'Product Manager': [85000, 120000, 160000, 200000],
        'DevOps Engineer': [70000, 100000, 135000, 175000]
    })
    
    # Skills demand data
    skills_data = pd.DataFrame({
        'Skill': ['Python', 'JavaScript', 'AWS', 'React', 'SQL', 'Docker', 'Kubernetes', 'Machine Learning'],
        'Demand_Score': [95, 88, 92, 78, 85, 82, 75, 90],
        'Growth_Rate': [15, 12, 25, 18, 8, 20, 28, 35]
    })
    
    # Geographic job distribution
    geo_data = pd.DataFrame({
        'City': ['San Francisco', 'New York', 'Seattle', 'Austin', 'Boston', 'Chicago', 'Los Angeles', 'Denver'],
        'Job_Count': [2500, 2200, 1800, 1200, 1100, 900, 1400, 800],
        'Avg_Salary': [165000, 145000, 155000, 125000, 140000, 120000, 135000, 115000],
        'Cost_of_Living_Index': [100, 85, 75, 60, 70, 55, 80, 58]
    })
    
    return job_trends, salary_data, skills_data, geo_data

def render_main_app():
    """Render the main AI Career Agent application"""
    # Header for main app
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0593A2 0%, #103778 100%); padding: 1rem 2rem; margin: -1rem -1rem 2rem -1rem; color: white; box-shadow: 0 4px 20px rgba(21, 31, 48, 0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 2rem;">🎓</span>
                <h1 style="margin: 0; font-size: 1.8rem;">AI Career Agent Dashboard</h1>
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <span style="color: rgba(255,255,255,0.8);">📧 Gmail Notifications: ON</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        if st.button("🏠 Home", use_container_width=True, key="nav_home_2"):
            st.session_state.current_page = 'Home'
    
    with col2:
        if st.button("📊 Dashboard", use_container_width=True, key="nav_dashboard_landing"):
            st.session_state.current_page = 'Dashboard'
    
    with col3:
        if st.button("💼 Jobs", use_container_width=True, key="nav_jobs_landing"):
            st.session_state.current_page = 'Jobs'
    
    with col4:
        if st.button("🎯 Career Plan", use_container_width=True, key="nav_career_landing"):
            st.session_state.current_page = 'Career Plan'
    
    with col5:
        if st.button("📝 Resume", use_container_width=True, key="nav_resume_landing"):
            st.session_state.current_page = 'Resume'
    
    with col6:
        if st.button("📧 Notifications", use_container_width=True, key="nav_notifications_landing"):
            st.session_state.current_page = 'Notifications'
    
    with col7:
        if st.button("← Back to Landing", use_container_width=True):
            st.session_state.show_main_app = False
            st.session_state.show_onboarding = False
            st.rerun()
    
    # Initialize current page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'
    
    # Render page content based on selection
    page = st.session_state.current_page
    
    if page == 'Home':
        render_home_dashboard()
    elif page == 'Dashboard':
        render_analytics_dashboard()
    elif page == 'Jobs':
        render_jobs_page()
    elif page == 'Career Plan':
        render_career_planning()
    elif page == 'Resume':
        render_resume_tools()
    elif page == 'Notifications':
        render_notifications_center()

def render_home_dashboard():
    """Render personalized home dashboard"""
    profile = st.session_state.get('user_profile', {})
    
    st.markdown(f"## 🎉 Welcome back, {profile.get('name', 'User')}!")
    st.markdown(f"**Dream Job:** {profile.get('dream_job', 'Not specified')}")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Jobs Found", "47", "+12 today")
    with col2:
        st.metric("📝 Applications", "23", "+5 today")
    with col3:
        st.metric("📞 Interviews", "8", "+2 this week")
    with col4:
        st.metric("✅ Response Rate", "34%", "+8%")
    
    # Recent activity
    st.markdown("### 🔄 Recent AI Activity")
    st.info("🤖 **2 hours ago:** Applied to Senior Developer position at Google")
    st.info("🎯 **4 hours ago:** Found 3 new job matches in your area")
    st.info("📝 **6 hours ago:** Optimized resume for Meta application")
    st.success("📞 **Yesterday:** Interview scheduled with Microsoft for tomorrow 2 PM")

def render_analytics_dashboard():
    """Render analytics dashboard"""
    st.markdown("## 📊 Career Analytics")
    
    job_trends, salary_data, skills_data, geo_data = create_sample_data()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(job_trends.melt(id_vars=['Month'], var_name='Role', value_name='Job_Postings'),
                     x='Month', y='Job_Postings', color='Role', title="Job Market Trends")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(salary_data.melt(id_vars=['Experience'], var_name='Role', value_name='Salary'),
                    x='Experience', y='Salary', color='Role', title="Salary by Experience")
        st.plotly_chart(fig, use_container_width=True)

def render_jobs_page():
    """Render jobs page"""
    st.markdown("## 💼 Job Opportunities")
    
    # Job listings
    jobs_data = pd.DataFrame({
        'Company': ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple'],
        'Position': ['Software Engineer', 'Product Manager', 'Data Scientist', 'ML Engineer', 'iOS Developer'],
        'Salary': ['$150K-$200K', '$140K-$180K', '$160K-$210K', '$170K-$220K', '$145K-$190K'],
        'Match': ['95%', '88%', '92%', '90%', '85%'],
        'Status': ['Applied ✅', 'Ready 🚀', 'Applied ✅', 'Interview 📞', 'Saved 💾']
    })
    
    st.dataframe(jobs_data, use_container_width=True)
    
    if st.button("🚀 Apply to All Matches", use_container_width=True):
        st.success("✅ AI is applying to 3 new positions! You'll get email confirmations.")

def render_career_planning():
    """Render career planning page"""
    st.markdown("## 🎯 Career Planning")
    
    profile = st.session_state.get('user_profile', {})
    
    st.markdown(f"### 📈 Career Roadmap for: {profile.get('dream_job', 'Your Career')}")
    
    timeline_data = pd.DataFrame({
        'Stage': ['Current', '6 Months', '1 Year', '2 Years'],
        'Role': ['Student/Entry', 'Junior Developer', 'Software Engineer', 'Senior Engineer'],
        'Salary': ['$0-60K', '$80K-100K', '$120K-150K', '$160K-200K'],
        'Key Skills': ['Basic Programming', 'Full Stack', 'System Design', 'Leadership']
    })
    
    st.dataframe(timeline_data, use_container_width=True)

def render_resume_tools():
    """Render resume tools page"""
    st.markdown("## 📝 Resume Optimization")
    
    uploaded_file = st.file_uploader("Upload your resume", type=['pdf', 'docx'])
    
    if uploaded_file:
        st.success("✅ Resume uploaded! AI is analyzing...")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Resume Score", "85/100", "+15")
        with col2:
            if st.button("🤖 Optimize with AI"):
                st.success("✅ Resume optimized and saved!")

def render_notifications_center():
    """Render notifications center"""
    st.markdown("## 📧 Notifications Center")
    
    st.markdown("### 📬 Recent Notifications")
    st.info("🎯 **2 hours ago:** New job match found at Tesla")
    st.success("📞 **Yesterday:** Interview confirmed with Google")
    st.warning("⏰ **Reminder:** Microsoft interview tomorrow at 2 PM")
    
    # Gmail settings
    st.markdown("### ⚙️ Email Settings")
    email_freq = st.selectbox("Email Frequency", ["Immediate", "Daily Digest", "Weekly Summary"])
    if st.button("💾 Save Settings"):
        st.success("✅ Email preferences updated!")

def render_features_page():
    """Render the features page"""
    st.markdown("# ⚡ AI Career Agent Features")
    st.markdown("### Discover the power of AI-driven career acceleration")
    
    # Feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🤖 AI-Powered Automation
        - **24/7 Job Discovery:** Scans 50+ job boards continuously
        - **Smart Matching:** AI analyzes job requirements vs your skills
        - **Auto-Application:** Applies to relevant positions automatically
        - **Resume Tailoring:** Customizes resume for each application
        """)
        
        st.markdown("""
        ### 📊 Market Intelligence
        - **Salary Insights:** Real-time compensation data
        - **Skill Trends:** Most in-demand skills in your field
        - **Company Analysis:** Insider info on hiring companies
        - **Location Data:** Best cities for your career goals
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Career Planning
        - **Timeline Assessment:** Based on graduation date
        - **Skill Gap Analysis:** What to learn for dream job
        - **Career Roadmap:** Step-by-step progression plan
        - **Interview Prep:** AI-generated practice questions
        """)
        
        st.markdown("""
        ### 📧 Smart Notifications
        - **Gmail Integration:** Seamless email notifications
        - **Interview Alerts:** Never miss an opportunity
        - **Progress Reports:** Weekly career advancement updates
        - **Job Matches:** Instant alerts for perfect opportunities
        """)
    
    # CTA
    if st.button("🚀 Try These Features Now", type="primary", use_container_width=True):
        st.session_state.show_onboarding = True
        st.rerun()

def render_how_it_works_page():
    """Render the how it works page"""
    st.markdown("# 🔄 How AI Career Agent Works")
    st.markdown("### Your journey from student to employed in 4 simple steps")
    
    # Step-by-step process
    st.markdown("## Step 1: 📋 Tell Us About Yourself")
    st.info("Share your graduation timeline, dream job, and career preferences. Our AI uses this to personalize everything.")
    
    st.markdown("## Step 2: 🤖 AI Gets to Work")
    st.success("While you focus on studies/interviews, our AI scans job boards, optimizes your resume, and applies to relevant positions.")
    
    st.markdown("## Step 3: 📞 Interview Coordination")
    st.warning("When companies respond, we automatically schedule interviews based on your availability and send you prep materials.")
    
    st.markdown("## Step 4: 🎉 Land Your Dream Job")
    st.success("With AI handling the heavy lifting, you get more interviews and better job offers in less time.")
    
    # Process visualization
    st.markdown("### 🔄 The AI Process")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jobs Scanned Daily", "10,000+", "Across 50+ platforms")
    with col2:
        st.metric("Applications Sent", "Average 15/day", "Tailored for each role")
    with col3:
        st.metric("Success Rate", "3x Higher", "vs manual applications")

def render_success_stories_page():
    """Render the success stories page"""
    st.markdown("# 🏆 Success Stories")
    st.markdown("### Real students who landed their dream jobs with AI Career Agent")
    
    # Success story cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 👨‍💻 Alex Chen - Software Engineer at Google
        **Timeline:** 3 months before graduation
        
        *"I was stressed about job hunting while finishing my CS degree. AI Career Agent found and applied to 200+ positions while I focused on finals. Got 15 interviews and landed my dream job at Google!"*
        
        **Results:**
        - 📝 200+ applications sent automatically
        - 📞 15 interviews scheduled
        - 💰 $165K starting salary
        - ⏱️ 2 weeks from graduation to job offer
        """)
        
        st.markdown("""
        ### 👩‍🔬 Sarah Johnson - Data Scientist at Microsoft
        **Timeline:** Recent graduate, 6 months job searching
        
        *"After 6 months of manual applications with no luck, I tried AI Career Agent. Within 3 weeks, I had multiple offers including Microsoft!"*
        
        **Results:**
        - 🎯 85% application response rate
        - 📊 5 job offers in 3 weeks
        - 💰 $145K + equity package
        - 🚀 Career acceleration beyond expectations
        """)
    
    with col2:
        st.markdown("""
        ### 👨‍💼 Marcus Williams - Product Manager at Meta
        **Timeline:** Career changer from finance
        
        *"Switching from finance to tech seemed impossible. AI Career Agent identified transferable skills and positioned me perfectly for PM roles."*
        
        **Results:**
        - 🔄 Successful career transition
        - 📈 40% salary increase from finance
        - 🎯 Landed at top-tier tech company
        - 💡 AI identified hidden opportunities
        """)
        
        st.markdown("""
        ### 👩‍💻 Emily Rodriguez - Full-Stack Developer at Startup
        **Timeline:** Bootcamp graduate, no CS degree
        
        *"As a bootcamp grad competing with CS majors, I needed an edge. AI Career Agent highlighted my projects perfectly and got me noticed."*
        
        **Results:**
        - 🎓 Overcame education gap
        - 💼 Multiple startup offers
        - 📈 $95K starting salary
        - 🚀 Fast-track to senior roles
        """)
    
    # Statistics
    st.markdown("### 📊 Overall Success Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Students Helped", "2,500+", "And growing daily")
    with col2:
        st.metric("Average Time to Offer", "3.2 weeks", "vs 4.5 months manual")
    with col3:
        st.metric("Success Rate", "94%", "Land job within 90 days")
    with col4:
        st.metric("Salary Increase", "+23%", "vs manual applications")

def render_pricing_page():
    """Render the pricing page"""
    st.markdown("# 💰 Pricing Plans")
    st.markdown("### Choose the plan that fits your career timeline")
    
    # Pricing cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🆓 Free Trial
        **Perfect for testing the waters**
        
        **$0** for 7 days
        
        ✅ 5 job applications per day
        ✅ Basic resume optimization
        ✅ Email notifications
        ✅ Career timeline assessment
        ❌ Premium job boards
        ❌ Interview scheduling
        ❌ Advanced analytics
        """)
        
        if st.button("Start Free Trial", key="pricing_free", use_container_width=True):
            st.session_state.show_onboarding = True
            st.rerun()
    
    with col2:
        st.markdown("""
        ### 🚀 Student Plan
        **Most popular for active job seekers**
        
        **$29/month** or $290/year (save 17%)
        
        ✅ Unlimited job applications
        ✅ Advanced resume optimization
        ✅ All job boards (50+ platforms)
        ✅ Interview scheduling
        ✅ Gmail integration
        ✅ Weekly progress reports
        ✅ Priority support
        """)
        
        if st.button("Choose Student Plan", key="pricing_student", type="primary", use_container_width=True):
            st.success("🎉 Student Plan selected! Complete onboarding to activate.")
            st.session_state.show_onboarding = True
            st.rerun()
    
    with col3:
        st.markdown("""
        ### 💼 Professional Plan
        **For career changers & experienced professionals**
        
        **$49/month** or $490/year (save 17%)
        
        ✅ Everything in Student Plan
        ✅ Executive job boards
        ✅ Salary negotiation support
        ✅ Personal career coach
        ✅ LinkedIn optimization
        ✅ Network introductions
        ✅ White-glove service
        """)
        
        if st.button("Choose Professional", key="pricing_pro", use_container_width=True):
            st.success("💼 Professional Plan selected! Complete onboarding to activate.")
            st.session_state.show_onboarding = True
            st.rerun()
    
    # FAQ
    st.markdown("### ❓ Frequently Asked Questions")
    
    with st.expander("How does the free trial work?"):
        st.write("Start immediately with no credit card required. Full access to core features for 7 days.")
    
    with st.expander("Can I cancel anytime?"):
        st.write("Yes! Cancel anytime with no penalties. Your AI agent stops working immediately upon cancellation.")
    
    with st.expander("What if I don't get a job?"):
        st.write("We offer a 90-day job guarantee. If you don't get at least 3 interviews in 90 days, we'll refund your money.")

def render_about_page():
    """Render the about us page"""
    st.markdown("# 👥 About AI Career Agent")
    st.markdown("### Empowering the next generation of professionals with AI")
    
    # Mission
    st.markdown("## 🎯 Our Mission")
    st.info("""
    **To democratize career success through AI technology.**
    
    We believe every student and graduate deserves access to the same career acceleration tools that top professionals use. 
    Our AI levels the playing field, giving everyone an unfair advantage in today's competitive job market.
    """)
    
    # Team
    st.markdown("## 👨‍💻 Our Team")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🧠 Dr. Sarah Chen
        **CEO & Co-Founder**
        
        Former Google AI researcher with 10+ years in machine learning. PhD from Stanford. 
        Passionate about using AI to solve real-world problems.
        """)
    
    with col2:
        st.markdown("""
        ### 💼 Marcus Johnson
        **CTO & Co-Founder**
        
        Ex-Microsoft engineer who built career platforms at scale. 
        Expert in job market data and recruitment automation.
        """)
    
    with col3:
        st.markdown("""
        ### 🎓 Emily Rodriguez
        **Head of Student Success**
        
        Former university career counselor who helped 1000+ students land jobs. 
        Understands the unique challenges students face.
        """)
    
    # Company stats
    st.markdown("## 📊 Company Highlights")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Founded", "2023", "Y Combinator S23")
    with col2:
        st.metric("Students Helped", "2,500+", "Across 200+ universities")
    with col3:
        st.metric("Job Placements", "2,350+", "94% success rate")
    with col4:
        st.metric("Funding Raised", "$5.2M", "Series A led by Andreessen Horowitz")
    
    # Values
    st.markdown("## 💡 Our Values")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Student-First
        Every decision we make prioritizes student success over profits.
        
        ### 🤖 AI for Good
        We use cutting-edge AI to solve meaningful problems, not create them.
        """)
    
    with col2:
        st.markdown("""
        ### 🌍 Accessibility
        Career success shouldn't depend on your network or background.
        
        ### 📈 Continuous Innovation
        We're constantly improving our AI to serve students better.
        """)

def render_landing_page():
    """Render the complete landing page"""
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-container">
            <div class="hero-content">
                <div class="hero-tagline">YOUR AI-POWERED CAREER PARTNER</div>
                <h1 class="hero-title">Land Your Dream Job Without Limits</h1>
                <p class="hero-subtitle">
                    AI-powered career acceleration for students and graduates. 
                    We handle job search, applications, and interview prep automatically.
                </p>
                <ul class="hero-features">
                    <li>Automated job discovery across 50+ platforms daily</li>
                    <li>AI-optimized resumes tailored for each application</li>
                    <li>Smart interview scheduling and preparation</li>
                    <li>Real-time market intelligence and salary insights</li>
                </ul>
                <div class="hero-actions">
                    <button class="primary-cta">🚀 START YOUR CAREER JOURNEY</button>
                    <div class="social-links">
                        <a href="#" class="social-link">📧</a>
                        <a href="#" class="social-link">💼</a>
                        <a href="#" class="social-link">🐦</a>
                        <a href="#" class="social-link">📱</a>
                    </div>
                </div>
            </div>
            <div class="hero-visual">
                <div class="ai-dashboard">
                    <div class="dashboard-header">
                        <div class="dashboard-title">🤖 AI Career Agent</div>
                        <div class="ai-status">
                            <div class="status-dot"></div>
                            AI Working
                        </div>
                    </div>
                    <div class="dashboard-content">
                        <div class="ai-metric">
                            <span>🎯 Jobs Found Today</span>
                            <span class="metric-value">23</span>
                        </div>
                        <div class="ai-metric">
                            <span>📝 Applications Sent</span>
                            <span class="metric-value">12</span>
                        </div>
                        <div class="ai-metric">
                            <span>📞 Interviews Scheduled</span>
                            <span class="metric-value">4</span>
                        </div>
                        <div class="ai-metric">
                            <span>✅ Response Rate</span>
                            <span class="metric-value">34%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive CTA Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 START FREE TRIAL", use_container_width=True, type="primary"):
            st.session_state.show_onboarding = True
            st.rerun()
    
    # Features Section
    st.markdown("""
    <div class="features-section">
        <div class="features-container">
            <h2 class="section-title">Why Choose AI Career Agent?</h2>
            <p class="section-subtitle">
                We combine cutting-edge AI with deep career expertise to give you an unfair advantage in today's competitive job market.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("""
    <div class="stats-section">
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">95%</div>
                <div class="stat-label">Job Match Accuracy</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">3x</div>
                <div class="stat-label">Faster Job Placement</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">50+</div>
                <div class="stat-label">Job Boards Monitored</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">24/7</div>
                <div class="stat-label">AI Agent Working</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Final CTA
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎓 START YOUR SUCCESS STORY", use_container_width=True, type="primary"):
            st.session_state.show_onboarding = True
            st.rerun()

def main():
    """Main application entry point with page routing"""
    
    # Initialize current page
    if 'current_nav_page' not in st.session_state:
        st.session_state.current_nav_page = 'home'
    
    # Always show navigation header
    render_navigation()
    
    # Check which view to show
    if st.session_state.get('show_main_app', False):
        render_main_app()
    elif st.session_state.get('show_onboarding', False):
        render_onboarding_flow()
    else:
        # Route to different pages based on navigation
        current_page = st.session_state.get('current_nav_page', 'home')
        
        if current_page == 'home':
            render_landing_page()
        elif current_page == 'features':
            render_features_page()
        elif current_page == 'how_it_works':
            render_how_it_works_page()
        elif current_page == 'success_stories':
            render_success_stories_page()
        elif current_page == 'pricing':
            render_pricing_page()
        elif current_page == 'about':
            render_about_page()
        else:
            render_landing_page()  # Default fallback

if __name__ == "__main__":
    main()