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
        'Month': pd.date_range('2024-01-01', periods=12, freq='M'),
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
    """Render professional header with navigation"""
    st.markdown("""
    <div class="professional-header">
        <div class="header-content">
            <div class="logo-section">
                <span style="font-size: 2rem;">🎓</span>
                <h1>AI Career Agent</h1>
            </div>
            <div class="nav-menu">
                <div class="nav-item">
                    <span>🏠</span> Home
                </div>
                <div class="nav-item">
                    <span>📊</span> Dashboard
                </div>
                <div class="nav-item">
                    <span>💼</span> Jobs
                </div>
                <div class="dropdown">
                    <div class="nav-item">
                        <span>⚙️</span> Services ▼
                    </div>
                    <div class="dropdown-content">
                        <a href="#" class="dropdown-item">🎯 Career Planning</a>
                        <a href="#" class="dropdown-item">📝 Resume Optimization</a>
                        <a href="#" class="dropdown-item">🔍 Job Search</a>
                        <a href="#" class="dropdown-item">📈 Market Intelligence</a>
                        <a href="#" class="dropdown-item">🎤 Interview Prep</a>
                        <a href="#" class="dropdown-item">📚 Skill Development</a>
                    </div>
                </div>
                <div class="nav-item">
                    <span>📞</span> Contact
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        st.markdown("""
        <div class="modal-overlay" id="graduationModal">
            <div class="modal-content">
                <h2 style="text-align: center; color: var(--primary-blue); margin-bottom: 1.5rem;">
                    🎓 Welcome to AI Career Agent
                </h2>
                <p style="text-align: center; margin-bottom: 2rem;">
                    Let's personalize your career journey based on your graduation timeline
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create form in the modal area
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
    
    # Check if user has completed onboarding
    if 'user_profile' not in st.session_state:
        render_graduation_popup()
    else:
        render_personalized_dashboard()
    
    render_footer()
    
    if selected_view == "Market Trends":
        st.header("📈 Job Market Trends")
        st.markdown("**Real-time job posting trends across key tech roles**")
        
        # Interactive line chart
        fig = px.line(
            job_trends.melt(id_vars=['Month'], var_name='Role', value_name='Job_Postings'),
            x='Month', y='Job_Postings', color='Role',
            title="Monthly Job Postings by Role (2024)",
            labels={'Job_Postings': 'Number of Job Postings', 'Month': 'Month'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#151F30'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🚀 Fastest Growing", "Software Engineer", "+112%")
        with col2:
            st.metric("📊 Most Stable", "Product Manager", "+103%")
        with col3:
            st.metric("🔥 Hottest Market", "Data Science", "+114%")
    
    elif selected_view == "Salary Analysis":
        st.header("💰 Salary Intelligence")
        st.markdown("**Compensation benchmarks by experience level**")
        
        # Salary comparison chart
        fig = px.bar(
            salary_data.melt(id_vars=['Experience'], var_name='Role', value_name='Salary'),
            x='Experience', y='Salary', color='Role',
            title="Average Salary by Experience Level",
            labels={'Salary': 'Annual Salary (USD)', 'Experience': 'Years of Experience'},
            barmode='group'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#151F30'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Salary calculator
        st.subheader("🧮 Salary Estimator")
        col1, col2 = st.columns(2)
        with col1:
            selected_role = st.selectbox("Select Role", salary_data.columns[1:])
            experience_level = st.selectbox("Experience Level", salary_data['Experience'])
        
        with col2:
            if selected_role and experience_level:
                estimated_salary = salary_data[salary_data['Experience'] == experience_level][selected_role].iloc[0]
                st.metric("💵 Estimated Salary", f"${estimated_salary:,}")
                st.info(f"Based on current market data for {selected_role} with {experience_level} experience")
    
    elif selected_view == "Skills Intelligence":
        st.header("🎯 Skills Market Intelligence")
        st.markdown("**In-demand skills and growth opportunities**")
        
        # Skills demand bubble chart
        fig = px.scatter(
            skills_data, x='Demand_Score', y='Growth_Rate', size='Demand_Score',
            hover_name='Skill', title="Skills: Demand vs Growth Rate",
            labels={'Demand_Score': 'Current Demand Score', 'Growth_Rate': 'Growth Rate (%)'},
            size_max=60
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#151F30'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top skills recommendations
        st.subheader("🚀 Recommended Skills to Learn")
        top_growth_skills = skills_data.nlargest(3, 'Growth_Rate')
        
        for idx, skill in top_growth_skills.iterrows():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{skill['Skill']}**")
            with col2:
                st.metric("Demand", f"{skill['Demand_Score']}/100")
            with col3:
                st.metric("Growth", f"+{skill['Growth_Rate']}%")
    
    elif selected_view == "Geographic Insights":
        st.header("🗺️ Geographic Job Market")
        st.markdown("**Location-based career opportunities and cost analysis**")
        
        # City comparison chart
        fig = px.scatter(
            geo_data, x='Cost_of_Living_Index', y='Avg_Salary', size='Job_Count',
            hover_name='City', title="Salary vs Cost of Living by City",
            labels={'Cost_of_Living_Index': 'Cost of Living Index', 'Avg_Salary': 'Average Salary (USD)'},
            size_max=60
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#151F30'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # City rankings
        st.subheader("🏆 Top Cities for Tech Careers")
        geo_data['Value_Score'] = (geo_data['Avg_Salary'] / geo_data['Cost_of_Living_Index']) * 100
        top_cities = geo_data.nlargest(5, 'Value_Score')[['City', 'Job_Count', 'Avg_Salary', 'Value_Score']]
        
        for idx, city in top_cities.iterrows():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**{city['City']}**")
            with col2:
                st.metric("Jobs", f"{city['Job_Count']:,}")
            with col3:
                st.metric("Avg Salary", f"${city['Avg_Salary']:,}")
            with col4:
                st.metric("Value Score", f"{city['Value_Score']:.0f}")
    
    elif selected_view == "Career Planner":
        st.header("🎯 Personalized Career Planner")
        st.markdown("**Plan your career path with data-driven insights**")
        
        with st.form("career_planner"):
            col1, col2 = st.columns(2)
            with col1:
                current_role = st.selectbox("Current Role", ["Junior Developer", "Software Engineer", "Senior Engineer", "Tech Lead"])
                experience_years = st.slider("Years of Experience", 0, 15, 3)
            
            with col2:
                target_role = st.selectbox("Target Role", ["Software Engineer", "Data Scientist", "Product Manager", "DevOps Engineer"])
                target_location = st.selectbox("Preferred Location", geo_data['City'].tolist())
            
            if st.form_submit_button("🚀 Generate Career Plan"):
                st.success("✅ Career plan generated!")
                
                # Show personalized insights
                target_salary = geo_data[geo_data['City'] == target_location]['Avg_Salary'].iloc[0]
                job_count = geo_data[geo_data['City'] == target_location]['Job_Count'].iloc[0]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🎯 Target Salary", f"${target_salary:,}")
                with col2:
                    st.metric("📍 Available Jobs", f"{job_count:,}")
                with col3:
                    st.metric("⏱️ Timeline", "6-12 months")
                
                st.info(f"💡 **Recommendation:** Focus on {target_role} skills in {target_location}. The market shows strong demand with {job_count:,} available positions.")
    
    # Footer
    st.markdown("---")
    st.markdown("*Data updated in real-time • AI Career Agent Dashboard*")

if __name__ == "__main__":
    main()