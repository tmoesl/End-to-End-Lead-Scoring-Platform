![EdTech Banner](/app/frontend/static/lsp_banner.png)

# End-to-End Lead Scoring Platform

![Status](https://img.shields.io/badge/-Completed-34A853?style=flat&label=Project&labelColor=23555555)

## Executive Summary

🔗 **Links:** [Live Model](https://leads.dataproject.io "Access model for real-time lead inference") | [Model Training and Evaluation Repository](https://github.com/tmoesl/lead-conversion-prediction "Explore data preprocessing, feature engineering, model training, and performance evaluation.")

This repository contains the deployment infrastructure for ExtraaLearn’s Lead Conversion Prediction application, which leverages an optimized Random Forest model (Recall: 0.88, Accuracy: 0.83) to predict lead conversion for an EdTech startup, helping prioritize high-potential leads. 

By identifying key conversion drivers—such as website engagement, initial interaction channels, and profile completion—the model enables data-driven resource allocation to boost conversion rates and optimize marketing strategies.

**Key Features**
- **Real-Time Predictions**: AI-powered lead scoring with a trained Random Forest model.
- **Data-Driven Insights**: Analyze lead attributes to assess conversion probability.
- **Seamless Integration**: Export predictions for further analysis and strategic planning.

**Business Impact**
- **Maximize ROI**: Focus efforts on leads with the highest conversion potential.
- **Enhance Decision-Making**: Utilize data insights to refine marketing and sales strategies.
- **Optimize Marketing**: Leverage conversion drivers to refine campaigns.

## Table of Contents
- [Introduction](#introduction)
- [Application Infrastructure](#application-infrastructure)
- [Deployment Infrastructure](#deployment-infrastructure)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)


## Introduction
This repository provides the end-to-end deployment infrastructure for ExtraaLearn’s Lead Conversion Prediction application. The platform transforms analytical insights into a fully operational application, allowing sales and marketing teams to make data-driven decisions in lead prioritization. 
The application integrates a trained **Random Forest model**, which identifies key lead conversion drivers, helping businesses improve their marketing efficiency and optimize customer acquisition costs.

## Application Infrastructure
The application is structured as a microservices-based system, ensuring modularity, scalability, and maintainability:

1. **Frontend (Streamlit UI)**: An interactive interface for lead scoring, visualization, and report generation.
2. **Backend (FastAPI Service)**: Exposes a RESTful API for lead scoring using the trained model, with endpoints for prediction and health checks.
3. **Model Service**: A containerized ML inference service for real-time predictions using the trained model.

This architecture ensures that each component operates independently, supporting efficient scaling and maintenance.


## Deployment Infrastructure
The application is deployed on AWS EC2, leveraging Docker for containerization and Docker Compose for orchestration. The infrastructure includes:

- **Containerization**: Docker containers for consistent environment and simplified deployment.
- **Orchestration**: Docker Compose for multi-container management.
- **Cloud Provider**: AWS EC2 for hosting the application with ALB for traffic distribution and Route 53 for domain management.

This architecture guarantees secure, reliable performance and efficient scalability.

## Repository Structure
```
├── .dockerignore       <- Files excluded from Docker context
├── .gitignore          <- Files excluded from git tracking
├── compose.yml         <- Docker Compose configuration
├── LICENSE.txt         <- Open-source project license
├── README.md           <- Project documentation
│
├── app
│   ├── .streamlit      <- Streamlit configuration
│   ├── backend         <- API and business logic
│   ├── frontend        <- Streamlit UI components and pages
│   │   └── static      <- Static assets (images) for the frontend
│   ├── model           <- ML model and inference code
│   └── src             <- Shared utility, style and config functions
```


## Requirements

- `Python 3.11.6` or higher ([Download](https://www.python.org))
- Docker and Docker Compose ([Download](https://www.docker.com/get-started/))
- AWS account for cloud deployment ([Sign Up](https://aws.amazon.com/free/)) - Optional

## Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/tmoesl/lcp-aws-ec2.git
```

#### 2. Navigate to the Project Directory
```bash
cd lcp-aws-ec2
```

#### 3. Build and Deploy the Application (locally)
```bash
docker compose up --build
```

#### 4. Verify Local Deployment 
```bash
docker compose ps
docker compose logs -f
```

The application will be available at http://localhost:8501.

---
