import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Define color scheme - brighter and more fun colors
primary_blue = "#0088FF"    # Bright blue
primary_orange = "#FF5722"  # Vibrant orange
primary_yellow = "#FFEB3B"  # Bright yellow
secondary_blue = "#00C8FF"  # Light bright blue
secondary_orange = "#FF9100" # Bright amber
secondary_teal = "#00E5FF"  # Bright cyan
secondary_beige = "#FFECB3" # Light amber
secondary_gold = "#FFC400"  # Amber accent
secondary_white = "#FFFFFF" # White
secondary_gray = "#424242"  # Dark gray
secondary_pink = "#FF4081"  # Pink accent
secondary_purple = "#AA00FF" # Purple
secondary_green = "#00E676" # Bright green

# Helper function for status badges
def status_badge(status):
    if status == "On Track":
        return f'<span style="background-color: #4CAF50; color: white; padding: 3px 8px; border-radius: 4px;">On Track</span>'
    elif status == "At Risk":
        return f'<span style="background-color: #FF9800; color: white; padding: 3px 8px; border-radius: 4px;">At Risk</span>'
    else:
        return f'<span style="background-color: #F44336; color: white; padding: 3px 8px; border-radius: 4px;">Off Track</span>'

# Add CSS for styling
st.markdown(
    """
    <style>
    .section-title {
        color: #1E3C72;
        padding-bottom: 10px;
        border-bottom: 2px solid #FF7043;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 14px;
        font-weight: bold;
        color: #666;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #1E3C72;
        margin: 10px 0;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# App title
st.title("GirlTREK Organizational Dashboard")
st.markdown("### Q2 2025 Metrics Overview")
st.markdown("*Data dashboard was published on April 25, 2025*")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Executive Summary", 
    "Recruitment", 
    "Engagement",
    "Development", 
    "Marketing", 
    "Impact & Member Care",
    "Advocacy"
])

with tab1:
    st.markdown('<h3 class="section-title">Executive Summary</h3>', unsafe_allow_html=True)
    
    # Key metrics
    st.markdown("<h3>Key Metrics</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL MEMBERSHIP</p>'
            f'<p class="metric-value">1,240,394</p>'
            f'<p>Goal: 2,000,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL NEW MEMBERS</p>'
            f'<p class="metric-value">11,356</p>'
            f'<p>Goal: 100,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL REVENUE</p>'
            f'<p class="metric-value">$9,999</p>'
            f'<p>Goal: $400,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
        
    with col4:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL EXPENSES</p>'
            f'<p class="metric-value">$40,000</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Report Card Progress
    st.markdown('<h3>Report Card Progress</h3>', unsafe_allow_html=True)
    
    # Create a data table for report card with more specific goals as in the screenshot
    report_data = {
        "Goal": [
            "Goal 1: Recruit 100,000 new members", 
            "Goal 2: Engage 250,000 members", 
            "Goal 3: Support 65,000 members walking at life-saving level",
            "Goal 4: Unite 20 national and local advocacy partners",
            "Goal 5: Raise $10M in donations, sales & sponsorships",
            "Goal 6: Establish Care Village (reach 40,000)",
            "Goal 7: Achieve 85% on org health"
        ],
        "Current Total": [
            "11,356", 
            "11,769", 
            "1,983",
            "2",
            "1,094,048.68",
            "2,869",
            "70%"
        ],
        "Percent Progress": [
            "11.356%", 
            "4.7076%", 
            "3.05%",
            "10%",
            "10.94%",
            "7.17%",
            "70%"
        ],
        "Status": [
            "On Track", 
            "On Track", 
            "At Risk",
            "At Risk",
            "On Track",
            "On Track",
            "On Track"
        ],
        "Progress": [
            11.356, 
            4.7076, 
            3.05,
            10,
            10.94,
            7.17,
            70
        ]
    }
    
    # Create styled progress bars with color based on status
    for i in range(len(report_data["Goal"])):
        goal = report_data["Goal"][i]
        current = report_data["Current Total"][i]
        percent = report_data["Percent Progress"][i]
        status = report_data["Status"][i]
        progress = report_data["Progress"][i]
        
        # Determine color based on status
        if status == "On Track":
            bar_color = "#4CAF50"  # Green
        else:
            bar_color = "#FF9800"  # Yellow/Orange for "At Risk"
        
        st.markdown(
            f"""
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <div><strong>{goal}</strong></div>
                    <div style="text-align: right;">
                        <span style="margin-right: 15px;"><strong>{current}</strong></span>
                        <span style="margin-right: 15px;"><strong>{percent}</strong></span>
                        <span><strong>{status}</strong></span>
                    </div>
                </div>
                <div style="width: 100%; background-color: #f0f2f5; height: 12px; border-radius: 6px;">
                    <div style="width: {progress}%; height: 100%; background-color: {bar_color}; border-radius: 6px;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Q2 highlights
    st.markdown("### Q2 2025 Highlights")
    
    highlights_col1, highlights_col2 = st.columns(2)
    
    with highlights_col1:
        st.markdown(
            """
            #### Achievements
            - Successfully launched the Self-Care Schools campaign with 7,500 registrants
            - Increased social media following by 25% since Q1
            - Secured new corporate sponsorship with Health Horizons ($350,000)
            - Launched 15 new local crews in underserved communities
            """
        )
    
    with highlights_col2:
        st.markdown(
            """
            #### Challenges
            - Donations tracking below target (trending at 13.7% of annual goal)
            - Health worker training program behind schedule
            - Cyber security audit revealed compliance gaps that need addressing
            - App user retention lower than expected for new members
            """
        )

with tab2:
    st.markdown('<h3 class="section-title">Recruitment Metrics</h3>', unsafe_allow_html=True)
    
    # Recruitment metrics
    recruitment_col1, recruitment_col2, recruitment_col3 = st.columns(3)
    
    with recruitment_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL NEW MEMBERS</p>'
            f'<p class="metric-value">11,356</p>'
            f'<p>Goal: 100,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with recruitment_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">CONVERSION RATE</p>'
            f'<p class="metric-value">15.2%</p>'
            f'<p>Goal: 20%</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with recruitment_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">COST PER ACQUISITION</p>'
            f'<p class="metric-value">$3.75</p>'
            f'<p>Goal: $5.00</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
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
                                                secondary_pink, secondary_purple, secondary_green])
        fig_new_age.update_traces(textposition='inside', textinfo='percent+label')
        fig_new_age.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(fig_new_age, use_container_width=True)
    
    # Recruitment sources
    st.markdown('<h4>Recruitment Sources</h4>', unsafe_allow_html=True)
    
    source_data = {
        'Source': ['Social Media', 'Word of Mouth', 'Events', 'Website', 'Email Campaigns', 'Partner Organizations'],
        'New Members': [3654, 2870, 1985, 1254, 857, 736]
    }
    df_source = pd.DataFrame(source_data)
    
    fig_source = px.bar(df_source, x='Source', y='New Members', 
                      title='New Members by Recruitment Source',
                      color='New Members',
                      color_continuous_scale=[secondary_blue, primary_blue, secondary_purple])
    fig_source.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(fig_source, use_container_width=True)
    
with tab3:
    st.markdown('<h3 class="section-title">Engagement Metrics</h3>', unsafe_allow_html=True)
    
    # Engagement metrics
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
            f'<p class="metric-value">3,732</p>'
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
                      color_continuous_scale=[secondary_green, primary_blue, secondary_purple])
    fig_badges.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(fig_badges, use_container_width=True)
    
    # Member engagement chart
    engagement_metrics = {
        'Metric': ['App Opens', 'Event Attendance', 'Resource Downloads', 'Forum Participation', 'Challenge Completion'],
        'Percentage': [86, 45, 72, 31, 58]
    }
    df_engagement = pd.DataFrame(engagement_metrics)
    
    fig_engagement = px.bar(df_engagement, x='Metric', y='Percentage',
                         title='Member Engagement Metrics (%)',
                         color='Percentage',
                         color_continuous_scale=[secondary_teal, primary_orange, secondary_pink])
    
    fig_engagement.update_layout(
        xaxis_title='Engagement Type',
        yaxis_title='Percentage of Active Members (%)',
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(fig_engagement, use_container_width=True)

with tab4:
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
    
    # Brief chart showing member growth
    member_data = {
        'Quarter': ['Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025'],
        'Members': [2500, 4500, 6800, 9200, 11356]
    }
    df_members = pd.DataFrame(member_data)
    
    fig_advocacy_growth = px.line(df_members, x='Quarter', y='Members', 
                    title='GirlTREK Membership Growth',
                    markers=True)
    
    fig_advocacy_growth.update_traces(
        line=dict(color=primary_blue, width=3),
        marker=dict(color=primary_orange, size=10)
    )
    
    fig_advocacy_growth.update_layout(title_font=dict(color=primary_blue))
    
    st.plotly_chart(fig_advocacy_growth, use_container_width=True)

with tab5:
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
        
        st.markdown(
            f"""
            <div style="font-size: 12px; color: {secondary_gray};">
            Industry Standard: SMS messages have click-through rates of 6.3% for fundraising messages and 10% for advocacy messages.
            </div>
            """, 
            unsafe_allow_html=True
        )

with tab6:
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
    st.markdown(
        f"""
        <div class="metric-card">
            <ul>
                <li>The App functionality and usability</li>
                <li>Join the Movement process and onboarding</li>
                <li>Finding local crew events</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
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
        )

with tab7:
    st.markdown('<h3 class="section-title">Advocacy</h3>', unsafe_allow_html=True)
    
    # Create a styled table for Advocacy metrics
    st.markdown(
        """
        <style>
        .advocacy-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            font-size: 16px;
        }
        .advocacy-table th {
            background-color: #f8f8f8;
            padding: 12px 10px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #ddd;
        }
        .advocacy-table td {
            padding: 12px 10px;
            border: 1px solid #ddd;
            vertical-align: top;
        }
        .highlight {
            background-color: #ffdddd;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    # Define advocacy metrics data
    advocacy_data = [
        {
            "metric": "# of Advocacy briefs produced establishing research basis for why each J&J agenda item leads to increase in Black women's life expectancy and uplifting best in class organizations",
            "goal": "10",
            "current": "4",
            "status": "On Track"
        },
        {
            "metric": "Secure at least 20 advocacy partners that align with GirlTREK's Joy & Justice Agenda through signed MOUs.",
            "goal": "20",
            "current": "2",
            "status": "On Track"
        }
    ]
    
    # Build the table HTML
    advocacy_html = """
    <table class="advocacy-table">
        <tr>
            <th>Metric</th>
            <th>Goal</th>
            <th>Current Total</th>
            <th>Status</th>
        </tr>
    """
    
    # Add rows
    for item in advocacy_data:
        # Adding highlighting to specific text as in the screenshot
        metric_text = item["metric"]
        if "life expectancy and uplifting best" in metric_text:
            parts = metric_text.split("life expectancy and uplifting best")
            metric_display = f"{parts[0]}<span class='highlight'>life expectancy and uplifting best</span>{parts[1]}"
        else:
            metric_display = metric_text
            
        advocacy_html += f"""
        <tr>
            <td>{metric_display}</td>
            <td>{item["goal"]}</td>
            <td>{item["current"]}</td>
            <td>{item["status"]}</td>
        </tr>
        """
    
    advocacy_html += "</table>"
    
    st.markdown(advocacy_html, unsafe_allow_html=True)
    
    # Additional advocacy metrics
    st.markdown("### Advocacy Partner Organizations")
    
    advocacy_partners = {
        "Current Partners": ["National Urban League", "Black Women's Health Imperative"],
        "Pending Partners": ["NAACP", "Color of Change", "African American Policy Forum"]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current Partners")
        for partner in advocacy_partners["Current Partners"]:
            st.markdown(f"- {partner}")
    
    with col2:
        st.subheader("Pending Partners")
        for partner in advocacy_partners["Pending Partners"]:
            st.markdown(f"- {partner}")
            
    # Advocacy impact metrics
    st.markdown("### Advocacy Impact")
    
    impact_col1, impact_col2 = st.columns(2)
    
    with impact_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">MEDIA MENTIONS</p>'
            f'<p class="metric-value">28</p>'
            f'<p>Goal: 50</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with impact_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">POLICY MEETINGS</p>'
            f'<p class="metric-value">6</p>'
            f'<p>Goal: 15</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Brief chart showing member growth
    member_data = {
        'Quarter': ['Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025'],
        'Members': [2500, 4500, 6800, 9200, 11356]
    }
    df_members = pd.DataFrame(member_data)
    
    fig_dev_growth = px.line(df_members, x='Quarter', y='Members', 
                    title='GirlTREK Membership Growth',
                    markers=True)
    
    fig_dev_growth.update_traces(
        line=dict(color=primary_blue, width=3),
        marker=dict(color=primary_orange, size=10)
    )
    
    fig_dev_growth.update_layout(title_font=dict(color=primary_blue))
    
    st.plotly_chart(fig_dev_growth, use_container_width=True)

# Sidebar for filters
st.sidebar.markdown("# Filters")
st.sidebar.markdown("### Date Range")
start_date = st.sidebar.date_input("Start Date", datetime(2025, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime(2025, 4, 25))

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
        <p>Data last updated: April 25, 2025</p>
        <p>For more information, visit <a href="https://www.girltrek.org" target="_blank" style="color: {primary_blue};">girltrek.org</a></p>
    </div>
    """, 
    unsafe_allow_html=True
)
