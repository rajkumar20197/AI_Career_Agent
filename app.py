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
    page_title="AI Career Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Use system fonts for better performance */
    
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
    }
    
    /* Global Styles */
    .main {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Smooth scrolling for navigation */
    html {
        scroll-behavior: smooth;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-blue) 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(21, 31, 48, 0.2);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    /* Card Styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(21, 31, 48, 0.1);
        border-left: 4px solid var(--primary-teal);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(21, 31, 48, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-teal);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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

def main():
    """Main application entry point"""
    st.title("🤖 AI Career Agent Dashboard")
    st.markdown("### Data-driven insights for your career success")
    
    # Generate sample data
    job_trends, salary_data, skills_data, geo_data = create_sample_data()
    
    # Sidebar for navigation
    st.sidebar.title("📊 Dashboard Navigation")
    selected_view = st.sidebar.selectbox(
        "Choose Analysis View",
        ["Market Trends", "Salary Analysis", "Skills Intelligence", "Geographic Insights", "Career Planner"]
    )
    
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