import streamlit as st
import json
import pandas as pd

st.set_page_config(
    page_title="Reports & Export",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #16213e 50%, #0f3460 100%);
        background-attachment: fixed;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0f1419 0%, #1a2332 100%);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(135deg, #0f1419 0%, #1a2332 100%);
    }
    
    .main {
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

if "prediction" not in st.session_state:
    st.warning("Please analyze a customer first.")
    st.stop()
result = st.session_state["prediction"]
profile = st.session_state["business_profile"]
analysis = st.session_state["llm_analysis"]

st.markdown("# 📄 Reports & Export")

st.markdown("""
    <p style="font-size: 1.1em; color: #666;">
    Download customer intelligence reports and AI insights
    </p>
""", unsafe_allow_html=True)

st.divider()
st.markdown("### 📊 Report Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Priority Level</div>
        <div style="font-size: 2em; font-weight: bold;">{profile["priority"]}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Value Score</div>
        <div style="font-size: 2em; font-weight: bold;">{profile["value_score"]}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Confidence</div>
        <div style="font-size: 2em; font-weight: bold;">{profile['confidence']:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Estimated Loss</div>
        <div style="font-size: 2em; font-weight: bold;">${profile['estimated_loss']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("### 📥 Download Full Report")
col1, col2 = st.columns(2)
with col1:
    json_report = json.dumps(result, indent=4)
    st.download_button(
        label="⬇️ Download JSON Report",
        data=json_report,
        file_name="customer_report.json",
        mime="application/json",
        width="stretch"
    )

with col2:
    st.markdown("<p style='text-align: center; color: #666; font-size: 0.9em;'>Complete analysis in JSON format</p>", unsafe_allow_html=True)

st.divider()
st.markdown("### 📋 Executive Summary")
executive_text = f"""
EXECUTIVE SUMMARY

{analysis['executive_summary']}

RISK ANALYSIS

{analysis['risk_analysis']}

BUSINESS IMPACT

{analysis['business_impact']}

MANAGER RECOMMENDATION

{analysis.get('manager_recommendation', '')}
"""

st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-left: 4px solid #667eea;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 15px;
">
</div>
""", unsafe_allow_html=True)

st.text_area(
    "Preview",
    executive_text,
    height=300
)
col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="⬇️ Download Executive Summary",
        data=executive_text,
        file_name="executive_summary.txt",
        mime="text/plain",
        width="stretch"
    )

with col2:
    st.markdown("<p style='text-align: center; color: #666; font-size: 0.9em;'>Manager insights and recommendations</p>", unsafe_allow_html=True)

st.divider()

st.markdown("### 💬 Customer Communication")

customer_message = analysis["customer_message"]

st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(67, 233, 123, 0.1) 0%, rgba(56, 249, 215, 0.1) 100%);
    border-left: 4px solid #43e97b;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 15px;
">
</div>
""", unsafe_allow_html=True)

st.text_area(
    "Customer Message",
    customer_message,
    height=200
)
col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="⬇️ Download Customer Message",
        data=customer_message,
        file_name="customer_message.txt",
        mime="text/plain",
        width="stretch"
    )

with col2:
    st.markdown("<p style='text-align: center; color: #666; font-size: 0.9em;'>Personalized message for customer</p>", unsafe_allow_html=True)

st.divider()

st.markdown("### 👤 Business Profile")

profile_json = json.dumps(profile, indent=4)

st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%);
    border-left: 4px solid #4facfe;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 15px;
">
</div>
""", unsafe_allow_html=True)

st.text_area(
    "Business Profile JSON",
    profile_json,
    height=250
)

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="⬇️ Download Business Profile",
        data=profile_json,
        file_name="business_profile.json",
        mime="application/json",
        width="stretch"
    )

with col2:
    st.markdown("<p style='text-align: center; color: #666; font-size: 0.9em;'>Complete customer profile data</p>", unsafe_allow_html=True)