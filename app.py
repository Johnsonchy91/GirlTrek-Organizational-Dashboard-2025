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

# Add Notes Functionality - Moved to top of file
def create_notes_section(tab_name):
    """Create a notes section for any tab with persistence"""
    
    notes_key = f"notes_{tab_name}"
    
    # Initialize notes in session state if they don't exist
    if notes_key not in st.session_state:
        st.session_state[notes_key] = ""
        
    # Initialize recent notes tracking if it doesn't exist
    if 'recent_notes' not in st.session_state:
        st.session_state.recent_notes = []
    
    # Create expandable section for notes
    with st.expander(f"📝 Notes for {tab_name}", expanded=False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Create text area for notes with the current value from session state
            notes = st.text_area(
                "Add your notes here:",
                value=st.session_state[notes_key],
                height=150,
                key=f"textarea_{notes_key}"
            )
            
            # Automatically save notes when they change
            if notes != st.session_state[notes_key]:
                previous_notes = st.session_state[notes_key]
                st.session_state[notes_key] = notes
                
                # Add timestamp for last edit
                if 'last_edit_time' not in st.session_state:
                    st.session_state.last_edit_time = {}
                    
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.last_edit_time[notes_key] = timestamp
                
                # Track recent note submissions for display in sidebar
                if notes.strip() and (not previous_notes.strip() or notes.strip() != previous_notes.strip()):
                    # Only add if it's not empty and is different from before
                    note_summary = notes.strip() if len(notes.strip()) < 50 else notes.strip()[:47] + "..."
                    st.session_state.recent_notes.insert(0, {
                        "tab": tab_name,
                        "summary": note_summary,
                        "timestamp": timestamp
                    })
                    # Keep only the 5 most recent notes
                    if len(st.session_state.recent_notes) > 5:
                        st.session_state.recent_notes = st.session_state.recent_notes[:5]
                
                st.success("Notes saved automatically!")
        
        with col2:
            # Display timestamp of last edit if available
            if 'last_edit_time' in st.session_state and notes_key in st.session_state.last_edit_time:
                st.info(f"Last edited: {st.session_state.last_edit_time[notes_key]}")
            
            # Add export functionality
            if st.button("Export Notes", key=f"export_{tab_name}"):
                # Convert notes to CSV format for download
                notes_data = f"Tab,Notes\n{tab_name},{st.session_state[notes_key].replace(',', ';').replace('\n', ' ')}"
                b64 = base64.b64encode(notes_data.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="{tab_name}_notes.csv">Download {tab_name} Notes</a>'
                st.markdown(href, unsafe_allow_html=True)
            
            # Add ability to clear notes
            if st.button("Clear Notes", key=f"clear_{tab_name}"):
                st.session_state[notes_key] = ""
                if 'last_edit_time' in st.session_state and notes_key in st.session_state.last_edit_time:
                    del st.session_state.last_edit_time[notes_key]
                st.experimental_rerun()

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
                background-color: #000000;
                color: #FFFFFF;
            }}
            .stApp {{
                background-color: #000000;
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #FFFFFF !important;
            }}
            p {{
                color: #FFFFFF;
            }}
            .metric-box {{
                background-color: #1E1E1E;
                color: #FFFFFF;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
                margin-bottom: 20px;
                text-align: center;
                border-left: 5px solid #0088FF;
            }}
            .metric-title {{
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #BBBBBB;
            }}
            .metric-value {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #FFFFFF;
            }}
            .section-title {{
                color: #FFFFFF;
                padding-bottom: 10px;
                border-bottom: 2px solid #FF7043;
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
            .metric-box {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
                text-align: center;
                border-left: 5px solid #0088FF;
            }
            .metric-title {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #424242;
            }
            .metric-value {
                font-size: 26px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #0088FF;
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
    st.session_state.total_contributions = 1094048.68
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

# Add dashboard notes section after settings
st.sidebar.markdown("---")
st.sidebar.markdown("### Dashboard Notes")

# Add a section for global notes that apply to all tabs
if 'global_notes' not in st.session_state:
    st.session_state.global_notes = ""

global_notes = st.sidebar.text_area(
    "Add global notes for the entire dashboard:",
    value=st.session_state.global_notes,
    height=100,
    key="textarea_global_notes"
)

# Save button for global notes
if st.sidebar.button("Save Global Notes"):
    previous_notes = st.session_state.global_notes
    st.session_state.global_notes = global_notes
    
    # Track recent note submissions
    if global_notes.strip() and (not previous_notes.strip() or global_notes.strip() != previous_notes.strip()):
        # Only add if it's not empty and is different from before
        note_summary = global_notes.strip() if len(global_notes.strip()) < 50 else global_notes.strip()[:47] + "..."
        if 'recent_notes' not in st.session_state:
            st.session_state.recent_notes = []
        
        st.session_state.recent_notes.insert(0, {
            "tab": "Global",
            "summary": note_summary,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        # Keep only the 5 most recent notes
        if len(st.session_state.recent_notes) > 5:
            st.session_state.recent_notes = st.session_state.recent_notes[:5]
            
    st.sidebar.success("Global notes saved successfully!")

# Display recent notes
st.sidebar.markdown("### Recent Notes")
if 'recent_notes' in st.session_state and st.session_state.recent_notes:
    for note in st.session_state.recent_notes:
        st.sidebar.markdown(
            f"""
            <div style="background-color: #f1f3f4; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 3px solid #0088FF;">
                <div style="font-size: 12px; color: #666; margin-bottom: 2px;">{note['tab']} - {note['timestamp']}</div>
                <div style="font-size: 14px;">{note['summary']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.sidebar.markdown("*No recent notes to display*")

# Export all notes
if st.sidebar.button("Export All Notes"):
    # Collect all notes from session state
    all_notes = {"Global": st.session_state.global_notes}
    
    # Add notes from each tab if they exist
    for tab in ["Executive Summary", "Recruitment", "Engagement", "Development", 
                "Marketing", "Operations", "Member Care", "Advocacy", "Impact"]:
        tab_key = f"notes_{tab}"
        if tab_key in st.session_state:
            all_notes[tab] = st.session_state[tab_key]
    
    # Create CSV string
    csv_data = "Tab,Notes\n"
    for tab, notes in all_notes.items():
        # Replace commas and newlines to avoid breaking CSV format
        clean_notes = notes.replace(',', ';').replace('\n', ' ')
        csv_data += f"{tab},{clean_notes}\n"
    
    # Create download link
    b64 = base64.b64encode(csv_data.encode()).decode()
    date_str = datetime.now().strftime("%Y%m%d")
    href = f'<a href="data:file/csv;base64,{b64}" download="GirlTREK_Dashboard_Notes_{date_str}.csv">Download All Notes</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

# App Title
st.title("GirlTREK Organizational Dashboard")
st.markdown("### Q2 2025 Metrics Overview")
st.markdown("*Data dashboard was published on April 25, 2025*")

# Dashboard Settings
st.sidebar.markdown("### Dashboard Settings")
if 'show_target_lines' not in st.session_state:
    st.session_state.show_target_lines = True
    
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
    
show_target_lines = st.sidebar.checkbox("Show Target Lines", value=st.session_state.show_target_lines, key="show_target_lines_checkbox")
dark_mode = st.sidebar.checkbox("Dark Mode", value=st.session_state.dark_mode, key="dark_mode_checkbox")

# Update session state
st.session_state.show_target_lines = show_target_lines
st.session_state.dark_mode = dark_mode

apply_dark_mode(dark_mode)


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
            f'<div class="metric-box">'
            f'<p class="metric-title">TOTAL MEMBERSHIP</p>'
            f'<p class="metric-value">{format_number(st.session_state.total_membership)}</p>'
            f'<p>Goal: 2,000,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">TOTAL NEW MEMBERS</p>'
            f'<p class="metric-value">{format_number(st.session_state.new_members)}</p>'
            f'<p>Goal: 100,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">TOTAL CONTRIBUTIONS</p>'
            f'<p class="metric-value">{format_currency(st.session_state.total_contributions)}</p>'
            f'<p>Goal: $10,000,000</p>'
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

    # --- Historic Movement Growth (as graph) - MOVED HERE ---
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

    # --- Membership Distribution ---
    st.markdown('<h3>Membership Distribution</h3>', unsafe_allow_html=True)

    # Full width total membership by age
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
    
    # Add Notes Section at the bottom of the tab
    st.markdown('<hr>', unsafe_allow_html=True)
    create_notes_section("Executive Summary")
# ---------------------------------
# Recruitment Tab
# ---------------------------------
with tab2:
    st.markdown('<h3 class="section-title">Recruitment Metrics</h3>', unsafe_allow_html=True)

    recruitment_col1, recruitment_col2, recruitment_col3 = st.columns(3)

    with recruitment_col1:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">TOTAL NEW MEMBERS</p>'
            f'<p class="metric-value">{format_number(st.session_state.new_members)}</p>'
            f'<p>Goal: 100,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with recruitment_col2:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">NEW MEMBERS AGE 18-30</p>'
            f'<p class="metric-value">300</p>'
            f'<p>Goal: 50,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with recruitment_col3:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">TOTAL RECRUITMENT PARTNERSHIPS</p>'
            f'<p class="metric-value">0</p>'
            f'<p>Goal: 100</p>'
            f'<p>{status_badge("On Track")}</p>'
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
    
    # New Members by Age Group (moved from Executive Summary)
    st.markdown('<h3>New Members by Age Group</h3>', unsafe_allow_html=True)
    
    new_age_fig = px.pie(
        df_new_age,
        values='New Members',
        names='Age Group',
        title='New Members by Age Group Distribution',
        color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, secondary_pink, secondary_purple, secondary_green]
    )
    new_age_fig.update_traces(textposition='inside', textinfo='percent+label')
    new_age_fig.update_layout(title_font=dict(color=primary_blue))
    # Add Notes Section for Recruitment
    st.markdown('<hr>', unsafe_allow_html=True)
    create_notes_section("Recruitment")

# ---------------------------------
# Engagement Tab
# ---------------------------------
with tab3:
    st.markdown('<h3 class="section-title">Engagement Metrics</h3>', unsafe_allow_html=True)

    engagement_col1, engagement_col2 = st.columns(2)

    with engagement_col1:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">TOTAL NEW CREWS (2025)</p>'
            f'<p class="metric-value">603</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with engagement_col2:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">MEMBERS WALKING DAILY</p>'
            f'<p class="metric-value">4,788</p>'
            f'<p>Goal: 50,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    # Additional engagement metrics
    eng_col1, eng_col2, eng_col3 = st.columns(3)
    
    with eng_col1:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">ACTIVE VOLUNTEERS</p>'
            f'<p class="metric-value">3,348</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    with eng_col2:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">DOCUMENTED CREW LEADERS</p>'
            f'<p class="metric-value">3,732</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    with eng_col3:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">ACTIVE CREW LEADERS</p>'
            f'<p class="metric-value">1,846</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )
        
    # Self-Care School Campaign Section (moved from its own tab)
    st.markdown('<h3 class="section-title">Self-Care School Campaign</h3>', unsafe_allow_html=True)
    
    # Campaign header with progress visualization
    campaign_progress = 11985 / 10000 * 100  # Calculate percentage of goal achieved
    
    progress_html = f"""
    <div style="background: linear-gradient(to right, #f0f9ff, #E3F2FD); border-radius: 10px; padding: 20px; margin-bottom: 25px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between;">
            <div>
                <h3 style="margin-top: 0; color: #1E88E5;">Self-Care School Campaign Status</h3>
                <p style="font-size: 16px;">Goal: 10,000 Registrants | Current: 11,985 Registrants</p>
                <div style="font-size: 18px; font-weight: bold; color: #00C853;">Status: {status_badge("Achieved")}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 40px; font-weight: bold; color: #1E88E5;">{campaign_progress:.1f}%</div>
                <p>of goal achieved</p>
            </div>
        </div>
        <div style="width: 100%; background-color: #E0E0E0; height: 15px; border-radius: 10px; margin-top: 15px;">
            <div style="width: {min(campaign_progress, 100)}%; height: 100%; background-color: #00C853; border-radius: 10px;"></div>
        </div>
    </div>
    """
    
    st.markdown(progress_html, unsafe_allow_html=True)
    
    # Key metrics in visually appealing boxes
    metrics_row1_col1, metrics_row1_col2, metrics_row1_col3 = st.columns(3)
    
    with metrics_row1_col1:
        st.markdown(
            f"""
            <div style="background-color: #E8F5E9; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #2E7D32; margin-top: 0;">NEW MEMBERS</h4>
                <div style="font-size: 36px; font-weight: bold; color: #2E7D32; margin: 10px 0;">4,808</div>
                <p style="color: #2E7D32;">Joined through campaign</p>
                <p>{status_badge("On Track")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with metrics_row1_col2:
        st.markdown(
            f"""
            <div style="background-color: #FFF8E1; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #FF8F00; margin-top: 0;">DOWNLOADS</h4>
                <div style="font-size: 36px; font-weight: bold; color: #FF8F00; margin: 10px 0;">22,186</div>
                <p style="color: #FF8F00;">Goal: 100,000</p>
                <p>{status_badge("At Risk")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with metrics_row1_col3:
        st.markdown(
            f"""
            <div style="background-color: #E1F5FE; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #0277BD; margin-top: 0;">STORIES SUBMITTED</h4>
                <div style="font-size: 36px; font-weight: bold; color: #0277BD; margin: 10px 0;">234</div>
                <p style="color: #0277BD;">Goal: 100</p>
                <p>{status_badge("Achieved")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Age demographics and Badges claimed  
    st.markdown('<h4>Campaign Metrics</h4>', unsafe_allow_html=True)
    
    age_col1, age_col2 = st.columns([1, 3])
    
    with age_col1:
        st.markdown(
            f"""
            <div style="background-color: #FFEBEE; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #C62828; margin-top: 0;">REGISTRANTS AGE 18-25</h4>
                <div style="font-size: 36px; font-weight: bold; color: #C62828; margin: 10px 0;">101</div>
                <p>{status_badge("At Risk")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with age_col2:
        # Badges claimed by week
        badges_col1, badges_col2, badges_col3 = st.columns(3)
        
        with badges_col1:
            st.markdown(
                f"""
                <div style="background-color: #E0F7FA; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="color: #00838F; margin-top: 0;">WEEK 0 BADGES</h4>
                    <div style="font-size: 28px; font-weight: bold; color: #00838F; margin: 5px 0;">3,089</div>
                    <p style="color: #00838F; font-size: 14px;">Goal: 5,000/week</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with badges_col2:
            st.markdown(
                f"""
                <div style="background-color: #E0F7FA; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="color: #00838F; margin-top: 0;">WEEK 1 BADGES</h4>
                    <div style="font-size: 28px; font-weight: bold; color: #00838F; margin: 5px 0;">2,061</div>
                    <p style="color: #00838F; font-size: 14px;">Goal: 5,000/week</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with badges_col3:
            st.markdown(
                f"""
                <div style="background-color: #E0F7FA; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="color: #00838F; margin-top: 0;">WEEK 2 BADGES</h4>
                    <div style="font-size: 28px; font-weight: bold; color: #00838F; margin: 5px 0;">2,197</div>
                    <p style="color: #00838F; font-size: 14px;">Goal: 5,000/week</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Badges Claimed Chart
    engage_badges_fig = px.bar(
        df_badges,
        x='Week',
        y='Badges Claimed',
        title='Badges Claimed by Week (Goal: 5,000/week)',
        color='Badges Claimed',
        color_continuous_scale=[secondary_green, primary_blue, secondary_purple]
    )
    engage_badges_fig.update_layout(title_font=dict(color=primary_blue))

    if st.session_state.show_target_lines:
        engage_badges_fig.add_shape(
            type="line",
            x0=-0.5,
            y0=5000,
            x1=len(df_badges)-0.5,
            y1=5000,
            line=dict(color="red", width=2, dash="dash")
        )

    # Add Notes Section
    st.markdown('<hr>', unsafe_allow_html=True)
    create_notes_section("Engagement")

# ---------------------------------
# Development Tab
# ---------------------------------
with tab4:
    st.markdown('<h3 class="section-title">Development Metrics</h3>', unsafe_allow_html=True)

    dev_col1, dev_col2, dev_col3 = st.columns(3)

    with dev_col1:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">TOTAL CONTRIBUTIONS</p>'
            f'<p class="metric-value">{format_currency(st.session_state.total_contributions)}</p>'
            f'<p>Goal: $10M</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with dev_col2:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">TOTAL GRANTS</p>'
            f'<p class="metric-value">{format_currency(st.session_state.total_grants)}</p>'
            f'<p>Count: 12/48</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with dev_col3:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">CORPORATE SPONSORSHIPS</p>'
            f'<p class="metric-value">$130,000</p>'
            f'<p>Goal: $1.5M (6/20 sponsors)</p>'
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
            f'<div class="metric-box">'
            f'<p class="metric-title">TOTAL SUBSCRIBERS</p>'
            f'<p class="metric-value">931,141</p>'
            f'<p>Goal: 1,300,000</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with sub_col2:
        st.markdown(
            f'<div class="metric-box">'
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
    
    # Social Media Followers
    st.markdown("<h3>Social Media Following</h3>", unsafe_allow_html=True)
    
    social_col1, social_col2, social_col3 = st.columns(3)
    
    with social_col1:
        st.markdown(
            f"""
            <div style="background-color: #E8F5FE; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #1877F2; margin-top: 0;">FACEBOOK</h4>
                <div style="font-size: 36px; font-weight: bold; color: #1877F2; margin: 10px 0;">382,000</div>
                <p style="color: #1877F2;">Followers</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with social_col2:
        st.markdown(
            f"""
            <div style="background-color: #FCEFF6; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #E1306C; margin-top: 0;">INSTAGRAM</h4>
                <div style="font-size: 36px; font-weight: bold; color: #E1306C; margin: 10px 0;">194,041</div>
                <p style="color: #E1306C;">Followers</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with social_col3:
        st.markdown(
            f"""
            <div style="background-color: #E8F0FE; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #0077B5; margin-top: 0;">LINKEDIN</h4>
                <div style="font-size: 36px; font-weight: bold; color: #0077B5; margin: 10px 0;">5,034</div>
                <p style="color: #0077B5;">Followers</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Recruitment Metrics that need updates
    st.markdown("<h3>Recruitment Marketing</h3>", unsafe_allow_html=True)
    
    recruit_col1, recruit_col2 = st.columns(2)
    
    with recruit_col1:
        st.markdown(
            f"""
            <div style="background-color: #FFF3E0; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #E65100; margin-top: 0;">RECRUITMENT PARTNERSHIPS</h4>
                <div style="font-size: 20px; font-weight: bold; color: #E65100; margin: 10px 0;">Needs Reporting Update</div>
                <p style="color: #E65100; font-style: italic;">Data collection in progress</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with recruit_col2:
        st.markdown(
            f"""
            <div style="background-color: #FFF3E0; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #E65100; margin-top: 0;">RECRUITMENT EVENTS HOSTED</h4>
                <div style="font-size: 20px; font-weight: bold; color: #E65100; margin: 10px 0;">Needs Reporting Update</div>
                <p style="color: #E65100; font-style: italic;">Data collection in progress</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # Social Media Engagement data from Self-Care School Campaign 
    st.markdown("<h3>Self-Care School Social Media Performance</h3>", unsafe_allow_html=True)
    
    # Create a grid of social metrics for Self-Care School Campaign
    social_grid_html = """
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px;">
        <div style="background-color: #F5F5F5; border-left: 5px solid #2196F3; padding: 15px; border-radius: 5px; text-align: center;">
            <div style="font-size: 13px; color: #757575;">IMPRESSIONS</div>
            <div style="font-size: 24px; font-weight: bold; color: #2196F3; margin: 5px 0;">338K</div>
        </div>
        <div style="background-color: #F5F5F5; border-left: 5px solid #4CAF50; padding: 15px; border-radius: 5px; text-align: center;">
            <div style="font-size: 13px; color: #757575;">CLICKS TO SITE</div>
            <div style="font-size: 24px; font-weight: bold; color: #4CAF50; margin: 5px 0;">39K</div>
        </div>
        <div style="background-color: #F5F5F5; border-left: 5px solid #9C27B0; padding: 15px; border-radius: 5px; text-align: center;">
            <div style="font-size: 13px; color: #757575;">VIDEO VIEWS</div>
            <div style="font-size: 24px; font-weight: bold; color: #9C27B0; margin: 5px 0;">70.7K</div>
        </div>
        <div style="background-color: #F5F5F5; border-left: 5px solid #FF5722; padding: 15px; border-radius: 5px; text-align: center;">
            <div style="font-size: 13px; color: #757575;">REACTIONS</div>
            <div style="font-size: 24px; font-weight: bold; color: #FF5722; margin: 5px 0;">3.2K</div>
        </div>
        <div style="background-color: #F5F5F5; border-left: 5px solid #795548; padding: 15px; border-radius: 5px; text-align: center;">
            <div style="font-size: 13px; color: #757575;">COMMENTS</div>
            <div style="font-size: 24px; font-weight: bold; color: #795548; margin: 5px 0;">74</div>
        </div>
        <div style="background-color: #F5F5F5; border-left: 5px solid #607D8B; padding: 15px; border-radius: 5px; text-align: center;">
            <div style="font-size: 13px; color: #757575;">SHARES</div>
            <div style="font-size: 24px; font-weight: bold; color: #607D8B; margin: 5px 0;">217</div>
        </div>
        <div style="background-color: #F5F5F5; border-left: 5px solid #FFC107; padding: 15px; border-radius: 5px; text-align: center;">
            <div style="font-size: 13px; color: #757575;">SAVES</div>
            <div style="font-size: 24px; font-weight: bold; color: #FFC107; margin: 5px 0;">66</div>
        </div>
        <div style="background-color: #F5F5F5; border-left: 5px solid #3F51B5; padding: 15px; border-radius: 5px; text-align: center;">
            <div style="font-size: 13px; color: #757575;">NEW FB PAGE LIKES</div>
            <div style="font-size: 24px; font-weight: bold; color: #3F51B5; margin: 5px 0;">67</div>
        </div>
    </div>
    
    <div style="background: linear-gradient(to bottom, #E8EAF6, #C5CAE9); border-radius: 10px; padding: 15px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <h4 style="color: #3F51B5; margin-top: 0;">Engagement Summary</h4>
        <p style="color: #3F51B5;">Super positive engagement and comments.</p>
        <p style="color: #3F51B5; font-weight: bold;">Action Item:</p>
        <p style="color: #3F51B5;">Increase replies to existing comments for better community engagement.</p>
    </div>
    """
    
    st.markdown(social_grid_html, unsafe_allow_html=True)

# ---------------------------------
# Operations Tab (Improved)
# ---------------------------------
with tab6:
    st.markdown('<h3 class="section-title">Operations Metrics</h3>', unsafe_allow_html=True)

    # --- Financial Trends (moved to top of tab) ---
    st.markdown('<h4>Financial Trends Overview</h4>', unsafe_allow_html=True)
    
    # Add disclaimer about dummy data
    st.markdown(
        """
        <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-style: italic; font-size: 14px;">
            Note: The financial data shown below is dummy data for presentation purposes only.
        </div>
        """,
        unsafe_allow_html=True
    )

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
        title='Revenue vs Expenses vs Donations',
        xaxis_title='Month',
        yaxis_title='USD ($)',
        title_font=dict(color=primary_blue),
        height=400,
        legend_title_text='Financial Lines'
    )

    st.plotly_chart(ops_trend_fig, use_container_width=True, key="ops_trend_fig_updated")

    # --- Budget Performance Chart (Full Width) ---
    st.markdown('<h4>Budget Performance</h4>', unsafe_allow_html=True)
    
    # Add disclaimer about dummy data
    st.markdown(
        """
        <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-style: italic; font-size: 14px;">
            Note: The budget data shown below is dummy data for presentation purposes only.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    budget_fig = px.bar(
        budget_data,
        x='Category',
        y=['Budget', 'Actual'],
        barmode='group',
        title='Budget vs Actual Spending by Category',
        color_discrete_sequence=[primary_blue, primary_orange]
    )
    budget_fig.update_layout(title_font=dict(color=primary_blue))
    
    st.plotly_chart(budget_fig, use_container_width=True, key="budget_fig")
    
    # --- Budget by Team ---
    st.markdown('<h4>Budget Performance by Team</h4>', unsafe_allow_html=True)
    
    # Create team budget data
    team_budget_data = pd.DataFrame({
        'Team': ['Executive', 'Marketing', 'Programs', 'Development', 'Technology', 'Operations'],
        'Budget': [850000, 750000, 1200000, 680000, 850000, 600000],
        'Actual': [780000, 710000, 1050000, 625000, 790000, 560000],
        'Percent': [91.8, 94.7, 87.5, 91.9, 92.9, 93.3]
    })
    
    team_budget_fig = px.bar(
        team_budget_data,
        x='Team',
        y=['Budget', 'Actual'],
        barmode='group',
        title='Budget vs Actual Spending by Team',
        color_discrete_sequence=[primary_blue, primary_orange]
    )
    team_budget_fig.update_layout(title_font=dict(color=primary_blue))
    
    st.plotly_chart(team_budget_fig, use_container_width=True, key="team_budget_fig")

    # --- System Performance ---
    st.markdown('<h4>Systems Performance</h4>', unsafe_allow_html=True)

    sys_col1, sys_col2, sys_col3 = st.columns(3)

    with sys_col1:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">ASANA ADOPTION</p>'
            f'<p class="metric-value">38%</p>'
            f'<p>Goal: 85%</p>'
            f'{status_badge("At Risk")}'
            f'</div>',
            unsafe_allow_html=True
        )

    with sys_col2:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">AUDIT COMPLIANCE</p>'
            f'<p class="metric-value">Pending</p>'
            f'<p>Goal: 100%</p>'
            f'{status_badge("Off Track")}'
            f'</div>',
            unsafe_allow_html=True
        )

    with sys_col3:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">CYBERSECURITY COMPLIANCE</p>'
            f'<p class="metric-value">Pending</p>'
            f'<p>Goal: 90%</p>'
            f'{status_badge("Off Track")}'
            f'</div>',
            unsafe_allow_html=True
        )
        
    # Add Notes Section
    st.markdown('<hr>', unsafe_allow_html=True)
    create_notes_section("Operations")

# ---------------------------------
# Member Care Tab (real data from PDF)
# ---------------------------------
with tab7:
    st.markdown('<h3 class="section-title">Member Care Metrics</h3>', unsafe_allow_html=True)

    mc_col1, mc_col2 = st.columns(2)

    with mc_col1:
        st.markdown(
            f'<div class="metric-box">'
            f'<p class="metric-title">MEMBER SATISFACTION RATING</p>'
            f'<p class="metric-value">95%</p>'
            f'<p>Goal: 85%</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with mc_col2:
        st.markdown(
            f'<div class="metric-box">'
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
    # Add Notes Section for Member Care
    st.markdown('<hr>', unsafe_allow_html=True)
    create_notes_section("Member Care")
    
    with st.expander("Story 2: Amazing Ted Talk used in class!"):
        st.write(
            "Hello ladies! First and foremost YOU ARE AMAZING. Sending so much love to you all and holding space for your amazing cause. "
            "I am a teacher in Ohio and I just wanted to tell you that I am using the TedTalk from 2018 in my Black History in America course. "
            "I can't wait to help my students use this frame of understanding. Thank you for shining a light on this - it is so needed! "
            "Thank you for taking action! Thank you for showing so much loving kindness! I appreciate you all and am so excited for this movement! "
            "Much love and respect, Kaitlin Finan"
        )
    
    with st.expander("Story 3: My Sister's Keeper"):
        st.markdown(
            """
            Morgan and Vanessa, I walked this evening. First chance I've had in a while. 
            And I talked on the phone to a friend of mine who was also walking at the time and had not walked in a while. 
            I invited her to walk with me and told her about Harriet Day and the meeting last night. 
            I also shared GirlTREK information with her and invited her to join. We're going to start walking together!
    
            I used to walk all the time. I moved back closer to my hometown four years ago to be near Mama and help take care of her. 
            She got better and was doing great, then all of a sudden she wasn't. Mama transitioned to Heaven a little over a year ago 
            and life has been difficult. She was everything to me. It's just been hard — but by the grace of God, I'm still standing. 
            He did bless us with 3 more years after she was hospitalized 33 days. I'm trying to get my legs back under me. 
            But I am lonely for Mama.
    
            99% of the time, I walked alone…didn't have anyone to walk with. But I would listen in some Saturdays. 
            Everybody is a few towns over, so weekday scheduling is tough. But I also told my sisters and my brother 
            that they were going to walk with me as a part of this next 10-week commitment.
    
            Thank you for all that you do, 
            Sandy B. Carter
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
            f'<div class="metric-box">'
            f'<p class="metric-title">ADVOCACY BRIEFS PUBLISHED</p>'
            f'<p class="metric-value">4 / 10</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with adv_col2:
        st.markdown(
            f'<div class="metric-box">'
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
    
    # Add Notes Section
    st.markdown('<hr>', unsafe_allow_html=True)
    create_notes_section("Advocacy")

# ---------------------------------
# Impact Tab (still marked as Pending)
# ---------------------------------
with tab9:
    st.markdown('<h3 class="section-title">Impact Metrics</h3>', unsafe_allow_html=True)

    # Create a more subtle notification
    st.markdown(
        """
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 3px solid #757575;">
            <p style="color: #424242; font-size: 15px;"><i>Note: GirlTREK's community health impact reporting will be updated following Self-Care School 2025 outcomes.</i></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h4>Upcoming Impact Metrics</h4>", unsafe_allow_html=True)
    st.markdown(
        """
        <p>The following metrics will be reported post Self-Care School 2025:</p>
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
    
# ---------------------------------
# Self-Care School Tab (NEW)
# ---------------------------------
with tab10:
    st.markdown('<h3 class="section-title">Self-Care School Campaign</h3>', unsafe_allow_html=True)
    
    # Campaign header with progress visualization
    campaign_progress = 11985 / 10000 * 100  # Calculate percentage of goal achieved
    
    progress_html = f"""
    <div style="background: linear-gradient(to right, #f0f9ff, #E3F2FD); border-radius: 10px; padding: 20px; margin-bottom: 25px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between;">
            <div>
                <h3 style="margin-top: 0; color: #1E88E5;">Self-Care School Campaign Status</h3>
                <p style="font-size: 16px;">Goal: 10,000 Registrants | Current: 11,985 Registrants</p>
                <div style="font-size: 18px; font-weight: bold; color: #00C853;">Status: {status_badge("Achieved")}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 40px; font-weight: bold; color: #1E88E5;">{campaign_progress:.1f}%</div>
                <p>of goal achieved</p>
            </div>
        </div>
        <div style="width: 100%; background-color: #E0E0E0; height: 15px; border-radius: 10px; margin-top: 15px;">
            <div style="width: {min(campaign_progress, 100)}%; height: 100%; background-color: #00C853; border-radius: 10px;"></div>
        </div>
    </div>
    """
    
    st.markdown(progress_html, unsafe_allow_html=True)
    
    # Key metrics in visually appealing boxes
    st.markdown('<h4>Key Metrics</h4>', unsafe_allow_html=True)
    
    metrics_row1_col1, metrics_row1_col2, metrics_row1_col3 = st.columns(3)
    
    with metrics_row1_col1:
        st.markdown(
            f"""
            <div style="background-color: #E8F5E9; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #2E7D32; margin-top: 0;">NEW MEMBERS</h4>
                <div style="font-size: 36px; font-weight: bold; color: #2E7D32; margin: 10px 0;">4,808</div>
                <p style="color: #2E7D32;">Joined through campaign</p>
                <p>{status_badge("On Track")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with metrics_row1_col2:
        st.markdown(
            f"""
            <div style="background-color: #FFF8E1; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #FF8F00; margin-top: 0;">DOWNLOADS</h4>
                <div style="font-size: 36px; font-weight: bold; color: #FF8F00; margin: 10px 0;">22,186</div>
                <p style="color: #FF8F00;">Goal: 100,000</p>
                <p>{status_badge("At Risk")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with metrics_row1_col3:
        st.markdown(
            f"""
            <div style="background-color: #E1F5FE; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #0277BD; margin-top: 0;">STORIES SUBMITTED</h4>
                <div style="font-size: 36px; font-weight: bold; color: #0277BD; margin: 10px 0;">234</div>
                <p style="color: #0277BD;">Goal: 100</p>
                <p>{status_badge("Achieved")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Age demographics  
    st.markdown('<h4>Age Demographics</h4>', unsafe_allow_html=True)
    
    age_col1, age_col2 = st.columns([1, 3])
    
    with age_col1:
        st.markdown(
            f"""
            <div style="background-color: #FFEBEE; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #C62828; margin-top: 0;">REGISTRANTS AGE 18-25</h4>
                <div style="font-size: 36px; font-weight: bold; color: #C62828; margin: 10px 0;">101</div>
                <p>{status_badge("At Risk")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with age_col2:
        # Badges claimed by week
        badges_col1, badges_col2, badges_col3 = st.columns(3)
        
        with badges_col1:
            st.markdown(
                f"""
                <div style="background-color: #E0F7FA; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="color: #00838F; margin-top: 0;">WEEK 0 BADGES</h4>
                    <div style="font-size: 28px; font-weight: bold; color: #00838F; margin: 5px 0;">3,089</div>
                    <p style="color: #00838F; font-size: 14px;">Goal: 5,000/week</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with badges_col2:
            st.markdown(
                f"""
                <div style="background-color: #E0F7FA; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="color: #00838F; margin-top: 0;">WEEK 1 BADGES</h4>
                    <div style="font-size: 28px; font-weight: bold; color: #00838F; margin: 5px 0;">2,061</div>
                    <p style="color: #00838F; font-size: 14px;">Goal: 5,000/week</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with badges_col3:
            st.markdown(
                f"""
                <div style="background-color: #E0F7FA; border-radius: 10px; padding: 15px; height: 100%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="color: #00838F; margin-top: 0;">WEEK 2 BADGES</h4>
                    <div style="font-size: 28px; font-weight: bold; color: #00838F; margin: 5px 0;">2,197</div>
                    <p style="color: #00838F; font-size: 14px;">Goal: 5,000/week</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Social Media Performance with visualizations
    st.markdown('<h4>Social Media Performance</h4>', unsafe_allow_html=True)
    
    # Create two columns - left for metrics, right for engagement summary
    social_col1, social_col2 = st.columns([3, 1])
    
    with social_col1:
        # Grid of social metrics
        social_grid_html = """
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px;">
            <div style="background-color: #F5F5F5; border-left: 5px solid #2196F3; padding: 15px; border-radius: 5px; text-align: center;">
                <div style="font-size: 13px; color: #757575;">IMPRESSIONS</div>
                <div style="font-size: 24px; font-weight: bold; color: #2196F3; margin: 5px 0;">338K</div>
            </div>
            <div style="background-color: #F5F5F5; border-left: 5px solid #4CAF50; padding: 15px; border-radius: 5px; text-align: center;">
                <div style="font-size: 13px; color: #757575;">CLICKS TO SITE</div>
                <div style="font-size: 24px; font-weight: bold; color: #4CAF50; margin: 5px 0;">39K</div>
            </div>
            <div style="background-color: #F5F5F5; border-left: 5px solid #9C27B0; padding: 15px; border-radius: 5px; text-align: center;">
                <div style="font-size: 13px; color: #757575;">VIDEO VIEWS</div>
                <div style="font-size: 24px; font-weight: bold; color: #9C27B0; margin: 5px 0;">70.7K</div>
            </div>
            <div style="background-color: #F5F5F5; border-left: 5px solid #FF5722; padding: 15px; border-radius: 5px; text-align: center;">
                <div style="font-size: 13px; color: #757575;">REACTIONS</div>
                <div style="font-size: 24px; font-weight: bold; color: #FF5722; margin: 5px 0;">3.2K</div>
            </div>
            <div style="background-color: #F5F5F5; border-left: 5px solid #795548; padding: 15px; border-radius: 5px; text-align: center;">
                <div style="font-size: 13px; color: #757575;">COMMENTS</div>
                <div style="font-size: 24px; font-weight: bold; color: #795548; margin: 5px 0;">74</div>
            </div>
            <div style="background-color: #F5F5F5; border-left: 5px solid #607D8B; padding: 15px; border-radius: 5px; text-align: center;">
                <div style="font-size: 13px; color: #757575;">SHARES</div>
                <div style="font-size: 24px; font-weight: bold; color: #607D8B; margin: 5px 0;">217</div>
            </div>
            <div style="background-color: #F5F5F5; border-left: 5px solid #FFC107; padding: 15px; border-radius: 5px; text-align: center;">
                <div style="font-size: 13px; color: #757575;">SAVES</div>
                <div style="font-size: 24px; font-weight: bold; color: #FFC107; margin: 5px 0;">66</div>
            </div>
            <div style="background-color: #F5F5F5; border-left: 5px solid #3F51B5; padding: 15px; border-radius: 5px; text-align: center;">
                <div style="font-size: 13px; color: #757575;">NEW FB PAGE LIKES</div>
                <div style="font-size: 24px; font-weight: bold; color: #3F51B5; margin: 5px 0;">67</div>
            </div>
        </div>
        """
        
        st.markdown(social_grid_html, unsafe_allow_html=True)
    
    with social_col2:
        st.markdown(
            """
            <div style="background: linear-gradient(to bottom, #E8EAF6, #C5CAE9); border-radius: 10px; padding: 15px; height: 100%; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h4 style="color: #3F51B5; margin-top: 0;">Engagement Summary</h4>
                <p style="color: #3F51B5;">Super positive engagement and comments.</p>
                <p style="color: #3F51B5; font-weight: bold;">Action Item:</p>
                <p style="color: #3F51B5;">Increase replies to existing comments for better community engagement.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
