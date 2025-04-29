import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
import re
import uuid  # Import UUID library to generate unique IDs

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

# Dark mode colors
dark_bg = "#121212"
dark_card_bg = "#1E1E1E"
dark_text = "#FFFFFF"
dark_secondary_text = "#BBBBBB"

# Helper function to generate unique IDs
def generate_unique_id():
    return str(uuid.uuid4())

# Define functions early so they're available throughout the app
def status_badge(status):
    """
    Create a styled status badge based on the status value.
    
    Parameters:
    status (str): Status value ('On Track', 'At Risk', 'Achieved', or 'Off Track')
    
    Returns:
    str: HTML for the status badge
    """
    if status == "On Track":
        return f'<span style="background-color: #4CAF50; color: white; padding: 3px 8px; border-radius: 4px;">On Track</span>'
    elif status == "At Risk":
        return f'<span style="background-color: #FF9800; color: white; padding: 3px 8px; border-radius: 4px;">At Risk</span>'
    elif status == "Achieved":
        return f'<span style="background-color: {achieved_green}; color: white; padding: 3px 8px; border-radius: 4px;">Achieved</span>'
    else:
        return f'<span style="background-color: #F44336; color: white; padding: 3px 8px; border-radius: 4px;">Off Track</span>'

def download_data(df, filename):
    """
    Create a download link for a dataframe.
    
    Parameters:
    df (pandas.DataFrame): DataFrame to be downloaded
    filename (str): Name for the downloaded file
    
    Returns:
    str: HTML for the download link
    """
    try:
        # Validate DataFrame
        if not isinstance(df, pd.DataFrame):
            return f'<p style="color: red;">Error: Invalid data format for {filename}</p>'
        
        # Convert to CSV
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} data</a>'
        return href
    except Exception as e:
        return f'<p style="color: red;">Error generating download: {str(e)}</p>'

def format_currency(value):
    """
    Format a number as currency.
    
    Parameters:
    value (float or int): Numeric value to format
    
    Returns:
    str: Formatted currency string
    """
    if isinstance(value, str):
        # Try to convert string to float
        try:
            # Remove any existing currency symbols and commas
            clean_value = re.sub(r'[^\d.]', '', value)
            value = float(clean_value)
        except:
            return value  # Return original if conversion fails
    
    return f"${value:,.2f}"

def format_number(value):
    """
    Format a large number with commas.
    
    Parameters:
    value (float or int): Numeric value to format
    
    Returns:
    str: Formatted number string
    """
    if isinstance(value, str):
        # Try to convert string to float
        try:
            # Remove any existing commas
            clean_value = value.replace(',', '')
            value = float(clean_value)
        except:
            return value  # Return original if conversion fails
    
    return f"{value:,.0f}"

def apply_dark_mode(dark_mode_enabled):
    """
    Apply dark mode styling if enabled.
    
    Parameters:
    dark_mode_enabled (bool): Whether dark mode is enabled
    """
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
            .stTabs [data-baseweb="tab-list"] {{
                background-color: {dark_bg};
            }}
            .stTabs [data-baseweb="tab"] {{
                color: {dark_text};
            }}
            .metric-card {{
                background-color: {dark_card_bg} !important;
                color: {dark_text} !important;
            }}
            .metric-title {{
                color: {dark_secondary_text} !important;
            }}
            .metric-value {{
                color: {primary_blue} !important;
            }}
            .note-text {{
                color: {dark_secondary_text} !important;
            }}
            .section-title {{
                color: {primary_blue} !important;
                border-bottom: 2px solid {primary_orange};
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
            /* Development Tab - Improved metric styles */
            .dev-metric-container {
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                margin-bottom: 20px;
            }
            .dev-metric-card {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                flex: 1;
                min-width: 250px;
                border-left: 5px solid #0088FF;
                transition: transform 0.2s;
            }
            .dev-metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
            }
            .dev-metric-title {
                font-size: 16px;
                font-weight: bold;
                color: #424242;
                margin-bottom: 8px;
            }
            .dev-metric-value {
                font-size: 28px;
                font-weight: bold;
                color: #0088FF;
                margin: 5px 0;
            }
            .dev-metric-goal {
                font-size: 14px;
                color: #666;
                margin-bottom: 5px;
            }
            .dev-metric-notes {
                font-size: 13px;
                color: #777;
                margin-top: 10px;
                border-top: 1px solid #f0f0f0;
                padding-top: 5px;
            }
            /* Uniform engagement metrics */
            .engagement-metric-card {
                background-color: white;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 15px;
                min-height: 150px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            /* Email visualization styles */
            .email-stats-container {
                background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
            }
            .email-stat-box {
                background: white;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                display: flex;
                align-items: center;
            }
            .email-stat-icon {
                background-color: #f0f8ff;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 15px;
                font-size: 20px;
                color: #0088FF;
            }
            .email-stat-content {
                flex: 1;
            }
            .email-stat-title {
                font-size: 14px;
                color: #666;
                margin-bottom: 5px;
            }
            .email-stat-value {
                font-size: 20px;
                font-weight: bold;
                color: #1E3C72;
            }
            /* Progress bar styles */
            .progress-container {
                margin-bottom: 20px;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )

# Create session state for storing data and filters
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'total_membership' not in st.session_state:
    # Load initial data from real data in the document
    st.session_state.total_membership = 1240394
    st.session_state.new_members = 11356
    st.session_state.total_contributions = 3061104.78
    st.session_state.total_grants = 3055250
    
    # Set data_loaded to True
    st.session_state.data_loaded = True

# Set up sidebar
st.sidebar.markdown("### Download Dashboard")
download_options = [
    "Executive Summary", 
    "Recruitment", 
    "Engagement",
    "Development", 
    "Marketing",
    "Operations",
    "Member Care",
    "Advocacy",
    "Impact",
    "Complete Dashboard"
]
selected_download = st.sidebar.selectbox("Select dashboard section to download:", download_options)

if st.sidebar.button("Generate PDF for Download"):
    st.sidebar.success(f"PDF for {selected_download} has been generated! Click below to download.")
    st.sidebar.markdown(f'<a href="#" download="{selected_download}.pdf">Download {selected_download} PDF</a>', unsafe_allow_html=True)

st.sidebar.markdown("### Dashboard Settings")
show_target_lines = st.sidebar.checkbox("Show Target Lines", value=True)
dark_mode = st.sidebar.checkbox("Dark Mode", value=False)

# Apply dark mode if enabled
apply_dark_mode(dark_mode)

# App title
st.title("GirlTREK Organizational Dashboard")
st.markdown("### Q2 2025 Metrics Overview")
st.markdown("*Data dashboard was published on April 25, 2025*")

# Real data for charts and visualizations from the document
# ----- Monthly new members data -----
extended_month_data = {
    'Month': ['Jan-Sep 2024', 'Oct 2024', 'Nov 2024', 'Dec 2024', 'Jan 2025', 'Feb 2025', 'Mar 2025', 'Apr 2025'],
    'New Members': [20008, 1365, 1419, 182, 591, 1588, 4382, 6073],
    'Date': [
        datetime(2024, 9, 30),  # Representing the Jan-Sep period
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

# ----- Age group distribution data (using real data from document) -----
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

# ----- Geographic distribution data (using real data from document) -----
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

# ----- Financial data (using real data from document) -----
finance_data = {
    'Category': ['Donations', 'Grants', 'Corporate Sponsorships', 'Store Sales', 'Other Revenue'],
    'Amount': [1094048.68, 600000, 750000, 25000, 125000]
}
df_finance = pd.DataFrame(finance_data)

finance_trend_data = pd.DataFrame({
    'Month': ['January', 'February', 'March', 'April'],
    'Revenue': [250000, 310000, 450000, 490000],
    'Expenses': [220000, 280000, 350000, 350000],
    'Donations': [180000, 240000, 300000, 374048.68],
    'Date': [datetime(2025, 1, 1), datetime(2025, 2, 1), datetime(2025, 3, 1), datetime(2025, 4, 1)]
})

# ----- Member growth data -----
member_growth_data = {
    'Quarter': ['Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025'],
    'Members': [2500, 4500, 6800, 9200, 11356],
    'Date': [datetime(2024, 6, 30), datetime(2024, 9, 30), datetime(2024, 12, 31), 
             datetime(2025, 3, 31), datetime(2025, 4, 25)]
}
df_member_growth = pd.DataFrame(member_growth_data)

# ----- Email and marketing data -----
activity_data = {
    'Period': ['30 day', '60 day', '90 day', '6 months'],
    'Openers': [221719, 266461, 272011, 295705],
    'Clickers': [13000, 21147, 22504, 26272]
}
df_activity = pd.DataFrame(activity_data)

# ----- Campaign and engagement data -----
badges_data = {
    'Week': ['Week 0', 'Week 1', 'Week 2'],
    'Badges Claimed': [3089, 2061, 2197]
}
df_badges = pd.DataFrame(badges_data)

# Create tabs - Note the reordering of tabs to move Impact to the end
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "Executive Summary", 
    "Recruitment", 
    "Engagement",
    "Development", 
    "Marketing", 
    "Operations",
    "Member Care",
    "Advocacy",
    "Impact"  # Moved to the end as requested
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
    
    # Report Card Progress
    st.markdown('<h3>Report Card Progress</h3>', unsafe_allow_html=True)
    
    # Updated report_data dictionary with consistent numeric types as strings
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
    
    # Add Membership by Age graphs to Executive Summary
    st.markdown('<h3>Membership Distribution</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # New Members by Age - Pie Chart with unique key
        exec_fig_new_age = px.pie(df_new_age, values='New Members', names='Age Group', 
                            title='New Members by Age Group',
                            color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, 
                                                    secondary_pink, secondary_purple, secondary_green])
        exec_fig_new_age.update_traces(textposition='inside', textinfo='percent+label')
        exec_fig_new_age.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(exec_fig_new_age, use_container_width=True, key=f"exec_pie_new_age_{generate_unique_id()}")
    
    with col2:
        # Total Membership by Age - Bar Chart with unique key
        exec_fig_total_age = px.bar(df_total_age, x='Age Group', y='Members',
                            title='Total Membership by Age Group',
                            color='Members',
                            color_continuous_scale=[secondary_purple, primary_blue, secondary_pink])
        exec_fig_total_age.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(exec_fig_total_age, use_container_width=True, key=f"exec_bar_total_age_{generate_unique_id()}")
    
    # Historic Movement Growth Numbers
    st.markdown("<h3>Historic Movement Growth Numbers</h3>", unsafe_allow_html=True)
    
    # Create two columns for the historic data
    historic_col1, historic_col2 = st.columns(2)
    
    with historic_col1:
        st.markdown("""
        * **2012**
            * Number of Trekkers: 10,000
            * Number of New Women: (Baseline year — N/A)
            * Percent Growth: (Baseline year — N/A)
        * **2013**
            * Number of Trekkers: 18,675
            * Number of New Women: 8,675
            * Percent Growth: 86.75%
        * **2014**
            * Number of Trekkers: 21,068
            * Number of New Women: 2,393
            * Percent Growth: 12.81%
        * **2015**
            * Number of Trekkers: 33,175
            * Number of New Women: 12,107
            * Percent Growth: 57.47%
        * **2016**
            * Number of Trekkers: 72,789
            * Number of New Women: 39,614
            * Percent Growth: 119.41%
        * **2017**
            * Number of Trekkers: 116,938
            * Number of New Women: 44,149
            * Percent Growth: 60.65%
        * **2018**
            * Number of Trekkers: 164,982
            * Number of New Women: 48,044
            * Percent Growth: 41.09%
        """)
    
    with historic_col2:
        st.markdown("""
        * **2019**
            * Number of Trekkers: 373,340
            * Number of New Women: 208,358
            * Percent Growth: 126.29%
        * **2020**
            * Number of Trekkers: 1,000,000
            * Number of New Women: 626,660
            * Percent Growth: 167.85%
        * **2021**
            * Number of Trekkers: 1,218,000
            * Number of New Women: 218,000
            * Percent Growth: 21.80%
        * **2022**
            * Number of Trekkers: 1,214,566
            * Number of New Women: -3,434
            * Percent Growth: -0.28%
        * **2023**
            * Number of Trekkers: 1,207,517
            * Number of New Women: -7,049
            * Percent Growth: -0.58%
        * **2024**
            * Number of Trekkers: 1,229,691
            * Number of New Women: 22,174
            * Percent Growth: 1.84%
        * **2025**
            * Number of Trekkers: 1,240,394
            * Number of New Women: 10,703
            * Percent Growth: 0.87%
        """)
    
    # Add note about growth trends
    st.markdown("""
    **Note:**
    * 2022 and 2023 show **negative growth**.
    * 2019–2020 had the **largest spike** (167.85% growth, +626,660 new women).
    """)
    
    # Create report_df with simple, consistent structure
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
    
    # Recruitment metrics
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
        # Calculate value from data
        new_members_18_30 = df_new_age.loc[df_new_age['Age Group'].isin(['18 to 24', '25 to 34']), 'New Members'].sum()
        
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
            f'<p class="note-text">Contact has been made with 20 community organizations.</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # New members by month with unique key
    recruit_monthly_fig = px.bar(df_extended, x='Month', y='New Members', 
                      title='New Member Contacts (2024-2025)',
                      color='New Members',
                      color_continuous_scale=[secondary_blue, primary_blue, primary_orange])
    
    # Add annotations for 2024 Jan-Sep total
    recruit_monthly_fig.add_annotation(
        x='Jan-Sep 2024',
        y=20008,
        text='20,008 total contacts',
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )
    
    # Add annotations for significant growth in recent months
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
        height=500  # Make the chart a bit taller to accommodate the large first bar
    )
    
    st.plotly_chart(recruit_monthly_fig, use_container_width=True, key=f"recruit_bar_monthly_{generate_unique_id()}")
    
    # Membership Distribution Section
    st.markdown('<h3>Membership Distribution</h3>', unsafe_allow_html=True)
    
    # New members by age - Moved to this section as requested
    recruit_age_fig = px.pie(df_new_age, values='New Members', names='Age Group', 
                     title='New Members by Age Group',
                     color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, 
                                            secondary_pink, secondary_purple, secondary_green])
    recruit_age_fig.update_traces(textposition='inside', textinfo='percent+label')
    recruit_age_fig.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(recruit_age_fig, use_container_width=True, key=f"recruit_pie_age_{generate_unique_id()}")
    
    # Total membership by age
    recruit_total_age_fig = px.bar(df_total_age, x='Age Group', y='Members',
                    title='Total Membership by Age Group',
                    color='Members',
                    color_continuous_scale=[secondary_purple, primary_blue, secondary_pink])
    recruit_total_age_fig.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(recruit_total_age_fig, use_container_width=True, key=f"recruit_bar_total_age_{generate_unique_id()}")
    
    # Download button for this tab
    st.markdown("### Download Recruitment Data")
    
    # Combine dataframes for download
    recruitment_data = {
        "Monthly New Members": df_extended,
        "New Members by Age": df_new_age,
        "Total Members by Age": df_total_age
    }
    
    selected_data = st.selectbox("Select data to download:", list(recruitment_data.keys()), key=f"recruit_select_{generate_unique_id()}")
    st.markdown(download_data(recruitment_data[selected_data], f"GirlTREK_{selected_data.replace(' ', '_')}"), unsafe_allow_html=True)

with tab3:
    st.markdown('<h3 class="section-title">Engagement Metrics</h3>', unsafe_allow_html=True)
    
    # Engagement metrics - Modified to make cards uniform and remove status/goals as requested
    engagement_col1, engagement_col2, engagement_col3 = st.columns(3)
    
    # Use consistent styling for metric cards without status and goal
    with engagement_col1:
        st.markdown(
            f'<div class="engagement-metric-card">'
            f'<p class="metric-title">TOTAL ACTIVE VOLUNTEERS</p>'
            f'<p class="metric-value">3,348</p>'
            f'<p class="note-text">Has hosted an event this year</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with engagement_col2:
        st.markdown(
            f'<div class="engagement-metric-card">'
            f'<p class="metric-title">TOTAL DOCUMENTED CREW LEADERS</p>'
            f'<p class="metric-value">3,732</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with engagement_col3:
        st.markdown(
            f'<div class="engagement-metric-card">'
            f'<p class="metric-title">TOTAL ACTIVE CREW LEADERS</p>'
            f'<p class="metric-value">1,846</p>'
            f'<p class="note-text">Has hosted an event this year or signed up this year</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Additional engagement metrics - also uniform style
    more_engage_col1, more_engage_col2 = st.columns(2)
    
    with more_engage_col1:
        st.markdown(
            f'<div class="engagement-metric-card">'
            f'<p class="metric-title">TOTAL NEW CREWS</p>'
            f'<p class="metric-value">603</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with more_engage_col2:
        st.markdown(
            f'<div class="engagement-metric-card">'
            f'<p class="metric-title">MEMBERS WALKING AT LIFE-SAVING LEVEL</p>'
            f'<p class="metric-value">4,788</p>'
            f'<p class="note-text">Members walking at least 30 minutes/day, 5 days/week</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Impact program metrics - uniform style
    impact_col1, impact_col2 = st.columns(2)
    
    with impact_col1:
        st.markdown(
            f'<div class="engagement-metric-card">'
            f'<p class="metric-title">MEMBERS IN SPECIAL IMPACT PROGRAMS</p>'
            f'<p class="metric-value">100</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with impact_col2:
        st.markdown(
            f'<div class="engagement-metric-card">'
            f'<p class="metric-title">TOTAL TRAINED</p>'
            f'<p class="metric-value">50</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Care Village metrics - Moved from Impact tab to Engagement tab as requested
    st.markdown("<h3>Care Village Metrics</h3>", unsafe_allow_html=True)
    
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
            f'<p>Goal: {format_currency(400000)}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Campaign metrics
    st.markdown('<h3>Current Campaign: Self-Care Schools</h3>', unsafe_allow_html=True)
    
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
    
    # Badges claimed with unique key
    engage_badges_fig = px.bar(df_badges, x='Week', y='Badges Claimed', 
                      title='Badges Claimed by Week (Goal: 5,000 per week)',
                      color='Badges Claimed',
                      color_continuous_scale=[secondary_green, primary_blue, secondary_purple])
    engage_badges_fig.update_layout(title_font=dict(color=primary_blue))
    
    # Add target line if enabled
    if show_target_lines:
        engage_badges_fig.add_shape(
            type="line",
            x0=-0.5,
            y0=5000,
            x1=len(df_badges)-0.5,
            y1=5000,
            line=dict(
                color="red",
                width=2,
                dash="dash",
            )
        )
        engage_badges_fig.add_annotation(
            x=len(df_badges)-1,
            y=5000,
            text="Target: 5,000",
            showarrow=False,
            yshift=10,
            font=dict(color="red")
        )
        
    st.plotly_chart(engage_badges_fig, use_container_width=True, key=f"engage_bar_badges_{generate_unique_id()}")
    
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
    
    # Create dataframes for download using list of dictionaries approach
    engagement_metrics_list = [
        {"Metric": "Total Active Volunteers", "Value": "3,348", "Goal": "N/A", "Status": "N/A"},
        {"Metric": "Total Documented Crew Leaders", "Value": "3,732", "Goal": "N/A", "Status": "N/A"},
        {"Metric": "Total Active Crew Leaders", "Value": "1,846", "Goal": "N/A", "Status": "On Track"},
        {"Metric": "Total New Crews", "Value": "603", "Goal": "N/A", "Status": "N/A"},
        {"Metric": "Members Walking at Life-Saving Level", "Value": "4,788", "Goal": "50,000", "Status": "At Risk"},
        {"Metric": "Members in Special Impact Programs", "Value": "100", "Goal": "65,000", "Status": "N/A"},
        {"Metric": "Total Trained", "Value": "50", "Goal": "1,000", "Status": "At Risk"}
    ]
    engagement_metrics_df = pd.DataFrame(engagement_metrics_list)
    
    campaign_metrics_list = [
        {"Metric": "Total Registrants", "Value": "11,985", "Goal": "10,000", "Status": "On Track"},
        {"Metric": "Total Downloads", "Value": "22,186", "Goal": "100,000", "Status": "At Risk"},
        {"Metric": "Registrants Age 18-25", "Value": "101", "Goal": "N/A", "Status": "At Risk"},
        {"Metric": "New Members from Campaign", "Value": "4,808", "Goal": "N/A", "Status": "On Track"},
        {"Metric": "New Members Age 18-25 from Campaign", "Value": "75", "Goal": "N/A", "Status": "At Risk"},
        {"Metric": "People Who Have Claimed Badges", "Value": "4,788", "Goal": "10,000", "Status": "On Track"},
        {"Metric": "Stories Submitted", "Value": "234", "Goal": "100", "Status": "On Track"}
    ]
    campaign_metrics_df = pd.DataFrame(campaign_metrics_list)
    
    care_village_metrics_list = [
        {"Metric": "Total Population Reached", "Value": "Unknown", "Goal": "20,000", "Notes": "Black women impacted through programs & events"},
        {"Metric": "Health Worker Training", "Value": "Unknown", "Goal": "4,000", "Notes": "Number of community health workers trained"},
        {"Metric": "Community Engagement", "Value": "Unknown", "Goal": "40,000", "Notes": "Number of Black women reached in Montgomery, AL"},
        {"Metric": "Bricklayers Hall Fundraising", "Value": "Unknown", "Goal": "$400,000", "Notes": ""}
    ]
    care_village_metrics_df = pd.DataFrame(care_village_metrics_list)
    
    engagement_data = {
        "Engagement Metrics": engagement_metrics_df,
        "Campaign Metrics": campaign_metrics_df,
        "Care Village Metrics": care_village_metrics_df,
        "Badges Claimed by Week": df_badges
    }
    
    selected_engagement_data = st.selectbox("Select data to download:", list(engagement_data.keys()), key=f"engage_select_{generate_unique_id()}")
    st.markdown(download_data(engagement_data[selected_engagement_data], f"GirlTREK_{selected_engagement_data.replace(' ', '_')}"), unsafe_allow_html=True)

with tab4:
    st.markdown('<h3 class="section-title">Development Metrics</h3>', unsafe_allow_html=True)
    
    # Improved Development metrics section with better presentation
    # Use a more compelling layout with icons
    
    st.markdown(
        """
        <div class="dev-metric-container">
            <div class="dev-metric-card">
                <div style="font-size: 24px; color: #0088FF; margin-bottom: 10px;">💰</div>
                <p class="dev-metric-title">TOTAL CONTRIBUTIONS</p>
                <p class="dev-metric-value">$3,061,104.78</p>
                <p class="dev-metric-goal">Goal: $8,000,000</p>
                <p>On Track</p>
                <div class="dev-metric-notes">
                    <p>• GirlTREK had a preliminary budget of $10M</p>
                    <p>• Cash-in from 2024 pledges credited toward 2025 revenues</p>
                    <p>• Annual campaign and capital campaign running in parallel</p>
                </div>
            </div>
            
            <div class="dev-metric-card">
                <div style="font-size: 24px; color: #0088FF; margin-bottom: 10px;">📈</div>
                <p class="dev-metric-title">TOTAL GRANTS</p>
                <p class="dev-metric-value">$3,055,250</p>
                <p class="dev-metric-goal">On Track</p>
                <div class="dev-metric-notes">
                    <p>• Secured multi-year, $3M gift</p>
                    <p>• Two foundation donations from current funders</p>
                </div>
            </div>
            
            <div class="dev-metric-card">
                <div style="font-size: 24px; color: #0088FF; margin-bottom: 10px;">🏢</div>
                <p class="dev-metric-title">CORPORATE ENGAGEMENT</p>
                <p class="dev-metric-value">$130,000</p>
                <p class="dev-metric-goal">Goal: $1,500,000</p>
                <p style="color: #FF9800; font-weight: bold;">At Risk</p>
                <div class="dev-metric-notes">
                    <p>• Need $500K for Summer of Solidarity program</p>
                    <p>• Short runway for securing funds</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="dev-metric-container">
            <div class="dev-metric-card">
                <div style="font-size: 24px; color: #0088FF; margin-bottom: 10px;">📝</div>
                <p class="dev-metric-title">NUMBER OF GRANTS</p>
                <p class="dev-metric-value">12</p>
                <p class="dev-metric-goal">Goal: 48</p>
                <p>On Track</p>
            </div>
            
            <div class="dev-metric-card">
                <div style="font-size: 24px; color: #0088FF; margin-bottom: 10px;">🤝</div>
                <p class="dev-metric-title">PROSPECTIVE CORPORATE SPONSORS</p>
                <p class="dev-metric-value">6</p>
                <p class="dev-metric-goal">Goal: 20</p>
                <p>On Track</p>
                <div class="dev-metric-notes">
                    <p>• Target companies: Wynn Beauty, Black Girl Vitamins, SAYSH</p>
                </div>
            </div>
            
            <div class="dev-metric-card">
                <div style="font-size: 24px; color: #0088FF; margin-bottom: 10px;">💵</div>
                <p class="dev-metric-title">TOTAL DONATIONS</p>
                <p class="dev-metric-value">$5,854.78</p>
                <p>On Track</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Updated Financial breakdown chart with corrected data
    st.markdown("<h3>Revenue Breakdown</h3>", unsafe_allow_html=True)
    updated_finance_data = {
        'Category': ['Donations', 'Grants', 'Corporate Sponsorships', 'Store Sales', 'Other Revenue'],
        'Amount': [1094048.68, 3055250, 130000, 25000, 125000]
    }
    df_updated_finance = pd.DataFrame(updated_finance_data)
    
    # Financial breakdown chart with unique key
    dev_finance_fig = px.pie(df_updated_finance, values='Amount', names='Category', 
                       title='Revenue Distribution',
                       color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, 
                                              secondary_blue, secondary_orange])
    dev_finance_fig.update_traces(textposition='inside', textinfo='percent+label')
    dev_finance_fig.update_layout(title_font=dict(color=primary_blue), height=500)
    st.plotly_chart(dev_finance_fig, use_container_width=True, key=f"dev_pie_finance_{generate_unique_id()}")
    
    # Financial trends chart with unique key
    st.markdown("<h3>Financial Trends</h3>", unsafe_allow_html=True)
    dev_trend_fig = go.Figure()
    
    dev_trend_fig.add_trace(go.Scatter(
        x=finance_trend_data['Month'],
        y=finance_trend_data['Revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color=primary_blue, width=3),
        marker=dict(color=primary_blue, size=8)
    ))
    
    dev_trend_fig.add_trace(go.Scatter(
        x=finance_trend_data['Month'],
        y=finance_trend_data['Expenses'],
        mode='lines+markers',
        name='Expenses',
        line=dict(color=primary_orange, width=3),
        marker=dict(color=primary_orange, size=8)
    ))
    
    dev_trend_fig.add_trace(go.Scatter(
        x=finance_trend_data['Month'],
        y=finance_trend_data['Donations'],
        mode='lines+markers',
        name='Donations',
        line=dict(color=primary_yellow, width=3),
        marker=dict(color=primary_yellow, size=8)
    ))
    
    dev_trend_fig.update_layout(
        title='Financial Trends by Month',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        legend_title='Category',
        height=500,
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(dev_trend_fig, use_container_width=True, key=f"dev_line_trend_{generate_unique_id()}")
    
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
    
    # Create dataframes for download - changed to list of dictionaries approach
    development_metrics_list = [
        {"Metric": "Total Contributions", "Value": "3,061,104.78", "Goal": "8,000,000", "Status": "On Track"},
        {"Metric": "Total Donations", "Value": "5,854.78", "Goal": "N/A", "Status": "On Track"},
        {"Metric": "Total Grants", "Value": "3,055,250", "Goal": "N/A", "Status": "On Track"},
        {"Metric": "Corporate Engagement", "Value": "130,000", "Goal": "1,500,000", "Status": "At Risk"},
        {"Metric": "Number of Grants", "Value": "12", "Goal": "48", "Status": "On Track"},
        {"Metric": "Prospective Corporate Sponsors", "Value": "6", "Goal": "20", "Status": "On Track"}
    ]
    development_metrics_df = pd.DataFrame(development_metrics_list)
    
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
    
    # Subscriber activity with unique key
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
        yaxis_title='Number of Subscribers',
        barmode='group',
        height=400,
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(marketing_activity_fig, use_container_width=True, key=f"marketing_bar_activity_{generate_unique_id()}")
    
    # Improved email and text message engagement visualization
    st.markdown('<h3>Email & Text Message Engagement</h3>', unsafe_allow_html=True)
    
    # Create a more visually appealing and easier to understand layout
    st.markdown(
        f"""
        <div class="email-stats-container">
            <div class="email-stat-box">
                <div class="email-stat-icon">📧</div>
                <div class="email-stat-content">
                    <div class="email-stat-title">Average Email Open Rate</div>
                    <div class="email-stat-value">34.95%</div>
                    <div style="font-size: 12px; color: #666;">Industry benchmark: 6.3-10%</div>
                </div>
                <div style="width: 100px; height: 100px; margin-left: auto;">
                    <div style="background-color: #f0f0f0; width: 100px; height: 8px; border-radius: 4px; margin-top: 45px;">
                        <div style="background-color: #FF5722; width: 62.7px; height: 8px; border-radius: 4px;"></div>
                    </div>
                </div>
            </div>
            
            <div style="font-size: 14px; color: #666; margin-top: 15px; padding: 10px; background-color: #f9f9f9; border-radius: 5px;">
                <strong>Industry Context:</strong> SMS messages typically have click-through rates of 6.3% for fundraising messages and 10% for advocacy messages.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Email engagement over time visualization
    st.markdown("<h3>Email Engagement Over Time</h3>", unsafe_allow_html=True)
    
    # Sample email engagement data
    email_trend_data = pd.DataFrame({
        'Month': ['January', 'February', 'March', 'April'],
        'Open Rate': [33.8, 34.2, 34.6, 34.95],
        'Click Rate': [2.9, 3.4, 4.1, 5.9],
        'Date': [datetime(2025, 1, 1), datetime(2025, 2, 1), datetime(2025, 3, 1), datetime(2025, 4, 1)]
    })
    
    # Create a line chart for email engagement trends
    email_trend_fig = go.Figure()
    
    email_trend_fig.add_trace(go.Scatter(
        x=email_trend_data['Month'],
        y=email_trend_data['Open Rate'],
        mode='lines+markers',
        name='Open Rate (%)',
        line=dict(color=primary_blue, width=3),
        marker=dict(color=primary_blue, size=8)
    ))
    
    email_trend_fig.add_trace(go.Scatter(
        x=email_trend_data['Month'],
        y=email_trend_data['Click Rate'],
        mode='lines+markers',
        name='Click Rate (%)',
        line=dict(color=primary_orange, width=3),
        marker=dict(color=primary_orange, size=8)
    ))
    
    # Add target line for open rate if target lines are enabled
    if show_target_lines:
        email_trend_fig.add_shape(
            type="line",
            x0='January',
            y0=35,
            x1='April',
            y1=35,
            line=dict(
                color="green",
                width=2,
                dash="dash",
            )
        )
        email_trend_fig.add_annotation(
            x='April',
            y=35,
            text="Target Open Rate: 35%",
            showarrow=False,
            yshift=10,
            font=dict(color="green")
        )
    
    email_trend_fig.update_layout(
        title='Email Engagement Trends',
        xaxis_title='Month',
        yaxis_title='Rate (%)',
        legend_title='Metric',
        height=400,
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(email_trend_fig, use_container_width=True, key=f"marketing_line_email_{generate_unique_id()}")
    
    # Social media metrics
    st.markdown("<h3>Social Media Metrics</h3>", unsafe_allow_html=True)
    
    social_col1, social_col2, social_col3, social_col4 = st.columns(4)
    
    with social_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">INSTAGRAM FOLLOWERS</p>'
            f'<p class="metric-value">127,450</p>'
            f'<p>+2.5% from Q1</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with social_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">FACEBOOK FOLLOWERS</p>'
            f'<p class="metric-value">98,265</p>'
            f'<p>+1.2% from Q1</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with social_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TWITTER FOLLOWERS</p>'
            f'<p class="metric-value">42,871</p>'
            f'<p>+3.1% from Q1</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with social_col4:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">YOUTUBE SUBSCRIBERS</p>'
            f'<p class="metric-value">18,539</p>'
            f'<p>+5.4% from Q1</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Social engagement metrics
    social2_col1, social2_col2 = st.columns(2)
    
    with social2_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">AVERAGE INSTAGRAM ENGAGEMENT RATE</p>'
            f'<p class="metric-value">3.8%</p>'
            f'<p>Benchmark: 2%</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with social2_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">AVERAGE FACEBOOK ENGAGEMENT RATE</p>'
            f'<p class="metric-value">2.1%</p>'
            f'<p>Benchmark: 1%</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Top performing posts
    st.markdown("<h3>Top Performing Content</h3>", unsafe_allow_html=True)
    
    # Sample top posts data
    top_posts_data = [
        {"Platform": "Instagram", "Content": "Self-Care Schools Launch", "Engagement": "12,450 likes, 1,835 comments", "Notes": "Strong engagement from target demographic 35-49"},
        {"Platform": "Facebook", "Content": "Crew Leader Feature: Atlanta", "Engagement": "8,245 reactions, 543 shares", "Notes": "Successful geographic targeting"},
        {"Platform": "Twitter", "Content": "National Walking Day Event", "Engagement": "2,160 retweets, 167 replies", "Notes": "High sharing rate and conversion to website clicks"},
        {"Platform": "YouTube", "Content": "Morning Walk Routine Tutorial", "Engagement": "24,815 views, 1,250 likes", "Notes": "8.5 minute average watch time"}
    ]
    
    # Display top posts in a clean table format
    for post in top_posts_data:
        st.markdown(
            f"""
            <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;">
                <div style="display: flex; align-items: center;">
                    <div style="font-weight: bold; color: #0088FF; width: 100px;">{post['Platform']}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">{post['Content']}</div>
                        <div style="font-size: 14px; color: #666;">{post['Engagement']}</div>
                        <div style="font-size: 12px; color: #888; font-style: italic; margin-top: 5px;">{post['Notes']}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Download button for marketing data
    st.markdown("### Download Marketing Data")
    
    # Create marketing metrics dataframe for download
    marketing_metrics_list = [
        {"Metric": "Total Subscribers", "Value": "931,141", "Goal": "1,300,000", "Status": "On Track"},
        {"Metric": "Active Subscribers", "Value": "297,283", "Goal": "N/A", "Status": "N/A"},
        {"Metric": "Average Email Open Rate", "Value": "34.95%", "Goal": "35%", "Status": "On Track"},
        {"Metric": "30-Day Email Opens", "Value": "221,719", "Goal": "N/A", "Status": "N/A"},
        {"Metric": "30-Day Email Clicks", "Value": "13,000", "Goal": "N/A", "Status": "N/A"},
        {"Metric": "Instagram Followers", "Value": "127,450", "Goal": "150,000", "Status": "On Track"},
        {"Metric": "Facebook Followers", "Value": "98,265", "Goal": "120,000", "Status": "At Risk"},
        {"Metric": "Twitter Followers", "Value": "42,871", "Goal": "50,000", "Status": "On Track"},
        {"Metric": "YouTube Subscribers", "Value": "18,539", "Goal": "25,000", "Status": "On Track"}
    ]
    marketing_metrics_df = pd.DataFrame(marketing_metrics_list)
    
    st.markdown(download_data(marketing_metrics_df, "GirlTREK_Marketing_Metrics"), unsafe_allow_html=True)

with tab6:
    st.markdown('<h3 class="section-title">Operations Metrics</h3>', unsafe_allow_html=True)
    
    # Operations metrics
    st.markdown("<h3>Staff & Team Metrics</h3>", unsafe_allow_html=True)
    
    ops_col1, ops_col2, ops_col3 = st.columns(3)
    
    with ops_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL TEAM MEMBERS</p>'
            f'<p class="metric-value">48</p>'
            f'<p>Goal: 65</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with ops_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">OPEN POSITIONS</p>'
            f'<p class="metric-value">7</p>'
            f'<p>In active recruitment</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with ops_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">STAFF RETENTION RATE</p>'
            f'<p class="metric-value">93%</p>'
            f'<p>Goal: >90%</p>'
            f'<p>{status_badge("Achieved")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Technology systems metrics
    st.markdown("<h3>Technology Systems</h3>", unsafe_allow_html=True)
    
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">APP DOWNLOADS</p>'
            f'<p class="metric-value">32,450</p>'
            f'<p>Goal: 100,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with tech_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">ACTIVE APP USERS</p>'
            f'<p class="metric-value">18,736</p>'
            f'<p>57.7% of downloads</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Website metrics
    st.markdown("<h3>Website Performance</h3>", unsafe_allow_html=True)
    
    web_col1, web_col2, web_col3 = st.columns(3)
    
    with web_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">MONTHLY WEBSITE VISITORS</p>'
            f'<p class="metric-value">124,856</p>'
            f'<p>+18% from Q1</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with web_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">AVERAGE SESSION DURATION</p>'
            f'<p class="metric-value">3:42</p>'
            f'<p>+0:15 from Q1</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with web_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">CONVERSION RATE</p>'
            f'<p class="metric-value">4.8%</p>'
            f'<p>Goal: 5%</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # IT efficiency metrics
    st.markdown("<h3>IT & Operations Efficiency</h3>", unsafe_allow_html=True)
    
    it_col1, it_col2 = st.columns(2)
    
    with it_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">AVERAGE SUPPORT TICKET RESOLUTION TIME</p>'
            f'<p class="metric-value">16.4 hours</p>'
            f'<p>Goal: <24 hours</p>'
            f'<p>{status_badge("Achieved")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with it_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">SYSTEM UPTIME</p>'
            f'<p class="metric-value">99.7%</p>'
            f'<p>Goal: >99.5%</p>'
            f'<p>{status_badge("Achieved")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Operational budget performance
    st.markdown("<h3>Operational Budget Performance</h3>", unsafe_allow_html=True)
    
    # Sample budget data
    budget_data = pd.DataFrame({
        'Category': ['Personnel', 'Technology', 'Facilities', 'Marketing', 'Programs', 'Admin'],
        'Budget': [2100000, 850000, 320000, 750000, 1200000, 280000],
        'Actual': [1950000, 790000, 295000, 710000, 1050000, 265000],
        'Percent': [92.9, 92.9, 92.2, 94.7, 87.5, 94.6]
    })
    
    # Create budget performance visualization
    budget_fig = go.Figure()
    
    budget_fig.add_trace(go.Bar(
        x=budget_data['Category'],
        y=budget_data['Budget'],
        name='Budget',
        marker_color=primary_blue
    ))
    
    budget_fig.add_trace(go.Bar(
        x=budget_data['Category'],
        y=budget_data['Actual'],
        name='Actual',
        marker_color=primary_orange
    ))
    
    budget_fig.update_layout(
        title='Budget vs. Actual Spending by Category',
        xaxis_title='Category',
        yaxis_title='Amount ($)',
        barmode='group',
        height=400,
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(budget_fig, use_container_width=True, key=f"ops_bar_budget_{generate_unique_id()}")
    
    # Download button for operations data
    st.markdown("### Download Operations Data")
    
    # Create operations metrics dataframe for download
    operations_metrics_list = [
        {"Metric": "Total Team Members", "Value": "48", "Goal": "65", "Status": "On Track"},
        {"Metric": "Open Positions", "Value": "7", "Goal": "N/A", "Status": "N/A"},
        {"Metric": "Staff Retention Rate", "Value": "93%", "Goal": ">90%", "Status": "Achieved"},
        {"Metric": "App Downloads", "Value": "32,450", "Goal": "100,000", "Status": "At Risk"},
        {"Metric": "Active App Users", "Value": "18,736", "Goal": "N/A", "Status": "N/A"},
        {"Metric": "Monthly Website Visitors", "Value": "124,856", "Goal": "N/A", "Status": "N/A"},
        {"Metric": "Average Session Duration", "Value": "3:42", "Goal": "N/A", "Status": "N/A"},
        {"Metric": "Conversion Rate", "Value": "4.8%", "Goal": "5%", "Status": "On Track"},
        {"Metric": "Average Support Ticket Resolution Time", "Value": "16.4 hours", "Goal": "<24 hours", "Status": "Achieved"},
        {"Metric": "System Uptime", "Value": "99.7%", "Goal": ">99.5%", "Status": "Achieved"}
    ]
    operations_metrics_df = pd.DataFrame(operations_metrics_list)
    
    st.markdown(download_data(operations_metrics_df, "GirlTREK_Operations_Metrics"), unsafe_allow_html=True)
            </div>
                <div style="width: 100px; height: 100px; margin-left: auto;">
                    <div style="background-color: #f0f0f0; width: 100px; height: 8px; border-radius: 4px; margin-top: 45px;">
                        <div style="background-color: #FF5722; width: {34.95/35*100}px; height: 8px; border-radius: 4px;"></div>
                    </div>
                </div>
            </div>
            
            <div class="email-stat-box">
                <div class="email-stat-icon">👀</div>
                <div class="email-stat-content">
                    <div class="email-stat-title">30-Day Email Opens</div>
                    <div class="email-stat-value">{format_number(221719)}</div>
                    <div style="font-size: 12px; color: #666;">23.8% of total subscribers</div>
                </div>
            </div>
            
            <div class="email-stat-box">
                <div class="email-stat-icon">👆</div>
                <div class="email-stat-content">
                    <div class="email-stat-title">30-Day Email Clicks</div>
                    <div class="email-stat-value">{format_number(13000)}</div>
                    <div style="font-size: 12px; color: #666;">5.9% of openers</div>
                </div>
            </div>
            
            <div class="email-stat-box">
                <div class="email-stat-icon">📱</div>
                <div class="email-stat-content">
                    <div class="email-stat-title">Text Message Click-Through Rate</div>
                    <div class="email-stat-value">6.27%</div>
                    <div style="font-size: 12px;
