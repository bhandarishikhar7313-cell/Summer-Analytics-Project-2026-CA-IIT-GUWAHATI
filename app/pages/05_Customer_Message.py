import streamlit as st

st.set_page_config(
    page_title="Customer Message",
    page_icon="💬",
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

if "llm_analysis" not in st.session_state:

    st.warning(
        "Please analyze a customer first."
    )

    st.stop()

analysis = st.session_state[
    "llm_analysis"
]

st.markdown("# 💬 Customer Communication")

st.markdown("""
    <p style="font-size: 1.1em; color: #666;">
    AI-generated personalized customer communication drafts
    </p>
""", unsafe_allow_html=True)

st.divider()

message = analysis["customer_message"]

st.markdown("### 📝 Core Message")

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, rgba(67, 233, 123, 0.1) 0%, rgba(56, 249, 215, 0.1) 100%);
    border-left: 4px solid #43e97b;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
">
    <p style="color: #FFFFFF; font-size: 1em; line-height: 1.8; margin: 0;">{message}</p>
</div>
""", unsafe_allow_html=True)

st.divider()
st.markdown("### ✉️ Email Draft")
email_text = f"""
Dear Customer,

{message}

Thank you for your continued loyalty.

Best Regards,
Airline Customer Success Team
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
    "Email Content",
    email_text,
    height=250,
    disabled=True
)
col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="⬇️ Download Email",
        data=email_text,
        file_name="customer_email.txt",
        mime="text/plain",
        width="stretch"
    )

with col2:
    st.markdown("<p style='text-align: center; color: #666; font-size: 0.9em;'>Professional email format</p>", unsafe_allow_html=True)

st.divider()

st.markdown("### 📱 SMS Draft")

sms = message[:160]

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
    "SMS Content (160 chars)",
    sms,
    height=100,
    disabled=True
)
col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="⬇️ Download SMS",
        data=sms,
        file_name="customer_sms.txt",
        mime="text/plain",
        width="stretch"
    )

with col2:
    st.markdown(f"<p style='text-align: center; color: #666; font-size: 0.9em;'>{len(sms)} / 160 characters</p>", unsafe_allow_html=True)

if "business_profile" in st.session_state:
    profile = st.session_state["business_profile"]
    st.divider()
    st.markdown("### 🎯 Communication Context")
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
            <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Customer Value</div>
            <div style="font-size: 2em; font-weight: bold;">{profile["customer_value"]}</div>
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
