# AWSAI-IIITB_Coders

AWSAI - AI Misconfiguration Assistant

The AWSAI - It is a system designed to help users understand, diagnose, and resolve AWS configuration issues using intelligent analysis and structured explanations. It simplifies troubleshooting by converting raw error messages into actionable insights.

1) Overview:

Cloud configuration errors are one of the most common causes of system failures and security risks. This project provides an intelligent assistant that analyzes AWS error messages, identifies root causes, and suggests corrective actions in a clear and structured manner.

2) Key Features:

a) Intelligent classification of AWS errors
b) Rule-based issue identification
c) AI-generated explanations and recommendations
d) Clean and intuitive user interface
e) User authentication and session management
f) History of previously analyzed issues

3) System Workflow :

Step-1: User provides an AWS error or configuration issue
Step-2: The system classifies the issue type
Step-3: A structured prompt is generated
Step-4: An AI model analyzes the issue
Step-5: The system returns a clear explanation and recommended fix

4) Technology Stack :

a) Frontend: Streamlit
b) Backend: Python
c) AI Engine: OpenAI API
d) Database: SQLite

5) Project Structure :
aws-ai-misconfig/
│
├── app.py
├── database.py
├── ai_clients.py
├── prompts.py
├── requirements.txt

6) Security Considerations :

a) Sensitive data is never hard-coded
b) API keys are stored securely using environment variables
c) User credentials are stored securely in the database

7) Summary:

This project demonstrates how AI can be effectively used to simplify cloud troubleshooting by combining intelligent automation with an intuitive user experience and solve it
