import streamlit as st
import pandas as pd

from testing.llm_report import (
    run_pipeline
)

st.set_page_config(
    page_title="Airline Retention Intelligence",
    page_icon="✈️",
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
    
    /* Main container styling */
    .main {
        padding: 20px;
    }
    
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }
    
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    /* Text color for readability */
    p, h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# ✈️ Airline Retention Intelligence Platform")
with col2:
    st.markdown("")

st.markdown("""
    <p style="font-size: 1.1em; color: #B8D4FF;">
    🎯 Predict churn risk, future value, and retention opportunities
    </p>
""", unsafe_allow_html=True)

st.divider()

# Tutorial Section
with st.expander("📚 **How to Use This Platform** (Click to expand)", expanded=False):
    st.markdown("""
    ### 🚀 Quick Start Guide
    
    Follow these 5 simple steps to analyze customer retention:
    
    #### Step 1️⃣: Upload Your Data
    - Click the **Upload** button below
    - Select a CSV file with customer data (12 months of history)
    - The system will analyze the file automatically
    
    #### Step 2️⃣: Select a Customer
    - Use the **Customer Selection** dropdown
    - Choose any customer from your dataset
    - View their complete history
    
    #### Step 3️⃣: Run Analysis
    - Click the **🚀 Analyze Customer** button
    - The AI will process the data (takes 30-60 seconds)
    - Results will appear across all pages
    
    #### Step 4️⃣: Review Insights
    - Navigate through the sidebar pages to see detailed analysis:
      - 📊 **Overview**: Customer profile & churn prediction
      - 📈 **Forecast**: 6-month future predictions
      - 🎯 **Retention Strategy**: Recommended actions to prevent churn
      - 🤖 **AI Summary**: AI-generated business intelligence
      - 💬 **Customer Message**: Email & SMS templates
      - 📄 **Report Export**: Download comprehensive reports
    
    #### Step 5️⃣: Export Results
    - Go to **Reports & Export** page
    - Download PDF reports, JSON data, or communication drafts
    - Share insights with your team
    
    ---
    
    ### 📌 Pro Tips
    - ✅ Ensure your CSV has 12 months of customer history
    - ✅ Required columns: Loyalty Number, CLV, Salary, Total Flights, Distance, Points Accumulated
    - ✅ You can upload a new CSV anytime using the "Upload New CSV" button
    - ✅ All analysis results are saved in your session - no data is lost when switching pages
    """)

with st.expander("🗂️ **Sidebar Navigation Guide** (Click to expand)", expanded=False):
    st.markdown("""
    ### 📋 All Available Pages & Features
    
    **🏠 Home** (Current Page)
    - Upload customer data (CSV)
    - View dataset overview and statistics
    - Select specific customers to analyze
    - Check data quality (missing values, duplicates)
    - Launch AI analysis pipeline
    
    ---
    
    **📊 Overview** 
    - Executive customer profile snapshot
    - **Key Metrics**: Churn Probability, Confidence, Priority, Value Score
    - **Customer Profile**: ID, Name, Gender, Loyalty Card, Cluster, Salary
    - **Customer Value Summary**: Total CLV, Flights, Distance, Points
    - **Churn Risk Gauge**: Visual indicator of churn probability
    - **Key Indicators**: Future flights, distance, points, estimated revenue loss
    - **Recommended Actions**: Top priority retention actions
    - **Business Insights**: AI-generated recommendations
    
    ---
    
    **📈 Forecast**
    - 6-month future value predictions
    - **Top Metrics**: Future CLV, Revenue at Risk, Confidence Score
    - **Visual Charts**: 
      - Future Flights (actual vs predicted)
      - Future Distance (actual vs predicted)
      - Future Points (actual vs predicted)
    - **Forecast Insights**: AI analysis of predictions
    - **Data-Driven**: ML models trained on customer history
    
    ---
    
    **🎯 Retention Strategy**
    - Comprehensive retention action plan
    - **Priority Metrics**: Priority Level, Recommended Actions, Revenue Loss, Expansion Cost, Expected ROI
    - **Recommended Actions**: Detailed list with impact levels (HIGH/MEDIUM/LOW)
    - **Retention Timeline**: 4 phases (Immediate, Short-term, Medium-term, Long-term)
    - **Expected Impact**: Revenue prevention, CLV increase, retention probability, lifetime value
    - **Business Rationale**: Why each action matters for this customer segment
    - **Key Insights**: Strategic recommendations
    
    ---
    
    **🤖 AI Executive Summary**
    - AI-generated business intelligence (5 interactive tabs)
    - **Executive Summary**: Strategic overview with key bullet points
    - **Risk Analysis**: Detailed churn risk factors and warning signs
    - **Retention Strategy**: Recommended approaches tailored to customer
    - **Business Impact**: Expected outcomes and financial implications
    - **Manager Recommendation**: Next steps for your team
    - **Model Confidence**: Score showing prediction reliability
    - 💡 *Powered by advanced LLM analysis*
    
    ---
    
    **💬 Customer Message**
    - Ready-to-use communication templates
    - **Core Message**: Personalized opening statement
    - **Email Draft**: Full email template for sending
    - **SMS Draft**: Short text message (160 characters max)
    - **Download**: Export templates as documents
    - **Context**: Customer profile information for reference
    
    ---
    
    **📄 Reports & Export**
    - Download comprehensive reports and data
    - **Available Exports**:
      - 📊 Complete Analysis Report (JSON)
      - 📋 Executive Summary (PDF)
      - 💬 Customer Messages (PDF)
      - 🗂️ Business Profile Data (JSON)
    - **Features**: 
      - Preview each report before download
      - One-click export to multiple formats
      - Share with stakeholders
    
    ---
    
    ### 🎨 Color Coding Guide
    
    **On Metric Cards & Indicators:**
    - 🟣 **Purple** = Priority/Strategy metrics
    - 🔵 **Cyan** = Confidence/Performance metrics
    - 🟢 **Green** = Positive/Healthy metrics
    - 🔴 **Red** = Risk/Warning metrics
    - 🟠 **Orange** = Growth/Opportunity metrics
    
    **On Status Indicators:**
    - 🟢 **Green** = Good/Active (e.g., Active Loyalty)
    - 🟠 **Orange** = Medium Risk/Caution
    - 🔴 **Red** = Critical/High Risk
    
    ---
    
    ### ⚡ Key Features Summary
    
    | Feature | Purpose | Page |
    |---------|---------|------|
    | Churn Prediction | Predict customer leaving probability | Overview |
    | CLV Forecast | Predict future customer value | Forecast |
    | Risk Analysis | Identify churn factors | AI Summary |
    | Action Plans | Retention recommendations | Retention Strategy |
    | Email Templates | Customer outreach | Customer Message |
    | PDF Reports | Share findings | Report Export |
    | Data Export | Integrate with other tools | Report Export |
    
    """)

st.divider()

if "uploaded_df" not in st.session_state:
    st.markdown("### 📥 Upload Your Data")
    uploaded_file = st.file_uploader(
        "Upload Customer CSV",
        type=["csv"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state["uploaded_df"] = df
        st.success("✅ CSV Loaded Successfully")
        st.rerun()
    else:
        st.info("📌 Upload a CSV file to begin your analysis.")
        st.stop()
else:
    df = st.session_state["uploaded_df"]
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.success("✅ CSV Already Loaded")
    with col2:
        st.write("")
    with col3:
        if st.button("📤 Upload New CSV", width='stretch'):
            del st.session_state["uploaded_df"]
            st.rerun()
rows = len(df)
columns = len(df.columns)

customer_col = None
if "Loyalty Number" in df.columns:
    customer_col = "Loyalty Number"
elif "CustomerID" in df.columns:
    customer_col = "CustomerID"
if customer_col is not None:
    customers = df[customer_col].nunique()
else:
    customers = 1

st.divider()
st.markdown("### 📊 Dataset Overview")
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
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Total Rows</div>
        <div style="font-size: 2.5em; font-weight: bold;">{rows:,}</div>
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
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Columns</div>
        <div style="font-size: 2.5em; font-weight: bold;">{columns}</div>
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
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Unique Customers</div>
        <div style="font-size: 2.5em; font-weight: bold;">{customers}</div>
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
        <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Features</div>
        <div style="font-size: 2.5em; font-weight: bold;">{len(df.columns)}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("### 🏷️ Available Features")
features = df.columns.tolist()
cols = st.columns(4)
for idx, feature in enumerate(features):
    with cols[idx % 4]:
        st.markdown(f"• **{feature}**")

st.divider()

st.markdown("### 👁️ Dataset Preview")

st.dataframe(df.head(), width='stretch')

if (customer_col is not None and customers > 1):
    st.divider()
    
    st.markdown("### 📈 Customer Statistics")

    avg_clv = (
        df["CLV"].mean()
        if "CLV" in df.columns
        else 0
    )

    avg_salary = (
        df["Salary"].mean()
        if "Salary" in df.columns
        else 0
    )

    avg_flights = (
        df["Total Flights"].mean()
        if "Total Flights" in df.columns
        else 0
    )

    avg_distance = (
        df["Distance"].mean()
        if "Distance" in df.columns
        else 0
    )

    avg_points = (
        df["Points Accumulated"].mean()
        if "Points Accumulated" in df.columns
        else 0
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        ">
            <div style="font-size: 0.85em; opacity: 0.9; margin-bottom: 8px;">Avg CLV</div>
            <div style="font-size: 1.8em; font-weight: bold;">${avg_clv:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        ">
            <div style="font-size: 0.85em; opacity: 0.9; margin-bottom: 8px;">Avg Salary</div>
            <div style="font-size: 1.8em; font-weight: bold;">${avg_salary:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        ">
            <div style="font-size: 0.85em; opacity: 0.9; margin-bottom: 8px;">Avg Flights</div>
            <div style="font-size: 1.8em; font-weight: bold;">{avg_flights:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        ">
            <div style="font-size: 0.85em; opacity: 0.9; margin-bottom: 8px;">Avg Distance</div>
            <div style="font-size: 1.8em; font-weight: bold;">{avg_distance:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        ">
            <div style="font-size: 0.85em; opacity: 0.9; margin-bottom: 8px;">Avg Points</div>
            <div style="font-size: 1.8em; font-weight: bold;">{avg_points:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.markdown("### 🔍 Dataset Health")
missing_values = int(df.isnull().sum().sum())
duplicates = int(df.duplicated().sum())
col1, col2 = st.columns(2)

with col1:
    if missing_values == 0:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        ">
            <div style="font-size: 1.2em;">✅ Missing Values</div>
            <div style="font-size: 2.5em; font-weight: bold; margin-top: 10px;">{missing_values}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #FF6B6B 0%, #FF4444 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        ">
            <div style="font-size: 1.2em;">⚠️ Missing Values</div>
            <div style="font-size: 2.5em; font-weight: bold; margin-top: 10px;">{missing_values}</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    if duplicates == 0:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        ">
            <div style="font-size: 1.2em;">✅ Duplicate Rows</div>
            <div style="font-size: 2.5em; font-weight: bold; margin-top: 10px;">{duplicates}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #FF6B6B 0%, #FF4444 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        ">
            <div style="font-size: 1.2em;">⚠️ Duplicate Rows</div>
            <div style="font-size: 2.5em; font-weight: bold; margin-top: 10px;">{duplicates}</div>
        </div>
        """, unsafe_allow_html=True)

if (customer_col is not None and customers > 1):
    st.divider()
    st.markdown("### 👤 Customer Selection")
    selected_customer = st.selectbox(
        f"Select {customer_col}",
        options=sorted(df[customer_col].unique()),
        key="customer_selector"
    )
    st.session_state["selected_customer"] = selected_customer
    customer_df = df[df[customer_col] == selected_customer]
else:
    customer_df = df
    selected_customer = None

st.session_state["selected_customer_df"] = customer_df

st.divider()

st.markdown("### 📍 Selected Customer Details")

if len(customer_df) > 0:

    latest = customer_df.iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if "CLV" in latest:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            ">
                <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">CLV</div>
                <div style="font-size: 2em; font-weight: bold;">${latest['CLV']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if "Salary" in latest:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                color: white;
                padding: 25px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            ">
                <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Salary</div>
                <div style="font-size: 2em; font-weight: bold;">${latest['Salary']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        if "Loyalty Card" in latest:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 25px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            ">
                <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Loyalty Card</div>
                <div style="font-size: 2em; font-weight: bold;">{latest['Loyalty Card']}</div>
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
            <div style="font-size: 0.9em; opacity: 0.9; margin-bottom: 10px;">Records Found</div>
            <div style="font-size: 2em; font-weight: bold;">{len(customer_df)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### Customer History")
    
    st.dataframe(customer_df, width='stretch')

    st.write(f"**Records Found:** {len(customer_df)}")

if st.button("🚀 Analyze Customer", width='stretch'):

        if len(customer_df) != 12:
            st.error("❌ Customer must contain exactly 12 months of history.")
            st.stop()

        with st.spinner("⏳ Running Analysis..."):
            result = run_pipeline(dataframe=customer_df)

        st.session_state["prediction"] = result

        if (isinstance(result, dict) and "business_profile" in result):
            st.session_state["business_profile"] = result["business_profile"]

        if (isinstance(result, dict) and "llm_analysis" in result):
            st.session_state["llm_analysis"] = result["llm_analysis"]

        st.success("✅ Analysis Complete!")
        st.balloons()
        st.rerun()