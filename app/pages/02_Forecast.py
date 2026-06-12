import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Forecast",
    page_icon="📈",
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

if "business_profile" not in st.session_state:

    st.warning(
        "Please analyze a customer first."
    )

    st.stop()

profile = st.session_state[
    "business_profile"
]

customer_df = st.session_state[
    "selected_customer_df"
]

st.markdown("# 📈 Future Forecast")

st.markdown("""
    <p style="font-size: 1.1em; color: #666;">
    6-Month future value prediction with historical trends
    </p>
""", unsafe_allow_html=True)

st.divider()
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
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Future Flights (6M)</div>
        <div style="font-size: 2.5em; font-weight: bold;">{profile['future_flights']:.0f}</div>
        <div style="font-size: 0.85em; opacity: 0.8; margin-top: 10px;">Expected trips</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Future Distance (6M)</div>
        <div style="font-size: 2.5em; font-weight: bold;">{profile['future_distance']:,.0f}</div>
        <div style="font-size: 0.85em; opacity: 0.8; margin-top: 10px;">km expected</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Future Points (6M)</div>
        <div style="font-size: 2.5em; font-weight: bold;">{profile['future_points']:,.0f}</div>
        <div style="font-size: 0.85em; opacity: 0.8; margin-top: 10px;">Loyalty points</div>
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
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Revenue Loss Risk</div>
        <div style="font-size: 2.5em; font-weight: bold;">${profile['estimated_loss']:,.0f}</div>
        <div style="font-size: 0.85em; opacity: 0.8; margin-top: 10px;">If churn occurs</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("### 📊 Trend Analysis")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### ✈️ Flights Trend")
    if "Total Flights" in customer_df.columns:
        history_flights = customer_df["Total Flights"].tolist()
        months = [f"M{i}" for i in range(1, len(history_flights) + 1)]
        fig, ax = plt.subplots(figsize=(8, 4))
        x = np.arange(len(months))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, history_flights, width, label="Actual", color="#0066FF")
        bars2 = ax.bar([len(months) - 0.5], [profile['future_flights']], width, label="Predicted", color="#8B00FF")
        
        ax.set_xlabel("Month")
        ax.set_ylabel("Flights")
        ax.set_xticks(np.arange(len(months)))
        ax.set_xticklabels(months)
        ax.legend()
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
with col2:
    st.markdown("#### 🌍 Distance Trend (km)")
    if "Distance" in customer_df.columns:
        history_distance = customer_df["Distance"].tolist()
        months = [f"M{i}" for i in range(1, len(history_distance) + 1)]
        fig, ax = plt.subplots(figsize=(8, 4))
        x = np.arange(len(months))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, history_distance, width, label="Actual", color="#0066FF")
        bars2 = ax.bar([len(months) - 0.5], [profile['future_distance']], width, label="Predicted", color="#8B00FF")
        
        ax.set_xlabel("Month")
        ax.set_ylabel("Distance (km)")
        ax.set_xticks(np.arange(len(months)))
        ax.set_xticklabels(months)
        ax.legend()
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
with col3:
    st.markdown("#### ⭐ Points Trend")
    if "Points Accumulated" in customer_df.columns:
        history_points = customer_df["Points Accumulated"].tolist()
        months = [f"M{i}" for i in range(1, len(history_points) + 1)]
        fig, ax = plt.subplots(figsize=(8, 4))
        x = np.arange(len(months))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, history_points, width, label="Actual", color="#0066FF")
        bars2 = ax.bar([len(months) - 0.5], [profile['future_points']], width, label="Predicted", color="#8B00FF")
        
        ax.set_xlabel("Month")
        ax.set_ylabel("Points")
        ax.set_xticks(np.arange(len(months)))
        ax.set_xticklabels(months)
        ax.legend()
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

st.divider()

st.markdown("### 🔮 Forecast Insights")

if profile["future_flights"] > 15:
    insight = f"If the current trend continues, the customer is likely to reduce activity significantly in the next 6 months. Early retention activities can prevent an estimated revenue loss of ${profile['estimated_loss']:,.0f}."
else:
    insight = f"If the current trend continues, the customer is likely to reduce activity significantly in the next 6 months. Early retention activities can prevent an estimated revenue loss of ${profile['estimated_loss']:,.0f}."

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-left: 4px solid #667eea;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
">
    <p style="color: #FFFFFF; font-size: 1em; line-height: 1.6; margin: 0;"><strong>💡 Key Insight:</strong> {insight}</p>
</div>
""", unsafe_allow_html=True)
