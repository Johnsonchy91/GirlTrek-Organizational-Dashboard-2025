import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="GirlTREK Organizational Dashboard 2025",
    page_icon="🚶‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Color scheme from brand guidelines
primary_blue = "#2B4C8C"
primary_orange = "#F37726"
primary_yellow = "#FBCD50"
secondary_blue = "#6CACE4"
secondary_orange = "#F68B1E"
secondary_teal = "#00A895"
secondary_beige = "#F8F3E6"
secondary_gold = "#D4A900"
secondary_white = "#FFFFFF"
secondary_gray = "#6B7280"

# Custom CSS
st.markdown(f"""
<style>
    /* Main header styling */
    .main-header {{
        background-color: {primary_blue};
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }}
    
    /* Metric card styling */
    .metric-card {{
        background-color: {secondary_beige};
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    .metric-title {{
        color: {primary_blue};
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}
    
    .metric-value {{
        color: {primary_orange};
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }}
    
    /* Section headers */
    .section-title {{
        color: {primary_blue};
        border-bottom: 3px solid {primary_orange};
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: {secondary_beige};
        color: {primary_blue};
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        font-weight: 600;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {primary_orange};
        color: white;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🚶‍♀️ GirlTREK Organizational Dashboard 2025</h1>
    <p style="font-size: 18px; margin-top: 10px;">Empowering Black Women to Walk for Better Health</p>
</div>
""", unsafe_allow_html=True)

# Helper function for status badges
def status_badge(status):
    if status == "On Track":
        return f'<span style="background-color: #28a745; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px;">{status}</span>'
    elif status == "At Risk":
        return f'<span style="background-color: #dc3545; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px;">{status}</span>'
    else:
        return f'<span style="background-color: #ffc107; color: black; padding: 4px 12px; border-radius: 20px; font-size: 12px;">{status}</span>'

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Executive Summary", "👥 Recruitment & Engagement", "💰 Development", "📱 Marketing", "❤️ Impact & Member Care"])

with tab1:
    st.markdown('<h3 class="section-title">Executive Summary</h3>', unsafe_allow_html=True)
    
    # Strategic goals overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">NEW MEMBERS RECRUITED</p>'
            f'<p class="metric-value">15,438</p>'
            f'<p>Goal: 100,000 (15.44%)</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">MEMBERS ENGAGED</p>'
            f'<p class="metric-value">13,119</p>'
            f'<p>Goal: 250,000 (5.25%)</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL FUNDS RAISED</p>'
            f'<p class="metric-value">$3.1M</p>'
            f'<p>Goal: $10M (31.09%)</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Additional key metrics
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">WALKING AT LIFE-SAVING LEVEL</p>'
            f'<p class="metric-value">5,634</p>'
            f'<p>Goal: 65,000 (8.67%)</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with col5:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">CARE VILLAGE REACHED</p>'
            f'<p class="metric-value">3,055</p>'
            f'<p>Goal: 40,000 (7.64%)</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with col6:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">ADVOCACY PARTNERS</p>'
            f'<p class="metric-value">2</p>'
            f'<p>Goal: 20 (10%)</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Progress visualization
    st.markdown('<h4>Annual Progress by Goal</h4>', unsafe_allow_html=True)
    
    goals_data = {
        'Goal': ['New Members', 'Members Engaged', 'Life-Saving Level', 'Advocacy Partners', 'Funds Raised', 'Care Village'],
        'Progress': [15.44, 5.25, 8.67, 10.00, 31.09, 7.64],
        'Target': [100, 100, 100, 100, 100, 100]
    }
    df_goals = pd.DataFrame(goals_data)
    
    fig_goals = go.Figure()
    
    fig_goals.add_trace(go.Bar(
        x=df_goals['Goal'],
        y=df_goals['Progress'],
        name='Current Progress',
        marker_color=primary_blue,
        text=df_goals['Progress'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside'
    ))
    
    fig_goals.add_trace(go.Bar(
        x=df_goals['Goal'],
        y=df_goals['Target'] - df_goals['Progress'],
        name='Remaining',
        marker_color=secondary_beige,
        text=''
    ))
    
    fig_goals.update_layout(
        barmode='stack',
        yaxis_title='Progress (%)',
        xaxis_title='Strategic Goals',
        height=400,
        showlegend=True,
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(fig_goals, use_container_width=True)
    
    # Member demographics
    col7, col8 = st.columns(2)
    
    with col7:
        st.markdown('<h4>Top 5 States by Membership</h4>', unsafe_allow_html=True)
        states_data = {
            'State': ['Texas', 'Georgia', 'California', 'New York', 'Florida'],
            'Members': [89043, 84799, 77919, 66670, 64880]
        }
        df_states = pd.DataFrame(states_data)
        
        fig_states = px.bar(df_states, x='State', y='Members',
                           color='Members',
                           color_continuous_scale=[primary_blue, primary_orange])
        fig_states.update_layout(
            showlegend=False,
            height=350,
            title_font=dict(color=primary_blue)
        )
        st.plotly_chart(fig_states, use_container_width=True)
    
    with col8:
        st.markdown('<h4>Membership by Age Group</h4>', unsafe_allow_html=True)
        age_data = {
            'Age Group': ['18-24', '25-34', '35-49', '50-64', '65+'],
            'Members': [1739, 16515, 82893, 164106, 108669]
        }
        df_age = pd.DataFrame(age_data)
        
        fig_age = px.pie(df_age, values='Members', names='Age Group',
                        color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, 
                                               secondary_blue, secondary_orange])
        fig_age.update_traces(textposition='inside', textinfo='percent+label')
        fig_age.update_layout(
            height=350,
            title_font=dict(color=primary_blue)
        )
        st.plotly_chart(fig_age, use_container_width=True)

with tab2:
    st.markdown('<h3 class="section-title">Recruitment & Engagement Metrics</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # New members by month - Real data
        month_data = {
            'Month': ['January', 'February', 'March', 'April', 'May', 'June'],
            'New Members': [591, 1588, 4382, 6073, 2610, 123]
        }
        df_months = pd.DataFrame(month_data)
        
        fig_months = px.line(df_months, x='Month', y='New Members', 
                          title='New Members by Month',
                          markers=True)
        fig_months.update_traces(
            line=dict(color=primary_blue, width=3),
            marker=dict(color=primary_orange, size=10)
        )
        fig_months.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(fig_months, use_container_width=True)
    
    with col2:
        # New members by age - Real data
        new_age_data = {
            'Age Group': ['18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+', 'Unknown'],
            'New Members': [90, 504, 1923, 2389, 2039, 8479]
        }
        df_new_age = pd.DataFrame(new_age_data)
        
        fig_new_age = px.pie(df_new_age, values='New Members', names='Age Group', 
                         title='New Members by Age Group',
                         color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, 
                                                secondary_blue, secondary_orange, secondary_teal])
        fig_new_age.update_traces(textposition='inside', textinfo='percent+label')
        fig_new_age.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(fig_new_age, use_container_width=True)
    
    # Engagement metrics
    st.markdown('<h4>Engagement Stats</h4>', unsafe_allow_html=True)
    
    engagement_col1, engagement_col2, engagement_col3 = st.columns(3)
    
    with engagement_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">ACTIVE VOLUNTEERS</p>'
            f'<p class="metric-value">3,348</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with engagement_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">DOCUMENTED CREW LEADERS</p>'
            f'<p class="metric-value">3,856</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with engagement_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">ACTIVE CREW LEADERS</p>'
            f'<p class="metric-value">1,846</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Training and volunteer metrics
    st.markdown('<h4>Volunteer Development</h4>', unsafe_allow_html=True)
    
    volunteer_col1, volunteer_col2 = st.columns(2)
    
    with volunteer_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL TRAINED VOLUNTEERS</p>'
            f'<p class="metric-value">11,535</p>'
            f'<p>Includes all training programs</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with volunteer_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">NEW CREWS FORMED</p>'
            f'<p class="metric-value">727</p>'
            f'<p>Year to Date</p>'
            f'</div>', 
            unsafe_allow_html=True
        )

with tab3:
    st.markdown('<h3 class="section-title">Development Metrics</h3>', unsafe_allow_html=True)
    
    # Financial summary - Real data
    financial_col1, financial_col2, financial_col3 = st.columns(3)
    
    with financial_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL DONATIONS</p>'
            f'<p class="metric-value">$3,109,294.25</p>'
            f'<p>Goal: $10,000,000</p>'
            f'<p>Progress: 31.09%</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with financial_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL REVENUE (YTD)</p>'
            f'<p class="metric-value">$3,243,526</p>'
            f'<p>Budget: $1,237,419</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with financial_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL EXPENSES (YTD)</p>'
            f'<p class="metric-value">$2,343,862</p>'
            f'<p>Budget: $1,608,765</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Grants and fundraising - Real data
    grants_col1, grants_col2 = st.columns(2)
    
    with grants_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL GRANTS</p>'
            f'<p class="metric-value">$3,101,133.09</p>'
            f'<p>17 Grants Funded</p>'
            f'<p>Goal: 48 Grants (35.42%)</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with grants_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">STORE SALES</p>'
            f'<p class="metric-value">$99,836</p>'
            f'<p>Goal: $400,000</p>'
            f'<p>Progress: 24.96%</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Financial breakdown chart
    finance_data = {
        'Category': ['Grants', 'Donations', 'Store Sales', 'Other Revenue'],
        'Amount': [3101133.09, 8161.16, 99836, 34395.75]
    }
    df_finance = pd.DataFrame(finance_data)
    
    fig_finance = px.pie(df_finance, values='Amount', names='Category', 
                       title='Revenue Breakdown',
                       color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, secondary_blue])
    fig_finance.update_traces(textposition='inside', textinfo='percent+label')
    fig_finance.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(fig_finance, use_container_width=True)
    
    # Store Performance
    st.markdown('<h4>Store Performance Metrics</h4>', unsafe_allow_html=True)
    
    store_col1, store_col2 = st.columns(2)
    
    with store_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">AVERAGE ORDER VALUE (AOV)</p>'
            f'<p class="metric-value">$44.36</p>'
            f'<p>Target: $20-60</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with store_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">GROSS PROFIT PERCENTAGE</p>'
            f'<p class="metric-value">37%</p>'
            f'<p>Target: 50-60%</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )

with tab4:
    st.markdown('<h3 class="section-title">Marketing Metrics</h3>', unsafe_allow_html=True)
    
    # Subscriber metrics - Real data
    sub_col1, sub_col2 = st.columns(2)
    
    with sub_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL SUBSCRIBERS</p>'
            f'<p class="metric-value">931,141</p>'
            f'<p>Goal: 1,300,000 (71.63%)</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with sub_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">ACTIVE SUBSCRIBERS</p>'
            f'<p class="metric-value">320,463</p>'
            f'<p>34.4% of Total Subscribers</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Email engagement
    st.markdown('<h4>Email Engagement (30 Day)</h4>', unsafe_allow_html=True)
    
    email_col1, email_col2 = st.columns(2)
    
    with email_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">EMAIL OPENERS</p>'
            f'<p class="metric-value">19,148</p>'
            f'<p>Open Rate: ~6%</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with email_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">EMAIL CLICKERS</p>'
            f'<p class="metric-value">12,904</p>'
            f'<p>Click Rate: ~4%</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # SMS Engagement Note
    st.markdown(
        f"""
        <div class="metric-card">
            <h6 style="color: {primary_blue};">SMS Engagement Benchmark</h6>
            <p>Industry Standard: SMS messages have click-through rates of 6.3% for fundraising messages and 10% for advocacy messages.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

with tab5:
    st.markdown('<h3 class="section-title">Impact & Member Care Metrics</h3>', unsafe_allow_html=True)
    
    # Care Village metrics - Real data
    care_col1, care_col2 = st.columns(2)
    
    with care_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">CARE VILLAGE: POPULATION REACHED</p>'
            f'<p class="metric-value">3,055</p>'
            f'<p>Goal: 40,000</p>'
            f'<p>Progress: 7.64%</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with care_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">WALKING AT LIFE-SAVING LEVEL</p>'
            f'<p class="metric-value">5,634</p>'
            f'<p>Goal: 65,000</p>'
            f'<p>Progress: 8.67%</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Member satisfaction metrics - Real data
    member_col1, member_col2 = st.columns(2)
    
    with member_col1:
        fig_satisfaction = go.Figure(go.Indicator(
            mode="gauge+number",
            value=93,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Member Satisfaction Rating", 'font': {'color': primary_blue}},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': primary_orange},
                'steps': [
                    {'range': [0, 50], 'color': secondary_beige},
                    {'range': [50, 85], 'color': secondary_gold},
                    {'range': [85, 100], 'color': primary_yellow}
                ],
                'threshold': {
                    'line': {'color': secondary_orange, 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))
        
        fig_satisfaction.update_layout(height=300)
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    with member_col2:
        st.markdown('<h4>Top Member Issues/Concerns</h4>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="metric-card">
                <ul>
                    <li>SCS Registration Error Message</li>
                    <li>Connecting to the Movement</li>
                    <li>App functionality and usability</li>
                    <li>Finding local crew events</li>
                </ul>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Walking metrics
    st.markdown('<h4>Health Impact Metrics</h4>', unsafe_allow_html=True)
    
    health_col1, health_col2 = st.columns(2)
    
    with health_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">MEMBERS WALKING 30 MIN/DAY, 5 DAYS/WEEK</p>'
            f'<p class="metric-value">5,439</p>'
            f'<p>Goal: 50,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with health_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">MEMBERS IN SPECIAL IMPACT PROGRAMS</p>'
            f'<p class="metric-value">100</p>'
            f'<p>Goal: 65,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )

# Sidebar for filters
st.sidebar.markdown("# Filters")
st.sidebar.markdown("### Date Range")
start_date = st.sidebar.date_input("Start Date", datetime(2025, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime(2025, 6, 30))

st.sidebar.markdown("### Regions")
regions = ['All', 'Northeast', 'Southeast', 'Midwest', 'Southwest', 'West']
selected_region = st.sidebar.selectbox("Select Region", regions)

st.sidebar.markdown("### Age Groups")
age_groups = ['All', '18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+']
selected_age = st.sidebar.multiselect("Select Age Groups", age_groups, default='All')

st.sidebar.markdown("### Dashboard Settings")
show_target_lines = st.sidebar.checkbox("Show Target Lines", value=True)
dark_mode = st.sidebar.checkbox("Dark Mode", value=False)

# Footer
st.markdown(
    f"""
    <div style="margin-top: 50px; padding: 20px; background-color: {secondary_beige}; border-radius: 10px; text-align: center;">
        <h3 style="color: {primary_blue};">GirlTREK - Inspiring Black Women to Walk for Better Health</h3>
        <p>Data last updated: June 2025</p>
        <p>For more information, visit <a href="https://www.girltrek.org" target="_blank" style="color: {primary_blue};">girltrek.org</a></p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Add documentation for deployment
st.sidebar.markdown("---")
st.sidebar.markdown("### Deployment Instructions")
with st.sidebar.expander("How to deploy this dashboard on GitHub"):
    st.markdown("""
        ### Deploying to GitHub
        
        1. Create a new GitHub repository
        2. Add the following files to your repository:
            - `app.py` (this Streamlit app)
            - `requirements.txt` (with dependencies)
            - `README.md` (documentation)
        3. Connect your repository to Streamlit Cloud:
            - Go to [Streamlit Cloud](https://streamlit.io/cloud)
            - Sign in with your GitHub account
            - Click "New app"
            - Select your repository, branch, and main file path
            - Click "Deploy"
        
        Your dashboard will be available at a public URL provided by Streamlit Cloud.
        """)

# Sample requirements.txt
with st.sidebar.expander("Sample requirements.txt"):
    st.code("""
streamlit>=1.10.0
pandas>=1.3.0
plotly>=5.5.0
    """)

# Sample config.toml with GirlTREK colors
with st.sidebar.expander("Sample .streamlit/config.toml"):
    st.code(f"""
[theme]
primaryColor = "{primary_orange}"
backgroundColor = "{secondary_white}"
secondaryBackgroundColor = "{secondary_beige}"
textColor = "{secondary_gray}"
font = "sans serif"
    """)
