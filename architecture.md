# AI Career Agent - Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Streamlit)                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Student       │  │   Dashboard     │  │   Job Search    │ │
│  │   Onboarding    │  │   Analytics     │  │   Interface     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Amazon Bedrock AgentCore                     │
│                     (Orchestration Layer)                      │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              Amazon Bedrock (Claude/Nova)                   │ │
│  │                   Reasoning Engine                          │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AWS Lambda Functions                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │   Market    │ │    Job      │ │   Resume    │ │  Interview  ││
│  │ Intelligence│ │   Search    │ │  Tailoring  │ │    Prep     ││
│  │   Service   │ │   Service   │ │   Service   │ │   Service   ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data & Storage Layer                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │  Amazon S3  │ │   Amazon    │ │   Amazon    │ │  External   ││
│  │ (Documents) │ │     SNS     │ │     SES     │ │    APIs     ││
│  │             │ │(Notifications)│ │   (Email)   │ │ (Job Boards)││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Intelligent Student Assessment

- **Graduation Timeline Analysis**: Determines urgency based on graduation date
- **Skill Gap Identification**: Analyzes current skills vs market requirements
- **Personalized Learning Path**: Suggests improvements based on timeline

### 2. Market Intelligence Dashboard

- **Real-time Salary Data**: Entry-level vs senior positions
- **Location-based Insights**: Job availability by geographic region
- **AI Impact Analysis**: Predicts job security and future trends
- **Skill Demand Tracking**: Most requested skills in target domain

### 3. Autonomous Job Application System

- **Smart Job Discovery**: Daily scanning of multiple job boards
- **Resume Optimization**: AI-powered tailoring for each application
- **Application Tracking**: Monitors application status and responses
- **Interview Scheduling**: Automated calendar management

### 4. Interview Preparation Engine

- **Company Research**: Automated gathering of company insights
- **Question Prediction**: AI-generated likely interview questions
- **Practice Sessions**: Mock interview capabilities
- **Performance Analytics**: Tracks improvement over time

## AWS Services Integration

### Amazon Bedrock AgentCore

- **Primary Orchestrator**: Manages all agent workflows
- **Decision Making**: Routes tasks to appropriate services
- **Context Management**: Maintains user session and preferences

### Amazon Bedrock (Claude/Nova)

- **Natural Language Processing**: Understands user requirements
- **Content Generation**: Creates tailored resumes and cover letters
- **Market Analysis**: Processes job market data for insights
- **Interview Preparation**: Generates personalized study materials

### AWS Lambda Functions

- **Serverless Execution**: Handles all backend processing
- **Scalable Architecture**: Automatically scales with demand
- **Cost Effective**: Pay-per-use model for optimal efficiency

### Storage & Communication

- **Amazon S3**: Secure document storage and retrieval
- **Amazon SNS**: Real-time notifications for job matches
- **Amazon SES**: Automated email communications
