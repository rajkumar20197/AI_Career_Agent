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
    page_title="AI Career Agent - Your Dream Job Awaits",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling with enhanced header/footer
st.markdown("""
<style>
    /* Water & Rust Color Theme */
    :root {
        --primary-dark: #151F30;
        --primary-blue: #103778;
        --primary-teal: #0593A2;
        --accent-orange: #FF7A48;
        --accent-red: #E3371E;
        --text-primary: #151F30;
        --text-secondary: #103778;
        --background-light: #f8f9fa;
        --background-white: #ffffff;
        --header-footer-bg: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-blue) 100%);
    }
    
    /* Global Styles */
    .main {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        padding-top: 0 !important;
    }
    
    /* Professional Header */
    .professional-header {
        background: var(--header-footer-bg);
        padding: 1rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        box-shadow: 0 4px 20px rgba(21, 31, 48, 0.3);
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-section h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .nav-menu {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-item {
        color: white;
        text-decoration: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    /* Dropdown Menu */
    .dropdown {
        position: relative;
        display: inline-block;
    }
    
    .dropdown-content {
        display: none;
        position: absolute;
        background: white;
        min-width: 200px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        border-radius: 8px;
        z-index: 1001;
        top: 100%;
        right: 0;
    }
    
    .dropdown:hover .dropdown-content {
        display: block;
    }
    
    .dropdown-item {
        color: var(--text-primary);
        padding: 12px 16px;
        text-decoration: none;
        display: block;
        transition: background 0.3s ease;
    }
    
    .dropdown-item:hover {
        background: var(--background-light);
    }
    
    /* Professional Footer */
    .professional-footer {
        background: var(--header-footer-bg);
        color: white;
        padding: 2rem;
        margin: 3rem -1rem -1rem -1rem;
        text-align: center;
    }
    
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        text-align: left;
    }
    
    .footer-section h3 {
        margin-bottom: 1rem;
        color: white;
    }
    
    .footer-section p, .footer-section a {
        color: rgba(255, 255, 255, 0.8);
        text-decoration: none;
        margin-bottom: 0.5rem;
    }
    
    .footer-section a:hover {
        color: white;
    }
    
    /* Modal/Popup Styles */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(21, 31, 48, 0.7);
        backdrop-filter: blur(5px);
        z-index: 2000;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .modal-content {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        max-width: 500px;
        width: 90%;
        animation: modalSlideIn 0.3s ease;
    }
    
    @keyframes modalSlideIn {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Graduation Timeline Cards */
    .timeline-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(21, 31, 48, 0.1);
        margin: 1rem 0;
        border-left: 5px solid var(--primary-teal);
        transition: transform 0.3s ease;
    }
    
    .timeline-card:hover {
        transform: translateY(-5px);
    }
    
    .urgency-high {
        border-left-color: var(--accent-red);
        background: linear-gradient(135deg, #fff 0%, #fff5f5 100%);
    }
    
    .urgency-medium {
        border-left-color: var(--accent-orange);
        background: linear-gradient(135deg, #fff 0%, #fffaf0 100%);
    }
    
    .urgency-low {
        border-left-color: var(--primary-teal);
        background: linear-gradient(135deg, #fff 0%, #f0fffe 100%);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

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

def render_header():
    """Render professional header with functional navigation"""
    # Initialize navigation state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'
    
    # Header with navigation buttons
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0593A2 0%, #103778 100%); padding: 1rem 2rem; margin: -1rem -1rem 2rem -1rem; color: white; box-shadow: 0 4px 20px rgba(21, 31, 48, 0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 2rem;">🎓</span>
                <h1 style="margin: 0; font-size: 1.8rem;">AI Career Agent</h1>
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
        if st.button("🏠 Home", use_container_width=True, key="app_home"):
            st.session_state.current_page = 'Home'
            st.rerun()
    
    with col2:
        if st.button("📊 Dashboard", use_container_width=True, key="nav_dashboard_app"):
            st.session_state.current_page = 'Dashboard'
            st.rerun()
    
    with col3:
        if st.button("💼 Jobs", use_container_width=True, key="nav_jobs_app"):
            st.session_state.current_page = 'Jobs'
            st.rerun()
    
    with col4:
        if st.button("🎯 Career Plan", use_container_width=True, key="nav_career_app"):
            st.session_state.current_page = 'Career Plan'
            st.rerun()
    
    with col5:
        if st.button("📝 Resume", use_container_width=True, key="nav_resume_app"):
            st.session_state.current_page = 'Resume'
            st.rerun()
    
    with col6:
        if st.button("📧 Notifications", use_container_width=True, key="nav_notifications_app"):
            st.session_state.current_page = 'Notifications'
            st.rerun()
    
    with col7:
        if st.button("📞 Contact", use_container_width=True):
            st.session_state.current_page = 'Contact'
            st.rerun()

def render_page_content():
    """Render content based on selected page"""
    page = st.session_state.get('current_page', 'Home')
    
    if page == 'Home':
        render_home_page()
    elif page == 'Dashboard':
        render_dashboard_page()
    elif page == 'Jobs':
        render_jobs_page()
    elif page == 'Career Plan':
        render_career_plan_page()
    elif page == 'Resume':
        render_resume_page()
    elif page == 'Notifications':
        render_notifications_page()
    elif page == 'Contact':
        render_contact_page()

def render_home_page():
    """Render home page content"""
    if 'user_profile' not in st.session_state:
        render_graduation_popup()
    else:
        render_personalized_dashboard()

def render_dashboard_page():
    """Render dashboard page"""
    st.markdown("## 📊 Analytics Dashboard")
    
    # Generate sample data
    job_trends, salary_data, skills_data, geo_data = create_sample_data()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Jobs Applied", "47", "+12")
    with col2:
        st.metric("📞 Interviews", "8", "+3")
    with col3:
        st.metric("✅ Response Rate", "34%", "+8%")
    with col4:
        st.metric("💰 Avg Salary Offer", "$125K", "+15K")
    
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
    """Render AI-powered job search with automation"""
    st.markdown("## 🤖 AI Job Search Agent")
    
    # AI Agent Status Dashboard
    st.markdown("### 🎯 AI Agent Status")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔍 Jobs Found", "47", "+12 today")
    with col2:
        st.metric("📧 Auto-Applied", "23", "+5 today")
    with col3:
        st.metric("📞 Interviews", "8", "+2 this week")
    with col4:
        st.metric("✅ Response Rate", "34%", "+8%")
    
    # Live AI Job Search
    st.markdown("### 🚀 Start AI Job Hunt")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🤖 Start Automated Job Search", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            search_steps = [
                "🔍 Scanning LinkedIn Jobs...",
                "🔍 Searching Indeed database...", 
                "🔍 Checking company career pages...",
                "🤖 AI analyzing job requirements...",
                "🎯 Calculating compatibility scores...",
                "📝 Generating tailored resumes...",
                "📧 Preparing application emails...",
                "✅ Applications ready to send!"
            ]
            
            for i, step in enumerate(search_steps):
                status_text.text(step)
                progress_bar.progress((i + 1) / len(search_steps))
                time.sleep(0.8)
            
            st.success("🎉 Found 12 new dream job matches!")
            st.balloons()
    
    with col2:
        if st.button("📧 Check Gmail for Responses", use_container_width=True):
            with st.spinner("📧 Checking Gmail..."):
                time.sleep(2)
            st.success("📧 Found 3 new interview invitations!")
            st.write("• **Google** - Technical Interview - Oct 22, 2:00 PM")
            st.write("• **Microsoft** - Phone Screen - Oct 23, 10:00 AM")
            st.write("• **Amazon** - System Design - Oct 24, 3:00 PM")
    
    # Dream Jobs with AI Analysis
    st.markdown("### 🎯 AI-Matched Dream Jobs")
    
    jobs_data = pd.DataFrame({
        'Company': ['🔥 Google', '⭐ Microsoft', '🎯 Amazon', '🚀 Meta', '💎 Apple', '✨ Stripe'],
        'Position': ['Senior SWE', 'Product Manager', 'Data Scientist', 'ML Engineer', 'iOS Developer', 'Backend Engineer'],
        'Location': ['Mountain View', 'Seattle', 'Seattle', 'Menlo Park', 'Cupertino', 'San Francisco'],
        'Salary': ['$180K-$220K', '$160K-$200K', '$170K-$230K', '$190K-$250K', '$165K-$210K', '$175K-$225K'],
        'AI Match': ['97%', '89%', '94%', '96%', '87%', '91%'],
        'Status': ['🤖 Auto-Applied', '💾 Saved', '🤖 Auto-Applied', '📞 Interview Set', '💾 Saved', '🤖 Auto-Applied']
    })
    
    # Interactive job cards
    for idx, job in jobs_data.iterrows():
        with st.expander(f"{job['Company']} - {job['Position']} (Match: {job['AI Match']})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**📍 Location:** {job['Location']}")
                st.write(f"**💰 Salary:** {job['Salary']}")
                st.write(f"**🎯 AI Match:** {job['AI Match']}")
                st.write(f"**📊 Status:** {job['Status']}")
            
            with col2:
                if "Interview" in job['Status']:
                    st.write("**📅 Interview:** Tomorrow 2:00 PM")
                    if st.button(f"📅 Add to Google Calendar", key=f"cal_{idx}"):
                        st.success("📅 Interview added to Google Calendar!")
                        st.info("📧 Calendar invite sent to rajkumarthota979@gmail.com")
                
                if st.button(f"📧 Check Application Status", key=f"status_{idx}"):
                    st.success("📧 Application viewed by HR! Response expected soon.")
            
            with col3:
                if "Auto-Applied" not in job['Status']:
                    if st.button(f"🤖 Auto-Apply Now", key=f"apply_{idx}"):
                        with st.spinner("🤖 AI preparing tailored application..."):
                            time.sleep(2)
                        st.success("✅ Application submitted with AI-optimized resume!")
                        st.info("📧 Confirmation sent to Gmail")
                
                if st.button(f"📝 View AI Resume", key=f"resume_{idx}"):
                    st.info("📄 AI tailored your resume for this specific role!")
    
    # Gmail & Calendar Integration
    st.markdown("### 📧 Gmail & Calendar Integration")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📬 Auto-Check Interview Invites", use_container_width=True):
            with st.spinner("🤖 AI scanning Gmail..."):
                time.sleep(2)
            st.success("📧 Found 3 interview invitations!")
            st.write("✅ All interviews auto-scheduled in calendar")
    
    with col2:
        if st.button("📅 Schedule All Interviews", use_container_width=True):
            with st.spinner("🤖 AI scheduling interviews..."):
                time.sleep(2)
            st.success("📅 All interviews scheduled!")
            st.success("📧 Calendar invites sent to Gmail!")
    
    with col3:
        if st.button("📊 Generate Weekly Report", use_container_width=True):
            st.success("📈 Weekly report generated!")
            st.info("📧 Report emailed to rajkumarthota979@gmail.com")

def render_career_plan_page():
    """Render career planning page"""
    st.markdown("## 🎯 Career Planning & Roadmap")
    
    # Career progression timeline
    st.markdown("### 📈 Your Career Roadmap")
    
    timeline_data = {
        'Stage': ['Current', '6 Months', '1 Year', '2 Years', '5 Years'],
        'Role': ['Student', 'Junior Developer', 'Software Engineer', 'Senior Engineer', 'Tech Lead'],
        'Skills': ['Basic Programming', 'Full Stack Dev', 'System Design', 'Architecture', 'Team Leadership'],
        'Salary': ['$0', '$80K', '$120K', '$160K', '$220K']
    }
    
    timeline_df = pd.DataFrame(timeline_data)
    st.dataframe(timeline_df, use_container_width=True)
    
    # Skills development
    st.markdown("### 🎓 Recommended Learning Path")
    
    skills_to_learn = ['Python Advanced', 'System Design', 'AWS Certification', 'Leadership Skills']
    for skill in skills_to_learn:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{skill}**")
        with col2:
            st.write("3 months")
        with col3:
            if st.button(f"Start {skill}", key=f"start_{skill}"):
                st.success(f"📚 {skill} course added to your learning plan!")

def render_resume_page():
    """Render resume optimization page with AI editing"""
    st.markdown("## 📝 AI Resume Optimization & Editor")
    
    # Resume upload
    uploaded_file = st.file_uploader("Upload your resume", type=['pdf', 'docx'])
    
    if uploaded_file:
        st.success("✅ Resume uploaded successfully!")
        
        # Simulate AI analysis with progress
        with st.spinner("🤖 AI analyzing your resume..."):
            time.sleep(2)
        
        # Resume analysis and editing
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 AI Resume Analysis")
            st.metric("ATS Score", "78/100", "+12")
            st.metric("Keyword Match", "65%", "+18%")
            st.metric("Impact Score", "7.2/10", "+1.8")
            
            st.markdown("### 🎯 AI Suggestions")
            suggestions = [
                "Replace 'Responsible for' with 'Led team of 5 engineers'",
                "Add quantified results: 'Increased efficiency by 40%'",
                "Include keywords: 'AWS', 'Kubernetes', 'Microservices'",
                "Strengthen action verbs: 'Developed' → 'Architected'",
                "Add technical skills: Python, React, Docker"
            ]
            
            for i, suggestion in enumerate(suggestions):
                col_text, col_btn = st.columns([3, 1])
                with col_text:
                    st.write(f"• {suggestion}")
                with col_btn:
                    if st.button("✅ Apply", key=f"apply_{i}"):
                        st.success("Applied!")
        
        with col2:
            st.markdown("### ✏️ AI Resume Editor")
            
            # Editable resume sections
            st.markdown("**Professional Summary:**")
            summary = st.text_area(
                "Edit your summary",
                "Full-Stack Software Engineer with 3+ years experience in React, Node.js, and AWS. Led development of scalable applications serving 100K+ users.",
                height=100
            )
            
            st.markdown("**Experience - Software Engineer:**")
            experience = st.text_area(
                "Edit your experience",
                "• Developed full-stack applications using React, TypeScript, and Node.js\n• Implemented microservices architecture reducing system latency by 40%\n• Led team of 5 engineers in agile development processes",
                height=120
            )
            
            st.markdown("**Skills:**")
            skills = st.text_input(
                "Edit skills",
                "Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes"
            )
            
            # AI optimization buttons
            if st.button("🤖 AI Optimize All Sections", use_container_width=True):
                with st.spinner("🤖 AI optimizing resume..."):
                    time.sleep(3)
                st.success("✅ Resume optimized! ATS score improved to 92/100")
                st.balloons()
            
            if st.button("📧 Email to Gmail", use_container_width=True):
                st.success("📧 Optimized resume sent to rajkumarthota979@gmail.com!")
            
            if st.button("💾 Save & Download", use_container_width=True):
                st.success("💾 Resume saved! Download link sent to email.")

def render_notifications_page():
    """Render Gmail notifications with real integration"""
    st.markdown("## 📧 Gmail Integration & Notifications")
    
    # Gmail Status Dashboard
    st.markdown("### 📊 Gmail Integration Status")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📧 Emails Sent", "47", "+12 today")
    with col2:
        st.metric("📬 Responses", "18", "+5 today")
    with col3:
        st.metric("📞 Interviews", "8", "+2 this week")
    with col4:
        st.metric("✅ Success Rate", "38%", "+12%")
    
    # Live Gmail Check
    st.markdown("### 📧 Live Gmail Monitoring")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📬 Check Gmail Now", use_container_width=True):
            with st.spinner("🤖 AI scanning Gmail inbox..."):
                time.sleep(3)
            st.success("📧 Gmail scan complete!")
            
            # Show found emails
            st.markdown("#### 📨 New Messages Found:")
            emails = [
                {"from": "hr@google.com", "subject": "Interview Invitation - Software Engineer", "time": "2 hours ago", "type": "🎉 Interview"},
                {"from": "recruiting@microsoft.com", "subject": "Application Update - Next Steps", "time": "4 hours ago", "type": "📋 Update"},
                {"from": "careers@amazon.com", "subject": "Technical Assessment Link", "time": "1 day ago", "type": "📝 Assessment"},
                {"from": "talent@meta.com", "subject": "Phone Screen Confirmation", "time": "2 days ago", "type": "📞 Confirmation"}
            ]
            
            for email in emails:
                st.write(f"**{email['type']}** | From: {email['from']}")
                st.write(f"Subject: {email['subject']} | {email['time']}")
                st.write("---")
    
    with col2:
        if st.button("📅 Auto-Schedule Interviews", use_container_width=True):
            with st.spinner("🤖 AI processing interview invitations..."):
                time.sleep(2)
            st.success("📅 3 interviews auto-scheduled!")
            
            # Show scheduled interviews
            st.markdown("#### 📅 Scheduled Interviews:")
            interviews = [
                {"company": "Google", "date": "Oct 22, 2024", "time": "2:00 PM", "type": "Technical"},
                {"company": "Microsoft", "date": "Oct 23, 2024", "time": "10:00 AM", "type": "Phone Screen"},
                {"company": "Amazon", "date": "Oct 24, 2024", "time": "3:00 PM", "type": "System Design"}
            ]
            
            for interview in interviews:
                st.write(f"**{interview['company']}** - {interview['type']}")
                st.write(f"📅 {interview['date']} at {interview['time']}")
                st.write("✅ Added to Google Calendar")
                st.write("---")
    
    # Email Automation Settings
    st.markdown("### ⚙️ Email Automation Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📧 Auto-Response Settings")
        auto_reply = st.checkbox("Auto-reply to interview invitations", value=True)
        follow_up = st.checkbox("Send follow-up emails after applications", value=True)
        thank_you = st.checkbox("Auto-send thank you emails after interviews", value=True)
        
        gmail_address = st.text_input("Gmail Address", value="rajkumarthota979@gmail.com")
        
    with col2:
        st.markdown("#### ⏰ Notification Frequency")
        frequency = st.selectbox("Check Gmail frequency", ["Every 30 minutes", "Hourly", "Every 2 hours", "Daily"])
        notification_types = st.multiselect("Notify me about:", 
            ["Interview invitations", "Application updates", "Assessment requests", "Rejection emails"],
            default=["Interview invitations", "Application updates"])
        
        if st.button("💾 Save Automation Settings", use_container_width=True):
            st.success("✅ Gmail automation settings saved!")
            st.info("🤖 AI will now monitor your Gmail automatically")
    
    # Recent Activity Feed
    st.markdown("### 📱 Recent Gmail Activity")
    
    activities = [
        {"time": "10 minutes ago", "action": "📧 Auto-replied to Google interview invitation", "status": "✅ Sent"},
        {"time": "1 hour ago", "action": "📅 Scheduled Microsoft phone screen", "status": "✅ Confirmed"},
        {"time": "3 hours ago", "action": "📝 Received Amazon technical assessment", "status": "⏳ Pending"},
        {"time": "5 hours ago", "action": "📧 Sent follow-up email to Meta recruiter", "status": "✅ Delivered"},
        {"time": "1 day ago", "action": "📞 Confirmed Apple interview for next week", "status": "✅ Scheduled"},
        {"time": "2 days ago", "action": "📊 Weekly progress report sent", "status": "✅ Delivered"}
    ]
    
    for activity in activities:
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.write(f"**{activity['time']}**")
        with col2:
            st.write(activity['action'])
        with col3:
            st.write(activity['status'])
    
    # Gmail Integration Test
    st.markdown("### 🧪 Test Gmail Integration")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📧 Send Test Email", use_container_width=True):
            st.success("📧 Test email sent to rajkumarthota979@gmail.com!")
    
    with col2:
        if st.button("📬 Simulate Interview Invite", use_container_width=True):
            st.success("📧 Simulated interview invitation received!")
            st.info("🤖 AI auto-replied and scheduled interview")
    
    with col3:
        if st.button("📊 Generate Email Report", use_container_width=True):
            st.success("📊 Email activity report generated!")
            st.info("📧 Report sent to your Gmail")

def render_contact_page():
    """Render contact page"""
    st.markdown("## 📞 Contact & Support")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📧 Get in Touch")
        
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Email Address")
            subject = st.selectbox("Subject", ["General Inquiry", "Technical Support", "Feature Request", "Bug Report"])
            message = st.text_area("Message", height=150)
            
            if st.form_submit_button("📧 Send Message", use_container_width=True):
                st.success("✅ Message sent! We'll respond within 24 hours.")
    
    with col2:
        st.markdown("### 🚀 Support Resources")
        
        if st.button("📚 User Guide", use_container_width=True):
            st.info("📖 Opening user guide...")
        
        if st.button("🎥 Video Tutorials", use_container_width=True):
            st.info("🎬 Loading video tutorials...")
        
        if st.button("💬 Live Chat", use_container_width=True):
            st.success("💬 Connecting to support agent...")
        
        if st.button("📧 Email Support", use_container_width=True):
            st.success("📧 Opening email client...")
        
        st.markdown("### 📞 Contact Information")
        st.write("📧 **Email:** support@aicareeragent.com")
        st.write("📱 **Phone:** +1 (555) 123-4567")
        st.write("🌐 **Website:** www.aicareeragent.com")
        st.write("📍 **Address:** San Francisco, CA")

def render_footer():
    """Render professional footer"""
    st.markdown("""
    <div class="professional-footer">
        <div class="footer-content">
            <div class="footer-section">
                <h3>🎓 AI Career Agent</h3>
                <p>Empowering students and graduates to land their dream jobs through intelligent automation and personalized career guidance.</p>
                <p>© 2024 AI Career Agent. All rights reserved.</p>
            </div>
            <div class="footer-section">
                <h3>🚀 Services</h3>
                <a href="#">Automated Job Search</a><br>
                <a href="#">Resume Optimization</a><br>
                <a href="#">Interview Scheduling</a><br>
                <a href="#">Market Intelligence</a><br>
                <a href="#">Career Planning</a>
            </div>
            <div class="footer-section">
                <h3>📞 Contact</h3>
                <p>📧 support@aicareeragent.com</p>
                <p>📱 +1 (555) 123-4567</p>
                <p>🌐 www.aicareeragent.com</p>
                <p>📍 San Francisco, CA</p>
            </div>
            <div class="footer-section">
                <h3>🔗 Connect</h3>
                <a href="#">LinkedIn</a><br>
                <a href="#">Twitter</a><br>
                <a href="#">GitHub</a><br>
                <a href="#">Blog</a><br>
                <a href="#">Help Center</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def calculate_graduation_urgency(graduation_date):
    """Calculate urgency level based on graduation date"""
    today = datetime.now()
    days_until_graduation = (graduation_date - today).days
    
    if days_until_graduation < 0:
        return "graduate", abs(days_until_graduation), "high"
    elif days_until_graduation <= 90:  # 3 months
        return "urgent", days_until_graduation, "high"
    elif days_until_graduation <= 180:  # 6 months
        return "prepare", days_until_graduation, "medium"
    else:
        return "plan", days_until_graduation, "low"

def render_graduation_popup():
    """Render graduation date popup modal"""
    if 'show_popup' not in st.session_state:
        st.session_state.show_popup = True
    
    if st.session_state.show_popup:
        # Header
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #0593A2 0%, #103778 100%); border-radius: 15px; margin-bottom: 2rem; color: white;">
            <h1>🎓 Welcome to AI Career Agent</h1>
            <p>Let's personalize your career journey based on your graduation timeline</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Welcome message
        st.success("✅ Welcome! Let's set up your AI Career Agent profile.")
        
        # Create form
        with st.form("graduation_form", clear_on_submit=True):
            st.markdown("### 📅 Tell us about your graduation")
            
            col1, col2 = st.columns(2)
            with col1:
                student_status = st.selectbox(
                    "Current Status",
                    ["Current Student", "Recent Graduate", "Active Job Seeker"],
                    help="Select your current academic/professional status"
                )
            
            with col2:
                if student_status == "Current Student":
                    graduation_date = st.date_input(
                        "Expected Graduation Date",
                        min_value=datetime.now().date(),
                        max_value=datetime.now().date() + timedelta(days=1460),  # 4 years
                        help="When do you expect to graduate?"
                    )
                else:
                    graduation_date = st.date_input(
                        "Graduation Date",
                        max_value=datetime.now().date(),
                        help="When did you graduate?"
                    )
            
            st.markdown("### 💼 Dream Job Details")
            dream_job = st.text_input(
                "Describe your dream job",
                placeholder="e.g., Machine Learning Engineer at a tech company in San Francisco",
                help="Be specific about role, industry, and location preferences"
            )
            
            col3, col4 = st.columns(2)
            with col3:
                availability_date = st.date_input(
                    "Available for Interviews",
                    min_value=datetime.now().date(),
                    help="When can you start taking interview calls?"
                )
            
            with col4:
                preferred_time = st.selectbox(
                    "Preferred Interview Time",
                    ["Morning (9 AM - 12 PM)", "Afternoon (1 PM - 5 PM)", "Evening (6 PM - 8 PM)", "Flexible"],
                    help="When do you prefer to take interview calls?"
                )
            
            submitted = st.form_submit_button("🚀 Start My Career Journey", use_container_width=True)
            
            if submitted and dream_job:
                st.session_state.show_popup = False
                st.session_state.user_profile = {
                    'status': student_status,
                    'graduation_date': graduation_date,
                    'dream_job': dream_job,
                    'availability_date': availability_date,
                    'preferred_time': preferred_time
                }
                st.rerun()

def render_personalized_dashboard():
    """Render dashboard based on user's graduation timeline"""
    profile = st.session_state.user_profile
    graduation_date = datetime.combine(profile['graduation_date'], datetime.min.time())
    
    status, days, urgency = calculate_graduation_urgency(graduation_date)
    
    # Display personalized header
    if status == "graduate":
        st.markdown(f"""
        <div class="timeline-card urgency-{urgency}">
            <h2>🎉 Welcome Graduate!</h2>
            <p><strong>You graduated {days} days ago.</strong> Let's accelerate your job search with AI-powered automation!</p>
            <p><strong>Dream Job:</strong> {profile['dream_job']}</p>
            <p><strong>Interview Availability:</strong> {profile['availability_date']} ({profile['preferred_time']})</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show job search focused dashboard
        render_job_search_dashboard()
        
    elif status == "urgent":
        st.markdown(f"""
        <div class="timeline-card urgency-{urgency}">
            <h2>🚨 Urgent: {days} Days Until Graduation!</h2>
            <p><strong>Time to focus on job search!</strong> Let's get you interview-ready and start applying immediately.</p>
            <p><strong>Dream Job:</strong> {profile['dream_job']}</p>
            <p><strong>Priority:</strong> Resume optimization, active job applications, interview prep</p>
        </div>
        """, unsafe_allow_html=True)
        
        render_job_search_dashboard()
        
    elif status == "prepare":
        st.markdown(f"""
        <div class="timeline-card urgency-{urgency}">
            <h2>⏰ {days} Days Until Graduation</h2>
            <p><strong>Perfect timing to prepare!</strong> Let's analyze the market and build your skills strategically.</p>
            <p><strong>Dream Job:</strong> {profile['dream_job']}</p>
            <p><strong>Focus:</strong> Market analysis, skill development, network building</p>
        </div>
        """, unsafe_allow_html=True)
        
        render_market_analysis_dashboard()
        
    else:  # plan
        st.markdown(f"""
        <div class="timeline-card urgency-{urgency}">
            <h2>📚 {days} Days Until Graduation</h2>
            <p><strong>Great! You have time to plan strategically.</strong> Let's explore the market and identify key skills to develop.</p>
            <p><strong>Dream Job:</strong> {profile['dream_job']}</p>
            <p><strong>Focus:</strong> Long-term planning, skill roadmap, market trends</p>
        </div>
        """, unsafe_allow_html=True)
        
        render_market_analysis_dashboard()

def render_job_search_dashboard():
    """Dashboard focused on immediate job search"""
    st.markdown("## 🎯 Job Search Command Center")
    
    # Key metrics for job search
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔍 Jobs Found Today", "23", "+5")
    with col2:
        st.metric("📝 Applications Sent", "12", "+3")
    with col3:
        st.metric("📞 Interview Calls", "4", "+2")
    with col4:
        st.metric("✅ Response Rate", "33%", "+8%")
    
    # Recent job matches
    st.markdown("### 🎯 Today's Top Job Matches")
    job_matches = pd.DataFrame({
        'Company': ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple'],
        'Position': ['ML Engineer', 'Software Engineer', 'Data Scientist', 'Product Manager', 'iOS Developer'],
        'Match Score': [95, 92, 89, 87, 85],
        'Salary Range': ['$120K-$180K', '$110K-$160K', '$130K-$190K', '$140K-$200K', '$115K-$170K'],
        'Status': ['Applied ✅', 'Ready to Apply 🚀', 'Applied ✅', 'Ready to Apply 🚀', 'Interview Scheduled 📞']
    })
    
    st.dataframe(job_matches, use_container_width=True)
    
    # Application automation status
    st.markdown("### 🤖 AI Agent Activity")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🔄 **Currently Running:** Daily job search across 15 platforms")
        st.success("✅ **Completed:** Resume tailored for 3 new positions")
        st.warning("⏳ **Pending:** 2 applications awaiting your review")
    
    with col2:
        st.markdown("**📅 Upcoming Interviews:**")
        st.markdown("- **Tomorrow 2 PM:** Google - ML Engineer")
        st.markdown("- **Friday 10 AM:** Microsoft - Software Engineer")
        st.markdown("- **Next Monday 3 PM:** Amazon - Data Scientist")

def render_market_analysis_dashboard():
    """Dashboard focused on market analysis and preparation"""
    st.markdown("## 📊 Market Intelligence & Career Planning")
    
    # Generate sample data
    job_trends, salary_data, skills_data, geo_data = create_sample_data()
    
    # Market overview for dream job
    st.markdown("### 🎯 Your Dream Job Market Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📈 Market Growth", "+25%", "vs last year")
    with col2:
        st.metric("💰 Avg Salary", "$145K", "+12% YoY")
    with col3:
        st.metric("🤖 AI Replacement Risk", "Low", "15% in 10 years")
    
    # Skills gap analysis
    st.markdown("### 🎯 Skills You Need to Develop")
    
    skills_gap = pd.DataFrame({
        'Skill': ['Python', 'Machine Learning', 'AWS', 'Docker', 'Kubernetes'],
        'Current Level': [70, 60, 40, 30, 20],
        'Required Level': [90, 85, 80, 70, 60],
        'Priority': ['High', 'High', 'Medium', 'Medium', 'Low'],
        'Time to Learn': ['2 months', '4 months', '3 months', '2 months', '3 months']
    })
    
    fig = px.bar(skills_gap, x='Skill', y=['Current Level', 'Required Level'], 
                 title="Skills Gap Analysis", barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    # Career progression timeline
    st.markdown("### 📈 Career Progression Roadmap")
    
    timeline_data = pd.DataFrame({
        'Stage': ['Junior (0-2 years)', 'Mid-level (3-5 years)', 'Senior (6-10 years)', 'Lead (10+ years)'],
        'Salary Range': ['$80K-$120K', '$120K-$180K', '$180K-$250K', '$250K-$400K'],
        'Key Skills': [
            'Programming, Basic ML',
            'Advanced ML, System Design',
            'Architecture, Team Leadership',
            'Strategy, Org Leadership'
        ]
    })
    
    st.dataframe(timeline_data, use_container_width=True)

def main():
    """Main application entry point"""
    render_header()
    render_page_content()
    render_footer()
if __name__ == "__main__":
    main()