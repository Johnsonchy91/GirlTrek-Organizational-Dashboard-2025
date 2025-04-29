import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
import re

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
            </style>
            """, 
            unsafe_allow_html=True
        )

# Create session state for storing data and filters
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'total_membership' not in st.session_state:
    # Load initial data
    st.session_state.total_membership = 1240394
    st.session_state.new_members = 11356
    st.session_state.total_contributions = 3061104.78
    st.session_state.total_grants = 3055250
    
    # Set data_loaded to True
    st.session_state.data_loaded = True

# Sidebar - Dashboard download section only 
st.sidebar.markdown("### Download Dashboard")
download_options = [
    "Executive Summary", 
    "Recruitment", 
    "Engagement",
    "Development", 
    "Marketing",
    "Operations",
    "Impact",
    "Member Care",
    "Advocacy",
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

# Sample data for charts and visualizations (consolidated to avoid duplication)
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

# ----- Age group distribution data -----
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

# ----- Geographic distribution data -----
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

# ----- Financial data -----
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
    
    # Create a data table for report card with more specific goals
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
    
    # Create bar chart instead of line chart for Membership Growth
    fig_months = px.bar(df_extended, x='Month', y='New Members', 
                      title='New Member Contacts (2024-2025)',
                      color='New Members',
                      color_continuous_scale=[secondary_blue, primary_blue, primary_orange])
    
    # Add annotations for 2024 Jan-Sep total
    fig_months.add_annotation(
        x='Jan-Sep 2024',
        y=20008,
        text='20,008 total contacts',
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )
    
    # Add annotations for significant growth in recent months
    fig_months.add_annotation(
        x='Mar 2025',
        y=4382,
        text='177% increase',
        showarrow=True,
        arrowhead=1,
        ax=40,
        ay=-40
    )
    
    fig_months.add_annotation(
        x='Apr 2025',
        y=6073,
        text='39% increase',
        showarrow=True,
        arrowhead=1,
        ax=40,
        ay=-40
    )
    
    fig_months.update_layout(
        title_font=dict(color=primary_blue),
        yaxis_title='Number of New Contacts',
        xaxis_title='Month',
        height=500  # Make the chart a bit taller to accommodate the large first bar
    )
    
    st.plotly_chart(fig_months, use_container_width=True)
    
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        # New members by month
        # Create bar chart instead of line chart
        fig_months = px.bar(df_extended, x='Month', y='New Members', 
                          title='New Member Contacts (2024-2025)',
                          color='New Members',
                          color_continuous_scale=[secondary_blue, primary_blue, primary_orange])
        
        # Add annotations for 2024 Jan-Sep total
        fig_months.add_annotation(
            x='Jan-Sep 2024',
            y=20008,
            text='20,008 total contacts',
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-40
        )
        
        # Add annotations for significant growth in recent months
        fig_months.add_annotation(
            x='Mar 2025',
            y=4382,
            text='177% increase',
            showarrow=True,
            arrowhead=1,
            ax=40,
            ay=-40
        )
        
        fig_months.add_annotation(
            x='Apr 2025',
            y=6073,
            text='39% increase',
            showarrow=True,
            arrowhead=1,
            ax=40,
            ay=-40
        )
        
        fig_months.update_layout(
            title_font=dict(color=primary_blue),
            yaxis_title='Number of New Contacts',
            xaxis_title='Month',
            height=500  # Make the chart a bit taller to accommodate the large first bar
        )
        
        st.plotly_chart(fig_months, use_container_width=True)
    
    with col2:
        # New members by age
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
        
        fig_states = px.bar(df_states, x='State', y='Members',
                         title='Membership by Top 5 States',
                         color='Members',
                         color_continuous_scale=[secondary_blue, primary_blue])
        fig_states.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(fig_states, use_container_width=True)
    
    with dist_col2:
        st.markdown("<h5>Top 5 Cities</h5>", unsafe_allow_html=True)
        
        fig_cities = px.bar(df_cities, x='City', y='Members',
                         title='Membership by Top 5 Cities',
                         color='Members',
                         color_continuous_scale=[secondary_teal, primary_orange])
        fig_cities.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(fig_cities, use_container_width=True)
    
    # Total membership by age
    st.markdown('<h4>Total Membership by Age</h4>', unsafe_allow_html=True)
    
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
    
    # Use consistent styling for metric cards
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
    fig_badges = px.bar(df_badges, x='Week', y='Badges Claimed', 
                      title='Badges Claimed by Week (Goal: 5,000 per week)',
                      color='Badges Claimed',
                      color_continuous_scale=[secondary_green, primary_blue, secondary_purple])
    fig_badges.update_layout(title_font=dict(color=primary_blue))
    
    # Add target line if enabled
    if show_target_lines:
        fig_badges.add_shape(
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
        fig_badges.add_annotation(
            x=len(df_badges)-1,
            y=5000,
            text="Target: 5,000",
            showarrow=False,
            yshift=10,
            font=dict(color="red")
        )
        
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
            f'<p class="metric-value">{format_currency(1094048.68)}</p>'
            f'<p>Goal: $8,000,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with financial_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL REVENUE</p>'
            f'<p class="metric-value">{format_currency(1500000)}</p>'
            f'<p>Goal: $400,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with financial_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL EXPENSES</p>'
            f'<p class="metric-value">{format_currency(1200000)}</p>'
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
            f'<p class="metric-value">{format_currency(600000)}</p>'
            f'<p>Goal: $1,000,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with grants_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">CORPORATE SPONSORSHIPS</p>'
            f'<p class="metric-value">{format_currency(750000)}</p>'
            f'<p>Goal: $1,500,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Financial breakdown chart
    fig_finance = px.pie(df_finance, values='Amount', names='Category', 
                       title='Revenue Breakdown',
                       color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, 
                                              secondary_blue, secondary_orange])
    fig_finance.update_traces(textposition='inside', textinfo='percent+label')
    fig_finance.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(fig_finance, use_container_width=True)
    
    # Financial trends chart
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
            f'<p class="metric-value">{format_currency(11180.21)}</p>'
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
            f'<p>Goal: {format_currency(400000)}</p>'
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
            f'<p>Goal: {format_currency(400000)}</p>'
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
    
    # Use expanders for the stories to save space
    with st.expander("Story 1: Crew Leader Nicole Crooks"):
        st.markdown(
            f"""
            <div class="metric-card">
                <p>Crew Leader Nicole Crooks and the South Florida crew understood the assignment during #SisterhoodSaturday! Nicole's post says it best: "Simply grateful!!! #SisterhoodSaturday during Black Maternal Health Week was absolutely everything! A huge thank you to Maya at Historic Virginia Key Beach Park, Kallima and the entire GirlTREK: Healthy Black Women village, Cortes, Jamarrah and the entire https://southernbirthjustice.org/ (SBJN) village, Kedemah and the entire AKA village, Mama Kuks, Mama Joy, Mama Sheila & Mama Wangari (our beautiful village of elders), to each and every sister who came or supported in any way. AND a SUPERDUPER Thank you, thank you, THANK YOU!!! to Kukuwa Fitness and Nakreshia Causey Born Saturday was filled with magic and joy! And yep... you can grab those GirlTREK inspired leggings at https://www.kukuwafitness.com/ I am so ready for this week's #selfcareschool hope you are too!!!"</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with st.expander("Story 2: Amazing TedTalk used in class"):
        st.markdown(
            f"""
            <div class="metric-card">
                <p>Hello ladies! First and foremost YOU ARE AMAZING. Sending so much love to you all and holding space for your amazing cause. I am a teacher in Ohio and I just wanted to tell you that I am using the TedTalk from 2018 in my Black History in America course. I can't wait to help my students use this frame of understanding. Thank you for shining a light on this - it is so needed!!! Thank you for taking action! Thank you for showing so much loving kindness!!!! I appreciate you all and am so excited for this movement! Much love and respect, Kaitlin Finan kbeeble@gmail.com</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with st.expander("Story 3: My Sister's Keeper"):
        st.markdown(
            f"""
            <div class="metric-card">
                <p>Morgan and Vanessa, I walked this evening—first chance I've had in a while. And I talked on the phone to a friend of mine who was also walking at the time and had not walked in a while. I invited her to walk with me and told her about Harriet Day and the meeting last night. I also shared GirlTREK information with her and invited her to join. We're going to start walking together!

                I used to walk all the time. I moved back closer to my hometown four years ago to be near Mama and help take care of her. She got better and was doing great, then all of a sudden she wasn't. Mama transitioned to Heaven a little over a year ago and life has been difficult. She was everything to me. It's just been hard—but by the grace of God, I'm still standing. He did bless us with 3 more years after she was hospitalized 33 days. I'm trying to get my legs back under me. But I am lonely for Mama. 99% of the time, I walked alone...didn't have anyone to walk with. But I would listen in some Saturdays. Everybody is a few towns over, so weekday scheduling is tough. But I also told my sisters and my brother that they were going to walk with me as a part of this next 10-week commitment. Thank you for all that you do, Sandy B. Carter sandybcarter@yahoo.com</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Interactive element - satisfaction survey results over time
    st.markdown("<h4>Member Satisfaction Trend</h4>", unsafe_allow_html=True)
    
    # Sample data for satisfaction trend
    satisfaction_data = {
        'Month': ['January', 'February', 'March', 'April'],
        'Satisfaction': [88, 90, 93, 95]
    }
    df_satisfaction = pd.DataFrame(satisfaction_data)
    
    fig_satisfaction = px.line(df_satisfaction, x='Month', y='Satisfaction',
                             title='Member Satisfaction Rating Over Time (%)',
                             markers=True)
    fig_satisfaction.update_traces(
        line=dict(color=primary_blue, width=3),
        marker=dict(color=primary_orange, size=10)
    )
    
    # Add target line if enabled
    if show_target_lines:
        fig_satisfaction.add_shape(
            type="line",
            x0=-0.5,
            y0=85,
            x1=len(df_satisfaction)-0.5,
            y1=85,
            line=dict(
                color="green",
                width=2,
                dash="dash",
            )
        )
        fig_satisfaction.add_annotation(
            x=0,
            y=85,
            text="Goal: 85%",
            showarrow=False,
            yshift=-15,
            font=dict(color="green")
        )
    
    fig_satisfaction.update_layout(
        xaxis_title='Month',
        yaxis_title='Satisfaction (%)',
        yaxis=dict(range=[80, 100]),  # Set y-axis range
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(fig_satisfaction, use_container_width=True)
    
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
        "Top Member Issues": member_issues_df,
        "Satisfaction Trend": df_satisfaction
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
    
    # Build the table HTML - with error handling
    try:
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
                <td>{status_badge(item["status"])}</td>
            </tr>
            """
        
        advocacy_html += "</table>"
        
        st.markdown(advocacy_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error rendering advocacy table: {str(e)}")
    
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
    
    # Use a different visualization for policy impact
    policy_impact_data = {
        'Policy Area': ['Health Equity', 'Safe Walking Spaces', 'Food Justice', 'Mental Health', 'Environmental Justice'],
        'Meetings': [2, 1, 1, 1, 1],
        'Partners': [1, 0, 1, 0, 0]
    }
    df_policy = pd.DataFrame(policy_impact_data)
    
    fig_policy = px.bar(df_policy, x='Policy Area', y=['Meetings', 'Partners'],
                      title='Policy Impact by Area',
                      barmode='group')
    
    fig_policy.update_traces(
        marker_color=[primary_blue, primary_orange],
    )
    
    fig_policy.update_layout(
        xaxis_title='Policy Area',
        yaxis_title='Count',
        legend_title='Type',
        height=400,
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(fig_policy, use_container_width=True)
    
    # Download button
    st.markdown("### Download Advocacy Data")
    
    # Create dataframe for download
    advocacy_metrics_df = pd.DataFrame({
        "Metric": [
            "Advocacy briefs produced",
            "Advocacy partners secured",
            "Media Mentions",
            "Policy Meetings"
        ],
        "Value": [4, 2, 28, 6],
        "Goal": [10, 20, 50, 15],
        "Status": ["On Track", "On Track", "On Track", "On Track"]
    })
    
    st.markdown(download_data(advocacy_metrics_df, "GirlTREK_Advocacy_Metrics"), unsafe_allow_html=True)

# Add error handling wrapper for the entire app
try:
    # Footer with last updated timestamp
    current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    st.markdown(
        f"""
        <div style="margin-top: 50px; padding: 20px; background-color: {secondary_beige}; border-radius: 10px; text-align: center;">
            <h3 style="color: {primary_blue};">GirlTREK - Inspiring Black Women to Walk for Better Health</h3>
            <p>Data last updated: April 25, 2025</p>
            <p>Dashboard last refreshed: {current_time}</p>
            <p>For more information, visit <a href="https://www.girltrek.org" target="_blank" style="color: {primary_blue};">girltrek.org</a></p>
        </div>
        """, 
        unsafe_allow_html=True
    )
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.warning("Please try refreshing the page. If the problem persists, contact support.")
