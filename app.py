import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
import re
import uuid  # Import UUID library to generate unique IDs

# Define color scheme
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

# Dark mode colors
dark_bg = "#121212"
dark_card_bg = "#1E1E1E"
dark_text = "#FFFFFF"
dark_secondary_text = "#BBBBBB"

# Helper functions
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
# Create session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'total_membership' not in st.session_state:
    st.session_state.total_membership = 1240394
    st.session_state.new_members = 11356
    st.session_state.total_contributions = 3061104.78
    st.session_state.total_grants = 3055250
    st.session_state.data_loaded = True

# Sidebar controls
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

# Apply dark mode
apply_dark_mode(dark_mode)

# Page Title
st.title("GirlTREK Organizational Dashboard")
st.markdown("### Q2 2025 Metrics Overview")
st.markdown("*Data dashboard was published on April 25, 2025*")

# Data for charts
extended_month_data = {
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
}
df_extended = pd.DataFrame(extended_month_data)

new_age_data = {
    'Age Group': ['18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+', 'Unknown'],
    'New Members': [86, 477, 1771, 2163, 1898, 4961]
}
df_new_age = pd.DataFrame(new_age_data)

total_age_data = {
    'Age Group': ['18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+', 'Unknown'],
    'Members': [1803, 16790, 83392, 163951, 106812, 752621]
}
df_total_age = pd.DataFrame(total_age_data)

states_data = {
    'State': ['Texas', 'Georgia', 'California', 'New York', 'Florida'],
    'Members': [91101, 86968, 80328, 68538, 66135],
    'Region': ['Southwest', 'Southeast', 'West', 'Northeast', 'Southeast']
}
df_states = pd.DataFrame(states_data)

cities_data = {
    'City': ['Chicago', 'Philadelphia', 'Houston', 'Brooklyn', 'Atlanta'],
    'Members': [20645, 17276, 17065, 15602, 13172],
    'Region': ['Midwest', 'Northeast', 'Southwest', 'Northeast', 'Southeast']
}
df_cities = pd.DataFrame(cities_data)

# Create tabs
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

with tab1:
    st.markdown('<h3 class="section-title">Executive Summary</h3>', unsafe_allow_html=True)
    
    # Key metrics
    st.markdown("<h3>Key Metrics</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

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

    # Report Card Progress Section
    st.markdown('<h3>Report Card Progress</h3>', unsafe_allow_html=True)

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
        else:
            bar_color = "#FF9800"

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
    # Membership Distribution
    st.markdown('<h3>Membership Distribution</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        # New Members by Age - Pie Chart
        exec_fig_new_age = px.pie(
            df_new_age,
            values='New Members',
            names='Age Group',
            title='New Members by Age Group',
            color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, secondary_pink, secondary_purple, secondary_green]
        )
        exec_fig_new_age.update_traces(textposition='inside', textinfo='percent+label')
        exec_fig_new_age.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(exec_fig_new_age, use_container_width=True)

    with col2:
        # Total Membership by Age - Bar Chart
        exec_fig_total_age = px.bar(
            df_total_age,
            x='Age Group',
            y='Members',
            title='Total Membership by Age Group',
            color='Members',
            color_continuous_scale=[secondary_purple, primary_blue, secondary_pink]
        )
        exec_fig_total_age.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(exec_fig_total_age, use_container_width=True)

    # Historic Movement Growth Numbers
    st.markdown("<h3>Historic Movement Growth Numbers</h3>", unsafe_allow_html=True)

    historic_col1, historic_col2 = st.columns(2)

    with historic_col1:
        st.markdown("""
        * **2012**
            * Trekkers: 10,000
            * New Women: N/A
        * **2013**
            * Trekkers: 18,675
            * New Women: 8,675
        * **2014**
            * Trekkers: 21,068
            * New Women: 2,393
        * **2015**
            * Trekkers: 33,175
            * New Women: 12,107
        * **2016**
            * Trekkers: 72,789
            * New Women: 39,614
        * **2017**
            * Trekkers: 116,938
            * New Women: 44,149
        * **2018**
            * Trekkers: 164,982
            * New Women: 48,044
        """)

    with historic_col2:
        st.markdown("""
        * **2019**
            * Trekkers: 373,340
            * New Women: 208,358
        * **2020**
            * Trekkers: 1,000,000
            * New Women: 626,660
        * **2021**
            * Trekkers: 1,218,000
            * New Women: 218,000
        * **2022**
            * Trekkers: 1,214,566
            * New Women: -3,434
        * **2023**
            * Trekkers: 1,207,517
            * New Women: -7,049
        * **2024**
            * Trekkers: 1,229,691
            * New Women: 22,174
        * **2025**
            * Trekkers: 1,240,394
            * New Women: 10,703
        """)

    st.markdown("""
    **Notes:**
    * 2022 and 2023 show negative growth.
    * 2019–2020 had the biggest spike (167%+ growth).
    """)

    # Create simple Executive Summary DataFrame for download
    report_df = pd.DataFrame([
        {"Goal": report_data["Goal"][i],
         "Current Total": report_data["Current Total"][i],
         "Percent Progress": report_data["Percent Progress"][i],
         "Status": report_data["Status"][i]}
        for i in range(len(report_data["Goal"]))
    ])
    st.markdown(download_data(report_df, "GirlTREK_Executive_Summary"), unsafe_allow_html=True)
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
            f'<p class="metric-title">TOTAL NEW MEMBERS AGE 18-30</p>'
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
            f'<p class="metric-value">0</p>'
            f'<p>Goal: 100</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'<p class="note-text">Contact made with 20 community organizations.</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    # New Members by Month - Bar Chart
    recruit_monthly_fig = px.bar(
        df_extended,
        x='Month',
        y='New Members',
        title='New Member Contacts (2024-2025)',
        color='New Members',
        color_continuous_scale=[secondary_blue, primary_blue, primary_orange]
    )

    recruit_monthly_fig.add_annotation(
        x='Jan-Sep 2024',
        y=20008,
        text='20,008 total contacts',
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )

    recruit_monthly_fig.add_annotation(
        x='Mar 2025',
        y=4382,
        text='177% increase',
        showarrow=True,
        arrowhead=1,
        ax=40,
        ay=-40
    )

    recruit_monthly_fig.add_annotation(
        x='Apr 2025',
        y=6073,
        text='39% increase',
        showarrow=True,
        arrowhead=1,
        ax=40,
        ay=-40
    )

    recruit_monthly_fig.update_layout(
        title_font=dict(color=primary_blue),
        yaxis_title='Number of New Contacts',
        xaxis_title='Month',
        height=500
    )

    st.plotly_chart(recruit_monthly_fig, use_container_width=True)

    # Membership by Age - Pie Chart
    st.markdown('<h3>Membership Distribution</h3>', unsafe_allow_html=True)

    recruit_age_fig = px.pie(
        df_new_age,
        values='New Members',
        names='Age Group',
        title='New Members by Age Group',
        color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, secondary_pink, secondary_purple, secondary_green]
    )
    recruit_age_fig.update_traces(textposition='inside', textinfo='percent+label')
    recruit_age_fig.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(recruit_age_fig, use_container_width=True)

    # Total Membership by Age - Bar Chart
    recruit_total_age_fig = px.bar(
        df_total_age,
        x='Age Group',
        y='Members',
        title='Total Membership by Age Group',
        color='Members',
        color_continuous_scale=[secondary_purple, primary_blue, secondary_pink]
    )
    recruit_total_age_fig.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(recruit_total_age_fig, use_container_width=True)

    # Download Section for Recruitment
    st.markdown("### Download Recruitment Data")
    
    recruitment_data = {
        "Monthly New Members": df_extended,
        "New Members by Age": df_new_age,
        "Total Members by Age": df_total_age
    }
    
    selected_data = st.selectbox("Select data to download:", list(recruitment_data.keys()))
    st.markdown(download_data(recruitment_data[selected_data], f"GirlTREK_{selected_data.replace(' ', '_')}"), unsafe_allow_html=True)

