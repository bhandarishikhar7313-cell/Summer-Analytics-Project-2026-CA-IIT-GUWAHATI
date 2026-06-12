import streamlit as st

st.set_page_config(
    page_title="Retention Strategy",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
    <style>
    /* Beautiful dark navy/black background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #16213e 50%, #0f3460 100%);
        background-attachment: fixed;
    }
    
    /* Contrast dark sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0f1419 0%, #1a2332 100%);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(135deg, #0f1419 0%, #1a2332 100%);
    }
    
    .main {
        padding: 20px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 0.9em;
        opacity: 0.9;
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

st.markdown("# 🎯 Retention Strategy")

st.markdown("""
    <p style="font-size: 1.1em; color: #666;">
    Recommended actions and expected impact
    </p>
""", unsafe_allow_html=True)

st.divider()
col1, col2, col3, col4, col5 = st.columns(5)
priority = profile["priority"]

with col1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #FF6B6B 0%, #FF4444 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 2em; margin-bottom: 10px;">🚨</div>
        <div style="font-size: 0.8em; opacity: 0.9; margin-bottom: 10px;">Priority Level</div>
        <div style="font-size: 1.5em; font-weight: bold;">{priority}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    action_count = len(profile["recommended_actions"])
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 2em; margin-bottom: 10px;">✅</div>
        <div style="font-size: 0.8em; opacity: 0.9; margin-bottom: 10px;">Recommended Actions</div>
        <div style="font-size: 1.5em; font-weight: bold;">{action_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #FF6B6B 0%, #FF4444 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 2em; margin-bottom: 10px;">💰</div>
        <div style="font-size: 0.8em; opacity: 0.9; margin-bottom: 10px;">Expected Revenue Loss</div>
        <div style="font-size: 1.5em; font-weight: bold;">${profile['estimated_loss']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    expansion_cost = profile['estimated_loss'] * 0.1
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 2em; margin-bottom: 10px;">💵</div>
        <div style="font-size: 0.8em; opacity: 0.9; margin-bottom: 10px;">Expansion Cost</div>
        <div style="font-size: 1.5em; font-weight: bold;">${expansion_cost:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    roi = profile['estimated_loss'] / (expansion_cost + 1)
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 2em; margin-bottom: 10px;">📊</div>
        <div style="font-size: 0.8em; opacity: 0.9; margin-bottom: 10px;">Expected ROI</div>
        <div style="font-size: 1.5em; font-weight: bold;">{roi:.2f}x</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("### ✅ Recommended Actions")
for idx, action in enumerate(profile["recommended_actions"], start=1):
    # Determine impact level based on action
    if idx == 1:
        impact = "🟥 HIGH IMPACT"
        impact_color = "#FF4444"
        cost = profile['estimated_loss'] * 0.4
    elif idx == 2:
        impact = "🟧 MEDIUM IMPACT"
        impact_color = "#FFA500"
        cost = profile['estimated_loss'] * 0.3
    elif idx == 3:
        impact = "🟨 MEDIUM IMPACT"
        impact_color = "#FFD700"
        cost = profile['estimated_loss'] * 0.2
    else:
        impact = "🟨 LOW IMPACT"
        impact_color = "#FFFF00"
        cost = profile['estimated_loss'] * 0.1
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-left: 4px solid {impact_color};
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0 0 8px 0; color: #FFFFFF; font-weight: bold; font-size: 1.2em;">✅ {action}</h4>
                <p style="margin: 0; color: #E0E0E0; font-size: 0.9em;">Action {idx} of {len(profile['recommended_actions'])}</p>
            </div>
            <div style="text-align: right;">
                <div style="
                    background-color: {impact_color};
                    color: white;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-weight: bold;
                    margin-bottom: 8px;
                    font-size: 0.85em;
                ">{impact}</div>
                <div style="
                    font-size: 1.2em;
                    font-weight: bold;
                    color: #667eea;
                ">${cost:,.0f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("### 📅 Retention Timeline")
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin: 30px 0;">
    <div style="text-align: center; flex: 1;">
        <div style="width: 20px; height: 20px; background-color: #00FF00; border-radius: 50%; margin: 0 auto; margin-bottom: 10px;"></div>
        <b>Immediate</b><br/>0 - 7 Days
    </div>
    <div style="flex: 1; height: 3px; background: linear-gradient(to right, #00FF00, #FFFF00);"></div>
    <div style="text-align: center; flex: 1;">
        <div style="width: 20px; height: 20px; background-color: #FFFF00; border-radius: 50%; margin: 0 auto; margin-bottom: 10px;"></div>
        <b>Short Term</b><br/>1 - 4 Weeks
    </div>
    <div style="flex: 1; height: 3px; background: linear-gradient(to right, #FFFF00, #9966FF);"></div>
    <div style="text-align: center; flex: 1;">
        <div style="width: 20px; height: 20px; background-color: #9966FF; border-radius: 50%; margin: 0 auto; margin-bottom: 10px;"></div>
        <b>Medium Term</b><br/>1 - 3 Months
    </div>
    <div style="flex: 1; height: 3px; background: linear-gradient(to right, #9966FF, #6B5BFF);"></div>
    <div style="text-align: center; flex: 1;">
        <div style="width: 20px; height: 20px; background-color: #6B5BFF; border-radius: 50%; margin: 0 auto; margin-bottom: 10px;"></div>
        <b>Long Term</b><br/>3 - 6 Months
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()
st.markdown("### 📊 Expected Impact")
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
        <div style="font-size: 2.5em; font-weight: bold; margin: 15px 0;">📉</div>
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Prevent Revenue Loss</div>
        <div style="font-size: 1.8em; font-weight: bold;">${profile['estimated_loss']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    clv_increase = profile['estimated_loss'] * 0.51
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 2.5em; font-weight: bold; margin: 15px 0;">💎</div>
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Increase in CLV</div>
        <div style="font-size: 1.8em; font-weight: bold;">${clv_increase:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    retention_prob = 1 - (profile['churn_probability'] * 0.5)
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 2.5em; font-weight: bold; margin: 15px 0;">📈</div>
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Retention Probability</div>
        <div style="font-size: 1.8em; font-weight: bold;">{retention_prob:.0%}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    lifetime_value = profile['estimated_loss'] * 1.5
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 2.5em; font-weight: bold; margin: 15px 0;">🎯</div>
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Customer Lifetime Value</div>
        <div style="font-size: 1.8em; font-weight: bold;">${lifetime_value:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("### 🎯 Business Rationale")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-left: 4px solid #667eea;
        padding: 20px;
        border-radius: 8px;
    ">
        <h4 style="color: #FFFFFF; margin-top: 0; font-weight: bold;">👥 Customer Segment</h4>
        <p style="font-size: 1.1em; color: #B8D4FF; font-weight: bold; margin: 0;">{profile['cluster_name']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(255, 68, 68, 0.1) 100%);
        border-left: 4px solid #FF6B6B;
        padding: 20px;
        border-radius: 8px;
        margin-top: 15px;
    ">
        <h4 style="color: #FFFFFF; margin-top: 0; font-weight: bold;">⚠️ Churn Risk</h4>
        <p style="font-size: 1.1em; color: #FFB3B3; font-weight: bold; margin: 0;">{profile['churn_probability']:.2%}</p>
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
        <h4 style="color: #FFFFFF; margin-top: 0; font-weight: bold;">💎 Customer Value</h4>
        <p style="font-size: 1.1em; color: #B3FFD4; font-weight: bold; margin: 0;">{profile['customer_value']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%);
        border-left: 4px solid #4facfe;
        padding: 20px;
        border-radius: 8px;
        margin-top: 15px;
    ">
        <h4 style="color: #FFFFFF; margin-top: 0; font-weight: bold;">🎯 Priority</h4>
        <p style="font-size: 1.1em; color: #B3E5FF; font-weight: bold; margin: 0;">{profile['priority']}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.info("""
💡 **Key Insight:** Early intervention can significantly improve retention outcomes. Focus on immediate actions within the next 7 days to prevent customer churn and maximize lifetime value.
""")
    
