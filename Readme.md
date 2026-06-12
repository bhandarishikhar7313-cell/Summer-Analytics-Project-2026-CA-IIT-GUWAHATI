# ✈️ Airline Retention Intelligence Platform

An AI-powered customer intelligence platform developed for the **Summer Projects '26 Challenge** organized by the **Consulting & Analytics Club, IIT Guwahati**.

The project addresses the challenge:

> **"Unlocking Behavioral Intelligence in Airline Loyalty Programs"**

Using airline loyalty program data, customer flight activity, customer lifetime value, and behavioral patterns, the platform helps airlines proactively identify at-risk customers, forecast future customer value, generate personalized retention strategies, and produce executive-level business intelligence reports.

---

# 📌 Project Overview

Airline loyalty programs are designed to improve customer retention and increase Customer Lifetime Value (CLV). However, many airlines struggle to identify disengaged customers before they leave, resulting in lost revenue and inefficient marketing efforts.

This project combines:

- Deep Learning (LSTM)
- Machine Learning (XGBoost)
- Customer Segmentation
- Future Value Forecasting
- Business Intelligence
- Generative AI (Qwen 3 8B)
- Streamlit Dashboarding

to transform raw customer behavior into actionable business decisions.

---

# 🎯 Business Problem

Airlines invest heavily in loyalty programs to encourage repeat business and increase customer lifetime value.

However, organizations often lack visibility into:

- Which customers are likely to churn
- Which customers generate the highest value
- Which customer segments require intervention
- How retention budgets should be allocated
- Which actions maximize customer lifetime value

As a result:

- Valuable customers may disengage unnoticed
- Retention campaigns become reactive
- Marketing resources are inefficiently allocated
- Revenue opportunities are lost

This platform helps airlines proactively identify customer risk and generate data-driven retention strategies.

---

# 🚀 Project Objectives

The system answers the following business questions:

### 1. Which customers are likely to churn?

Predicts churn probability using historical loyalty behavior and flight activity.

---

### 2. Which customers are most valuable?

Analyzes:

- Customer Lifetime Value (CLV)
- Loyalty Tier
- Salary
- Flight Activity
- Points Behavior

---

### 3. What customer segment do they belong to?

Automatically groups customers into meaningful business segments.

---

### 4. What is their future value?

Forecasts:

- Future Flights
- Future Distance
- Future Loyalty Points

---

### 5. What revenue is at risk?

Calculates estimated revenue loss based on churn risk and customer value.

---

### 6. What retention action should be taken?

Generates personalized business recommendations.

---

### 7. How should management respond?

Creates executive-level reports using Large Language Models.

---

# 🏆 Competition Context

This project was developed for:

### Summer Projects '26

**Consulting & Analytics Club**  
**Indian Institute of Technology (IIT) Guwahati**

Challenge:

### Unlocking Behavioral Intelligence in Airline Loyalty Programs

Category:

- Strategy
- Business Analytics
- Machine Learning
- Generative AI

---

# 📊 Dataset Overview

The project uses four integrated datasets:

## 1. Customer Loyalty History

Contains:

- Customer ID
- Loyalty Card
- Enrollment Information
- Customer Lifetime Value
- Demographics
- Cancellation Information

---

## 2. Customer Flight Activity

Contains monthly activity such as:

- Flights Booked
- Distance Traveled
- Points Accumulated
- Points Redeemed

---

## 3. Calendar Data

Contains:

- Month
- Quarter
- Seasonal Information

---

## 4. Data Dictionary

Provides complete feature definitions and business descriptions.

---

# 🏗 System Architecture

```text
Customer CSV
      │
      ▼
Data Validation
      │
      ▼
Feature Engineering
      │
      ▼
LSTM Behavioral Encoder
      │
      ▼
XGBoost Churn Predictor
      │
      ▼
Customer Segmentation
      │
      ▼
Future Value Forecasting
      │
      ▼
Retention Engine
      │
      ▼
Business Profile Generation
      │
      ▼
Qwen 3 8B (Ollama)
      │
      ▼
Executive Intelligence Report
      │
      ▼
Streamlit Dashboard
```

# 🧠 Machine Learning Pipeline

## Stage 1 — Behavioral Intelligence Extraction

Model:

```text
LSTM
```

Input:

```text
12 Months Historical Customer Activity
```

Features:

- Flights
- Distance
- Points
- Loyalty Engagement

Output:

```text
Customer Behavior Embedding
```

---

## Stage 2 — Churn Prediction

Model:

```text
XGBoost Classifier
```

Predicts:

- Churn Probability
- Risk Level

Output Example:

```json
{
  "churn_probability": 0.81,
  "priority": "HIGH"
}
```

---

## Stage 3 — Customer Segmentation

Model:

```text
KMeans Clustering
```

Segments:

- Premium Frequent Flyers
- Rising High-Value Customers
- Regular Travelers
- Value Seekers
- Dormant Customers

---

## Stage 4 — Future Value Forecasting

Models:

```text
XGBoost Regressors
```

Predicts:

- Future Flights
- Future Distance
- Future Points

Output Example:

```json
{
  "future_flights": 18,
  "future_distance": 32000,
  "future_points": 28500
}
```

---

## Stage 5 — Retention Engine

Calculates:

- Value Score
- Customer Priority
- Revenue Risk
- Estimated Loss

Generates:

- Recommended Actions
- Retention Strategies

Example:

```json
{
  "priority": "HIGH",
  "recommended_actions": [
    "Offer Bonus Points",
    "Tier Upgrade Review",
    "Personalized Outreach"
  ]
}
```

---

## Stage 6 — AI Executive Intelligence

Model:

```text
Qwen 3 8B
```

Running via:

```text
Ollama
```

Generates:

```json
{
  "executive_summary": "...",
  "risk_analysis": "...",
  "retention_strategy": "...",
  "business_impact": "...",
  "customer_message": "...",
  "manager_recommendation": "..."
}
```

---

# 📂 Project Structure

```text
Airline-Retention-Intelligence/

│
├── app/
│
│   ├── Home.py
│
│   └── pages/
│
│       ├── 01_Overview.py
│       ├── 02_Forecast.py
│       ├── 03_Retention_Strategy.py
│       ├── 04_AI_Executive_Summary.py
│       ├── 05_Customer_Message.py
│       └── 06_Reports_Export.py
│
├── testing/
│
│   ├── inference.py
│   ├── business_predictor.py
│   └── llm_report.py
│
├── models/
│
├── encoders/
│
├── datasets/
│
├── reports/
│
├── requirements.txt
│
└── README.md
```

# 📊 Dashboard Pages

## 🏠 Home

Purpose:

Dataset Intelligence Hub

Features:

- Upload CSV
- Dataset Overview
- Dataset Health Check
- Customer Statistics
- Customer Search
- Customer Selection
- Run Analysis

---

## 📊 Overview

Purpose:

Executive Customer Snapshot

Displays:

- Churn Probability
- Confidence Score
- Priority
- Value Score
- Customer Profile
- Segment Information

---

## 📈 Forecast

Purpose:

Future Customer Intelligence

Displays:

- Future Flights
- Future Distance
- Future Points
- Revenue Risk
- Forecast Insights

---

## 🎯 Retention Strategy

Purpose:

Action Recommendation Center

Displays:

- Recommended Actions
- Business Rationale
- Action Roadmap
- Retention Outcome Estimate

---

## 🤖 AI Executive Summary

Purpose:

Management Insights

Displays:

- Executive Summary
- Risk Analysis
- Business Impact
- Retention Strategy
- Manager Recommendation

---

## 💬 Customer Message

Purpose:

Customer Communication Generator

Displays:

- Personalized Customer Message
- Email Draft
- SMS Draft
- Communication Context

---

## 📄 Reports & Export

Purpose:

Download and Reporting Center

Supports:

- Full JSON Report
- Executive Summary
- Customer Communication
- Business Profile Export

---

# 📥 Input Requirements

The system supports:

## Single Customer Dataset

Requirements:

- Exactly 12 months of history

---

## Multi-Customer Dataset

Requirements:

- Customer selection using Loyalty Number
- Exactly 12 months of history per customer

---

# 📤 Outputs

## Business Profile

Example:

```json
{
  "cluster_name": "Premium Frequent Flyers",
  "customer_value": "HIGH",
  "value_score": 88.2,
  "priority": "HIGH",
  "confidence": 96.4
}
```

## AI Business Report

Example:

```json
{
  "executive_summary": "...",
  "risk_analysis": "...",
  "business_impact": "...",
  "customer_message": "..."
}
```

# 📈 Key Business KPIs

The platform tracks:

- Churn Probability
- Customer Lifetime Value (CLV)
- Value Score
- Customer Segment
- Future Flights
- Future Distance
- Future Points
- Estimated Revenue Loss
- Retention Priority
- Customer Confidence Score

---

# 💼 Business Impact

The solution enables airlines to:

- Reduce customer churn
- Increase customer retention
- Improve loyalty program engagement
- Prioritize high-value customers
- Estimate revenue at risk
- Improve marketing efficiency
- Generate executive-ready reports
- Support data-driven business decisions

---

# 🛠 Technology Stack

## Frontend

- Streamlit

## Machine Learning

- TensorFlow
- Keras
- XGBoost
- Scikit-Learn

## Data Processing

- Pandas
- NumPy

## AI

- Qwen 3 8B
- Ollama

## Visualization

- Streamlit Charts

---

# ▶️ Installation

## Clone Repository

```bash
git clone https://github.com/bhandarishikhar7313-cell/Airline-Retention-Intelligence.git
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start Ollama

```bash
ollama run qwen3:8b
```

## Launch Dashboard

```bash
streamlit run Home.py
```

---

# 🔮 Future Enhancements

- PDF Report Generation
- Excel Report Export
- Interactive Plotly Dashboards
- SHAP Explainability
- Real-Time API Deployment
- Cloud Deployment
- Multi-Airline Support
- Customer Cohort Analysis
- Automated Campaign Generation

---

# 👨‍💻 Authors

### Shikhar Bhandari

GitHub:
https://github.com/bhandarishikhar7313-cell

---

### Summer Projects '26

Consulting & Analytics Club  
Indian Institute of Technology Guwahati

---

# ⭐ If you found this project useful, consider giving the repository a star.