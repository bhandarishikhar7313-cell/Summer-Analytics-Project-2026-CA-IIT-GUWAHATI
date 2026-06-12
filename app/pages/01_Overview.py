import streamlit as st

st.set_page_config(
    page_title="Overview",
    page_icon="📊",
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
        "Please analyze a customer first from the Home page."
    )

    st.stop()

profile = st.session_state[
    "business_profile"
]

st.markdown("# 📊 Customer Overview")

st.markdown("""
    <p style="font-size: 1.1em; color: #666;">
    Executive summary of customer risk, value, and loyalty profile
    </p>
""", unsafe_allow_html=True)

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #FF6B6B 0%, #FF4444 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Churn Probability</div>
        <div style="font-size: 2em; font-weight: bold;">{profile['churn_probability']:.2%}</div>
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
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Confidence</div>
        <div style="font-size: 2em; font-weight: bold;">{profile['confidence']:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Priority</div>
        <div style="font-size: 2em; font-weight: bold;">{profile["priority"]}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
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

st.divider()

st.markdown("### 👤 Customer Profile")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-left: 4px solid #667eea;
        padding: 20px;
        border-radius: 8px;
    ">
        <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 10px;font-weight: bold;">🎯 Cluster</h4>
        <p style="font-size: 1.1em; color: #B8D4FF; font-weight: bold; margin: 0;">{profile['cluster_name']}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(67, 233, 123, 0.1) 0%, rgba(56, 249, 215, 0.1) 100%);
        border-left: 4px solid #43e97b;
        padding: 20px;
        border-radius: 8px;
    ">
        <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 10px;font-weight: bold;">💰 Customer Value</h4>
        <p style="font-size: 1.1em; color: #B3FFD4; font-weight: bold; margin: 0;">{profile['customer_value']}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(250, 112, 154, 0.1) 0%, rgba(254, 225, 64, 0.1) 100%);
        border-left: 4px solid #fa709a;
        padding: 20px;
        border-radius: 8px;
    ">
        <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 10px;font-weight: bold;">💵 CLV</h4>
        <p style="font-size: 1.1em; color: #FFD9B3; font-weight: bold; margin: 0;">${profile['clv']:,.0f}</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    card_status = "✅ Active" if profile['loyalty_card'] else "❌ Inactive"
    card_color = "#43e97b" if profile['loyalty_card'] else "#FF6B6B"
    card_bg = "rgba(67, 233, 123, 0.1)" if profile['loyalty_card'] else "rgba(255, 107, 107, 0.1)"
    card_text = "#B3FFD4" if profile['loyalty_card'] else "#FFB3B3"
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {card_bg} 0%, {card_bg} 100%);
        border-left: 4px solid {card_color};
        padding: 20px;
        border-radius: 8px;
    ">
        <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 10px;font-weight: bold;">🎫 Loyalty Card</h4>
        <p style="font-size: 1.1em; color: {card_text}; font-weight: bold; margin: 0;">{card_status}</p>
    </div>
    """, unsafe_allow_html=True)
st.divider()

st.markdown("### 🚨 Customer Status")

priority = profile["priority"]

if priority == "CRITICAL":
    status_html = """
    <div style="
        background: linear-gradient(135deg, #FF6B6B 0%, #FF4444 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 2em; margin-bottom: 10px;">🔴</div>
        <div style="font-size: 1.5em; font-weight: bold;">At Risk Customer</div>
        <div style="font-size: 0.95em; opacity: 0.9; margin-top: 10px;">Immediate intervention recommended</div>
    </div>
    """
elif priority in ["HIGH", "MEDIUM"]:
    status_html = """
    <div style="
        background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 2em; margin-bottom: 10px;">🟡</div>
        <div style="font-size: 1.5em; font-weight: bold;">Monitor Closely</div>
        <div style="font-size: 0.95em; opacity: 0.9; margin-top: 10px;">Proactive engagement required</div>
    </div>
    """
else:
    status_html = """
    <div style="
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 2em; margin-bottom: 10px;">🟢</div>
        <div style="font-size: 1.5em; font-weight: bold;">Healthy Customer</div>
        <div style="font-size: 0.95em; opacity: 0.9; margin-top: 10px;">Continue standard engagement</div>
    </div>
    """

st.markdown(status_html, unsafe_allow_html=True)

st.divider()

st.markdown("### 📋 Segment Analysis")

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-left: 4px solid #667eea;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
">
    <p style="color: #FFFFFF; font-size: 1em; line-height: 1.6; margin: 0;">{profile['profile_segment_description']}</p>
</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("### 💼 Key Customer Information")

col1, col2, col3 = st.columns(3)

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
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Annual Salary</div>
        <div style="font-size: 2em; font-weight: bold;">${profile['salary']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #FF6B6B 0%, #FF4444 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Revenue Loss Risk</div>
        <div style="font-size: 2em; font-weight: bold;">${profile['estimated_loss']:,.0f}</div>
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
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Future Value Segment</div>
        <div style="font-size: 2em; font-weight: bold;">{profile["customer_value"]}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("### ✅ Recommended Actions Preview")

for idx, action in enumerate(profile["recommended_actions"], start=1):
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(67, 233, 123, 0.1) 0%, rgba(56, 249, 215, 0.1) 100%);
        border-left: 4px solid #43e97b;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 10px;
    ">
        <p style="color: #B3FFD4; font-weight: bold; margin: 0;"><span style="color: #FFFFFF;">✅</span> {action}</p>
    </div>
    """, unsafe_allow_html=True)
