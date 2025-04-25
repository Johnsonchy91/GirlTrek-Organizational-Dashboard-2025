with tab5:
    st.markdown('<h3 class="section-title">Impact & Member Care Metrics</h3>', unsafe_allow_html=True)
    
    # Care Village metrics
    care_col1, care_col2 = st.columns(2)
    
    with care_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">CARE VILLAGE: POPULATION REACHED</p>'
            f'<p class="metric-value">2,869</p>'
            f'<p>Goal: 20,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with care_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">HEALTH WORKER TRAINING</p>'
            f'<p class="metric-value">450</p>'
            f'<p>Goal: 4,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Member satisfaction metrics
    member_col1, member_col2 = st.columns(2)
    
    with member_col1:
        fig_satisfaction = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=95,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Member Satisfaction Rating", 'font': {'color': primary_blue}},
            delta={'reference': 85, 'increasing': {'color': primary_orange}},
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
                    'value': 85
                }
            }
        ))
        
        fig_satisfaction.update_layout(height=300)
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    with member_col2:
        fig_response = go.Figure(go.Indicator(
            mode="number+delta",
            value=2,
            number={'suffix': " hours", 'font': {'color': primary_blue}},
            title={'text': "Resolution/Responsiveness Rate", 'font': {'color': primary_blue}},
            delta={'reference': 48, 'decreasing': {'color': primary_orange}}
        ))
        
        fig_response.update_layout(height=300)
        st.plotly_chart(fig_response, use_container_width=True)
    
    # Health impact metrics (dummy data)
    st.markdown('<h4>Health Impact</h4>', unsafe_allow_html=True)
    
    health_data = {
        'Metric': [
            'Improved Mental Well-being', 
            'Feel More Connected', 
            'Weight Loss', 
            'Improved Management of Chronic Conditions',
            'Reduced Medication Dependency',
            'Fewer Symptoms of Depression or Anxiety'
        ],
        'Percentage': [78, 85, 65, 58, 42, 72]
    }
    df_health = pd.DataFrame(health_data)
    
    fig_health = px.bar(df_health, x='Metric', y='Percentage',
                     title='Self-Reported Health Improvements',
                     color='Percentage',
                     color_continuous_scale=[primary_blue, primary_orange, primary_yellow])
    
    fig_health.update_layout(
        xaxis_title='Health Outcome',
        yaxis_title='Percentage of Respondents (%)',
        height=500,
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(fig_health, use_container_width=True)
    
    # Top member issues
    st.markdown('<h4>Top Member Issues/Concerns</h4>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metric-card">
        <ul>
            <li>The App functionality and usability</li>
            <li>Join the Movement process and onboarding</li>
            <li>Finding local crew events</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Operations metrics
    st.markdown('<h4>Operations</h4>', unsafe_allow_html=True)
    
    ops_col1, ops_col2, ops_col3 = st.columns(3)
    
    with ops_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">STORE SALES</p>'
            f'<p class="metric-value">$25,000</p>'
            f'<p>Goal: $50,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with ops_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">AUDIT COMPLIANCE</p>'
            f'<p class="metric-value">90%</p>'
            f'<p>Goal: 100%</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with ops_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">CYBER SECURITY COMPLIANCE</p>'
            f'<p class="metric-value">60%</p>'
            f'<p>Goal: 90%</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64

# Set page configuration
st.set_page_config(
    page_title="GirlTREK Organizational Dashboard",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# GirlTREK Brand Colors
# Primary Colors
primary_blue = "#2628cc"
primary_orange = "#fa8320"
primary_yellow = "#ffff00"

# Secondary Colors
secondary_orange = "#ff4713"
secondary_blue = "#0765ff"
secondary_gold = "#ffb607"
secondary_yellow = "#e9f504"
secondary_teal = "#00adca"
secondary_beige = "#f0e6d0"
secondary_gray = "#333132"
secondary_black = "#000000"
secondary_white = "#ffffff"

# Function to set background image or logo
def add_logo():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .logo {
            max-width: 200px;
        }
        </style>
        <div class="logo-container">
            <img class="logo" src="data:image/png;base64,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" alt="GirlTREK Logo">
        </div>
        """,
        unsafe_allow_html=True
    )

# Custom CSS for styling with updated brand colors
st.markdown(
    f"""
    <style>
        .main {{
            padding: 20px;
        }}
        .reportcard {{
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            background-color: {secondary_white};
            border-left: 5px solid {primary_orange};
        }}
        .header-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            color: {primary_blue};
        }}
        .metric-card {{
            background-color: {secondary_white};
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
            border-top: 4px solid {primary_orange};
        }}
        .status-green {{
            color: white;
            background-color: #28a745;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }}
        .status-yellow {{
            color: black;
            background-color: {primary_yellow};
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }}
        .status-red {{
            color: white;
            background-color: {secondary_orange};
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }}
        .status-bright-green {{
            color: white;
            background-color: #00cc44;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: {primary_blue};
        }}
        .metric-title {{
            color: {secondary_gray};
            font-size: 14px;
            font-weight: bold;
        }}
        .section-title {{
            font-size: 20px;
            font-weight: bold;
            margin-top: 30px;
            margin-bottom: 20px;
            color: {primary_blue};
            border-bottom: 2px solid {primary_orange};
            padding-bottom: 10px;
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 24px;
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            white-space: pre-wrap;
            background-color: {secondary_white};
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            color: {secondary_gray};
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {primary_blue};
            color: white;
        }}
        button[kind="secondary"] {{
            background-color: {primary_orange};
            color: white;
        }}
        .stSidebar {{
            background-color: {secondary_beige};
        }}
        .stSidebar [data-testid="stMarkdownContainer"] h1, 
        .stSidebar [data-testid="stMarkdownContainer"] h2, 
        .stSidebar [data-testid="stMarkdownContainer"] h3 {{
            color: {primary_blue};
        }}
    </style>
    """, 
    unsafe_allow_html=True
)

# Add logo
add_logo()

# Create header
st.markdown(
    f"""
    <div class="header-container">
        <h1>GirlTREK Organizational Dashboard</h1>
        <p>Last Updated: April 25, 2025</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Function to display status badges
def status_badge(status):
    if status == "On Track":
        return '<span class="status-green">On Track</span>'
    elif status == "At Risk":
        return '<span class="status-yellow">At Risk</span>'
    elif status == "Off Track":
        return '<span class="status-red">Off Track</span>'
    elif status == "Achieved":
        return '<span class="status-bright-green">Achieved</span>'
    else:
        return status

# Top metrics with (*) data
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<div class="metric-card">'
        f'<p class="metric-title">TOTAL MEMBERSHIP (*)</p>'
        f'<p class="metric-value">1,240,394</p>'
        f'<p>Goal: 2,000,000</p>'
        f'</div>', 
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="metric-card">'
        f'<p class="metric-title">TOTAL NEW MEMBERS (*)</p>'
        f'<p class="metric-value">11,356</p>'
        f'<p>Goal: 100,000</p>'
        f'</div>', 
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<div class="metric-card">'
        f'<p class="metric-title">TOTAL DONATIONS (*)</p>'
        f'<p class="metric-value">$1,094,048.68</p>'
        f'<p>Goal: $8,000,000</p>'
        f'<p>{status_badge("At Risk")}</p>'
        f'</div>', 
        unsafe_allow_html=True
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown(
        f'<div class="metric-card">'
        f'<p class="metric-title">TOTAL REVENUE (*)</p>'
        f'<p class="metric-value">$1,500,000</p>'
        f'<p>Goal: $400,000</p>'
        f'<p>{status_badge("On Track")}</p>'
        f'</div>', 
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f'<div class="metric-card">'
        f'<p class="metric-title">TOTAL EXPENSES (*)</p>'
        f'<p class="metric-value">$1,200,000</p>'
        f'<p>Goal: N/A</p>'
        f'<p>{status_badge("On Track")}</p>'
        f'</div>', 
        unsafe_allow_html=True
    )

with col6:
    st.markdown(
        f'<div class="metric-card">'
        f'<p class="metric-title">ACTIVE VOLUNTEERS</p>'
        f'<p class="metric-value">3,348</p>'
        f'<p>{status_badge("On Track")}</p>'
        f'</div>', 
        unsafe_allow_html=True
    )

# Report Card Progress
st.markdown('<h2 class="section-title">Report Card Progress</h2>', unsafe_allow_html=True)

report_data = {
    'Goal': [
        'Goal 1: Recruit 100,000 new members',
        'Goal 2: Engage 250,000 members',
        'Goal 3: Support 65,000 members walking at life-saving level',
        'Goal 4: Unite 20 national and local advocacy partners',
        'Goal 5: Raise $10M in donations, sales & sponsorships',
        'Goal 6: Establish Care Village (reach 40,000)',
        'Goal 7: Achieve 85% on org health'
    ],
    'Current': [11356, 11769, 1983, 2, 1094048.68, 2869, "70%"],
    'Total_Percent': ["11.356%", "4.7076%", "3.05%", "10%", "10.94%", "7.17%", "70%"],
    'Status': ["On Track", "On Track", "At Risk", "At Risk", "On Track", "On Track", "On Track"]
}

df_report = pd.DataFrame(report_data)

# Create a horizontal bar chart for goal progress
fig = go.Figure()

for i, row in df_report.iterrows():
    percent = float(row['Total_Percent'].replace('%', ''))
    color = '#28a745' if row['Status'] == 'On Track' else primary_yellow if row['Status'] == 'At Risk' else secondary_orange
    
    fig.add_trace(go.Bar(
        y=[row['Goal']],
        x=[percent],
        orientation='h',
        name=row['Goal'],
        marker=dict(color=color),
        text=f"{percent}%",
        textposition='auto',
        hoverinfo='text',
        hovertext=f"{row['Goal']}: {row['Current']} ({row['Total_Percent']})<br>Status: {row['Status']}"
    ))

fig.update_layout(
    title='Goal Progress',
    title_x=0.5,
    xaxis=dict(
        title='Progress (%)',
        range=[0, 100],
        tickvals=[0, 25, 50, 75, 100],
        ticktext=['0%', '25%', '50%', '75%', '100%']
    ),
    height=400,
    margin=dict(l=20, r=20, t=40, b=20),
    plot_bgcolor='white',
    paper_bgcolor='white',
    barmode='group',
    showlegend=False,
    title_font=dict(color=primary_blue)
)

st.plotly_chart(fig, use_container_width=True)

# Display report card as a table
st.markdown('<div class="reportcard">', unsafe_allow_html=True)
report_table = """
| Goal | Current | Progress | Status |
|------|---------|----------|--------|
"""

for i, row in df_report.iterrows():
    report_table += f"| {row['Goal']} | {row['Current']} | {row['Total_Percent']} | {status_badge(row['Status'])} |\n"

st.markdown(report_table, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Organizing", "Recruitment & Engagement", "Development", "Marketing", "Impact"])

with tab1:
    st.markdown('<h3 class="section-title">Organizing Metrics</h3>', unsafe_allow_html=True)
    
    # Membership by state
    state_data = {
        'State': ['Texas', 'Georgia', 'California', 'New York', 'Florida', 'Other States'],
        'Members': [91101, 86968, 80328, 68538, 66135, 847324]
    }
    df_states = pd.DataFrame(state_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_states = px.pie(df_states, values='Members', names='State', 
                           title='Membership by Top 5 States',
                           color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, 
                                                   secondary_blue, secondary_orange, secondary_teal])
        fig_states.update_traces(textposition='inside', textinfo='percent+label')
        fig_states.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(fig_states, use_container_width=True)
    
    # Membership by city
    city_data = {
        'City': ['Chicago', 'Philadelphia', 'Houston', 'Brooklyn', 'Atlanta', 'Other Cities'],
        'Members': [20645, 17276, 17065, 15602, 13172, 1156634]
    }
    df_cities = pd.DataFrame(city_data)
    
    with col2:
        fig_cities = px.bar(df_cities[:5], x='City', y='Members', 
                          title='Membership by Top 5 Cities',
                          color='Members',
                          color_continuous_scale=[primary_blue, primary_orange, primary_yellow])
        fig_cities.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(fig_cities, use_container_width=True)
    
    # Membership by age
    age_data = {
        'Age Group': ['18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+', 'Unknown'],
        'Members': [1803, 16790, 83392, 163951, 106812, 752621]
    }
    df_age = pd.DataFrame(age_data)
    
    fig_age = px.bar(df_age, x='Age Group', y='Members', 
                   title='Membership by Age Group',
                   color='Members',
                   color_continuous_scale=[secondary_blue, primary_blue, primary_orange])
    fig_age.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        fig_cities = px.bar(df_cities[:5], x='City', y='Members', 
                          title='Membership by Top 5 Cities',
                          color='Members',
                          color_continuous_scale=px.colors.sequential.Viridis)
        st.plotly_chart(fig_cities, use_container_width=True)
    
    # Membership by age
    age_data = {
        'Age Group': ['18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+', 'Unknown'],
        'Members': [1803, 16790, 83392, 163951, 106812, 752621]
    }
    df_age = pd.DataFrame(age_data)
    
    fig_age = px.bar(df_age, x='Age Group', y='Members', 
                   title='Membership by Age Group',
                   color='Members',
                   color_continuous_scale=px.colors.sequential.Viridis)
    st.plotly_chart(fig_age, use_container_width=True)

with tab2:
    st.markdown('<h3 class="section-title">Recruitment & Engagement Metrics</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # New members by month
        month_data = {
            'Month': ['January', 'February', 'March', 'April'],
            'New Members': [591, 1574, 4382, 4809]
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
        # New members by age
        new_age_data = {
            'Age Group': ['18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+', 'Unknown'],
            'New Members': [86, 477, 1771, 2163, 1898, 4961]
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
        st.markdown('<div class="metric-card">'
                    '<p class="metric-title">ACTIVE VOLUNTEERS</p>'
                    '<p class="metric-value">3,348</p>'
                    f'<p>{status_badge("On Track")}</p>'
                    '</div>', unsafe_allow_html=True)
    
    with engagement_col2:
        st.markdown('<div class="metric-card">'
                    '<p class="metric-title">DOCUMENTED CREW LEADERS</p>'
                    '<p class="metric-value">3,732</p>'
                    '</div>', unsafe_allow_html=True)
    
    with engagement_col3:
        st.markdown('<div class="metric-card">'
                    '<p class="metric-title">ACTIVE CREW LEADERS</p>'
                    '<p class="metric-value">1,846</p>'
                    f'<p>{status_badge("On Track")}</p>'
                    '</div>', unsafe_allow_html=True)
    
    # Campaign metrics
    st.markdown('<h4>Current Campaign: Self-Care Schools</h4>', unsafe_allow_html=True)
    
    campaign_col1, campaign_col2 = st.columns(2)
    
    with campaign_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL REGISTRANTS</p>'
            f'<p class="metric-value">7,500</p>'
            f'<p>Goal: 10,000</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with campaign_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL DOWNLOADS</p>'
            f'<p class="metric-value">32,000</p>'
            f'<p>Goal: 50,000</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Badges claimed
    badges_data = {
        'Week': ['Week 0', 'Week 1', 'Week 2'],
        'Badges Claimed': [3000, 2000, 1500]
    }
    df_badges = pd.DataFrame(badges_data)
    
    fig_badges = px.bar(df_badges, x='Week', y='Badges Claimed', 
                      title='Badges Claimed by Week',
                      color='Badges Claimed',
                      color_continuous_scale=[primary_yellow, primary_orange, secondary_orange])
    fig_badges.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(fig_badges, use_container_width=True)

with tab3:
    st.markdown('<h3 class="section-title">Development Metrics</h3>', unsafe_allow_html=True)
    
    # Financial summary
    financial_col1, financial_col2, financial_col3 = st.columns(3)
    
    with financial_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL DONATIONS</p>'
            f'<p class="metric-value">$1,094,048.68</p>'
            f'<p>Goal: $8,000,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with financial_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL REVENUE</p>'
            f'<p class="metric-value">$1,500,000</p>'
            f'<p>Goal: $400,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with financial_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL EXPENSES</p>'
            f'<p class="metric-value">$1,200,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Grants and fundraising
    grants_col1, grants_col2 = st.columns(2)
    
    with grants_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL GRANTS</p>'
            f'<p class="metric-value">$600,000</p>'
            f'<p>Goal: $1,000,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with grants_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">CORPORATE SPONSORSHIPS</p>'
            f'<p class="metric-value">$750,000</p>'
            f'<p>Goal: $1,500,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Financial breakdown chart
    finance_data = {
        'Category': ['Donations', 'Grants', 'Corporate Sponsorships', 'Store Sales', 'Other Revenue'],
        'Amount': [1094048.68, 600000, 750000, 25000, 125000]
    }
    df_finance = pd.DataFrame(finance_data)
    
    fig_finance = px.pie(df_finance, values='Amount', names='Category', 
                       title='Revenue Breakdown',
                       color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, 
                                              secondary_blue, secondary_orange])
    fig_finance.update_traces(textposition='inside', textinfo='percent+label')
    fig_finance.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(fig_finance, use_container_width=True)
    
    # Dummy data for financial trends
    months = ['January', 'February', 'March', 'April']
    revenue = [250000, 310000, 450000, 490000]
    expenses = [220000, 280000, 350000, 350000]
    donations = [180000, 240000, 300000, 374048.68]
    
    finance_trend_data = pd.DataFrame({
        'Month': months,
        'Revenue': revenue,
        'Expenses': expenses,
        'Donations': donations
    })
    
    fig_trend = go.Figure()
    
    fig_trend.add_trace(go.Scatter(
        x=finance_trend_data['Month'],
        y=finance_trend_data['Revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color=primary_blue, width=3),
        marker=dict(color=primary_blue, size=8)
    ))
    
    fig_trend.add_trace(go.Scatter(
        x=finance_trend_data['Month'],
        y=finance_trend_data['Expenses'],
        mode='lines+markers',
        name='Expenses',
        line=dict(color=primary_orange, width=3),
        marker=dict(color=primary_orange, size=8)
    ))
    
    fig_trend.add_trace(go.Scatter(
        x=finance_trend_data['Month'],
        y=finance_trend_data['Donations'],
        mode='lines+markers',
        name='Donations',
        line=dict(color=primary_yellow, width=3),
        marker=dict(color=primary_yellow, size=8)
    ))
    
    fig_trend.update_layout(
        title='Financial Trends by Month',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        legend_title='Category',
        height=500,
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)

with tab4:
    st.markdown('<h3 class="section-title">Marketing Metrics</h3>', unsafe_allow_html=True)
    
    # Subscriber metrics
    sub_col1, sub_col2 = st.columns(2)
    
    with sub_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL SUBSCRIBERS</p>'
            f'<p class="metric-value">931,141</p>'
            f'<p>Goal: 1,300,000</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with sub_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">ACTIVE SUBSCRIBERS</p>'
            f'<p class="metric-value">297,283</p>'
            f'<p>31.9% of Total Subscribers</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Subscriber activity
    activity_data = {
        'Period': ['30 day', '60 day', '90 day', '6 months'],
        'Openers': [221719, 266461, 272011, 295705],
        'Clickers': [13000, 21147, 22504, 26272]
    }
    df_activity = pd.DataFrame(activity_data)
    
    fig_activity = go.Figure()
    
    fig_activity.add_trace(go.Bar(
        x=df_activity['Period'],
        y=df_activity['Openers'],
        name='Openers',
        marker_color=primary_blue
    ))
    
    fig_activity.add_trace(go.Bar(
        x=df_activity['Period'],
        y=df_activity['Clickers'],
        name='Clickers',
        marker_color=primary_orange
    ))
    
    fig_activity.update_layout(
        title='Subscriber Activity',
        xaxis_title='Time Period',
        yaxis_title='Number of Subscribers',
        barmode='group',
        height=400,
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(fig_activity, use_container_width=True)
    
    # Email metrics
    st.markdown('<h4>Email Engagement</h4>', unsafe_allow_html=True)
    
    email_col1, email_col2 = st.columns(2)
    
    with email_col1:
        fig_open = go.Figure(go.Indicator(
            mode="gauge+number",
            value=34.95,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Average Open Rate", 'font': {'color': primary_blue}},
            gauge={
                'axis': {'range': [None, 50]},
                'bar': {'color': primary_blue},
                'steps': [
                    {'range': [0, 20], 'color': secondary_beige},
                    {'range': [20, 35], 'color': secondary_gold},
                    {'range': [35, 50], 'color': primary_orange}
                ],
                'threshold': {
                    'line': {'color': secondary_orange, 'width': 4},
                    'thickness': 0.75,
                    'value': 35
                }
            }
        ))
        
        fig_open.update_layout(height=300)
        st.plotly_chart(fig_open, use_container_width=True)
    
    with email_col2:
        fig_click = go.Figure(go.Indicator(
            mode="gauge+number",
            value=6.27,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Text Message Click-Through Rate", 'font': {'color': primary_blue}},
            gauge={
                'axis': {'range': [None, 15]},
                'bar': {'color': primary_blue},
                'steps': [
                    {'range': [0, 5], 'color': secondary_beige},
                    {'range': [5, 10], 'color': secondary_gold},
                    {'range': [10, 15], 'color': primary_orange}
                ],
                'threshold': {
                    'line': {'color': secondary_orange, 'width': 4},
                    'thickness': 0.75,
                    'value': 10
                }
            }
        ))
        
        fig_click.update_layout(height=300)
        st.plotly_chart(fig_click, use_container_width=True)
        
        st.markdown(f"""
        <div style="font-size: 12px; color: {secondary_gray};">
        Industry Standard: SMS messages have click-through rates of 6.3% for fundraising messages and 10% for advocacy messages.
        </div>
        """, unsafe_allow_html=True)

with tab5:
    st.markdown('<h3 class="section-title">Impact & Member Care Metrics</h3>', unsafe_allow_html=True)
    
    # Care Village metrics
    care_col1, care_col2 = st.columns(2)
    
    with care_col1:
        st.markdown('<div class="metric-card">'
                    '<p class="metric-title">CARE VILLAGE: POPULATION REACHED</p>'
                    '<p class="metric-value">2,869</p>'
                    '<p>Goal: 20,000</p>'
                    f'<p>{status_badge("On Track")}</p>'
                    '</div>', unsafe_allow_html=True)
    
    with care_col2:
        st.markdown('<div class="metric-card">'
                    '<p class="metric-title">HEALTH WORKER TRAINING</p>'
                    '<p class="metric-value">450</p>'
                    '<p>Goal: 4,000</p>'
                    f'<p>{status_badge("At Risk")}</p>'
                    '</div>', unsafe_allow_html=True)
    
    # Member satisfaction metrics
    member_col1, member_col2 = st.columns(2)
    
    with member_col1:
        fig_satisfaction = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=95,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Member Satisfaction Rating"},
            delta={'reference': 85, 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 85], 'color': "gray"},
                    {'range': [85, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 85
                }
            }
        ))
        
        fig_satisfaction.update_layout(height=300)
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    with member_col2:
        fig_response = go.Figure(go.Indicator(
            mode="number+delta",
            value=2,
            number={'suffix': " hours"},
            title={'text': "Resolution/Responsiveness Rate"},
            delta={'reference': 48, 'decreasing': {'color': "green"}}
        ))
        
        fig_response.update_layout(height=300)
        st.plotly_chart(fig_response, use_container_width=True)
    
    # Health impact metrics (dummy data)
    st.markdown('<h4>Health Impact</h4>', unsafe_allow_html=True)
    
    health_data = {
        'Metric': [
            'Improved Mental Well-being', 
            'Feel More Connected', 
            'Weight Loss', 
            'Improved Management of Chronic Conditions',
            'Reduced Medication Dependency',
            'Fewer Symptoms of Depression or Anxiety'
        ],
        'Percentage': [78, 85, 65, 58, 42, 72]
    }
    df_health = pd.DataFrame(health_data)
    
    fig_health = px.bar(df_health, x='Metric', y='Percentage',
                     title='Self-Reported Health Improvements',
                     color='Percentage',
                     color_continuous_scale=px.colors.sequential.Viridis)
    
    fig_health.update_layout(
        xaxis_title='Health Outcome',
        yaxis_title='Percentage of Respondents (%)',
        height=500
    )
    
    st.plotly_chart(fig_health, use_container_width=True)
    
    # Top member issues
    st.markdown('<h4>Top Member Issues/Concerns</h4>', unsafe_allow_html=True)
    st.markdown("""
    <div class="metric-card">
        <ul>
            <li>The App functionality and usability</li>
            <li>Join the Movement process and onboarding</li>
            <li>Finding local crew events</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Operations metrics
    st.markdown('<h4>Operations</h4>', unsafe_allow_html=True)
    
    ops_col1, ops_col2, ops_col3 = st.columns(3)
    
    with ops_col1:
        st.markdown('<div class="metric-card">'
                    '<p class="metric-title">STORE SALES</p>'
                    '<p class="metric-value">$25,000</p>'
                    '<p>Goal: $50,000</p>'
                    f'<p>{status_badge("On Track")}</p>'
                    '</div>', unsafe_
