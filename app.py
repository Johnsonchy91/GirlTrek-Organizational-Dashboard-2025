import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
import io

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
achieved_green = "#00C853"  # Bright green for Achieved status

# Helper function for status badges
def status_badge(status):
    if status == "On Track":
        return f'<span style="background-color: #4CAF50; color: white; padding: 3px 8px; border-radius: 4px;">On Track</span>'
    elif status == "At Risk":
        return f'<span style="background-color: #FF9800; color: white; padding: 3px 8px; border-radius: 4px;">At Risk</span>'
    elif status == "Achieved":
        return f'<span style="background-color: {achieved_green}; color: white; padding: 3px 8px; border-radius: 4px;">Achieved</span>'
    else:
        return f'<span style="background-color: #F44336; color: white; padding: 3px 8px; border-radius: 4px;">Off Track</span>'

# Function to download data as CSV
def download_data(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} data</a>'
    return href

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
    .note-text {
        font-size: 14px;
        font-style: italic;
        color: #666;
        margin-top: 5px;
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "Executive Summary", 
    "Recruitment", 
    "Engagement",
    "Development", 
    "Marketing", 
    "Operations",
    "Impact",
    "Member Care",
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
            f'<p class="metric-title">TOTAL CONTRIBUTIONS</p>'
            f'<p class="metric-value">$3,061,104.78</p>'
            f'<p>Goal: $8,000,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
        
    with col4:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL GRANTS</p>'
            f'<p class="metric-value">$3,055,250</p>'
            f'<p>{status_badge("On Track")}</p>'
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
            "4,858",
            "2",
            "3,061,104.78",
            "2,869",
            "Unknown"
        ],
        "Percent Progress": [
            "11.356%", 
            "4.7076%", 
            "7.47%",
            "10%",
            "30.61%",
            "7.17%",
            "Unknown"
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
            7.47,
            10,
            30.61,
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
        elif status == "Achieved":
            bar_color = achieved_green  # Bright green
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
    
    # Download button for this tab
    report_df = pd.DataFrame({
        "Goal": report_data["Goal"],
        "Current Total": report_data["Current Total"],
        "Percent Progress": report_data["Percent Progress"],
        "Status": report_data["Status"]
    })
    
    st.markdown(download_data(report_df, "GirlTREK_Executive_Summary"), unsafe_allow_html=True)

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
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with recruitment_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL NEW MEMBERS AGE 18-30</p>'
            f'<p class="metric-value">300</p>'
            f'<p>Goal: 50,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with recruitment_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL RECRUITMENT PARTNERSHIPS</p>'
            f'<p class="metric-value">0</p>'
            f'<p>Goal: 100</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'<p class="note-text">Contact has been made with 20 community organizations.</p>'
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
    
    # Membership by top states and cities
    st.markdown('<h4>Membership Distribution</h4>', unsafe_allow_html=True)
    
    dist_col1, dist_col2 = st.columns(2)
    
    with dist_col1:
        st.markdown("<h5>Top 5 States</h5>", unsafe_allow_html=True)
        states_data = {
            'State': ['Texas', 'Georgia', 'California', 'New York', 'Florida'],
            'Members': [91101, 86968, 80328, 68538, 66135]
        }
        df_states = pd.DataFrame(states_data)
        
        fig_states = px.bar(df_states, x='State', y='Members',
                         title='Membership by Top 5 States',
                         color='Members',
                         color_continuous_scale=[secondary_blue, primary_blue])
        fig_states.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(fig_states, use_container_width=True)
    
    with dist_col2:
        st.markdown("<h5>Top 5 Cities</h5>", unsafe_allow_html=True)
        cities_data = {
            'City': ['Chicago', 'Philadelphia', 'Houston', 'Brooklyn', 'Atlanta'],
            'Members': [20645, 17276, 17065, 15602, 13172]
        }
        df_cities = pd.DataFrame(cities_data)
        
        fig_cities = px.bar(df_cities, x='City', y='Members',
                         title='Membership by Top 5 Cities',
                         color='Members',
                         color_continuous_scale=[secondary_teal, primary_orange])
        fig_cities.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(fig_cities, use_container_width=True)
    
    # Total membership by age
    st.markdown('<h4>Total Membership by Age</h4>', unsafe_allow_html=True)
    
    total_age_data = {
        'Age Group': ['18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+', 'Unknown'],
        'Members': [1803, 16790, 83392, 163951, 106812, 752621]
    }
    df_total_age = pd.DataFrame(total_age_data)
    
    fig_total_age = px.bar(df_total_age, x='Age Group', y='Members',
                       title='Total Membership by Age Group',
                       color='Members',
                       color_continuous_scale=[secondary_purple, primary_blue, secondary_pink])
    fig_total_age.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(fig_total_age, use_container_width=True)
    
    # Download button for this tab
    st.markdown("### Download Recruitment Data")
    
    # Combine dataframes for download
    recruitment_data = {
        "Monthly New Members": df_months,
        "New Members by Age": df_new_age,
        "Members by State": df_states,
        "Members by City": df_cities,
        "Total Members by Age": df_total_age
    }
    
    selected_data = st.selectbox("Select data to download:", list(recruitment_data.keys()))
    st.markdown(download_data(recruitment_data[selected_data], f"GirlTREK_{selected_data.replace(' ', '_')}"), unsafe_allow_html=True)

with tab3:
    st.markdown('<h3 class="section-title">Engagement Metrics</h3>', unsafe_allow_html=True)
    
    # Engagement metrics
    engagement_col1, engagement_col2, engagement_col3 = st.columns(3)
    
    with engagement_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL ACTIVE VOLUNTEERS</p>'
            f'<p class="metric-value">3,348</p>'
            f'<p class="note-text">Has hosted an event this year</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with engagement_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL DOCUMENTED CREW LEADERS</p>'
            f'<p class="metric-value">3,732</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with engagement_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL ACTIVE CREW LEADERS</p>'
            f'<p class="metric-value">1,846</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'<p class="note-text">Has hosted an event this year or signed up this year</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Additional engagement metrics
    more_engage_col1, more_engage_col2 = st.columns(2)
    
    with more_engage_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL NEW CREWS</p>'
            f'<p class="metric-value">603</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with more_engage_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">MEMBERS WALKING AT LIFE-SAVING LEVEL</p>'
            f'<p class="metric-value">4,788</p>'
            f'<p>Goal: 50,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'<p class="note-text">Members walking at least 30 minutes/day, 5 days/week</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Impact program metrics
    impact_col1, impact_col2 = st.columns(2)
    
    with impact_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">MEMBERS IN SPECIAL IMPACT PROGRAMS</p>'
            f'<p class="metric-value">100</p>'
            f'<p>Goal: 65,000</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with impact_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL TRAINED</p>'
            f'<p class="metric-value">50</p>'
            f'<p>Goal: 1,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Campaign metrics
    st.markdown('<h4>Current Campaign: Self-Care Schools</h4>', unsafe_allow_html=True)
    
    campaign_col1, campaign_col2, campaign_col3 = st.columns(3)
    
    with campaign_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL REGISTRANTS</p>'
            f'<p class="metric-value">11,985</p>'
            f'<p>Goal: 10,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with campaign_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL DOWNLOADS</p>'
            f'<p class="metric-value">22,186</p>'
            f'<p>Goal: 100,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with campaign_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">REGISTRANTS AGE 18-25</p>'
            f'<p class="metric-value">101</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Campaign related metrics
    campaign2_col1, campaign2_col2 = st.columns(2)
    
    with campaign2_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">NEW MEMBERS FROM CAMPAIGN</p>'
            f'<p class="metric-value">4,808</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with campaign2_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">NEW MEMBERS AGE 18-25 FROM CAMPAIGN</p>'
            f'<p class="metric-value">75</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Badges claimed
    badges_data = {
        'Week': ['Week 0', 'Week 1', 'Week 2'],
        'Badges Claimed': [3089, 2061, 2197]
    }
    df_badges = pd.DataFrame(badges_data)
    
    fig_badges = px.bar(df_badges, x='Week', y='Badges Claimed', 
                      title='Badges Claimed by Week (Goal: 5,000 per week)',
                      color='Badges Claimed',
                      color_continuous_scale=[secondary_green, primary_blue, secondary_purple])
    fig_badges.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(fig_badges, use_container_width=True)
    
    # Additional campaign metrics
    stories_claimed_col1, stories_claimed_col2 = st.columns(2)
    
    with stories_claimed_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">PEOPLE WHO HAVE CLAIMED BADGES</p>'
            f'<p class="metric-value">4,788</p>'
            f'<p>Goal: 10,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with stories_claimed_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">STORIES SUBMITTED</p>'
            f'<p class="metric-value">234</p>'
            f'<p>Goal: 100</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Download button for this tab
    st.markdown("### Download Engagement Data")
    
    # Create dataframes for download
    engagement_metrics_df = pd.DataFrame({
        "Metric": ["Total Active Volunteers", "Total Documented Crew Leaders", "Total Active Crew Leaders", 
                  "Total New Crews", "Members Walking at Life-Saving Level", "Members in Special Impact Programs", 
                  "Total Trained"],
        "Value": [3348, 3732, 1846, 603, 4788, 100, 50],
        "Goal": ["N/A", "N/A", "N/A", "N/A", 50000, 65000, 1000],
        "Status": ["N/A", "N/A", "On Track", "N/A", "At Risk", "N/A", "At Risk"]
    })
    
    campaign_metrics_df = pd.DataFrame({
        "Metric": ["Total Registrants", "Total Downloads", "Registrants Age 18-25", 
                  "New Members from Campaign", "New Members Age 18-25 from Campaign",
                  "People Who Have Claimed Badges", "Stories Submitted"],
        "Value": [11985, 22186, 101, 4808, 75, 4788, 234],
        "Goal": [10000, 100000, "N/A", "N/A", "N/A", 10000, 100],
        "Status": ["On Track", "At Risk", "At Risk", "On Track", "At Risk", "On Track", "On Track"]
    })
    
    engagement_data = {
        "Engagement Metrics": engagement_metrics_df,
        "Campaign Metrics": campaign_metrics_df,
        "Badges Claimed by Week": df_badges
    }
    
    selected_engagement_data = st.selectbox("Select data to download:", list(engagement_data.keys()))
    st.markdown(download_data(engagement_data[selected_engagement_data], f"GirlTREK_{selected_engagement_data.replace(' ', '_')}"), unsafe_allow_html=True)

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
    
    # Download button for this tab
    st.markdown("### Download Development Data")
    
    # Create dataframes for download
    development_metrics_df = pd.DataFrame({
        "Metric": ["Total Donations", "Total Revenue", "Total Expenses", 
                 "Total Grants", "Corporate Sponsorships"],
        "Value": [1094048.68, 1500000, 1200000, 600000, 750000],
        "Goal": [8000000, 400000, "N/A", 1000000, 1500000],
        "Status": ["At Risk", "On Track", "On Track", "On Track", "On Track"]
    })
    
    st.markdown(download_data(development_metrics_df, "GirlTREK_Development_Metrics"), unsafe_allow_html=True)

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
    st.markdown('<h4>Email & Text Message Engagement</h4>', unsafe_allow_html=True)
    
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
    
    # Marketing spend
    st.markdown('<h4>Marketing Spend</h4>', unsafe_allow_html=True)
    
    spend_col1, spend_col2 = st.columns(2)
    
    with spend_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TEXT MESSAGING SPEND</p>'
            f'<p class="metric-value">$11,180.21</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with spend_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL MARKETING SPEND</p>'
            f'<p class="metric-value">Unknown</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Download button
    st.markdown("### Download Marketing Data")
    
    # Create dataframes for download
    subscriber_metrics_df = pd.DataFrame({
        "Metric": ["Total Subscribers", "Active Subscribers", "Average Open Rate", "Text Message Click-Through Rate"],
        "Value": [931141, 297283, "34.95%", "6.27%"],
        "Goal/Benchmark": [1300000, "N/A", "35%", "6.3-10%"]
    })
    
    st.markdown(download_data(subscriber_metrics_df, "GirlTREK_Marketing_Metrics"), unsafe_allow_html=True)
    st.markdown(download_data(df_activity, "GirlTREK_Subscriber_Activity"), unsafe_allow_html=True)

with tab6:
    st.markdown('<h3 class="section-title">Operations Metrics</h3>', unsafe_allow_html=True)
    
    # Operations metrics
    ops_col1, ops_col2, ops_col3 = st.columns(3)
    
    with ops_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL EXPENSES</p>'
            f'<p class="metric-value">Unknown</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with ops_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">EARNED REVENUE (STORE SALES)</p>'
            f'<p class="metric-value">Unknown</p>'
            f'<p>Goal: $400,000</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with ops_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">AUDIT COMPLIANCE</p>'
            f'<p class="metric-value">Unknown</p>'
            f'<p>Goal: 100%</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # More operations metrics
    ops2_col1, ops2_col2 = st.columns(2)
    
    with ops2_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">CYBER SECURITY COMPLIANCE</p>'
            f'<p class="metric-value">Unknown</p>'
            f'<p>Goal: 90%</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with ops2_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">ASANA ADOPTION</p>'
            f'<p class="metric-value">38%</p>'
            f'<p>Goal: 85%</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Simulated expense categories for visualization
    expense_categories = {
        'Category': ['Staff Salaries', 'Program Expenses', 'Marketing', 'Technology', 'Administrative', 'Other'],
        'Percentage': [45, 25, 15, 8, 5, 2]
    }
    df_expenses = pd.DataFrame(expense_categories)
    
    fig_expenses = px.pie(df_expenses, values='Percentage', names='Category', 
                       title='Estimated Expense Distribution',
                       color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, 
                                              secondary_blue, secondary_pink, secondary_green])
    fig_expenses.update_traces(textposition='inside', textinfo='percent+label')
    fig_expenses.update_layout(title_font=dict(color=primary_blue))
    
    st.plotly_chart(fig_expenses, use_container_width=True)
    
    # Operations progress chart
    fig_ops_progress = go.Figure()
    
    fig_ops_progress.add_trace(go.Bar(
        x=['Asana Adoption', 'Cyber Security', 'Audit Compliance'],
        y=[38, 0, 0],
        name='Current',
        marker_color=primary_blue
    ))
    
    fig_ops_progress.add_trace(go.Bar(
        x=['Asana Adoption', 'Cyber Security', 'Audit Compliance'],
        y=[85, 90, 100],
        name='Goal',
        marker_color=secondary_gold,
        opacity=0.7
    ))
    
    fig_ops_progress.update_layout(
        title='Operations Goals Progress',
        xaxis_title='Metric',
        yaxis_title='Percentage (%)',
        barmode='group',
        height=400,
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(fig_ops_progress, use_container_width=True)
    
    # Download button
    st.markdown("### Download Operations Data")
    
    # Create dataframe for download
    operations_metrics_df = pd.DataFrame({
        "Metric": ["Total Expenses", "Earned Revenue (Store Sales)", "Audit Compliance", 
                  "Cyber Security Compliance", "Asana Adoption"],
        "Value": ["Unknown", "Unknown", "Unknown", "Unknown", "38%"],
        "Goal": ["N/A", "$400,000", "100%", "90%", "85%"],
        "Status": ["N/A", "N/A", "N/A", "N/A", "At Risk"]
    })
    
    st.markdown(download_data(operations_metrics_df, "GirlTREK_Operations_Metrics"), unsafe_allow_html=True)

with tab7:
    st.markdown('<h3 class="section-title">Impact Metrics</h3>', unsafe_allow_html=True)
    
    # Impact metrics - to be reported post Self-Care School 2025
    st.markdown(
        """
        ### Self-Reported Health Improvements
        
        The following metrics will be reported post Self-Care School 2025:
        
        - Women who have reported a change in health knowledge
        - Changes in self-reported mental well-being
        - Number of women who report feeling more connected and less isolated as a result of GirlTREK programming
        - % of participants reporting: Weight loss
        - % of participants reporting: Improved management of chronic conditions (e.g., diabetes, hypertension)
        - % of participants reporting: Reduced medication dependency
        - % of participants reporting: Fewer symptoms of depression or anxiety
        """
    )
    
    # Anticipated impact visualization
    impact_data = {
        'Health Outcome': ['Improved Mental Well-being', 'Feel More Connected', 'Weight Loss', 
                         'Improved Chronic Conditions', 'Reduced Medication', 'Reduced Depression/Anxiety'],
        'Target Percentage': [75, 80, 60, 55, 40, 70]
    }
    df_impact = pd.DataFrame(impact_data)
    
    fig_impact = px.bar(df_impact, x='Health Outcome', y='Target Percentage',
                      title='Anticipated Health Outcomes (Target Percentages)',
                      color='Target Percentage',
                      color_continuous_scale=[primary_blue, primary_orange, primary_yellow])
    
    fig_impact.update_layout(
        xaxis_title='Health Outcome',
        yaxis_title='Target Percentage (%)',
        height=500,
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(fig_impact, use_container_width=True)
    
    # Care Village metrics
    st.markdown("<h4>Care Village Metrics</h4>", unsafe_allow_html=True)
    
    care_col1, care_col2 = st.columns(2)
    
    with care_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL POPULATION REACHED</p>'
            f'<p class="metric-value">Unknown</p>'
            f'<p>Goal: 20,000</p>'
            f'<p class="note-text">Black women impacted through programs & events</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with care_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">HEALTH WORKER TRAINING</p>'
            f'<p class="metric-value">Unknown</p>'
            f'<p>Goal: 4,000</p>'
            f'<p class="note-text">Number of community health workers trained</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    care2_col1, care2_col2 = st.columns(2)
    
    with care2_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">COMMUNITY ENGAGEMENT</p>'
            f'<p class="metric-value">Unknown</p>'
            f'<p>Goal: 40,000</p>'
            f'<p class="note-text">Number of Black women reached in Montgomery, AL</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with care2_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">BRICKLAYERS HALL FUNDRAISING</p>'
            f'<p class="metric-value">Unknown</p>'
            f'<p>Goal: $400,000</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Download button
    st.markdown("### Download Impact Data")
    
    # Create dataframe for download
    care_village_metrics_df = pd.DataFrame({
        "Metric": ["Total Population Reached", "Health Worker Training", 
                  "Community Engagement", "Bricklayers Hall Fundraising"],
        "Value": ["Unknown", "Unknown", "Unknown", "Unknown"],
        "Goal": ["20,000", "4,000", "40,000", "$400,000"],
        "Notes": [
            "Black women impacted through programs & events",
            "Number of community health workers trained",
            "Number of Black women reached in Montgomery, AL",
            ""
        ]
    })
    
    st.markdown(download_data(care_village_metrics_df, "GirlTREK_Care_Village_Metrics"), unsafe_allow_html=True)

with tab8:
    st.markdown('<h3 class="section-title">Member Care Metrics</h3>', unsafe_allow_html=True)
    
    # Member care metrics
    member_col1, member_col2 = st.columns(2)
    
    with member_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">MEMBER SATISFACTION RATING</p>'
            f'<p class="metric-value">95%</p>'
            f'<p>Goal: 85%</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with member_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">RESOLUTION/RESPONSIVENESS RATE</p>'
            f'<p class="metric-value">2 hours</p>'
            f'<p>Goal: 48 hours</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
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
    
    # Inspirational Stories
    st.markdown('<h4>Voices from the Field: Top 3 Inspirational Stories</h4>', unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div class="metric-card">
            <h5>Story 1</h5>
            <p>Crew Leader Nicole Crooks and the South Florida crew understood the assignment during #SisterhoodSaturday! Nicole's post says it best: "Simply grateful!!! #SisterhoodSaturday during Black Maternal Health Week was absolutely everything! A huge thank you to Maya at Historic Virginia Key Beach Park, Kallima and the entire GirlTREK: Healthy Black Women village, Cortes, Jamarrah and the entire https://southernbirthjustice.org/ (SBJN) village, Kedemah and the entire AKA village, Mama Kuks, Mama Joy, Mama Sheila & Mama Wangari (our beautiful village of elders), to each and every sister who came or supported in any way. AND a SUPERDUPER Thank you, thank you, THANK YOU!!! to Kukuwa Fitness and Nakreshia Causey Born Saturday was filled with magic and joy! And yep... you can grab those GirlTREK inspired leggings at https://www.kukuwafitness.com/ I am so ready for this week's #selfcareschool hope you are too!!!"</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div class="metric-card">
            <h5>Story 2</h5>
            <p>Amazing TedTalk used in class! Hello ladies! First and foremost YOU ARE AMAZING. Sending so much love to you all and holding space for your amazing cause. I am a teacher in Ohio and I just wanted to tell you that I am using the TedTalk from 2018 in my Black History in America course. I can't wait to help my students use this frame of understanding. Thank you for shining a light on this - it is so needed!!! Thank you for taking action! Thank you for showing so much loving kindness!!!! I appreciate you all and am so excited for this movement! Much love and respect, Kaitlin Finan kbeeble@gmail.com</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div class="metric-card">
            <h5>Story 3</h5>
            <p>Subject: My Sister's Keeper

Morgan and Vanessa, I walked this evening—first chance I've had in a while. And I talked on the phone to a friend of mine who was also walking at the time and had not walked in a while. I invited her to walk with me and told her about Harriet Day and the meeting last night. I also shared GirlTrek information with her and invited her to join. We're going to start walking together!

I used to walk all the time. I moved back closer to my hometown four years ago to be near Mama and help take care of her. She got better and was doing great, then all of a sudden she wasn't. Mama transitioned to Heaven a little over a year ago and life has been difficult. She was everything to me. It's just been hard—but by the grace of God, I'm still standing. He did bless us with 3 more years after she was hospitalized 33 days. I'm trying to get my legs back under me. But I am lonely for Mama. 99% of the time, I walked alone...didn't have anyone to walk with. But I would listen in some Saturdays. Everybody is a few towns over, so weekday scheduling is tough. But I also told my sisters and my brother that they were going to walk with me as a part of this next 10-week commitment. Thank you for all that you do, Sandy B. Carter sandybcarter@yahoo.com</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Download button
    st.markdown("### Download Member Care Data")
    
    # Create dataframe for download
    member_care_metrics_df = pd.DataFrame({
        "Metric": ["Member Satisfaction Rating", "Resolution/Responsiveness Rate"],
        "Value": ["95%", "2 hours"],
        "Goal": ["85%", "48 hours"]
    })
    
    member_issues_df = pd.DataFrame({
        "Top Member Issues/Concerns": [
            "The App functionality and usability",
            "Join the Movement process and onboarding",
            "Finding local crew events"
        ]
    })
    
    member_care_data = {
        "Member Care Metrics": member_care_metrics_df,
        "Top Member Issues": member_issues_df
    }
    
    selected_member_care_data = st.selectbox("Select data to download:", list(member_care_data.keys()))
    st.markdown(download_data(member_care_data[selected_member_care_data], 
                           f"GirlTREK_{selected_member_care_data.replace(' ', '_')}"), unsafe_allow_html=True)

with tab9:
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
            unsafe_allow_
