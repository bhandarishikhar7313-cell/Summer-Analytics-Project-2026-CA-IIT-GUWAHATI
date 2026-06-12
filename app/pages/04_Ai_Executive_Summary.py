import streamlit as st

st.set_page_config(
    page_title="AI Executive Summary",
    page_icon="🤖",
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
    st.warning("Please analyze a customer first.")
    st.stop()

analysis = st.session_state["llm_analysis"]
profile = st.session_state.get("business_profile", {})

st.markdown("# 🤖 AI Executive Summary")
st.markdown("""
    <p style="font-size: 1.1em; color: #B8D4FF;">
    AI-generated business analysis and recommendations
    </p>
""", unsafe_allow_html=True)

# Create tabs for different analysis sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Executive Summary", "Risk Analysis", "Retention Strategy", "Business Impact", "Manager Recommendation"]
)

with tab1:
    col1, col2 = st.columns([3, 1], gap="large")
    with col1:
        st.markdown("#### Executive Summary")
        summary_text = analysis.get('executive_summary', '')
        for line in summary_text.split('\n'):
            line = line.strip()
            if line:
                st.markdown(f"""
                <div style="display: flex; align-items: flex-start; margin-bottom: 12px;">
                    <span style="color: #43e97b; margin-right: 10px; font-size: 1.2em;">✓</span>
                    <span style="color: #FFFFFF; line-height: 1.5;">{line}</span>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <div style="font-size: 4em;">🤖</div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([3, 1], gap="large")
    
    with col1:
        st.markdown("#### Risk Analysis")
        risk_text = analysis.get('risk_analysis', '')
        for line in risk_text.split('\n'):
            line = line.strip()
            if line:
                st.markdown(f"""
                <div style="display: flex; align-items: flex-start; margin-bottom: 12px;">
                    <span style="color: #FF6B6B; margin-right: 10px; font-size: 1.2em;">⚠️</span>
                    <span style="color: #FFFFFF; line-height: 1.5;">{line}</span>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(255, 68, 68, 0.2) 100%);
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <div style="font-size: 4em;">⚡</div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    col1, col2 = st.columns([3, 1], gap="large")
    
    with col1:
        st.markdown("#### Retention Strategy")
        strategy_text = analysis.get('retention_strategy', '')
        for line in strategy_text.split('\n'):
            line = line.strip()
            if line:
                st.markdown(f"""
                <div style="display: flex; align-items: flex-start; margin-bottom: 12px;">
                    <span style="color: #43e97b; margin-right: 10px; font-size: 1.2em;">✓</span>
                    <span style="color: #FFFFFF; line-height: 1.5;">{line}</span>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(67, 233, 123, 0.2) 0%, rgba(56, 249, 215, 0.2) 100%);
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <div style="font-size: 4em;">📈</div>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    col1, col2 = st.columns([3, 1], gap="large")
    
    with col1:
        st.markdown("#### Business Impact")
        impact_text = analysis.get('business_impact', '')
        for line in impact_text.split('\n'):
            line = line.strip()
            if line:
                st.markdown(f"""
                <div style="display: flex; align-items: flex-start; margin-bottom: 12px;">
                    <span style="color: #4facfe; margin-right: 10px; font-size: 1.2em;">💼</span>
                    <span style="color: #FFFFFF; line-height: 1.5;">{line}</span>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(79, 172, 254, 0.2) 0%, rgba(0, 242, 254, 0.2) 100%);
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <div style="font-size: 4em;">💎</div>
        </div>
        """, unsafe_allow_html=True)

with tab5:
    if "manager_recommendation" in analysis:
        col1, col2 = st.columns([3, 1], gap="large")
        
        with col1:
            st.markdown("#### Manager Recommendation")
            rec_text = analysis.get('manager_recommendation', '')
            for line in rec_text.split('\n'):
                line = line.strip()
                if line:
                    st.markdown(f"""
                    <div style="display: flex; align-items: flex-start; margin-bottom: 12px;">
                        <span style="color: #fa709a; margin-right: 10px; font-size: 1.2em;">👨‍💼</span>
                        <span style="color: #FFFFFF; line-height: 1.5;">{line}</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(250, 112, 154, 0.2) 0%, rgba(254, 225, 64, 0.2) 100%);
                border-radius: 12px;
                padding: 30px;
                text-align: center;
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                <div style="font-size: 4em;">🎯</div>
            </div>
            """, unsafe_allow_html=True)

st.divider()

if profile:
    st.markdown("### 🎯 Model Confidence")
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    ">
        <div style="font-size: 0.95em; opacity: 0.9; margin-bottom: 15px;">Prediction Confidence Score</div>
        <div style="font-size: 3em; font-weight: bold;">{profile.get('confidence', 0):.2f}%</div>
        <div style="font-size: 0.9em; opacity: 0.8; margin-top: 15px;">High confidence in model predictions</div>
    </div>
    """, unsafe_allow_html=True)
