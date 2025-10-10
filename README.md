AI Career Agent 🤖💼
An autonomous AI agent that manages the entire job application lifecycle for students and new graduates, from search to interview. This project was built for the AWS AI Agent Global Hackathon.

✨ What it Does
The AI Career Agent is designed to be a "set it and forget it" career assistant. A user simply provides their resume and a natural language description of their dream job. The agent then takes over, performing the following tasks autonomously:

Daily Job Discovery: Scans major job boards every day to find the best new opportunities that match the user's profile.

Intelligent Resume Tailoring: Uses an LLM to dynamically rewrite and optimize the user's resume and cover letter for each specific job application, maximizing the chance of success.

Automated Scheduling: Monitors the user's inbox for interview invitations, parses the details, and automatically schedules the interview on their calendar based on preset availability.

Proactive Interview Prep: Generates a curated study guide with potential questions, key topics, and helpful resources for every scheduled interview.

🛠️ How It's Built
At its core, the AI Career Agent uses Amazon Bedrock AgentCore to orchestrate a series of "tools" that are hosted as serverless AWS Lambda functions. The agent reasons about the user's goals, creates a plan, and then invokes the necessary tools—like searching for jobs, tailoring a resume, or checking an email—to execute that plan. All user documents are stored securely in Amazon S3.

🚀 Tech Stack
Cloud & AI: AWS, Amazon Bedrock (Anthropic Claude), Amazon Bedrock AgentCore

Backend: AWS Lambda, Python

Storage: Amazon S3

Notifications: Amazon SNS, Amazon SES

External APIs: Google Calendar, Google Mail, various Job Board APIs

Frontend: Streamlit

🔗 Links
Live Demo: Try the AI Career Agent

Video Demonstration: Watch the 3-Minute Demo

🔧 Getting Started
To get a local copy up and running, follow these simple steps.

Clone the repo:

Bash

git clone https://github.com/YourUsername/ai-career-agent.git
Configure your AWS credentials.

Install Python packages:

Bash

pip install -r requirements.txt
Run the Streamlit application:

Bash

streamlit run app.py
