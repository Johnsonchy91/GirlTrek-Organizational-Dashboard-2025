import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
import re
import uuid

# Color Scheme
primary_blue = "#0088FF"
primary_orange = "#FF5722"
primary_yellow = "#FFEB3B"
secondary_blue = "#00C8FF"
secondary_orange = "#FF9100"
secondary_teal = "#00E5FF"
secondary_beige = "#FFECB3"
secondary_gold = "#FFC400"
secondary_white = "#FFFFFF"
secondary_gray = "#424242"
secondary_pink = "#FF4081"
secondary_purple = "#AA00FF"
secondary_green = "#00E676"
achieved_green = "#00C853"

dark_bg = "#121212"
dark_card_bg = "#1E1E1E"
dark_text = "#FFFFFF"
dark_secondary_text = "#BBBBBB"

# Helper Functions
def generate_unique_id():
    return str(uuid.uuid4())

def status_badge(status):
    if status == "On Track":
        return f'<span style="background-color: #4CAF50; color: white; padding: 3px 8px; border-radius: 4px;">On Track</span>'
    elif status == "At Risk":
        return f'<span style="background-color: #FF9800; color: white; padding: 3px 8px; border-radius: 4px;">At Risk</span>'
    elif status == "Achieved":
        return f'<span style="background-color: {achieved_green}; color: white; padding: 3px 8px; border-radius: 4px;">Achieved</span>'
    else:
        return f'<span style="background-color: #F44336; color: white; padding: 3px 8px; border-radius: 4px;">Off Track</span>'

def download_data(df, filename):
    try:
        if not isinstance(df, pd.DataFrame):
            return f'<p style="color: red;">Error: Invalid data format for {filename}</p>'
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} data</a>'
        return href
    except Exception as e:
        return f'<p style="color: red;">Error generating download: {str(e)}</p>'

def format_currency(value):
    if isinstance(value, str):
        try:
            clean_value = re.sub(r'[^\d.]', '', value)
            value = float(clean_value)
        except:
            return value
    return f"${value:,.2f}"

def format_number(value):
    if isinstance(value, str):
        try:
            clean_value = value.replace(',', '')
            value = float(clean_value)
        except:
            return value
    return f"{value:,.0f}"

def apply_dark_mode(dark_mode_enabled):
    if dark_mode_enabled:
        st.markdown(
            f"""
            <style>
            .reportview-container .main .block-container {{
                background-color: {dark_bg};
                color: {dark_text};
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: {dark_text} !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            .section-title {
                color: #1E3C72;
                padding-bottom: 10px;
                border-bottom: 2px solid #FF7043;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

# Session State
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'total_membership' not in st.session_state:
    st.session_state.total_membership = 1240394
    st.session_state.new_members = 11356
    st.session_state.total_contributions = 3061104.78
    st.session_state.total_grants = 3055250
    st.session_state.data_loaded = True

# Sidebar
st.sidebar.markdown("### Download Dashboard")
download_options = [
    "Executive Summary", "Recruitment", "Engagement",
    "Development", "Marketing", "Operations",
    "Member Care", "Advocacy", "Impact", "Complete Dashboard"
]
selected_download = st.sidebar.selectbox("Select dashboard section to download:", download_options)

if st.sidebar.button("Generate PDF for Download"):
    st.sidebar.success(f"PDF for {selected_download} has been generated! Click below to download.")
    st.sidebar.markdown(
        f'<a href="#" download="{selected_download}.pdf">Download {selected_download} PDF</a>',
        unsafe_allow_html=True
    )

st.sidebar.markdown("### Dashboard Settings")
show_target_lines = st.sidebar.checkbox("Show Target Lines", value=True)
dark_mode = st.sidebar.checkbox("Dark Mode", value=False)

apply_dark_mode(dark_mode)

# App Title
st.title("GirlTREK Organizational Dashboard")
st.markdown("### Q2 2025 Metrics Overview")
st.markdown("*Data dashboard was published on April 25, 2025*")


# Load dataframes early for faster page load

# New Members by Month (Recruitment)
df_extended = pd.DataFrame({
    'Month': ['Jan-Sep 2024', 'Oct 2024', 'Nov 2024', 'Dec 2024', 'Jan 2025', 'Feb 2025', 'Mar 2025', 'Apr 2025'],
    'New Members': [20008, 1365, 1419, 182, 591, 1588, 4382, 6073],
    'Date': [
        datetime(2024, 9, 30),
        datetime(2024, 10, 1),
        datetime(2024, 11, 1),
        datetime(2024, 12, 1),
        datetime(2025, 1, 1),
        datetime(2025, 2, 1),
        datetime(2025, 3, 1),
        datetime(2025, 4, 1)
    ]
})

# New Members by Age
df_new_age = pd.DataFrame({
    'Age Group': ['18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+', 'Unknown'],
    'New Members': [86, 477, 1771, 2163, 1898, 4961]
})

# Total Membership by Age
df_total_age = pd.DataFrame({
    'Age Group': ['18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+', 'Unknown'],
    'Members': [1803, 16790, 83392, 163951, 106812, 752621]
})

# Top States & Top Cities
df_top_states = pd.DataFrame({
    'State': ['Texas', 'Georgia', 'California', 'New York', 'Florida'],
    'Members': [91101, 86968, 80328, 68538, 66135]
})

df_top_cities = pd.DataFrame({
    'City': ['Chicago', 'Philadelphia', 'Houston', 'Brooklyn', 'Atlanta'],
    'Members': [20645, 17276, 17065, 15602, 13172]
})

# Historic Movement Growth Numbers
df_historic_growth = pd.DataFrame({
    'Year': [
        2012, 2013, 2014, 2015, 2016, 2017,
        2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025
    ],
    'Trekkers': [
        10000, 18675, 21068, 33175, 72789, 116938,
        164982, 373340, 1000000, 1218000, 1214566, 1207517, 1229691, 1240394
    ],
    'New Women': [
        0, 8675, 2393, 12107, 39614, 44149,
        48044, 208358, 626660, 218000, -3434, -7049, 22174, 10703
    ]
})

# Financial Revenue Breakdown
df_finance = pd.DataFrame({
    'Category': ['Donations', 'Grants', 'Corporate Sponsorships', 'Store Sales', 'Other Revenue'],
    'Amount': [1094048.68, 3055250, 130000, 25000, 125000]
})

# Financial Trend Data
finance_trend_data = pd.DataFrame({
    'Month': ['January', 'February', 'March', 'April'],
    'Revenue': [250000, 310000, 450000, 490000],
    'Expenses': [220000, 280000, 350000, 350000],
    'Donations': [180000, 240000, 300000, 374048.68]
})

# Email and Subscriber Activity Data
df_activity = pd.DataFrame({
    'Period': ['30 day', '60 day', '90 day', '6 months'],
    'Openers': [221719, 266461, 272011, 295705],
    'Clickers': [13000, 21147, 22504, 26272]
})

# Badges Claimed
df_badges = pd.DataFrame({
    'Week': ['Week 0', 'Week 1', 'Week 2'],
    'Badges Claimed': [3089, 2061, 2197]
})

# Sample Budget Data for Operations
budget_data = pd.DataFrame({
    'Category': ['Personnel', 'Technology', 'Facilities', 'Marketing', 'Programs', 'Admin'],
    'Budget': [2100000, 850000, 320000, 750000, 1200000, 280000],
    'Actual': [1950000, 790000, 295000, 710000, 1050000, 265000],
    'Percent': [92.9, 92.9, 92.2, 94.7, 87.5, 94.6]
})

# Member Care Data
member_care_data = pd.DataFrame({
    'Metric': ['Member Satisfaction Rating', 'Resolution/Responsiveness Rate', 'Top Member Issues/Concerns'],
    'Goal': ['85%', '48 hours', '-'],
    'Current Total': ['95%', '2 hours', 'The App & Join the Movement']
})

# Advocacy Data
advocacy_data = pd.DataFrame({
    'Metric': ['Advocacy Briefs Published', 'Secure Advocacy Partners'],
    'Goal': ['10', '20'],
    'Current Total': ['4', '2'],
    'Status': ['On Track', 'On Track']
})


# Create Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "Executive Summary",
    "Recruitment",
    "Engagement",
    "Development",
    "Marketing",
    "Operations",
    "Member Care",
    "Advocacy",
    "Impact"
])

# ---------------------------------
# Executive Summary Tab
# ---------------------------------
with tab1:
    st.markdown('<h3 class="section-title">Executive Summary</h3>', unsafe_allow_html=True)

    # --- Key Metrics ---
    st.markdown("<h3>Key Metrics</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL MEMBERSHIP</p>'
            f'<p class="metric-value">{format_number(st.session_state.total_membership)}</p>'
            f'<p>Goal: 2,000,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL NEW MEMBERS</p>'
            f'<p class="metric-value">{format_number(st.session_state.new_members)}</p>'
            f'<p>Goal: 100,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL CONTRIBUTIONS</p>'
            f'<p class="metric-value">{format_currency(st.session_state.total_contributions)}</p>'
            f'<p>Goal: $8,000,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    # --- Report Card Progress ---
    st.markdown('<h3>Report Card Progress</h3>', unsafe_allow_html=True)

    report_data = {
        "Goal": [
            "Recruit 100,000 new members",
            "Engage 250,000 members",
            "Support 65,000 walking daily",
            "Unite 20 advocacy partners",
            "Raise $10M",
            "Establish Care Village",
            "Achieve 85% organizational health"
        ],
        "Current Total": [
            "11,356", "11,769", "4,858", "2",
            "3,061,104.78", "2,869", "Pending"
        ],
        "Percent Progress": [
            "11%", "5%", "7%", "10%", "31%", "7%", "Pending"
        ],
        "Status": [
            "On Track", "On Track", "At Risk", "At Risk",
            "On Track", "At Risk", "Pending"
        ],
        "Progress": [
            11.4, 4.7, 7.5, 10, 30.6, 7.2, 0
        ]
    }

    for i in range(len(report_data["Goal"])):
        goal = report_data["Goal"][i]
        current = report_data["Current Total"][i]
        percent = report_data["Percent Progress"][i]
        status = report_data["Status"][i]
        progress = report_data["Progress"][i]

        if status == "On Track":
            bar_color = "#4CAF50"
        elif status == "Achieved":
            bar_color = achieved_green
        elif status == "At Risk":
            bar_color = "#FF9800"
        else:
            bar_color = secondary_gray

        progress_html = f"""
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
        """
        st.markdown(progress_html, unsafe_allow_html=True)

    # --- Membership Distribution ---
    st.markdown('<h3>Membership Distribution</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        exec_fig_new_age = px.pie(
            df_new_age,
            values='New Members',
            names='Age Group',
            title='New Members by Age Group',
            color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, secondary_pink, secondary_purple, secondary_green]
        )
        exec_fig_new_age.update_traces(textposition='inside', textinfo='percent+label')
        exec_fig_new_age.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(exec_fig_new_age, use_container_width=True, key="exec_fig_new_age")

    with col2:
        exec_fig_total_age = px.bar(
            df_total_age,
            x='Age Group',
            y='Members',
            title='Total Membership by Age Group',
            color='Members',
            color_continuous_scale=[secondary_purple, primary_blue, secondary_pink]
        )
        exec_fig_total_age.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(exec_fig_total_age, use_container_width=True, key="exec_fig_total_age")

    # --- Top States ---
    st.markdown('<h3>Top States</h3>', unsafe_allow_html=True)

    states_fig = px.bar(
        df_top_states,
        x='State',
        y='Members',
        title='Top 5 States by Membership',
        color='Members',
        color_continuous_scale=[primary_blue, secondary_purple]
    )
    states_fig.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(states_fig, use_container_width=True, key="states_fig")

    # --- Top Cities ---
    st.markdown('<h3>Top Cities</h3>', unsafe_allow_html=True)

    cities_fig = px.bar(
        df_top_cities,
        x='City',
        y='Members',
        title='Top 5 Cities by Membership',
        color='Members',
        color_continuous_scale=[primary_blue, secondary_orange]
    )
    cities_fig.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(cities_fig, use_container_width=True, key="cities_fig")

    # --- Historic Movement Growth (as graph) ---
    st.markdown("<h3>Historic Movement Growth Numbers</h3>", unsafe_allow_html=True)

    historic_fig = go.Figure()

    historic_fig.add_trace(go.Scatter(
        x=df_historic_growth['Year'],
        y=df_historic_growth['Trekkers'],
        mode='lines+markers',
        name='Trekkers',
        line=dict(color=primary_blue, width=3),
        marker=dict(size=8)
    ))

    historic_fig.update_layout(
        title='Historic Growth of Trekkers (2012–2025)',
        xaxis_title='Year',
        yaxis_title='Total Trekkers',
        title_font=dict(color=primary_blue),
        height=400
    )

    st.plotly_chart(historic_fig, use_container_width=True, key="historic_growth_fig")
# ---------------------------------
# Recruitment Tab
# ---------------------------------
with tab2:
    st.markdown('<h3 class="section-title">Recruitment Metrics</h3>', unsafe_allow_html=True)

    recruitment_col1, recruitment_col2, recruitment_col3 = st.columns(3)

    with recruitment_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL NEW MEMBERS</p>'
            f'<p class="metric-value">{format_number(st.session_state.new_members)}</p>'
            f'<p>Goal: 100,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with recruitment_col2:
        new_members_18_30 = df_new_age.loc[
            df_new_age['Age Group'].isin(['18 to 24', '25 to 34']),
            'New Members'
        ].sum()

        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">NEW MEMBERS AGE 18-30</p>'
            f'<p class="metric-value">{format_number(new_members_18_30)}</p>'
            f'<p>Goal: 50,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with recruitment_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL RECRUITMENT PARTNERSHIPS</p>'
            f'<p class="metric-value">2</p>'
            f'<p>Goal: 20</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    recruit_monthly_fig = px.bar(
        df_extended,
        x='Month',
        y='New Members',
        title='New Member Contacts (2024-2025)',
        color='New Members',
        color_continuous_scale=[secondary_blue, primary_blue, primary_orange]
    )
    recruit_monthly_fig.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(recruit_monthly_fig, use_container_width=True, key="recruit_monthly_fig")

# ---------------------------------
# Engagement Tab
# ---------------------------------
with tab3:
    st.markdown('<h3 class="section-title">Engagement Metrics</h3>', unsafe_allow_html=True)

    engagement_col1, engagement_col2 = st.columns(2)

    with engagement_col1:
        st.markdown(
            f'<div class="engagement-metric-card">'
            f'<p class="metric-title">TOTAL ACTIVE CREWS</p>'
            f'<p class="metric-value">603</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with engagement_col2:
        st.markdown(
            f'<div class="engagement-metric-card">'
            f'<p class="metric-title">MEMBERS WALKING DAILY</p>'
            f'<p class="metric-value">4,788</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    engage_badges_fig = px.bar(
        df_badges,
        x='Week',
        y='Badges Claimed',
        title='Badges Claimed by Week',
        color='Badges Claimed',
        color_continuous_scale=[secondary_green, primary_blue, secondary_purple]
    )
    engage_badges_fig.update_layout(title_font=dict(color=primary_blue))

    if show_target_lines:
        engage_badges_fig.add_shape(
            type="line",
            x0=-0.5,
            y0=5000,
            x1=len(df_badges)-0.5,
            y1=5000,
            line=dict(color="red", width=2, dash="dash")
        )

    st.plotly_chart(engage_badges_fig, use_container_width=True, key="engage_badges_fig")

# ---------------------------------
# Development Tab
# ---------------------------------
with tab4:
    st.markdown('<h3 class="section-title">Development Metrics</h3>', unsafe_allow_html=True)

    dev_col1, dev_col2, dev_col3 = st.columns(3)

    with dev_col1:
        st.markdown(
            f'<div class="dev-metric-card">'
            f'<p class="dev-metric-title">TOTAL CONTRIBUTIONS</p>'
            f'<p class="dev-metric-value">{format_currency(st.session_state.total_contributions)}</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with dev_col2:
        st.markdown(
            f'<div class="dev-metric-card">'
            f'<p class="dev-metric-title">TOTAL GRANTS</p>'
            f'<p class="dev-metric-value">{format_currency(st.session_state.total_grants)}</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with dev_col3:
        st.markdown(
            f'<div class="dev-metric-card">'
            f'<p class="dev-metric-title">CORPORATE SPONSORSHIPS</p>'
            f'<p class="dev-metric-value">$130,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    dev_finance_fig = px.pie(
        df_finance,
        values='Amount',
        names='Category',
        title='Revenue Distribution',
        color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, secondary_blue, secondary_orange]
    )
    dev_finance_fig.update_traces(textposition='inside', textinfo='percent+label')
    dev_finance_fig.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(dev_finance_fig, use_container_width=True, key="dev_finance_fig")

    dev_trend_fig = go.Figure()

    dev_trend_fig.add_trace(go.Scatter(
        x=finance_trend_data['Month'],
        y=finance_trend_data['Revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color=primary_blue)
    ))
    dev_trend_fig.add_trace(go.Scatter(
        x=finance_trend_data['Month'],
        y=finance_trend_data['Expenses'],
        mode='lines+markers',
        name='Expenses',
        line=dict(color=primary_orange)
    ))
    dev_trend_fig.add_trace(go.Scatter(
        x=finance_trend_data['Month'],
        y=finance_trend_data['Donations'],
        mode='lines+markers',
        name='Donations',
        line=dict(color=primary_yellow)
    ))

    dev_trend_fig.update_layout(
        title='Financial Trends',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        title_font=dict(color=primary_blue),
        height=400
    )

    st.plotly_chart(dev_trend_fig, use_container_width=True, key="dev_trend_fig")

# ---------------------------------
# Marketing Tab
# ---------------------------------
with tab5:
    st.markdown('<h3 class="section-title">Marketing Metrics</h3>', unsafe_allow_html=True)

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
            f'<p>31.9% of Total</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    marketing_activity_fig = go.Figure()

    marketing_activity_fig.add_trace(go.Bar(
        x=df_activity['Period'],
        y=df_activity['Openers'],
        name='Openers',
        marker_color=primary_blue
    ))

    marketing_activity_fig.add_trace(go.Bar(
        x=df_activity['Period'],
        y=df_activity['Clickers'],
        name='Clickers',
        marker_color=primary_orange
    ))

    marketing_activity_fig.update_layout(
        title='Subscriber Activity',
        xaxis_title='Time Period',
        yaxis_title='Subscribers',
        barmode='group',
        title_font=dict(color=primary_blue)
    )

    st.plotly_chart(marketing_activity_fig, use_container_width=True, key="marketing_activity_fig")
    
    # Add text messaging engagement
    st.markdown("<h3>Text Message Engagement</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background-color: #f7f7f7; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            <p><strong>Text Message Engagement (Clicks):</strong> 6.27%</p>
            <p><em>Industry Standard: SMS messages boast click-through rates of 6.3% for fundraising messages and 10% for advocacy messages.</em></p>
            <p><strong>Text Messaging Spend:</strong> $11,180.21</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------
# Operations Tab (Updated with real data)
# ---------------------------------
with tab6:
    st.markdown('<h3 class="section-title">Operations Metrics</h3>', unsafe_allow_html=True)

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

    ops2_col1, ops2_col2 = st.columns(2)

    with ops2_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">ASANA ADOPTION</p>'
            f'<p class="metric-value">38%</p>'
            f'<p>Goal: 85%</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with ops2_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">CYBER SECURITY COMPLIANCE</p>'
            f'<p class="metric-value">Unknown</p>'
            f'<p>Goal: 90%</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    # Financial Trends 
    st.markdown('<h3>Financial Trends</h3>', unsafe_allow_html=True)

    ops_trend_fig = go.Figure()

    ops_trend_fig.add_trace(go.Scatter(
        x=finance_trend_data['Month'],
        y=finance_trend_data['Revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color=primary_blue)
    ))
    ops_trend_fig.add_trace(go.Scatter(
        x=finance_trend_data['Month'],
        y=finance_trend_data['Expenses'],
        mode='lines+markers',
        name='Expenses',
        line=dict(color=primary_orange)
    ))
    ops_trend_fig.add_trace(go.Scatter(
        x=finance_trend_data['Month'],
        y=finance_trend_data['Donations'],
        mode='lines+markers',
        name='Donations',
        line=dict(color=primary_yellow)
    ))

    ops_trend_fig.update_layout(
        title='Financial Trends',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        title_font=dict(color=primary_blue),
        height=400
    )

    st.plotly_chart(ops_trend_fig, use_container_width=True, key="ops_trend_fig")

# ---------------------------------
# Member Care Tab (real data from PDF)
# ---------------------------------
with tab7:
    st.markdown('<h3 class="section-title">Member Care Metrics</h3>', unsafe_allow_html=True)

    mc_col1, mc_col2 = st.columns(2)

    with mc_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">MEMBER SATISFACTION RATING</p>'
            f'<p class="metric-value">95%</p>'
            f'<p>Goal: 85%</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with mc_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">RESOLUTION/RESPONSIVENESS RATE</p>'
            f'<p class="metric-value">2 hours</p>'
            f'<p>Goal: 48 hours</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('<h3>Top Member Issues/Concerns</h3>', unsafe_allow_html=True)
    st.markdown(
        """
        - The App & Join the Movement
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<h3>Voices from the Field: Top Inspirational Stories</h3>', unsafe_allow_html=True)
    
    with st.expander("Story 1: Crew Leader Nicole Crooks and the South Florida crew"):
        st.markdown(
            """
            Crew Leader Nicole Crooks and the South Florida crew understood the assignment during #SisterhoodSaturday! 
            Nicole's post says it best: "Simply grateful!!! #SisterhoodSaturday during Black Maternal Health Week was absolutely everything! 
            A huge thank you to Maya at Historic Virginia Key Beach Park, Kallima and the entire GirlTREK: Healthy Black Women village, 
            Cortes, Jamarrah and the entire https://southernbirthjustice.org/ (SBJN) village, Kedemah and the entire AKA village, 
            Mama Kuks, Mama Joy, Mama Sheila & Mama Wangari (our beautiful village of elders), to each and every sister who came or 
            supported in any way. AND a SUPER DUPER Thank you, thank you, THANK YOU!!! to Kukuwa Fitness and Nakreshia Causey Borno 
            Saturday was filled with magic and joy! And yep... you can grab those GirlTREK inspired leggings at https://www.kukuwafitness.com/ 
            I am so ready for this week's #selfcareschool hope you are too!!!"
            """
        )
    
    with st.expander("Story 2: Amazing Ted Talk used in class!"):
        st.markdown(
            """
            Hello ladies! First and foremost YOU ARE AMAZING. Sending so much love to you all and holding space for your amazing cause. 
            I am a teacher in Ohio and I just wanted to tell you that I am using the TedTalk from 2018 in my Black History in America course. 
            I can't wait to help my students use this frame of understanding. Thank you for shining a light on this - it is so needed!!! 
            Thank you for taking action! Thank you for showing so much loving kindness!!!! I appreciate you all and am so excited for this movement! 
            Much love and respect, Kaitlin Finan
            """
        )
    
    with st.expander("Story 3: My Sister's Keeper"):
        st.markdown(
            """
            Morgan and Vanessa, I walked this evening_ first chance I've had in a while. And I talked on the phone to a friend of mine who was 
            also walking at the time and had not walked in a while. I invited her to walk with me and told her about Harriet Day and the meeting 
            last night. I also shared GirlTREK information with her and invited her to join. We're going to start walking together!
            
            I used to walk all the time. I moved back closer to my hometown a four years ago to be near Mama and help take care of her. 
            She got better and was doing great, then all of a sudden she wasn't. Mama transitioned to Heaven a little over a year ago and 
            life has been difficult. She was everything to me. It's just been hard_ but by the grace of God, I'm still standing. 
            He did bless us with 3 more years after she was hospitalized 33 days. I'm trying to get my legs back under me. But I am lonely for Mama.
            
            99% of the time, I walked alone…didn't have anyone to walk with. But I would listen in some Saturdays. Everybody is a few towns over, 
            so weekday scheduling is tough. But I also told my sisters and my brother that they were going to walk with me as a part of this 
            next 10-week commitment.
            
            Thank you for all that you do, Sandy B. Carter
            """
        )

# ---------------------------------
# Advocacy Tab (real data from PDF)
# ---------------------------------
with tab8:
    st.markdown('<h3 class="section-title">Advocacy Metrics</h3>', unsafe_allow_html=True)

    adv_col1, adv_col2 = st.columns(2)

    with adv_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">ADVOCACY BRIEFS PUBLISHED</p>'
            f'<p class="metric-value">4 / 10</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with adv_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">ADVOCACY PARTNERSHIPS</p>'
            f'<p class="metric-value">2 / 20</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('<h3>Current Focus Areas</h3>', unsafe_allow_html=True)
    st.markdown(
        """
        - Produce advocacy briefs establishing research basis for why each J&J agenda item leads to an increase in Black women's life expectancy
        - Uplift best-in-class organizations
        - Secure advocacy partners that align with GirlTREK's Joy & Justice Agenda through signed MOUs
        """,
        unsafe_allow_html=True
    )

# ---------------------------------
# Impact Tab (still marked as Pending)
# ---------------------------------
with tab9:
    st.markdown('<h3 class="section-title">Impact Metrics</h3>', unsafe_allow_html=True)

    st.markdown(
        """
        <p>GirlTREK's community health impact reporting will be updated following Self-Care School 2025 outcomes.</p>
        <p>Metrics to be reported post Self-Care School 2025:</p>
        <ul>
            <li>Women who have reported a change in health knowledge</li>
            <li>Changes in self-reported mental well-being</li>
            <li>Number of women who report feeling more connected and less isolated as a result of GirlTREK programming</li>
            <li>% of participants reporting weight loss</li>
            <li>% of participants reporting improved management of chronic conditions (e.g., diabetes, hypertension)</li>
            <li>% of participants reporting reduced medication dependency</li>
            <li>% of participants reporting fewer symptoms of depression or anxiety</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

