import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from wordcloud import WordCloud
from textblob import TextBlob
import matplotlib.pyplot as plt

# --- Page configuration ---
st.set_page_config(
    page_title="Data Insights Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Cyber-Tech Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap');
    
    :root {
        --cyber-blue: #00f2ff;
        --cyber-purple: #bc13fe;
        --cyber-bg: #030712;
        --neon-glow: rgba(0, 242, 255, 0.3);
    }

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        color: #e2e8f0;
    }

    /* Animated Cyber Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1e1b4b 0%, #030712 100%);
        background-attachment: fixed;
    }
    
    /* Grid Pattern Overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: linear-gradient(rgba(0, 242, 255, 0.05) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(0, 242, 255, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        z-index: -1;
    }

    /* Main Container */
    .main .block-container {
        padding: 4rem 6% !important;
    }

    /* Cyber Hero Section */
    .hero-container {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 20px;
        padding: 4rem;
        margin-bottom: 4rem;
        text-align: center;
        box-shadow: 0 0 40px rgba(0, 242, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::after {
        content: "";
        position: absolute;
        top: 0; left: -100%; width: 50%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 242, 255, 0.1), transparent);
        animation: scan 4s infinite linear;
    }

    @keyframes scan {
        0% { left: -100%; }
        100% { left: 200%; }
    }

    .main-title {
        font-size: 4.5rem !important;
        font-weight: 700 !important;
        letter-spacing: -3px !important;
        text-transform: uppercase;
        background: linear-gradient(90deg, #00f2ff, #bc13fe);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        filter: drop-shadow(0 0 10px rgba(0, 242, 255, 0.5));
        margin-bottom: 0.5rem !important;
    }
    
    .sub-title {
        color: #94a3b8;
        font-size: 1.4rem;
        letter-spacing: 1px;
    }

    /* Neon Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(0, 242, 255, 0.15) !important;
        padding: 30px !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1) !important;
    }

    div[data-testid="stMetric"]:hover {
        transform: scale(1.05) translateY(-10px);
        border-color: var(--cyber-blue) !important;
        box-shadow: 0 0 30px rgba(0, 242, 255, 0.3) !important;
        background: rgba(15, 23, 42, 0.9) !important;
    }

    div[data-testid="stMetricLabel"] {
        color: var(--cyber-blue) !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        opacity: 0.8;
    }
    
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        text-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }

    /* Cyber Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15, 23, 42, 0.8);
        padding: 12px;
        border-radius: 12px;
        border: 1px solid rgba(0, 242, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #64748b !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        background-color: transparent !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00f2ff22, #bc13fe22) !important;
        color: var(--cyber-blue) !important;
        border-bottom: 2px solid var(--cyber-blue) !important;
    }

    /* Sidebar Fix */
    section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Top Nav Pills Styling */
    div[data-testid="stPills"] {
        background: rgba(15, 23, 42, 0.8) !important;
        padding: 8px !important;
        border-radius: 50px !important;
        border: 1px solid rgba(0, 242, 255, 0.2) !important;
    }
    
    div[data-testid="stPills"] button {
        border-radius: 50px !important;
        border: none !important;
        padding: 10px 25px !important;
        background: transparent !important;
        color: #94a3b8 !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stPills"] button[aria-checked="true"] {
        background: var(--cyber-blue) !important;
        color: #030712 !important;
        box-shadow: 0 0 15px var(--cyber-blue) !important;
    }

    /* Filter Expander Styling */
    .stExpander {
        background: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid rgba(0, 242, 255, 0.1) !important;
        border-radius: 16px !important;
        margin-bottom: 2rem !important;
    }
    
    .stExpander summary {
        color: var(--cyber-blue) !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading Logic ---
@st.cache_data
def load_hospital_data():
    if os.path.exists('hospital_dataset.csv'):
        return pd.read_csv('hospital_dataset.csv')
    return None

@st.cache_data
def load_icecream_data():
    if os.path.exists('icecream_sales.csv'):
        return pd.read_csv('icecream_sales.csv')
    return None

@st.cache_data
def load_coffee_data():
    if os.path.exists('index_1.csv'):
        df = pd.read_csv('index_1.csv')
        # Preprocessing
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['hour'] = df['datetime'].dt.hour
        df['day_name'] = df['datetime'].dt.day_name()
        df['month'] = df['datetime'].dt.month_name()
        df['is_weekend'] = df['datetime'].dt.dayofweek >= 5
        return df
    return None

# --- Text Intelligence Helper ---
def analyze_sentiment(text):
    if not text:
        return 0, 0
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def generate_cyber_wordcloud(data_list, title):
    text = " ".join(str(x) for x in data_list)
    wc = WordCloud(
        width=800, height=400,
        background_color="#030712",
        colormap="cool"
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    fig.patch.set_facecolor('#030712')
    plt.tight_layout(pad=0)
    return fig

# --- Top Navigation Bar ---
nav_col1, nav_col2 = st.columns([1, 2])
with nav_col1:
    st.markdown('<div style="padding-top: 10px;"><span style="font-size: 1.5rem; font-weight: 800; color: #00f2ff; letter-spacing: 2px;">HUB_OS v2.0</span></div>', unsafe_allow_html=True)

with nav_col2:
    dataset_choice = st.pills(
        "SELECT DATA STREAM",
        ["Coffee Sales", "Hospital Analytics", "Ice Cream Sales"],
        default="Coffee Sales",
        label_visibility="collapsed"
    )

st.markdown('<div style="margin-bottom: 2rem; border-bottom: 1px solid rgba(0, 242, 255, 0.1);"></div>', unsafe_allow_html=True)

# --- Main Application Logic ---
if dataset_choice == "Coffee Sales":
    df = load_coffee_data()
    if df is not None:
        st.markdown('''
            <div class="hero-container">
                <h1 class="main-title">☕ Coffee Sales Insights</h1>
                <p class="sub-title">Exploring beverage trends and transaction velocity across your outlets.</p>
            </div>
        ''', unsafe_allow_html=True)

        # Top Filter Bar
        with st.expander("🔍 ADVANCED DATA FILTERS", expanded=True):
            f1, f2 = st.columns(2)
            with f1:
                coffee_types = st.multiselect("Coffee Name", options=df['coffee_name'].unique(), default=df['coffee_name'].unique())
            with f2:
                cash_types = st.multiselect("Payment Type", options=df['cash_type'].unique(), default=df['cash_type'].unique())
        
        filtered_df = df[df['coffee_name'].isin(coffee_types) & df['cash_type'].isin(cash_types)]

        # KPIs
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Revenue", f"${filtered_df['money'].sum():,.2f}")
        c2.metric("Orders", f"{len(filtered_df):,}")
        c3.metric("Top Coffee", f"{filtered_df['coffee_name'].mode()[0]}")
        c4.metric("Avg Order Value", f"${filtered_df['money'].mean():,.2f}")

        st.markdown("---")

        # Charts
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Sales Performance", "⏰ Time Analysis", "🧠 Deep Dive Insights", "🧠 Text Intelligence"])
        
        with tab1:
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Revenue by Coffee Type")
                rev_by_coffee = filtered_df.groupby('coffee_name')['money'].sum().sort_values(ascending=False).reset_index()
                fig1 = px.bar(rev_by_coffee, x='coffee_name', y='money', color='money', 
                             color_continuous_scale="Plasma", labels={'money':'Revenue ($)', 'coffee_name':'Coffee Type'},
                             template='plotly_dark')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col_b:
                st.subheader("Payment Method Split")
                fig2 = px.pie(filtered_df, names='cash_type', values='money', 
                             hole=0.5, color_discrete_sequence=px.colors.sequential.Electric,
                             template='plotly_dark')
                st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown("---")
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.subheader("Transaction Size Distribution")
                fig_box = px.box(filtered_df, y="money", points="all", 
                               template='plotly_dark', color_discrete_sequence=['#00f2ff'])
                st.plotly_chart(fig_box, use_container_width=True)
            
            with col_c2:
                st.subheader("Cumulative Revenue Growth")
                df_sorted = filtered_df.sort_values('datetime')
                df_sorted['cumulative_money'] = df_sorted['money'].cumsum()
                fig_area = px.area(df_sorted, x='datetime', y='cumulative_money',
                                 template='plotly_dark', color_discrete_sequence=['#bc13fe'])
                st.plotly_chart(fig_area, use_container_width=True)

        with tab2:
            st.subheader("Sales Volume by Hour")
            hourly_sales = filtered_df.groupby('hour').size().reset_index(name='Orders')
            fig3 = px.line(hourly_sales, x="hour", y="Orders", markers=True,
                          line_shape='spline', render_mode='svg',
                          template='plotly_dark')
            fig3.update_traces(line_color='#00f2ff', fill='tozeroy', fillcolor='rgba(0, 242, 255, 0.1)')
            st.plotly_chart(fig3, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Weekly Revenue Pattern")
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            weekly_rev = filtered_df.groupby('day_name')['money'].sum().reindex(days_order).reset_index()
            fig4 = px.bar(weekly_rev, x='day_name', y='money', color='money',
                         labels={'day_name':'Day of Week', 'money':'Revenue ($)'},
                         template='plotly_dark', color_continuous_scale="Viridis")
            st.plotly_chart(fig4, use_container_width=True)

        with tab3:
            col_z1, col_z2 = st.columns(2)
            with col_z1:
                st.subheader("Hourly Intensity Heatmap")
                # Heatmap: Day of Week vs Hour
                heatmap_data = filtered_df.groupby(['day_name', 'hour']).size().unstack(fill_value=0)
                heatmap_data = heatmap_data.reindex(days_order)
                fig5 = px.imshow(heatmap_data, labels=dict(x="Hour of Day", y="Day of Week", color="Orders"),
                               x=heatmap_data.columns, y=heatmap_data.index,
                               color_continuous_scale="YlOrRd", template='plotly_white')
                st.plotly_chart(fig5, use_container_width=True)
            
            with col_z2:
                st.subheader("Customer Loyalty Distribution")
                # Count occurrences of Card IDs (excluding empty/cash transactions)
                loyalty_df = filtered_df[filtered_df['card'].notna() & (filtered_df['card'] != '')]
                loyalty_counts = loyalty_df['card'].value_counts().reset_index()
                loyalty_counts.columns = ['Card_ID', 'Purchase_Count']
                fig6 = px.histogram(loyalty_counts, x="Purchase_Count", 
                                   labels={'Purchase_Count':'Visits per Customer'},
                                   nbins=20, template='plotly_dark', color_discrete_sequence=['#10b981'])
                fig6.update_layout(bargap=0.1)
                st.plotly_chart(fig6, use_container_width=True)
                st.info("💡 Most customers visit 1-3 times, but look at the tail for loyal regulars!")

        with tab4:
            st.subheader("Coffee Type Semantic Analysis")
            fig_wc = generate_cyber_wordcloud(filtered_df['coffee_name'], "Coffee Preferences")
            st.pyplot(fig_wc)
            
            st.markdown("---")
            st.subheader("Feedback Sentiment Simulator")
            user_text = st.text_area("Input Sample Feedback (e.g., 'The latte was amazing!')", height=100)
            if user_text:
                pol, subj = analyze_sentiment(user_text)
                c1, c2 = st.columns(2)
                c1.metric("Polarity (Sentiment)", f"{pol:.2f}", delta="Positive" if pol > 0 else "Negative")
                c2.metric("Subjectivity", f"{subj:.2f}")
                st.progress((pol + 1) / 2)
                st.caption("Scale: -1 (Negative) to 1 (Positive)")

    else:
        st.error("Coffee Sales dataset (index_1.csv) not found.")

elif dataset_choice == "Hospital Analytics":
    df = load_hospital_data()
    if df is not None:
        st.markdown('''
            <div class="hero-container">
                <h1 class="main-title">🏥 Hospital Care Metrics</h1>
                <p class="sub-title">Detailed analysis of patient throughput, recovery rates, and operational efficiency.</p>
            </div>
        ''', unsafe_allow_html=True)

        # Top Filter Bar
        with st.expander("🔍 PATIENT DATA FILTERS", expanded=True):
            f1, f2 = st.columns(2)
            with f1:
                depts = st.multiselect("Department", options=df['Department'].unique(), default=df['Department'].unique())
            with f2:
                diseases = st.multiselect("Disease", options=df['Disease'].unique(), default=df['Disease'].unique())
        
        filtered_df = df[df['Department'].isin(depts) & df['Disease'].isin(diseases)]

        # KPIs
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Patients", f"{len(filtered_df)}")
        c2.metric("Avg Cost", f"${filtered_df['Treatment_Cost'].mean():,.0f}")
        c3.metric("Avg Recovery", f"{filtered_df['Recovery_Score'].mean():.1f}%")
        c4.metric("Avg Length of Stay", f"{filtered_df['Days_Admitted'].mean():.1f} days")

        st.markdown("---")

        # Charts
        tab1, tab2, tab3 = st.tabs(["📊 Performance Overview", "🧬 Patient Correlations", "🧠 Text Intelligence"])
        
        with tab1:
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Patients by Department")
                fig1 = px.bar(filtered_df.groupby('Department').size().reset_index(name='Count'), 
                             x='Department', y='Count', color='Department', 
                             template='plotly_dark', color_discrete_sequence=px.colors.sequential.Electric)
                st.plotly_chart(fig1, use_container_width=True)
            
            with col_b:
                st.subheader("Treatment Cost by Disease")
                fig2 = px.pie(filtered_df, names='Disease', values='Treatment_Cost', 
                             hole=0.4, template='plotly_dark', color_discrete_sequence=px.colors.sequential.Plasma)
                st.plotly_chart(fig2, use_container_width=True)

        with tab2:
            st.subheader("Age vs Recovery Score (Sized by Cost)")
            fig3 = px.scatter(filtered_df, x="Age", y="Recovery_Score", 
                             size="Treatment_Cost", color="Department",
                             hover_name="Patient_Name", log_x=False, size_max=40,
                             template='plotly_dark', color_discrete_sequence=px.colors.qualitative.Alphabet,
                             trendline="ols")
            st.plotly_chart(fig3, use_container_width=True)
            
            st.markdown("---")
            col_h1, col_h2 = st.columns(2)
            with col_h1:
                st.subheader("Recovery Score Benchmarking")
                fig_box_h = px.box(filtered_df, x="Department", y="Recovery_Score", color="Department",
                                 template='plotly_dark')
                st.plotly_chart(fig_box_h, use_container_width=True)
            
            with col_h2:
                st.subheader("Hospital Hierarchy: Costs")
                fig_sun = px.sunburst(filtered_df, path=['Department', 'Disease'], values='Treatment_Cost',
                                   color='Recovery_Score', template='plotly_dark',
                                   color_continuous_scale='RdYlGn')
                st.plotly_chart(fig_sun, use_container_width=True)

        with tab3:
            st.subheader("Diagnostic Term Cloud (Diseases)")
            fig_wc_h = generate_cyber_wordcloud(filtered_df['Disease'], "Disease Prevalence")
            st.pyplot(fig_wc_h)
            
            st.markdown("---")
            st.subheader("Patient Symptom Analysis (Simulator)")
            patient_notes = st.text_area("Enter Patient Feedback or Treatment Notes", height=100)
            if patient_notes:
                pol, subj = analyze_sentiment(patient_notes)
                st.write(f"**Health Sentiment Index:** {'Positive' if pol > 0 else 'Critical/Negative'}")
                st.metric("Polarity", f"{pol:.2f}")
                st.progress((pol + 1) / 2)

    else:
        st.error("Hospital dataset not found.")

elif dataset_choice == "Ice Cream Sales":
    df = load_icecream_data()
    if df is not None:
        st.markdown('''
            <div class="hero-container">
                <h1 class="main-title">🍦 Ice Cream Performance</h1>
                <p class="sub-title">Seasonality patterns, flavor demand, and marketing ROI analysis.</p>
            </div>
        ''', unsafe_allow_html=True)

        # Top Filter Bar
        with st.expander("🔍 MARKET FILTERS", expanded=True):
            f1, f2 = st.columns(2)
            with f1:
                flavors = st.multiselect("Flavor", options=df['Flavor'].unique(), default=df['Flavor'].unique())
            with f2:
                regions = st.multiselect("Region", options=df['Region'].unique(), default=df['Region'].unique())
        
        filtered_df = df[df['Flavor'].isin(flavors) & df['Region'].isin(regions)]

        # KPIs
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.0f}")
        c2.metric("Units Sold", f"{filtered_df['Units_Sold'].sum():,}")
        c3.metric("Avg Rating", f"⭐ {filtered_df['Customer_Rating'].mean():.1f}")
        c4.metric("ROI (Rev/Spend)", f"{filtered_df['Revenue'].sum()/filtered_df['Marketing_Spend'].sum():.2f}x")

        st.markdown("---")

        # Charts
        tab1, tab2, tab3 = st.tabs(["🍦 Market Performance", "🌡️ Temperature Correlation", "🧠 Text Intelligence"])
        
        with tab1:
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Revenue by Month")
                fig1 = px.line(filtered_df.groupby('Month')['Revenue'].sum().reset_index(), 
                               x='Month', y='Revenue', markers=True, template='plotly_dark')
                fig1.update_traces(line_color='#bc13fe', marker=dict(size=10, color='#00f2ff'))
                st.plotly_chart(fig1, use_container_width=True)
            
            with col_b:
                st.subheader("Top Flavors by Units Sold")
                fig2 = px.bar(filtered_df.groupby('Flavor')['Units_Sold'].sum().sort_values(ascending=False).reset_index(), 
                             x='Flavor', y='Units_Sold', color='Flavor', template='plotly_dark',
                             color_discrete_sequence=px.colors.sequential.Agsunset)
                st.plotly_chart(fig2, use_container_width=True)

        with tab2:
            st.subheader("Temperature vs Units Sold")
            fig3 = px.scatter(filtered_df, x="Temperature", y="Units_Sold", 
                             trendline="ols", color="Season",
                             hover_data=["Flavor", "Revenue"],
                             template='plotly_dark', color_discrete_sequence=px.colors.qualitative.G10)
            st.plotly_chart(fig3, use_container_width=True)
            
            st.markdown("---")
            col_i1, col_i2 = st.columns(2)
            with col_i1:
                st.subheader("Marketing Efficiency (ROI)")
                fig_bubble = px.scatter(filtered_df, x="Marketing_Spend", y="Revenue",
                                      size="Units_Sold", color="Flavor",
                                      hover_name="Flavor", template='plotly_dark',
                                      size_max=60)
                st.plotly_chart(fig_bubble, use_container_width=True)
            
            with col_i2:
                st.subheader("Customer Satisfaction by Flavor")
                fig_box_i = px.box(filtered_df, x="Flavor", y="Customer_Rating", color="Flavor",
                                 template='plotly_dark')
                st.plotly_chart(fig_box_i, use_container_width=True)

        with tab3:
            st.subheader("Flavor Popularity Cloud")
            fig_wc_i = generate_cyber_wordcloud(filtered_df['Flavor'], "Flavor Insights")
            st.pyplot(fig_wc_i)
            
            st.markdown("---")
            st.subheader("Flavor Review Sentiment")
            flavor_review = st.text_area("Simulate a Flavor Review", height=100)
            if flavor_review:
                pol, subj = analyze_sentiment(flavor_review)
                st.metric("Sentiment Score", f"{pol:.2f}")
                st.progress((pol + 1) / 2)

    else:
        st.error("Ice cream dataset not found.")

# --- Raw Data Expander ---
with st.expander("📂 View Raw Data"):
    if 'filtered_df' in locals():
        st.write(filtered_df)
    else:
        st.write("No data loaded.")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.8rem;">
    Powered by Streamlit & Plotly | Data Insights Hub v2.0 | Advanced Analytics Enabled
</div>
""", unsafe_allow_html=True)
