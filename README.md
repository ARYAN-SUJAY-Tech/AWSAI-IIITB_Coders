# AWSAI-IIITB_Coders

AWSAI – AI Misconfiguration Assistant

AWSAI is an intelligent system designed to help users understand, diagnose, and resolve AWS configuration issues using AI-powered analysis and structured explanations.

Overview

Cloud configuration errors are one of the most common causes of service outages and security vulnerabilities.
This project provides an intelligent assistant that analyzes AWS error messages, identifies root causes, and suggests corrective actions in a clear and structured manner.

Key Features

Intelligent classification of AWS errors

Rule-based issue identification

AI-generated explanations and recommendations

Clean and intuitive user interface

User authentication and session handling

History of previously analyzed issues

System Workflow

User provides an AWS error or configuration issue

The system classifies the issue type

A structured prompt is generated

An AI model analyzes the issue

A clear explanation and fix are presented

Technology Stack

Frontend: Streamlit

Backend: Python

AI Engine: OpenAI API

Database: SQLite

Project Structure
aws-ai-misconfig/
│
├── app.py
├── database.py
├── ai_clients.py
├── prompts.py
├── requirements.txt

Security Considerations

Sensitive information is never hard-coded

API keys are stored securely using environment variables

User credentials are securely handled in the database

Summary

This project demonstrates how AI can simplify cloud troubleshooting by combining automation, intelligent reasoning, and a clean user interface. It serves as a practical solution for developers dealing with AWS configuration challenges.
