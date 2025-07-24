import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
import re
import uuid
import io
import sys
import subprocess

# Initialize persistent state
if "persist" not in st.session_state:
    st.session_state.persist = True

# Check if reportlab is installed, if not install it
try:
    import reportlab
except ImportError:
    print("ReportLab not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
    print("ReportLab installed successfully!")
    import reportlab

# Import reportlab components after ensuring installation
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart

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

def add_board_update(tab_name):
    """Add a leadership update section to the top of a tab"""
    dark_mode = st.session_state.dark_mode if 'dark_mode' in st.session_state else False
    
    # Check if there are notes for this tab
    notes_key = f"notes_{tab_name}"
    update_content = ""
    
    # Special content for Advocacy tab
    if tab_name == "Advocacy":
        update_content = """
        <p>In Phase 1, Year 1, our strategic focus is on designing the plan for phases 1 and 2, socializing the advocacy agenda amongst our members, establishing the research basis for the 10 points, and beginning to build advocacy engagement models with our members in our most active geographies. Our key activities have included / will include:</p>
        
        <p><strong>Robust Articulation of 10-Point Plan:</strong> During the first half of 2025, worked in close partnership with GT co-founders to expand and make more robust our 10-Point Plan for Joy & Justice. Co-Founders then anchored to the plan during the 10 week curriculum of Self-Care School, and will continue socializing the Plan to our members during Summer of Solidarity.</p>
        
        <p><strong>Design of Phases 1 and 2:</strong> As detailed above, we are responding to the current political environment by designing a phased approach to member organizing and coalition building, all in service of achieving our organizational 10x10 mission.</p>
        
        <p><strong>Establish Research Foundation for Advocacy Agenda:</strong> Research Director is leading the development of "Advocacy Briefs" for each of the 10 points on the Advocacy Agenda, clearly articulating the research basis for each of the demands (seeking to answer the question: why is this issue killing Black women at a disproportionate rate?).</p>
        
        <p><strong>Utilize Launch of Mobile App to Engage Membership around Advocacy Agenda:</strong> Through Summer of Solidarity programming, members will be encouraged to download the mobile app and begin logging walks; encouragement will come in the form of "weekly dispatches," with content dedicated to uplifting and advancing the advocacy agenda (e.g. calls to action from strategic partners, member reflections on key questions).</p>
        
        <p><strong>Relationship Building with Key Constituencies:</strong> Director of Civic Partnerships is building and deepening relationships with youth-serving organizations to align with stated commitment to "next generation leadership;" will use the launch of the mobile app to encourage partner organizations to engage their youth members.</p>
        
        <p><strong>Test Advocacy-Led Member Engagement in Key Geographies:</strong> Advocacy team will identify 10 most active GT geographies, and correlate these to most populated domestic Black geographies as well as Care Village location(s). Will liaise with GT crew leaders and member care team, especially through formation of "Women of Wisdom" advisory council, to engage in advocacy listening sessions. Will consider "on the ground" training or "test sites" depending on outcome(s) of listening sessions.</p>
        
        <p><strong>Lay the Foundation for Phase 2 by Forming Organizational Relationships:</strong> Proactively identify and cultivate relationships with potential Coalition partners whose missions and work align with our agenda.</p>
        """
    elif notes_key in st.session_state and st.session_state[notes_key].strip():
        update_content = st.session_state[notes_key]
    else:
        update_content = "<p style='font-style: italic; color: #999;'>No leadership updates at this time.</p>"
    
    if dark_mode:
        board_update_html = f'''
        <div style="background-color: #1E2130; border-left: 5px solid #0088FF; 
             padding: 20px; border-radius: 5px; margin: 15px 0 25px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">
            <h4 style="color: #4DA6FF; margin-top: 0; margin-bottom: 15px; font-size: 18px;">Leadership Update: {tab_name}</h4>
            <div style="color: #E0E0E0; line-height: 1.5;">
                {update_content}
        </div>
        '''
    else:
        board_update_html = f'''
        <div style="background-color: #F3F9FF; border-left: 5px solid #0088FF; 
             padding: 20px; border-radius: 5px; margin: 15px 0 25px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h4 style="color: #0088FF; margin-top: 0; margin-bottom: 15px; font-size: 18px;">Leadership Update: {tab_name}</h4>
            <div style="color: #333333; line-height: 1.5;">
                {update_content}
        </div>
        '''
    
    st.markdown(board_update_html, unsafe_allow_html=True)

def create_notes_section(tab_name):
    """Create a notes section for any tab with persistence across sessions"""
    notes_key = f"notes_{tab_name}"
    
    # Initialize notes in session state if they don't exist
    if notes_key not in st.session_state:
        # Try to load from disk if available
        try:
            with open(f"{notes_key}.txt", "r") as f:
                st.session_state[notes_key] = f.read()
        except FileNotFoundError:
            st.session_state[notes_key] = ""
    
    if 'recent_notes' not in st.session_state:
        st.session_state.recent_notes = []
    
    with st.expander(f"📝 Notes for {tab_name}", expanded=False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Create text area for notes with the current value from session state
            notes = st.text_area(
                "Add your notes here:",
                value=st.session_state[notes_key],
                height=150,
                key=f"textarea_{notes_key}_{tab_name}"  # Made key more unique
            )
            
            # Automatically save notes when they change
            if notes != st.session_state[notes_key]:
                previous_notes = st.session_state[notes_key]
                st.session_state[notes_key] = notes
                
                # Save to disk for persistence across sessions
                try:
                    with open(f"{notes_key}.txt", "w") as f:
                        f.write(notes)
                except Exception as e:
                    st.error(f"Error saving notes: {str(e)}")
                
                if 'last_edit_time' not in st.session_state:
                    st.session_state.last_edit_time = {}
                    
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.last_edit_time[notes_key] = timestamp
                
                # Track recent note submissions
                if notes.strip() and (not previous_notes.strip() or notes.strip() != previous_notes.strip()):
                    note_summary = notes.strip() if len(notes.strip()) < 50 else notes.strip()[:47] + "..."
                    st.session_state.recent_notes.insert(0, {
                        "tab": tab_name,
                        "summary": note_summary,
                        "timestamp": timestamp
                    })
                    if len(st.session_state.recent_notes) > 5:
                        st.session_state.recent_notes = st.session_state.recent_notes[:5]
                
                st.success("✅ Notes saved automatically!")

        with col2:
            # Display timestamp of last edit if available
            if 'last_edit_time' in st.session_state and notes_key in st.session_state.last_edit_time:
                st.info(f"Last edited: {st.session_state.last_edit_time[notes_key]}")
            
            # Add export functionality
            if st.button("Export Notes", key=f"export_{tab_name}"):
                notes_data = f"Tab,Notes\n{tab_name},{st.session_state[notes_key].replace(',', ';').replace('\n', ' ')}"
                b64 = base64.b64encode(notes_data.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="{tab_name}_notes.csv">Download {tab_name} Notes</a>'
                st.markdown(href, unsafe_allow_html=True)
            
            # Add ability to clear notes
            if st.button("Clear Notes", key=f"clear_{tab_name}"):
                st.session_state[notes_key] = ""
                if 'last_edit_time' in st.session_state and notes_key in st.session_state.last_edit_time:
                    del st.session_state.last_edit_time[notes_key]
                
                # Remove the file to reflect cleared notes
                try:
                    import os
                    os.remove(f"{notes_key}.txt")
                except FileNotFoundError:
                    pass
                
                st.rerun()  # Updated from experimental_rerun

def save_global_notes(global_notes):
    """Save global notes with persistence across sessions"""
    previous_notes = st.session_state.global_notes
    st.session_state.global_notes = global_notes
    
    # Save to disk for persistence across sessions
    try:
        with open("global_notes.txt", "w") as f:
            f.write(global_notes)
    except Exception as e:
        st.sidebar.error(f"Error saving global notes: {str(e)}")
        return
    
    # Track recent note submissions
    if global_notes.strip() and (not previous_notes.strip() or global_notes.strip() != previous_notes.strip()):
        note_summary = global_notes.strip() if len(global_notes.strip()) < 50 else global_notes.strip()[:47] + "..."
        if 'recent_notes' not in st.session_state:
            st.session_state.recent_notes = []
        
        st.session_state.recent_notes.insert(0, {
            "tab": "Global",
            "summary": note_summary,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        if len(st.session_state.recent_notes) > 5:
            st.session_state.recent_notes = st.session_state.recent_notes[:5]
            
    st.sidebar.success("✅ Global notes saved successfully!")

# PDF Generation Function
def generate_pdf(section_name, dark_mode=False):
    """Generate a PDF report for the selected dashboard section"""
    buffer = io.BytesIO()
    
    if dark_mode:
        background_color = colors.HexColor('#121212')
        text_color = colors.white
        accent_color = colors.HexColor('#0088FF')
    else:
        background_color = colors.white
        text_color = colors.black
        accent_color = colors.HexColor('#0088FF')
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        textColor=accent_color,
        spaceAfter=12
    )
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading1'],
        textColor=accent_color,
        spaceAfter=10
    )
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        textColor=text_color,
        spaceAfter=6
    )
    
    elements = []
    
    elements.append(Paragraph(f"GirlTREK Organizational Dashboard", title_style))
    elements.append(Paragraph(f"Q2 2025 Metrics Overview - {section_name}", heading_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add section-specific content based on real data
    if section_name == "Executive Summary":
        elements.append(Paragraph("Key Metrics", heading_style))
        
        data = [
            ["Metric", "Current Value", "Goal", "Status"],
            ["Total Membership", f"{format_number(st.session_state.total_membership)}", "1,700,000", "On Track"],
            ["Total New Members", f"{format_number(st.session_state.new_members)}", "100,000", "On Track"],
            ["Total Contributions", f"{format_currency(st.session_state.total_contributions)}", "$10,000,000", "On Track"]
        ]
        
        t = Table(data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.25*inch))
        
        elements.append(Paragraph("Report Card Progress", heading_style))
        report_data = [
            ["Goal", "Current Total", "Percent Progress", "Status"],
            ["Recruit 100,000 new members", "15,438", "15.44%", "On Track"],
            ["Engage 250,000 members", "13,119", "5.25%", "On Track"],
            ["Support 65,000 walking daily", "5,634", "8.67%", "At Risk"],
            ["Unite 3 advocacy partners", "0", "0%", "On Track"],
            ["Raise $10M", "$3,109,294.25", "31.09%", "On Track"],
            ["Establish Care Village", "3,055", "7.64%", "On Track"],
            ["Achieve 85% organizational health", "100%", "100%", "On Track"]
        ]
        
        t2 = Table(report_data, colWidths=[2.5*inch, 1.5*inch, 1*inch, 1*inch])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t2)
    
    # Add notes if they exist
    if section_name in ["Executive Summary", "Recruitment", "Engagement", "Development", "Marketing", "Operations", "Member Care", "Advocacy", "Impact"]:
        notes_key = f"notes_{section_name}"
        if notes_key in st.session_state and st.session_state[notes_key]:
            elements.append(Spacer(1, 0.5*inch))
            elements.append(Paragraph("Notes", heading_style))
            elements.append(Paragraph(st.session_state[notes_key], normal_style))
    
    if 'global_notes' in st.session_state and st.session_state.global_notes:
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("Global Dashboard Notes", heading_style))
        elements.append(Paragraph(st.session_state.global_notes, normal_style))
    
    doc.build(elements)
    
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(pdf_data).decode()

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

# Initialize global notes from disk if available
if 'global_notes' not in st.session_state:
    try:
        with open("global_notes.txt", "r") as f:
            st.session_state.global_notes = f.read()
    except FileNotFoundError:
        st.session_state.global_notes = ""

# Session State - Updated with real data from CSV
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'total_membership' not in st.session_state:
    st.session_state.total_membership = 1244476  # Real data from CSV
    st.session_state.new_members = 15438  # Real data from CSV
    st.session_state.total_contributions = 3109294.25  # Real data from CSV
    st.session_state.total_grants = 3101133.09  # Real data from CSV
    st.session_state.data_loaded = True

# Main App
def main():
    # Sidebar
    st.sidebar.markdown("### Download Dashboard")
    download_options = [
        "Executive Summary", "Recruitment", "Engagement",
        "Development", "Marketing", "Operations",
        "Member Care", "Advocacy", "Impact", "Complete Dashboard"
    ]
    selected_download = st.sidebar.selectbox("Select dashboard section to download:", download_options)

    if st.sidebar.button("Generate PDF for Download"):
        with st.sidebar:
            with st.spinner("Generating PDF..."):
                pdf_base64 = generate_pdf(selected_download, dark_mode=st.session_state.dark_mode)
                filename = f"{selected_download.replace(' ', '_')}_report.pdf"
                download_link = f'<a href="data:application/pdf;base64,{pdf_base64}" download="{filename}">Download {selected_download} PDF</a>'
                st.success(f"PDF for {selected_download} has been generated!")
                st.markdown(download_link, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Dashboard Settings")
    if 'show_target_lines' not in st.session_state:
        st.session_state.show_target_lines = True
        
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
        
    show_target_lines = st.sidebar.checkbox("Show Target Lines", value=st.session_state.show_target_lines, key="show_target_lines_checkbox")
    dark_mode = st.sidebar.checkbox("Dark Mode", value=st.session_state.dark_mode, key="dark_mode_checkbox")

    st.session_state.show_target_lines = show_target_lines
    st.session_state.dark_mode = dark_mode

    apply_dark_mode(dark_mode)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Dashboard Notes")

    global_notes = st.sidebar.text_area(
        "Add global notes for the entire dashboard:",
        value=st.session_state.global_notes,
        height=100,
        key="textarea_global_notes"
    )

    if st.sidebar.button("Save Global Notes"):
        save_global_notes(global_notes)

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

    if st.sidebar.button("Export All Notes"):
        all_notes = {"Global": st.session_state.global_notes}
        
        for tab in ["Executive Summary", "Recruitment", "Engagement", "Development", 
                    "Marketing", "Operations", "Member Care", "Advocacy", "Impact"]:
            tab_key = f"notes_{tab}"
            if tab_key in st.session_state:
                all_notes[tab] = st.session_state[tab_key]
        
        csv_data = "Tab,Notes\n"
        for tab, notes in all_notes.items():
            clean_notes = notes.replace(',', ';').replace('\n', ' ')
            csv_data += f"{tab},{clean_notes}\n"
        
        b64 = base64.b64encode(csv_data.encode()).decode()
        date_str = datetime.now().strftime("%Y%m%d")
        href = f'<a href="data:file/csv;base64,{b64}" download="GirlTREK_Dashboard_Notes_{date_str}.csv">Download All Notes</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)

    # App Title
    st.title("GirlTREK Organizational Dashboard")
    st.markdown("### Q2 2025 Metrics Overview")
    st.markdown("*Data dashboard was published on June 30, 2025*")

    # Load dataframes with real data from CSV

    # New Members by Month - Real data
    df_extended = pd.DataFrame({
        'Month': ['Oct 2024', 'Nov 2024', 'Dec 2024', 'Jan 2025', 'Feb 2025', 'Mar 2025', 'Apr 2025', 'May 2025', 'Jun 2025'],
        'New Members': [1365, 1419, 182, 591, 1588, 4382, 6073, 2610, 123],
        'Date': [
            datetime(2024, 10, 1),
            datetime(2024, 11, 1),
            datetime(2024, 12, 1),
            datetime(2025, 1, 1),
            datetime(2025, 2, 1),
            datetime(2025, 3, 1),
            datetime(2025, 4, 1),
            datetime(2025, 5, 1),
            datetime(2025, 6, 1)
        ]
    })

    # New Members by Age - Real data
    df_new_age = pd.DataFrame({
        'Age Group': ['18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+', 'Unknown'],
        'New Members': [90, 504, 1923, 2389, 2039, 8479]
    })

    # Total Membership by Age - Real data
    df_total_age = pd.DataFrame({
        'Age Group': ['18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+', 'Unknown*'],
        'Members': [1739, 16515, 82893, 164106, 108669, 755521]
    })

    # Top States & Top Cities - Real data
    df_top_states = pd.DataFrame({
        'State': ['Texas', 'Georgia', 'California', 'New York', 'Florida'],
        'Members': [89043, 84799, 77919, 66670, 64880]
    })

    df_top_cities = pd.DataFrame({
        'City': ['Chicago', 'Philadelphia', 'Houston', 'Brooklyn', 'Atlanta'],
        'Members': [20166, 16775, 16662, 15197, 12797]
    })

    # Historic Movement Growth Numbers - Real data where available
    df_historic_growth = pd.DataFrame({
        'Year': [2020, 2021, 2022, 2023, 2024, 2025],
        'Trekkers': [1000000, 1218000, 1214566, 1207517, 1229038, 1244476],
        'New Women': [626660, 218000, -3434, -7049, 21521, 15438]
    })

    # Financial Revenue Breakdown - Real data
    df_finance = pd.DataFrame({
        'Category': ['Donations', 'Grants'],
        'Amount': [8161.16, 3101133.09]
    })

    # Financial Trend Data - Real data (May 2025 YTD)
    finance_trend_data = pd.DataFrame({
        'Month': ['January', 'February', 'March', 'April', 'May'],
        'Revenue': [648705, 648705, 648705, 648705, 648706],  # Total: 3,243,526
        'Expenses': [468772, 468772, 468772, 468773, 468773]  # Total: 2,343,862
    })

    # Email and Subscriber Activity Data - Real data
    df_activity = pd.DataFrame({
        'Period': ['30 day'],
        'Openers': [19148],
        'Clickers': [12904]
    })

    # Member Care Data - Real data
    member_care_data = pd.DataFrame({
        'Metric': ['Member Satisfaction Rating', 'Resolution/Responsiveness Rate', 'Top Member Issues/Concerns'],
        'Goal': ['95%', '48 hours', '-'],
        'Current Total': ['93%', '2 hours', 'SCS Registration Error Message & Connecting to the Movement']
    })

    # Email Performance Comparison Data
    comparison_data = pd.DataFrame({
        'Metric': ['Open Rate', 'Click-Through Rate'],
        'GirlTREK': [18.54, 1.06],
        'Nonprofit Industry Average': [28.59, 3.29]
    })
    
    # Knowledge Impact Data for Campaigns
    knowledge_data = pd.DataFrame({
        'Topic': [
            'Land rights, housing & environmental justice',
            'Civic engagement & political participation',
            'Safety, self-defense & public resource access',
            'Decarceration, gun safety & restorative justice',
            'Mental health & emotional boundaries',
            'Radical care, family legacy & intergenerational healing',
            'Parenting, mentorship & end-of-life planning',
            'Self-esteem, celebration & personal empowerment'
        ],
        'Members': [710, 569, 645, 658, 622, 695, 536, 602]
    })
    
    # Age Distribution Data for Campaigns
    age_dist_data = pd.DataFrame({
        'Age Group': ['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75-84', '85-94'],
        'Participants': [21, 66, 386, 1316, 2268, 1077, 440, 50, 2]
    })
    
    # Badge Week Data for Campaigns
    badge_week_data = pd.DataFrame({
        'Week': ['Week 0', 'Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 
                'Week 6', 'Week 7', 'Week 8', 'Week 9', 'Week 10', 'Final Impact'],
        'Badges Claimed': [3442, 2400, 2862, 1928, 1521, 1477, 2234, 1531, 1460, 1847, 1334, 867]
    })

    # Create Tabs - Adding Campaigns tab
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "Executive Summary",
        "Recruitment",
        "Engagement",
        "Development",
        "Marketing",
        "Campaigns",
        "Operations",
        "Member Care",
        "Advocacy",
        "Impact"
    ])

    # ---------------------------------
    # Executive Summary Tab
    # ---------------------------------
    with tab1:
        add_board_update("Executive Summary")
        
        st.markdown('<h3 class="section-title">Executive Summary</h3>', unsafe_allow_html=True)

        st.markdown("<h3>Key Metrics</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL MEMBERSHIP</p>'
                f'<p class="metric-value">{format_number(st.session_state.total_membership)}</p>'
                f'<p>Goal: 1,700,000</p>'
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
                f'<p>{status_badge("At Risk")}</p>'
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

        st.markdown('<h3>Report Card Progress</h3>', unsafe_allow_html=True)

        report_data = {
            "Goal": [
                "Recruit 100,000 new members",
                "Engage 250,000 members",
                "Support 65,000 walking daily",
                "Unite 3 advocacy partners",
                "Raise $10M",
                "Establish Care Village (40k)",
                "Achieve 85% organizational health"
            ],
            "Current Total": [
                "15,438", "13,119", "5,634", "0",
                "$3,109,294.25", "3,055", "100%"
            ],
            "Percent Progress": [
                "15.44%", "5.25%", "8.67%", "0%", "31.09%", "7.64%", "100%"
            ],
            "Status": [
                "On Track", "On Track", "At Risk", "On Track",
                "On Track", "On Track", "On Track"
            ],
            "Progress": [
                15.44, 5.25, 8.67, 0, 31.09, 7.64, 100
            ]
        }

        for i in range(len(report_data["Goal"])):
            goal = report_data["Goal"][i]
            current = report_data["Current Total"][i]
            percent = report_data["Percent Progress"][i]
            status = report_data["Status"][i]
            progress = report_data["Progress"][i]

            # Add context for Care Village
            if "Care Village" in goal:
                goal += '<br><span style="font-size: 12px; font-style: italic; color: #666;">Reach 40,000 Black women with localized public health services</span>'

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
                    <div style="width: {min(progress, 100)}%; height: 100%; background-color: {bar_color}; border-radius: 6px;"></div>
                </div>
            </div>
            """
            st.markdown(progress_html, unsafe_allow_html=True)

        st.markdown("<h3>Historic Movement Growth Numbers</h3>", unsafe_allow_html=True)
        
        # Add historic comparison note
        st.markdown(
            f"""
            <div style="background-color: #E3F2FD; border-radius: 10px; padding: 15px; margin-bottom: 20px; border-left: 5px solid #2196F3;">
                <h5 style="color: #1565C0; margin-top: 0;">Historic Comparison - 2017</h5>
                <p style="color: #424242;">In 2017: <strong>116,938 Trekkers</strong> | <strong>44,149 New Women</strong> | <strong>60.65% Growth</strong></p>
                <p style="color: #424242;">For comparison: In 2020, we reached <strong>1,000,000 Trekkers</strong> with <strong>626,660 New Women</strong> joining (<strong>167.85% Growth</strong>)</p>
            </div>
            """,
            unsafe_allow_html=True
        )

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
            title='Historic Growth of Trekkers (2020–2025)',
            xaxis_title='Year',
            yaxis_title='Total Trekkers',
            title_font=dict(color=primary_blue),
            height=400
        )

        st.plotly_chart(historic_fig, use_container_width=True, key="historic_growth_fig")

        st.markdown('<h3>Membership Distribution</h3>', unsafe_allow_html=True)

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
        
        # Add note about Unknown age group
        st.markdown(
            """
            <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; margin-top: -10px; font-style: italic; font-size: 13px;">
                *Unknown: Members who have not submitted date of birth or age in data collection. Date of birth is optional.
            </div>
            """,
            unsafe_allow_html=True
        )

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
        
        # Data Analysis & Recommendations
        st.markdown('### 📊 Data Analysis & Recommendations')
        
        # Key Insights
        st.markdown('#### 🔍 Key Insights')
        st.info("""
        **Strong Overall Progress:** 4 out of 7 major goals are on track, with organizational health at 100% and fundraising at 31% of target
        
        **Membership Growth:** At 73% of target membership (1.24M vs 1.7M goal), showing solid foundation
        
        **Geographic Concentration:** Top 5 states represent 25% of total membership, indicating strong regional presence
        
        **Age Distribution Opportunity:** 61% of members have not provided age data, suggesting data collection improvements needed
        """)
        
        # Strategic Recommendations
        st.markdown('#### 💡 Strategic Recommendations')
        st.success("""
        **Address At-Risk Goals:** Focus resources on walking daily support (8.67% progress) and advocacy partnerships (0% progress)
        
        **Accelerate Recruitment:** New member acquisition at 15.44% needs strategic boost to reach 100K goal
        
        **Enhance Data Collection:** Implement incentives for members to complete profile information, especially age demographics
        
        **Geographic Expansion:** Leverage success in top states to develop strategies for underrepresented regions
        
        **Capitalize on Strengths:** Use strong fundraising momentum and organizational health to support struggling areas
        """)
        
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Executive Summary")
        
    # ---------------------------------
    # Recruitment Tab
    # ---------------------------------
    with tab2:
        add_board_update("Recruitment")
        
        st.markdown('<h3 class="section-title">Recruitment Metrics</h3>', unsafe_allow_html=True)

        recruitment_col1, recruitment_col2, recruitment_col3 = st.columns(3)

        with recruitment_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL NEW MEMBERS</p>'
                f'<p class="metric-value">{format_number(st.session_state.new_members)}</p>'
                f'<p>Goal: 100,000</p>'
                f'<p>{status_badge("At Risk")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        with recruitment_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">NEW MEMBERS AGE 18-25</p>'
                f'<p class="metric-value">316</p>'
                f'<p>Goal: 100,000</p>'
                f'<p>{status_badge("At Risk")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        with recruitment_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL RECRUITMENT PARTNERSHIPS</p>'
                f'<p class="metric-value">18</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666; margin-bottom: 5px;">Contact has been made with 20 community organizations</p>'
                f'<p>Goal: 10</p>'
                f'<p>{status_badge("Achieved")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        recruit_monthly_fig = px.bar(
            df_extended,
            x='Month',
            y='New Members',
            title='New Member Recruitment by Month (2024-2025)',
            color='New Members',
            color_continuous_scale=[secondary_blue, primary_blue, primary_orange]
        )
        recruit_monthly_fig.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(recruit_monthly_fig, use_container_width=True, key="recruit_monthly_fig")
        
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
        
        st.plotly_chart(new_age_fig, use_container_width=True, key="new_age_fig")

        # Recruitment Programs Section
        st.markdown('<h3>Recruitment Programs</h3>', unsafe_allow_html=True)
        
        # College Aged Women Program
        with st.expander("📚 College Aged Women - Nyra Govan", expanded=False):
            # Program Overview
            st.markdown('<h5>Program Overview</h5>', unsafe_allow_html=True)
            st.markdown(
                """
                The GirlTREK College Crews initiative was created because GirlTREK has been waiting for students to be the revolutionaries that the world has been waiting for. Throughout history we have seen the youth at the forefront of many revolutions with their eyes locked on long-term reforms. Given the current economic climate and conditions, there is concern for students' well-being as they progress through college. 
                
                GirlTREK aims to provide a safe space for the next generation. GirlTREK looks forward to bringing its culture to college campuses to help the next generation prioritize their health and create a safe space on college campuses. Through daily walking, students will be able to connect with like minded individuals as they walk to better health, being leaders on campus and in the community. 
                
                The practice of radical self-care is not in the academic curriculum, so we want to ensure that students are starting this behavior change early in their life instead of falling to the system of burnout throughout their collegiate experience. The northern star of this goal is to get 100 college students across 100 college campuses to start crews on colleges across the country, with a focus on HBCUs. These college students will be our college leads that are leading their peers by walking, talking, and solving problems at their universities. 
                
                **Things change when Black women walk** – GirlTREK is excited to empower young women to start their self-care journey now.
                """
            )
            
            # Program Goals
            st.markdown('<h5>Program Goals</h5>', unsafe_allow_html=True)
            st.markdown(
                """
                * **Recruitment**: Identify and train 100 students in MHFA to serve as College Crew Leads on 100 campuses
                * **Engagement**: Encourage students to host walks once a month on campus, creating safe spaces for college women
                * **Impact**: Promote physical activity and empower the next generation of Legacy Builders for the movement
                """
            )
            
            # Current Status Metrics
            st.markdown('<h5>Current Status</h5>', unsafe_allow_html=True)
            
            college_col1, college_col2 = st.columns(2)
            
            with college_col1:
                st.markdown(
                    f'<div class="metric-box">'
                    f'<p class="metric-title">COLLEGE LEADS RECRUITED</p>'
                    f'<p class="metric-value">11 / 100</p>'
                    f'<p style="font-size: 14px; color: #666;">11% of target achieved</p>'
                    f'<p>{status_badge("At Risk")}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            with college_col2:
                st.markdown(
                    f'<div class="metric-box">'
                    f'<p class="metric-title">WALKS COMPLETED</p>'
                    f'<p class="metric-value">0</p>'
                    f'<p style="font-style: italic; font-size: 12px; color: #666;">Due to semester not beginning yet</p>'
                    f'<p>Goal: Monthly walks on campus</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            # Walk Schedule
            st.markdown('<h5>Scheduled Solidarity Walks</h5>', unsafe_allow_html=True)
            st.markdown('<p style="font-style: italic;">Rounds of walks scheduled for college students to walk in solidarity together:</p>', unsafe_allow_html=True)
            
            college_schedule_html = f"""
            <div style="background-color: #F3F9FF; border-radius: 10px; padding: 15px; margin: 10px 0;">
                <p><strong>Round 1</strong>: September 18th, 2025</p>
                <p><strong>Round 2</strong>: January 22nd, 2026</p>
                <p><strong>Round 3</strong>: April 9th, 2026</p>
            </div>
            """
            st.markdown(college_schedule_html, unsafe_allow_html=True)
            
            # Mission Statement
            st.markdown(
                f"""
                <div style="background-color: #E8F5E8; border-left: 5px solid #4CAF50; 
                     padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <p style="color: #2E7D32; font-style: italic; margin: 0;">
                    This programming represents the heart of GirlTrek's mission—empowering Black women to reclaim their health and legacy through the simple yet radical act of walking. Together, we are ensuring that self-care and wellness become a lifestyle in the lives of young women to have the wit to carry the choice of our foremothers.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Mommy and Me Program
        with st.expander("👩‍👧‍👦 Mommy and Me - Keturah Queen", expanded=False):
            # Program Overview
            st.markdown('<h5>Program Overview</h5>', unsafe_allow_html=True)
            st.markdown(
                """
                The "Mommy and Me" Walks initiative recruits GirlTrek moms to serve as Mom Coaches, leading family-centered wellness experiences in their communities. The program creates safe, supportive spaces for mothers and children to gather, move, and connect while promoting health and sisterhood within the GirlTrek movement.
                """
            )
            
            # Key Objectives
            st.markdown('<h5>Key Objectives</h5>', unsafe_allow_html=True)
            st.markdown(
                """
                * **Recruitment**: Train 50 GirlTrek moms as Mom Coaches
                * **Engagement**: Host fun, family-friendly community walks
                * **Impact**: Promote physical activity, strengthen community ties, and inspire the next generation
                * **Summer Goal**: Complete 100 "Mommy and Me" Walks nationwide
                """
            )
            
            # Current Progress Metrics
            st.markdown('<h5>Current Progress (July 2025)</h5>', unsafe_allow_html=True)
            
            mommy_col1, mommy_col2 = st.columns(2)
            
            with mommy_col1:
                st.markdown(
                    f'<div class="metric-box">'
                    f'<p class="metric-title">MOM COACHES RECRUITED</p>'
                    f'<p class="metric-value">45 / 50</p>'
                    f'<p style="font-size: 14px; color: #666;">90% Complete</p>'
                    f'<p>{status_badge("On Track")}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            with mommy_col2:
                st.markdown(
                    f'<div class="metric-box">'
                    f'<p class="metric-title">WALKS COMPLETED</p>'
                    f'<p class="metric-value">8</p>'
                    f'<p style="font-style: italic; font-size: 12px; color: #666;">Successful "Mommy and Me" Walks</p>'
                    f'<p>Goal: 100</p>'
                    f'<p>{status_badge("On Track")}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            mommy_col3, mommy_col4 = st.columns(2)
            
            with mommy_col3:
                st.markdown(
                    f'<div class="metric-box">'
                    f'<p class="metric-title">COMMUNITY ENGAGEMENT</p>'
                    f'<p class="metric-value">83</p>'
                    f'<p style="font-style: italic; font-size: 12px; color: #666;">Free tickets sold in Round 1</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            with mommy_col4:
                st.markdown(
                    f'<div class="metric-box">'
                    f'<p class="metric-title">REMAINING NEED</p>'
                    f'<p class="metric-value">5</p>'
                    f'<p style="font-style: italic; font-size: 12px; color: #666;">Additional Mom Coaches to reach target</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            # Walk Schedule
            st.markdown('<h5>Walk Schedule</h5>', unsafe_allow_html=True)
            
            schedule_html = f"""
            <div style="background-color: #F3F9FF; border-radius: 10px; padding: 15px; margin: 10px 0;">
                <p><strong>Round 1</strong>: Completed July 5th ✅</p>
                <p><strong>Round 2</strong>: Currently in progress</p>
                <ul style="margin-left: 20px;">
                    <li>July 19</li>
                    <li>August 2 & 23</li>
                    <li>September 6</li>
                </ul>
            </div>
            """
            st.markdown(schedule_html, unsafe_allow_html=True)

        # Data Analysis & Recommendations
        st.markdown('### 📊 Data Analysis & Recommendations')
        
        # Key Insights
        st.markdown('#### 🔍 Key Insights')
        st.warning("""
        **Recruitment Challenge:** At 15.44% of annual goal (15,438 vs 100,000), significant acceleration needed
        
        **Seasonal Patterns:** Strong recruitment in March-May (12,065 members) suggests effective spring campaigns
        
        **Age Gap:** Only 316 new members aged 18-25, highlighting need for youth engagement strategies
        
        **Partnership Success:** 18 recruitment partnerships exceeded goal of 10, showing strong community connections
        
        **Program Potential:** Mommy and Me at 90% completion vs College Crews at 11% shows varying program effectiveness
        """)
        
        # Strategic Recommendations
        st.markdown('#### 💡 Strategic Recommendations')
        st.success("""
        **Replicate Spring Success:** Analyze March-May campaigns and apply learnings to remaining quarters
        
        **Youth Strategy Overhaul:** Accelerate College Crews program and develop campus-specific recruitment tactics
        
        **Partnership Leverage:** Utilize existing 18 partnerships for member referrals and joint recruitment events
        
        **Scale Successful Programs:** Expand Mommy and Me model and recruit additional Mom Coaches beyond 50 target
        
        **Digital Focus:** Invest in social media and digital recruitment to reach younger demographics
        
        **Retention Integration:** Ensure recruitment efforts include onboarding strategies to improve member retention
        """)

        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Recruitment")

    # ---------------------------------
    # Engagement Tab
    # ---------------------------------
    with tab3:
        add_board_update("Engagement")
        
        st.markdown('<h3 class="section-title">Engagement Metrics</h3>', unsafe_allow_html=True)

        engagement_col1, engagement_col2 = st.columns(2)

        with engagement_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL NEW CREWS (2025)</p>'
                f'<p class="metric-value">727</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        with engagement_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">MEMBERS WALKING DAILY</p>'
                f'<p class="metric-value">5,439</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Walking at least 30 min/day, 5 days/week (from Self-Care School exit data)</p>'
                f'<p>Goal: 50,000</p>'
                f'<p>{status_badge("At Risk")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        eng_col1, eng_col2, eng_col3 = st.columns(3)
        
        with eng_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">ACTIVE VOLUNTEERS</p>'
                f'<p class="metric-value">3,348</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Has hosted an event this year</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with eng_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">DOCUMENTED CREW LEADERS</p>'
                f'<p class="metric-value">3,856</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Submitted crew via website, attended training, or previously noted as leader</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with eng_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">ACTIVE CREW LEADERS</p>'
                f'<p class="metric-value">1,846</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Hosted an event this year or signed up this year</p>'
                f'<p>{status_badge("On Track")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Additional engagement metrics with definitions
        st.markdown('<h4>Training & Development</h4>', unsafe_allow_html=True)
        
        train_col1, train_col2, train_col3 = st.columns(3)
        
        with train_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL TRAINED VOLUNTEERS</p>'
                f'<p class="metric-value">11,535</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Includes: Self-care for Freedom Fighters, Ketruah training, Mental Health First Aid, training walks, teach-in events</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with train_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">CREW LEADERS TRAINED (2025)</p>'
                f'<p class="metric-value">124</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Total number of crew leaders trained in 2025</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with train_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">SPECIAL IMPACT PROGRAMS</p>'
                f'<p class="metric-value">100</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Members in MHFA, crew leader training, faith initiatives, caregiver events, justice programs</p>'
                f'<p>Goal: 65,000</p>'
                f'<p>{status_badge("At Risk")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        # Training and volunteer metrics already exist above
        
        # Care Village Section
        st.markdown('<h4>Care Village Initiative</h4>', unsafe_allow_html=True)
        
        care_col1, care_col2 = st.columns(2)
        
        with care_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">CARE VILLAGE POPULATION REACHED</p>'
                f'<p class="metric-value">3,055</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Black women reached with localized public health services</p>'
                f'<p>Goal: 40,000 (7.64%)</p>'
                f'<p>{status_badge("On Track")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with care_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL POPULATION REACHED</p>'
                f'<p class="metric-value">7,146</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Black women impacted through all programs & events</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        # Data Analysis & Recommendations
        st.markdown('### 📊 Data Analysis & Recommendations')
        
        # Key Insights
        st.markdown('#### 🔍 Key Insights')
        st.info("""
        **Leadership Pipeline:** Strong volunteer base with 3,856 documented crew leaders and 1,846 active leaders
        
        **Training Scale:** 11,535 trained volunteers demonstrates robust capacity building efforts
        
        **Daily Walking Gap:** Only 5,439 walking daily vs 50,000 goal (10.9%) indicates engagement challenge
        
        **Care Village Progress:** 7,146 total population reached shows community impact expansion
        
        **New Crew Growth:** 727 new crews in 2025 indicates healthy local expansion
        """)
        
        # Strategic Recommendations
        st.markdown('#### 💡 Strategic Recommendations')
        st.success("""
        **Walking Habit Activation:** Develop targeted interventions to convert trained volunteers into daily walkers
        
        **Crew Leader Activation:** Focus on converting documented leaders (3,856) to active status (1,846)
        
        **Special Programs Scale:** Expand successful programs beyond current 100 participants to reach 65,000 goal
        
        **Care Village Acceleration:** Leverage successful model to reach remaining 32,945 women for 40,000 target
        
        **Technology Integration:** Use mobile app and digital tools to support daily walking accountability
        
        **Peer Support Systems:** Create walking buddy programs and crew-based accountability structures
        """)

        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Engagement")

    # ---------------------------------
    # Development Tab
    # ---------------------------------
    with tab4:
        add_board_update("Development")
        
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
                f'<p>17 of 48 Grants</p>'
                f'<p>{status_badge("On Track")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        with dev_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">CORPORATE SPONSORSHIPS</p>'
                f'<p class="metric-value">$130,000</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666; margin-bottom: 5px;">Additional $60k verbally agreed to but not yet in bank</p>'
                f'<p>Goal: $1.5M</p>'
                f'<p>{status_badge("At Risk")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        dev_finance_fig = px.pie(
            df_finance,
            values='Amount',
            names='Category',
            title='Total Contributions Breakdown',
            color_discrete_sequence=[primary_blue, primary_orange]
        )
        dev_finance_fig.update_traces(textposition='inside', textinfo='percent+label')
        dev_finance_fig.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(dev_finance_fig, use_container_width=True, key="dev_finance_fig")
        
        # Funding Definitions Section (moved below chart and always visible)
        st.markdown('<h4>Funding Categories Definitions</h4>', unsafe_allow_html=True)
        
        # Create expandable sections for each funding category
        with st.expander("💰 View Funding Category Definitions", expanded=True):
            st.markdown("**Grants:**")
            st.info("Funding awarded by foundations, government agencies, or corporations for specific projects or general operations. These are typically awarded through a competitive application process and may have specific requirements or restrictions on how funds are used.")
            
            st.markdown("**Donations:**")
            st.info("Individual contributions from supporters, members, and donors. These include one-time gifts, recurring donations, monthly giving programs, and major gifts from individual philanthropists. Donations are often unrestricted and provide flexible funding for organizational priorities.")
            
            st.markdown("**Corporate Sponsorships:**")
            st.info("Financial support from businesses and corporations, often in exchange for marketing benefits, brand visibility, or partnership opportunities. These may include event sponsorships, program partnerships, or cause marketing initiatives.")
            
            st.markdown("**Earned Revenue:**")
            st.info("Income generated through GirlTREK's own activities and services, including online store sales (merchandise, apparel, wellness products), training and workshop fees, licensing or consulting revenue, and investment income.")
            
            st.markdown("**Bricklayer's Fundraising:**")
            st.info("Contributions from GirlTREK's major donor network, typically involving significant individual gifts from high-capacity donors who are deeply committed to the organization's mission.")
        
        # Grant Tracking Table
        st.markdown('<h4>2025 Grant Applications Tracking</h4>', unsafe_allow_html=True)
        
        # Create grants data
        grants_data = {
            'Account': [
                'Pivotal Ventures', 'National Trust for Historic Preservation', 'Echoing Green', 'Emerson Collective',
                'National Trust for Historic Preservation', 'Gabell Foundation', 'National Trust for Historic Preservation',
                'National Trust for Historic Preservation', 'Borealis Philanthropy', 'National Trust for Historic Preservation',
                'Robert Wood Johnson Foundation', 'Emergent Fund', 'Southern Black Girls', 'Lumena Foundation',
                'Sun Life', 'Black Feminist Fund', 'Elevate Prize Foundation', 'Saks Fifth Avenue Foundation',
                'Borealis Philanthropy', 'Central Alabama Community Foundation', 'JusPax Fund', 'Tow Foundation'
            ],
            'Grant Name': [
                '2025 Action for Women\'s Health', '2025 National Trust Preservation', '2025 Follow-On Funding',
                '2025 EC Special Grant', '2025 AACHAF', '2025 CF Special Grant', '2025 Johanna Favrot',
                '2025 Cynthia Woods Mitchell', '2025 Black Led Movement', '2025 Black Modernism',
                '2025 Data Equity', '2025 Emergent Fund', '2025 SBG Defense Fund', '2025 Lumena Foundation Moon',
                '2025 Sun Life Health Access', '2025 Sustain Fund', '2025 Elevate Prize', '2025 Local Funding',
                '2025 Borealis Philanthropy REACH Fund', '2025 Montgomery City Council', '2025 JusPax Fund: Gender Justice',
                'Tow Foundation'
            ],
            'Amount Requested': [
                '$5,000,000', '$5,000', '$100,000', '$224,250', '$75,000', '$10,000', '$15,000', '$15,000',
                '$183,500', '$150,000', '$50,000', '$25,000', '$2,000', '$50,000', '$100,000', '$1,600,000',
                '$100,000', '$30,000', '$150,000', '$10,000', '$25,000', '$600,000'
            ],
            'Amount Funded': [
                '', '$2,500', '', '', '', '$10,000', '', '', '', '', '', '', '$2,000', '', '', '', '', '', '', '', '', ''
            ],
            'Due Date': [
                'Jan', 'Feb', 'Feb', 'Feb', 'Feb', 'Feb', 'Mar', 'Mar', 'Mar', 'Mar', 'Mar', 'Mar', 'Apr', 'Apr',
                'Apr', 'May', 'Jun', 'Jul', 'Jul', 'Jul', 'Jul', 'Jul'
            ],
            'Status': [
                'Pending', 'Closed - Funded', 'Closed - Declined', 'Closed - Declined', 'Pending', 'Closed - Funded',
                'Pending', 'Pending', 'Pending', 'Pending', 'Closed - Declined', 'Pending', 'Closed - Funded',
                'Closed - Declined', 'Closed - Declined', 'Pending', 'Pending', 'Pending', 'Prepare', 'Prepare',
                'Prepare', 'Prepare'
            ]
        }
        
        # Create DataFrame
        grants_df = pd.DataFrame(grants_data)
        
        # Display the table with status color coding
        st.markdown(
            """
            <style>
            .grants-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 12px;
            }
            .grants-table th, .grants-table td {
                padding: 8px;
                text-align: left;
                border: 1px solid #ddd;
            }
            .grants-table th {
                background-color: #4A90E2;
                color: white;
                font-weight: bold;
            }
            .status-pending { background-color: #E3F2FD; }
            .status-funded { background-color: #E8F5E8; }
            .status-declined { background-color: #FFEBEE; }
            .status-prepare { background-color: #FFF3E0; }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Create HTML table with color coding
        table_html = '<table class="grants-table"><thead><tr>'
        table_html += '<th>Account</th><th>Grant Name</th><th>Amount Requested</th><th>Amount Funded</th><th>Due Date</th><th>Status</th>'
        table_html += '</tr></thead><tbody>'
        
        for _, row in grants_df.iterrows():
            status_class = ""
            if "Pending" in row['Status']:
                status_class = "status-pending"
            elif "Funded" in row['Status']:
                status_class = "status-funded"
            elif "Declined" in row['Status']:
                status_class = "status-declined"
            elif "Prepare" in row['Status']:
                status_class = "status-prepare"
                
            table_html += f'<tr class="{status_class}">'
            table_html += f'<td>{row["Account"]}</td>'
            table_html += f'<td>{row["Grant Name"]}</td>'
            table_html += f'<td>{row["Amount Requested"]}</td>'
            table_html += f'<td>{row["Amount Funded"]}</td>'
            table_html += f'<td>{row["Due Date"]}</td>'
            table_html += f'<td><strong>{row["Status"]}</strong></td>'
            table_html += '</tr>'
        
        # Add total row
        table_html += '<tr style="background-color: #FFF9C4; font-weight: bold;">'
        table_html += '<td colspan="2"><strong>TOTAL</strong></td>'
        table_html += '<td><strong>$8,519,750.00</strong></td>'
        table_html += '<td><strong>$14,500.00</strong></td>'
        table_html += '<td colspan="2"></td>'
        table_html += '</tr>'
        
        table_html += '</tbody></table>'
        
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Summary statistics
        st.markdown('<h5>Grant Application Summary</h5>', unsafe_allow_html=True)
        
        grant_summary_col1, grant_summary_col2, grant_summary_col3 = st.columns(3)
        
        with grant_summary_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL APPLICATIONS</p>'
                f'<p class="metric-value">22</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Grant applications submitted in 2025</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with grant_summary_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">SUCCESS RATE</p>'
                f'<p class="metric-value">18.2%</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">3 funded out of 11 decided applications</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with grant_summary_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">PENDING DECISIONS</p>'
                f'<p class="metric-value">7</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Applications awaiting funding decisions</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Additional Development Metrics
        st.markdown('<h4>Additional Fundraising Metrics</h4>', unsafe_allow_html=True)
        
        fund_col1, fund_col2 = st.columns(2)
        
        with fund_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">EARNED REVENUE (STORE)</p>'
                f'<p class="metric-value">$99,836</p>'
                f'<p>Goal: $400,000</p>'
                f'<p>{status_badge("At Risk")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with fund_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">BRICKLAYER\'S FUNDRAISING</p>'
                f'<p class="metric-value">$2,500</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666; margin-bottom: 5px;">Another significant donation is anticipated by fall of 2025</p>'
                f'<p>Goal: $500,000</p>'
                f'<p>{status_badge("At Risk")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Data Analysis & Recommendations
        st.markdown('### 📊 Data Analysis & Recommendations')
        
        # Key Insights
        st.markdown('#### 🔍 Key Insights')
        st.info("""
        **Strong Grant Performance:** $3.1M in grants represents 99.7% of total contributions, showing successful institutional fundraising
        
        **Grant Pipeline Value:** $8.5M in applications with $14.5K secured (0.17% success rate) indicates need for strategy refinement
        
        **Corporate Sponsorship Gap:** $130K vs $1.5M goal (8.7%) represents significant untapped revenue potential
        
        **Earned Revenue Underperformance:** Store sales at $99.8K vs $400K goal (25%) suggests operational challenges
        
        **Diverse Application Portfolio:** 22 grant applications across varied funders shows good diversification strategy
        """)
        
        # Strategic Recommendations
        st.markdown('#### 💡 Strategic Recommendations')
        st.success("""
        **Grant Strategy Optimization:** Analyze successful vs declined applications to improve 18.2% success rate
        
        **Corporate Partnership Development:** Hire dedicated corporate relations staff to capture $1.37M sponsorship gap
        
        **Store Operations Review:** Conduct comprehensive analysis of product mix, pricing, and marketing for earned revenue
        
        **Major Donor Cultivation:** Accelerate Bricklayers program beyond current $2.5K to approach $500K goal
        
        **Pipeline Management:** Implement CRM system to better track and nurture the 7 pending grant applications
        
        **Diversification Focus:** Balance grant dependence with growth in other revenue streams for sustainability
        """)
        
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Development")

    # ---------------------------------
    # Marketing Tab
    # ---------------------------------
    with tab5:
        add_board_update("Marketing")
        
        st.markdown('<h3 class="section-title">Marketing Metrics</h3>', unsafe_allow_html=True)

        sub_col1, sub_col2 = st.columns(2)

        with sub_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL SUBSCRIBERS</p>'
                f'<p class="metric-value">931,141</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666; margin-bottom: 5px;">Total number of people subscribed to our email list</p>'
                f'<p>Goal: 1,300,000 (71.63%)</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        with sub_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">ACTIVE SUBSCRIBERS</p>'
                f'<p class="metric-value">320,463</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666; margin-bottom: 5px;">People who have opened an email, clicked on an email, or joined the email list in the last 120 days</p>'
                f'<p>34.4% of Total</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown("<h3>Email Performance Metrics</h3>", unsafe_allow_html=True)
        
        email_col1, email_col2 = st.columns(2)
        
        with email_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">AVERAGE OPEN RATE</p>'
                f'<p class="metric-value">18.54%</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666; margin-bottom: 5px;">Percentage of recipients who open your email out of the total number successfully delivered</p>'
                f'<p><strong>Industry Standard:</strong> Nonprofits average 28.59%</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with email_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">CLICK-THROUGH RATE</p>'
                f'<p class="metric-value">1.06%</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666; margin-bottom: 5px;">Measures how effectively your email drives recipients to take action by clicking on a link, button, or image</p>'
                f'<p><strong>Industry Standard:</strong> Nonprofits average 3.29%</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Email Engagement Comparison Chart
        st.markdown("<h4>Email Performance vs Industry Standards</h4>", unsafe_allow_html=True)
        
        comparison_fig = go.Figure()
        
        comparison_fig.add_trace(go.Bar(
            name='GirlTREK',
            x=comparison_data['Metric'],
            y=comparison_data['GirlTREK'],
            marker_color=primary_blue,
            text=comparison_data['GirlTREK'].apply(lambda x: f'{x}%'),
            textposition='auto'
        ))
        
        comparison_fig.add_trace(go.Bar(
            name='Nonprofit Industry Average',
            x=comparison_data['Metric'],
            y=comparison_data['Nonprofit Industry Average'],
            marker_color=secondary_orange,
            text=comparison_data['Nonprofit Industry Average'].apply(lambda x: f'{x}%'),
            textposition='auto'
        ))
        
        comparison_fig.update_layout(
            title='Email Performance Comparison',
            yaxis_title='Percentage (%)',
            barmode='group',
            title_font=dict(color=primary_blue),
            height=400
        )
        
        st.plotly_chart(comparison_fig, use_container_width=True, key="email_comparison_fig")
        
        # META Advertising Performance
        st.markdown("<h3>META Advertising Performance (Year to Date)</h3>", unsafe_allow_html=True)
        
        # WNBA Campaign
        st.markdown('<h4>WNBA Campaign</h4>', unsafe_allow_html=True)
        
        wnba_col1, wnba_col2, wnba_col3 = st.columns(3)
        
        with wnba_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL SPEND</p>'
                f'<p class="metric-value">$3,901.12</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">WNBA campaign investment</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with wnba_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">IMPRESSIONS</p>'
                f'<p class="metric-value">336,543</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Total ad impressions</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with wnba_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">CLICK-THROUGH RATE</p>'
                f'<p class="metric-value">1.23%</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">CTR performance</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        wnba_col4, wnba_col5 = st.columns(2)
        
        with wnba_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">COST PER CLICK</p>'
                f'<p class="metric-value">$0.94</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Average CPC</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with wnba_col5:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL CLICKS</p>'
                f'<p class="metric-value">1,986</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Total ad clicks</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # WNBA Top Audience
        st.markdown(
            f"""
            <div style="background-color: #E8F5E8; border-left: 5px solid #4CAF50; 
                 padding: 15px; border-radius: 5px; margin: 15px 0;">
                <p style="color: #2E7D32; margin: 0;"><strong>🎯 Top Performing Audience:</strong> Email List + LAL (Lookalike Audiences)</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Underground App Campaign
        st.markdown('<h4>Underground App Campaign</h4>', unsafe_allow_html=True)
        
        app_col1, app_col2, app_col3 = st.columns(3)
        
        with app_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL SPEND</p>'
                f'<p class="metric-value">$7,279.07</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Underground App campaign investment</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with app_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">IMPRESSIONS</p>'
                f'<p class="metric-value">522,347</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Total ad impressions</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with app_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">CLICK-THROUGH RATE</p>'
                f'<p class="metric-value">1.30%</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">CTR performance</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        app_col4, app_col5, app_col6 = st.columns(3)
        
        with app_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">COST PER CLICK</p>'
                f'<p class="metric-value">$2.37</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Average CPC</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with app_col5:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL CLICKS</p>'
                f'<p class="metric-value">3,074</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Total ad clicks</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with app_col6:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">COST PER LEAD</p>'
                f'<p class="metric-value">$25.90</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Average CPL</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        app_col7, app_col8 = st.columns(2)
        
        with app_col7:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL LEADS</p>'
                f'<p class="metric-value">281</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Total leads generated</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with app_col8:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">LEAD CONVERSION RATE</p>'
                f'<p class="metric-value">9.14%</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Leads per total clicks</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Underground App Audience Performance
        st.markdown('<h5>Underground App - Top Performing Audiences</h5>', unsafe_allow_html=True)
        
        audience_data = pd.DataFrame({
            'Audience Type': ['Lookalikes', 'Cultural Interests'],
            'Leads Generated': [128, 116]
        })
        
        audience_fig = px.bar(
            audience_data,
            x='Audience Type',
            y='Leads Generated',
            title='Underground App Campaign - Leads by Audience Type',
            color='Leads Generated',
            color_continuous_scale=[primary_blue, primary_orange]
        )
        audience_fig.update_layout(
            title_font=dict(color=primary_blue),
            height=350
        )
        
        st.plotly_chart(audience_fig, use_container_width=True, key="audience_performance_fig")
        
        # Campaign Comparison
        st.markdown('<h4>Campaign Performance Comparison</h4>', unsafe_allow_html=True)
        
        campaign_comparison = pd.DataFrame({
            'Campaign': ['WNBA', 'Underground App'],
            'Spend': [3901.12, 7279.07],
            'CTR': [1.23, 1.30],
            'CPC': [0.94, 2.37],
            'Clicks': [1986, 3074]
        })
        
        # Create comparison chart for spend vs clicks
        comparison_spend_fig = go.Figure()
        
        comparison_spend_fig.add_trace(go.Scatter(
            x=campaign_comparison['Spend'],
            y=campaign_comparison['Clicks'],
            mode='markers+text',
            text=campaign_comparison['Campaign'],
            textposition="top center",
            marker=dict(
                size=[20, 30],  # Scaled by relative spend
                color=[primary_blue, primary_orange],
                opacity=0.8
            ),
            name='Campaigns'
        ))
        
        comparison_spend_fig.update_layout(
            title='Campaign Spend vs Clicks Performance',
            xaxis_title='Total Spend ($)',
            yaxis_title='Total Clicks',
            title_font=dict(color=primary_blue),
            height=400
        )
        
        st.plotly_chart(comparison_spend_fig, use_container_width=True, key="campaign_comparison_fig")
        
        # META Advertising Summary
        st.markdown('<h4>META Advertising Summary</h4>', unsafe_allow_html=True)
        
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL AD SPEND</p>'
                f'<p class="metric-value">$11,180.19</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Combined WNBA + Underground App</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with summary_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL IMPRESSIONS</p>'
                f'<p class="metric-value">858,890</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Combined campaign reach</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with summary_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL CLICKS</p>'
                f'<p class="metric-value">5,060</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Combined campaign clicks</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Data Analysis & Recommendations
        st.markdown('### 📊 Data Analysis & Recommendations')
        
        # Key Insights
        st.markdown('#### 🔍 Key Insights')
        st.warning("""
        **Email Performance Gap:** 18.54% open rate vs 28.59% industry average indicates significant improvement opportunity
        
        **Engagement Challenge:** 1.06% CTR vs 3.29% industry standard suggests content relevance issues
        
        **Subscriber Growth Need:** 931K vs 1.3M goal (71.6%) requires 369K additional subscribers
        
        **Active Audience Strength:** 34.4% active subscriber rate (320K) provides solid engagement foundation
        
        **Ad Campaign Performance:** Underground App (1.30% CTR) outperforming WNBA (1.23% CTR) with better lead generation
        
        **Cost Efficiency Variance:** WNBA $0.94 CPC vs Underground App $2.37 shows significant cost differences
        """)
        
        # Strategic Recommendations
        st.markdown('#### 💡 Strategic Recommendations')
        st.success("""
        **Email Optimization:** A/B test subject lines, send times, and content formats to improve open rates by 10%
        
        **Content Strategy Overhaul:** Implement personalization and segmentation to triple CTR toward industry standards
        
        **Subscriber Acquisition:** Scale Underground App campaign model (9.14% conversion) across more platforms
        
        **Audience Optimization:** Focus ad spend on Lookalike audiences (128 leads) and Email List + LAL combinations
        
        **Cost Management:** Analyze WNBA campaign efficiency to reduce overall ad costs while maintaining reach
        
        **List Health:** Implement re-engagement campaigns to convert inactive subscribers to active status
        """)
        
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Marketing")

    # ---------------------------------
    # Campaigns Tab (NEW)
    # ---------------------------------
    with tab6:
        add_board_update("Campaigns")
        
        st.markdown('<h3 class="section-title">Self-Care School 2025</h3>', unsafe_allow_html=True)
        
        # Campaign Overview
        st.markdown('<h4>Campaign Overview</h4>', unsafe_allow_html=True)
        
        campaign_col1, campaign_col2, campaign_col3 = st.columns(3)
        
        with campaign_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">MEMBERS RECRUITED</p>'
                f'<p class="metric-value">5,377</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Through Self-Care School campaign</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with campaign_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">WALKING AT LIFE-SAVING LEVEL</p>'
                f'<p class="metric-value">12,037</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Walking 30+ min/day, 5 days/week (from exit tickets)</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with campaign_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL SUPPORTING GOAL</p>'
                f'<p class="metric-value">5,634</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Badge earners + Claimed the Victory</p>'
                f'<p>Goal: 65,000</p>'
                f'<p>{status_badge("At Risk")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Knowledge Increase Metrics
        st.markdown('<h4>Self-Care School Knowledge Impact</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-style: italic;">Members reporting significant increase in knowledge by topic:</p>', unsafe_allow_html=True)
        
        knowledge_fig = px.bar(
            knowledge_data,
            x='Topic',
            y='Members',
            title='Members Reporting Significant Knowledge Increase by Topic',
            color='Members',
            color_continuous_scale=[primary_blue, primary_orange, primary_yellow]
        )
        knowledge_fig.update_layout(
            title_font=dict(color=primary_blue),
            xaxis_tickangle=-45,
            height=500
        )
        
        st.plotly_chart(knowledge_fig, use_container_width=True, key="knowledge_fig")
        
        # Summary stats
        st.markdown('<h4>Campaign Impact Summary</h4>', unsafe_allow_html=True)
        
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL KNOWLEDGE IMPACT</p>'
                f'<p class="metric-value">999</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Women reporting change in health knowledge</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with summary_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">AVERAGE KNOWLEDGE GAIN</p>'
                f'<p class="metric-value">630</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Average members per topic area</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Additional Impact Metrics from Impact Tab
        st.markdown('<h4>Self-Care School Health & Behavior Outcomes</h4>', unsafe_allow_html=True)
        
        outcome_col1, outcome_col2, outcome_col3 = st.columns(3)
        
        with outcome_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">MENTAL WELL-BEING</p>'
                f'<p class="metric-value">998</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Changes in self-reported mental well-being</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with outcome_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">SOCIAL CONNECTION</p>'
                f'<p class="metric-value">673</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Feel more connected and less isolated</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with outcome_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">EMPOWERED TO ACT</p>'
                f'<p class="metric-value">907</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Feel empowered to take action</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        behavior_col1, behavior_col2, behavior_col3 = st.columns(3)
        
        with behavior_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">NEW HABITS</p>'
                f'<p class="metric-value">293</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Implemented new habits/mindsets</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with behavior_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">SHARED LESSONS</p>'
                f'<p class="metric-value">819</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Shared lessons with others</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with behavior_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">WALKING HABIT</p>'
                f'<p class="metric-value">709</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Built stronger walking habit</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        st.markdown('<hr>', unsafe_allow_html=True)
        
        # Copy Impact Metrics from Impact Tab
        st.markdown('<h3 class="section-title">Detailed Impact Metrics - Self-Care School 2025</h3>', unsafe_allow_html=True)

        # Health and Well-being Impact
        st.markdown('<h4>Health & Well-being Outcomes</h4>', unsafe_allow_html=True)
        
        health_col1, health_col2, health_col3 = st.columns(3)
        
        with health_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">HEALTH KNOWLEDGE CHANGE</p>'
                f'<p class="metric-value">999</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Women reporting a change in health knowledge</p>'
                f'<p style="font-size: 14px; color: #666;">0.00% (baseline measure)</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with health_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">MENTAL WELL-BEING IMPROVEMENT</p>'
                f'<p class="metric-value">998</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Women reporting changes in self-reported mental well-being</p>'
                f'<p style="font-size: 14px; color: #666;">99.90% of respondents</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with health_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">SOCIAL CONNECTION</p>'
                f'<p class="metric-value">673</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Women feeling more connected and less isolated through GirlTREK</p>'
                f'<p style="font-size: 14px; color: #666;">68.53% of respondents</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Behavior Change Impact
        st.markdown('<h4>Behavior Change & Empowerment</h4>', unsafe_allow_html=True)
        
        behavior_col1, behavior_col2 = st.columns(2)
        
        with behavior_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">EMPOWERED TO TAKE ACTION</p>'
                f'<p class="metric-value">907</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Participants feeling empowered to make positive changes</p>'
                f'<p style="font-size: 14px; color: #666;">90.52% of respondents</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with behavior_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">STRONGER WALKING HABIT</p>'
                f'<p class="metric-value">709</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Participants who built a stronger walking habit</p>'
                f'<p style="font-size: 14px; color: #666;">68.70% of respondents</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        behavior_col3, behavior_col4 = st.columns(2)
        
        with behavior_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">IMPLEMENTED NEW HABITS</p>'
                f'<p class="metric-value">293</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Participants who implemented new habits, actions, or mindsets</p>'
                f'<p style="font-size: 14px; color: #666;">34.92% of respondents</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with behavior_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">SHARED WITH OTHERS</p>'
                f'<p class="metric-value">819</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Participants who shared lessons learned with others</p>'
                f'<p style="font-size: 14px; color: #666;">83.66% of respondents</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Knowledge Increase by Topic
        st.markdown('<h4>Knowledge Increase by Self-Care School Topics</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-style: italic; color: #666;">Number of participants reporting significant increase in knowledge:</p>', unsafe_allow_html=True)
        
        # Display as metric boxes with correct percentages
        knowledge_col1, knowledge_col2 = st.columns(2)
        
        knowledge_items = [
            ("Land rights, housing & environmental justice", 710, 71.60),
            ("Civic engagement & political participation", 569, 57.00),
            ("Safety, self-defense & public resource access", 645, 64.40),
            ("Decarceration, gun safety & restorative justice", 658, 63.76),
            ("Mental health & emotional boundaries", 622, 60.27),
            ("Radical care, family legacy & intergenerational healing", 695, 67.34),
            ("Parenting, mentorship & end-of-life planning", 536, 51.94),
            ("Self-esteem, celebration & personal empowerment", 602, 58.33)
        ]
        
        for i in range(0, 4):
            with knowledge_col1:
                topic, count, pct = knowledge_items[i]
                st.markdown(
                    f"""
                    <div class="metric-box" style="margin-bottom: 15px;">
                        <p class="metric-title" style="font-size: 14px;">{topic.upper()}</p>
                        <p class="metric-value" style="font-size: 24px;">{count}</p>
                        <p style="font-size: 14px; color: #666;">{pct}% of respondents</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        for i in range(4, 8):
            with knowledge_col2:
                topic, count, pct = knowledge_items[i]
                st.markdown(
                    f"""
                    <div class="metric-box" style="margin-bottom: 15px;">
                        <p class="metric-title" style="font-size: 14px;">{topic.upper()}</p>
                        <p class="metric-value" style="font-size: 24px;">{count}</p>
                        <p style="font-size: 14px; color: #666;">{pct}% of respondents</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        # Create visualization of knowledge topics
        knowledge_impact_fig_campaigns = px.bar(
            knowledge_data,
            x='Members',
            y='Topic',
            orientation='h',
            title='Self-Care School Knowledge Impact by Topic',
            color='Members',
            color_continuous_scale=[primary_blue, primary_orange, primary_yellow]
        )
        knowledge_impact_fig_campaigns.update_layout(
            title_font=dict(color=primary_blue),
            height=400,
            xaxis_title='Number of Participants',
            yaxis_title=''
        )
        
        st.plotly_chart(knowledge_impact_fig_campaigns, use_container_width=True, key="knowledge_impact_fig_campaigns")
        
        # Summary metrics
        st.markdown('<h4>Impact Summary</h4>', unsafe_allow_html=True)
        
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            st.markdown(
                f"""
                <div class="metric-box">
                    <p class="metric-title">TOTAL KNOWLEDGE TOPICS</p>
                    <p class="metric-value">8</p>
                    <p style="font-style: italic; font-size: 12px; color: #666;">Areas of significant knowledge increase</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with summary_col2:
            st.markdown(
                f"""
                <div class="metric-box">
                    <p class="metric-title">AVERAGE IMPACT PER TOPIC</p>
                    <p class="metric-value">630</p>
                    <p style="font-style: italic; font-size: 12px; color: #666;">Average participants reporting knowledge gain per topic</p>
                    <p style="font-size: 14px; color: #666;">61.08% average response rate</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with summary_col3:
            st.markdown(
                f"""
                <div class="metric-box">
                    <p class="metric-title">TOTAL KNOWLEDGE IMPACTS</p>
                    <p class="metric-value">5,037</p>
                    <p style="font-style: italic; font-size: 12px; color: #666;">Sum of all topic-specific knowledge gains</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Data Analysis & Recommendations
        st.markdown('### 📊 Data Analysis & Recommendations')
        
        # Key Insights
        st.markdown('#### 🔍 Key Insights')
        st.info("""
        **Exceptional Mental Health Impact:** 99.90% reported mental well-being improvements demonstrates program effectiveness
        
        **Strong Knowledge Transfer:** Average 61.08% knowledge increase across 8 topics shows comprehensive education success
        
        **Community Building Success:** 83.66% shared lessons with others indicates viral knowledge spread
        
        **Walking Habit Development:** 68.70% built stronger walking habits, directly supporting organizational mission
        
        **Goal Gap:** 5,634 supporting vs 65,000 goal (8.67%) reveals significant scaling opportunity
        
        **High Engagement Quality:** 90.52% feel empowered to take action shows transformative impact
        """)
        
        # Strategic Recommendations
        st.markdown('#### 💡 Strategic Recommendations')
        st.success("""
        **Scale Successful Model:** Expand Self-Care School format to reach remaining 59,366 members for goal achievement
        
        **Leverage Social Sharing:** Create formal referral programs based on 83.66% organic sharing behavior
        
        **Focus on Top Topics:** Prioritize Radical care (67.34%) and Land rights (71.60%) themes in future content
        
        **Walking Integration:** Develop specific programs for the 31.30% who have not built walking habits yet
        
        **Knowledge Retention:** Implement follow-up programs to reinforce learning and maintain engagement
        
        **Community Activation:** Channel empowerment (90.52%) into advocacy and leadership development programs
        """)
        
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Campaigns")
    
    # ---------------------------------
    # Operations Tab (moved to tab7)
    # ---------------------------------
    with tab7:
        add_board_update("Operations")
        
        st.markdown('<h3 class="section-title">Operations Metrics</h3>', unsafe_allow_html=True)

        st.markdown('<h4>Financial Overview (YTD May 2025)</h4>', unsafe_allow_html=True)

        ytd_revenue = finance_trend_data['Revenue'].sum()
        ytd_expenses = finance_trend_data['Expenses'].sum()
        
        finance_col1, finance_col2 = st.columns(2)
        
        with finance_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">YTD REVENUE</p>'
                f'<p class="metric-value">{format_currency(ytd_revenue)}</p>'
                f'<p>Budget: $1,237,419</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with finance_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">YTD EXPENSES</p>'
                f'<p class="metric-value">{format_currency(ytd_expenses)}</p>'
                f'<p>Budget: $1,608,765</p>'
                f'</div>',
                unsafe_allow_html=True
            )

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
                f'<p class="metric-value">100%</p>'
                f'<p>Goal: 100%</p>'
                f'{status_badge("Achieved")}'
                f'</div>',
                unsafe_allow_html=True
            )

        with sys_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">CYBERSECURITY COMPLIANCE</p>'
                f'<p class="metric-value">70%</p>'
                f'<p>Goal: 90%</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Additional Operations Metrics
        st.markdown('<h4>Store Performance</h4>', unsafe_allow_html=True)
        
        store_col1, store_col2, store_col3 = st.columns(3)
        
        with store_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">STORE SALES</p>'
                f'<p class="metric-value">$99,836</p>'
                f'<p>Goal: $400,000</p>'
                f'{status_badge("At Risk")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with store_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">AVERAGE ORDER VALUE</p>'
                f'<p class="metric-value">$44.36</p>'
                f'<p>Target: $20-60</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with store_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">GROSS PROFIT %</p>'
                f'<p class="metric-value">37%</p>'
                f'<p>Target: 50-60%</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # HR/People Operations Section
        st.markdown('<h4>People Operations</h4>', unsafe_allow_html=True)
        
        hr_col1, hr_col2, hr_col3 = st.columns(3)
        
        with hr_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">STAFF RETENTION</p>'
                f'<p class="metric-value">94%</p>'
                f'<p>Industry Avg: 86%</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with hr_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TRAINING COMPLETION</p>'
                f'<p class="metric-value">100%</p>'
                f'<p>Digital Safety Training</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with hr_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">EMPLOYEE SATISFACTION</p>'
                f'<p class="metric-value">88%</p>'
                f'<p>Target: 85%</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
            
        # Data Analysis & Recommendations
        st.markdown('### 📊 Data Analysis & Recommendations')
        
        # Key Insights
        st.markdown('#### 🔍 Key Insights')
        st.info("""
        **Strong People Operations:** 94% staff retention vs 86% industry average shows excellent workplace culture
        
        **Financial Health:** YTD revenue of $3.24M vs $1.24M budget indicates strong financial performance
        
        **Technology Adoption Gap:** 38% Asana adoption vs 85% goal suggests change management challenges
        
        **Store Performance Issues:** $99.8K vs $400K goal (25%) indicates significant operational gaps
        
        **Security Compliance Progress:** 70% cybersecurity compliance shows steady improvement toward 90% goal
        
        **Employee Satisfaction:** 88% vs 85% target demonstrates positive workplace environment
        """)
        
        # Strategic Recommendations
        st.markdown('#### 💡 Strategic Recommendations')
        st.success("""
        **Technology Training Initiative:** Implement comprehensive Asana training program to reach 85% adoption target
        
        **Store Operations Overhaul:** Conduct full audit of product mix, pricing, marketing, and fulfillment processes
        
        **Cybersecurity Priority:** Accelerate security protocols implementation to achieve 90% compliance
        
        **Retain HR Excellence:** Document and replicate successful retention strategies across all departments
        
        **Financial Optimization:** Analyze budget variance to optimize resource allocation for maximum impact
        
        **Process Documentation:** Leverage high employee satisfaction to capture institutional knowledge
        """)
            
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Operations")

    # ---------------------------------
    # Member Care Tab (moved to tab8)
    # ---------------------------------
    with tab8:
        add_board_update("Member Care")
        
        st.markdown('<h3 class="section-title">Member Care Metrics</h3>', unsafe_allow_html=True)

        mc_col1, mc_col2 = st.columns(2)

        with mc_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">MEMBER SATISFACTION RATING</p>'
                f'<p class="metric-value">93%</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">How happy members are with GirlTREK services (via Zendesk tickets)</p>'
                f'<p>Goal: 95%</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        with mc_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">RESOLUTION/RESPONSIVENESS RATE</p>'
                f'<p class="metric-value">2 hours</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Percentage of support tickets resolved within specified timeframe</p>'
                f'<p>Goal: 48 hours</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown('<h3>Top Member Issues/Concerns</h3>', unsafe_allow_html=True)
        st.markdown(
            """
            - SCS Registration Error Message
            - Connecting to the Movement
            """,
            unsafe_allow_html=True
        )
        
        # Add Member Testimonials
        st.markdown('<h3>Member Testimonials</h3>', unsafe_allow_html=True)
        
        with st.expander("Karen Laing - Finding Joy and Healing"):
            st.markdown(
                """
                *"I have found more joy and healing spaces during these weeks and participating in GirlTrek's self-care school has been mission critical in this time when I was fired after six months on the job and it jeopardized the affordable housing my daughter and I found last fall. But God continues to keep us and y'all continue to educate, empower and inspire us as we encourage ourselves in the Lord. Thank you. and amen.*
                
                **— Karen Laing**
                """
            )
        
        with st.expander("Angelia Taylor - Plant Forward Success"):
            st.markdown(
                """
                *"I love the Week 4 'Plant Forward' message! Thank you so much for inspiring us to feed our souls and bodies better. While working on my Master in Public Health, I designed a project that researched Black women's health. One of the three areas that I focused on included buying and eating more fruits and vegetables. Eating what the earth provides helped me lose 106 pounds! It was actually a lot of fun! I also taught plant-based meals to kids, complete with 'chocolate pudding' made from eggplant. LOL! You should have seen them lick the bowls. PRICELESS!! Again, thank you soooooo much for providing such a warm space for us to heal our communities. You are so appreciated.*
                
                **— Angelia Taylor, Champaign, Illinois**
                """
            )
        
        with st.expander("Alicia Cross - Perseverance Through Recovery"):
            st.markdown(
                """
                *"I have walked with GirlTrek since 2019, but had a full knee replacement in 2024, so I'm still rehabbing and my surgeon approved me to ride my Trek bike to continue to break up the scar tissue which is working. Walking is causing quite a bit of swelling, but I'm taking one day at a time. Seven weeks of GirlTrek has been a lifesaver. I appreciate you ALL SO MUCH!!*
                
                **— Alicia Cross, Lanham, MD**
                """
            )
        
        # Data Analysis & Recommendations
        st.markdown('### 📊 Data Analysis & Recommendations')
        
        # Key Insights
        st.markdown('#### 🔍 Key Insights')
        st.info("""
        **Excellent Response Time:** 2-hour resolution vs 48-hour goal demonstrates exceptional member service
        
        **Near-Target Satisfaction:** 93% vs 95% goal shows strong member satisfaction with minimal gap
        
        **Technical Issues Focus:** SCS registration errors indicate system improvement opportunities
        
        **Connection Challenges:** Connecting to the Movement suggests onboarding/engagement gaps
        
        **Powerful Member Stories:** Testimonials show life-changing impact during difficult circumstances
        
        **Health Transformation:** 106-pound weight loss and recovery stories demonstrate program effectiveness
        """)
        
        # Strategic Recommendations
        st.markdown('#### 💡 Strategic Recommendations')
        st.success("""
        **Technical System Improvements:** Priority fix for SCS registration system to reduce support ticket volume
        
        **Enhanced Onboarding:** Develop comprehensive Connecting to Movement resources and guided experiences
        
        **Proactive Support:** Use 2-hour response capability to implement proactive member outreach
        
        **Satisfaction Bridge:** Identify specific areas to close 2% gap to reach 95% satisfaction goal
        
        **Story Amplification:** Systematically collect and share member success stories for recruitment/retention
        
        **Support Specialization:** Train team members in specific technical and engagement issue resolution
        """)
        
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Member Care")

    # ---------------------------------
    # Advocacy Tab (moved to tab9)
    # ---------------------------------
    with tab9:
        add_board_update("Advocacy")
        
        st.markdown('<h3 class="section-title">Advocacy Metrics</h3>', unsafe_allow_html=True)

        adv_col1, adv_col2 = st.columns(2)

        with adv_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">ADVOCACY BRIEFS PUBLISHED</p>'
                f'<p class="metric-value">7 / 10</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Research basis for how J&J agenda items increase Black women\'s life expectancy</p>'
                f'<p>{status_badge("On Track")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        with adv_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">ADVOCACY PARTNERSHIPS</p>'
                f'<p class="metric-value">0 / 3</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Partner-led advocacy activations</p>'
                f'<p>{status_badge("On Track")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        # Additional Advocacy Metrics
        st.markdown('<h4>Additional Advocacy Initiatives</h4>', unsafe_allow_html=True)
        
        adv_col3, adv_col4 = st.columns(2)
        
        with adv_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">MEMBER LISTENING SESSIONS</p>'
                f'<p class="metric-value">0 / 5</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">In 5 key geographies</p>'
                f'<p>{status_badge("On Track")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with adv_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">CASE STUDIES</p>'
                f'<p class="metric-value">0 / 4</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Showcasing GirlTREK\'s local advocacy impact</p>'
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
            - Catalyze local advocacy by convening member listening sessions in key geographies
            - Produce compelling case studies showcasing GirlTREK's impact through local advocacy engagement
            """,
            unsafe_allow_html=True
        )
        
        # Strategic Context
        st.markdown('<h3>Strategic Context - Timeline Adjustment</h3>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background-color: #FFF3E0; border-left: 5px solid #FF9800; 
                 padding: 15px; border-radius: 5px; margin: 10px 0;">
                <p style="color: #E65100; margin: 0;">
                <strong>Note:</strong> Given c-suite conversations, external conditions, and internal priorities we have been reevaluating the pacing of advocacy goals. We are currently considering shifting timeline to Q1 2026, and reevaluating the approach to these objectives. Current focus includes relationship building with national and place-based organizations to test potential activations and applications, participation in national convenings and briefings, and active conversations with 1K Women Strong and Health in Partnership (HiP).
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Data Analysis & Recommendations
        st.markdown('### 📊 Data Analysis & Recommendations')
        
        # Key Insights
        st.markdown('#### 🔍 Key Insights')
        st.warning("""
        **Strong Research Foundation:** 7/10 advocacy briefs completed (70%) provides solid evidence base
        
        **Partnership Development Needed:** 0/3 partner activations indicates relationship building challenges
        
        **Strategic Timing Adjustment:** Q1 2026 timeline shift reflects thoughtful response to external conditions
        
        **Comprehensive Planning:** Phase 1 strategic focus shows systematic approach to advocacy development
        
        **Coalition Building Progress:** Active conversations with 1K Women Strong and HiP show promising partnerships
        
        **Member Engagement Gap:** 0/5 listening sessions suggest need for community outreach acceleration
        """)
        
        # Strategic Recommendations
        st.markdown('#### 💡 Strategic Recommendations')
        st.success("""
        **Complete Research Phase:** Finalize remaining 3 advocacy briefs to establish full evidence foundation
        
        **Pilot Partnership Programs:** Convert HiP and 1K Women Strong conversations into formal pilot activations
        
        **Member Listening Strategy:** Launch listening sessions in 2-3 pilot geographies before full 5-location rollout
        
        **Mobile App Integration:** Accelerate advocacy content in Summer of Solidarity weekly dispatches
        
        **Youth Partnership Priority:** Leverage civic partnerships director relationships for next-generation leadership
        
        **Timeline Communication:** Clearly communicate adjusted timeline to maintain member and partner confidence
        """)
        
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Advocacy")

    # ---------------------------------
    # Impact Tab (moved to tab10)
    # ---------------------------------
    with tab10:
        add_board_update("Impact")
        
        st.markdown('<h3 class="section-title">Impact Metrics - Self-Care School 2025</h3>', unsafe_allow_html=True)

        # Health and Well-being Impact
        st.markdown('<h4>Health & Well-being Outcomes</h4>', unsafe_allow_html=True)
        
        health_col1, health_col2, health_col3 = st.columns(3)
        
        with health_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">HEALTH KNOWLEDGE CHANGE</p>'
                f'<p class="metric-value">999</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Women reporting a change in health knowledge</p>'
                f'<p style="font-size: 14px; color: #666;">0.00% (baseline measure)</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with health_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">MENTAL WELL-BEING IMPROVEMENT</p>'
                f'<p class="metric-value">998</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Women reporting changes in self-reported mental well-being</p>'
                f'<p style="font-size: 14px; color: #666;">99.90% of respondents</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with health_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">SOCIAL CONNECTION</p>'
                f'<p class="metric-value">673</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Women feeling more connected and less isolated through GirlTREK</p>'
                f'<p style="font-size: 14px; color: #666;">68.53% of respondents</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Behavior Change Impact
        st.markdown('<h4>Behavior Change & Empowerment</h4>', unsafe_allow_html=True)
        
        behavior_col1, behavior_col2 = st.columns(2)
        
        with behavior_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">EMPOWERED TO TAKE ACTION</p>'
                f'<p class="metric-value">907</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Participants feeling empowered to make positive changes</p>'
                f'<p style="font-size: 14px; color: #666;">90.52% of respondents</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with behavior_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">STRONGER WALKING HABIT</p>'
                f'<p class="metric-value">709</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Participants who built a stronger walking habit</p>'
                f'<p style="font-size: 14px; color: #666;">68.70% of respondents</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        behavior_col3, behavior_col4 = st.columns(2)
        
        with behavior_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">IMPLEMENTED NEW HABITS</p>'
                f'<p class="metric-value">293</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Participants who implemented new habits, actions, or mindsets</p>'
                f'<p style="font-size: 14px; color: #666;">34.92% of respondents</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with behavior_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">SHARED WITH OTHERS</p>'
                f'<p class="metric-value">819</p>'
                f'<p style="font-style: italic; font-size: 12px; color: #666;">Participants who shared lessons learned with others</p>'
                f'<p style="font-size: 14px; color: #666;">83.66% of respondents</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Knowledge Increase by Topic
        st.markdown('<h4>Knowledge Increase by Self-Care School Topics</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-style: italic; color: #666;">Number of participants reporting significant increase in knowledge:</p>', unsafe_allow_html=True)
        
        # Display as metric boxes with correct percentages
        knowledge_col1, knowledge_col2 = st.columns(2)
        
        knowledge_items = [
            ("Land rights, housing & environmental justice", 710, 71.60),
            ("Civic engagement & political participation", 569, 57.00),
            ("Safety, self-defense & public resource access", 645, 64.40),
            ("Decarceration, gun safety & restorative justice", 658, 63.76),
            ("Mental health & emotional boundaries", 622, 60.27),
            ("Radical care, family legacy & intergenerational healing", 695, 67.34),
            ("Parenting, mentorship & end-of-life planning", 536, 51.94),
            ("Self-esteem, celebration & personal empowerment", 602, 58.33)
        ]
        
        for i in range(0, 4):
            with knowledge_col1:
                topic, count, pct = knowledge_items[i]
                st.markdown(
                    f"""
                    <div class="metric-box" style="margin-bottom: 15px;">
                        <p class="metric-title" style="font-size: 14px;">{topic.upper()}</p>
                        <p class="metric-value" style="font-size: 24px;">{count}</p>
                        <p style="font-size: 14px; color: #666;">{pct}% of respondents</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        for i in range(4, 8):
            with knowledge_col2:
                topic, count, pct = knowledge_items[i]
                st.markdown(
                    f"""
                    <div class="metric-box" style="margin-bottom: 15px;">
                        <p class="metric-title" style="font-size: 14px;">{topic.upper()}</p>
                        <p class="metric-value" style="font-size: 24px;">{count}</p>
                        <p style="font-size: 14px; color: #666;">{pct}% of respondents</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        # Create visualization of knowledge topics
        knowledge_impact_fig = px.bar(
            knowledge_data,
            x='Members',
            y='Topic',
            orientation='h',
            title='Self-Care School Knowledge Impact by Topic',
            color='Members',
            color_continuous_scale=[primary_blue, primary_orange, primary_yellow]
        )
        knowledge_impact_fig.update_layout(
            title_font=dict(color=primary_blue),
            height=400,
            xaxis_title='Number of Participants',
            yaxis_title=''
        )
        
        st.plotly_chart(knowledge_impact_fig, use_container_width=True, key="knowledge_impact_fig")
        
        # Summary metrics
        st.markdown('<h4>Impact Summary</h4>', unsafe_allow_html=True)
        
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            st.markdown(
                f"""
                <div class="metric-box">
                    <p class="metric-title">TOTAL KNOWLEDGE TOPICS</p>
                    <p class="metric-value">8</p>
                    <p style="font-style: italic; font-size: 12px; color: #666;">Areas of significant knowledge increase</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with summary_col2:
            st.markdown(
                f"""
                <div class="metric-box">
                    <p class="metric-title">AVERAGE IMPACT PER TOPIC</p>
                    <p class="metric-value">630</p>
                    <p style="font-style: italic; font-size: 12px; color: #666;">Average participants reporting knowledge gain per topic</p>
                    <p style="font-size: 14px; color: #666;">61.08% average response rate</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with summary_col3:
            st.markdown(
                f"""
                <div class="metric-box">
                    <p class="metric-title">TOTAL KNOWLEDGE IMPACTS</p>
                    <p class="metric-value">5,037</p>
                    <p style="font-style: italic; font-size: 12px; color: #666;">Sum of all topic-specific knowledge gains</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Data Analysis & Recommendations
        st.markdown('### 📊 Data Analysis & Recommendations')
        
        # Key Insights
        st.markdown('#### 🔍 Key Insights')
        st.info("""
        **Universal Mental Health Impact:** 99.90% reporting mental well-being improvements shows exceptional program efficacy
        
        **Knowledge Transfer Success:** 5,037 total knowledge impacts across 8 topics demonstrates comprehensive education
        
        **Behavior Change Achievement:** 90.52% empowered to take action indicates transformative program design
        
        **Community Multiplication:** 83.66% shared lessons creates organic program expansion
        
        **Sustainable Habit Formation:** 68.70% built stronger walking habits supports long-term health goals
        
        **Topic Resonance Variation:** Land rights (71.60%) vs parenting (51.94%) shows content preference differences
        """)
        
        # Strategic Recommendations
        st.markdown('#### 💡 Strategic Recommendations')
        st.success("""
        **Scale Proven Model:** Replicate Self-Care School structure for year-round programming to maximize impact
        
        **Content Optimization:** Expand high-resonance topics (land rights, radical care) and enhance lower-performing areas
        
        **Peer Network Development:** Formalize the 83.66% sharing behavior into structured peer mentorship programs
        
        **Walking Habit Support:** Create specific interventions for the 31.30% who have not developed consistent walking habits
        
        **Impact Documentation:** Implement longitudinal tracking to measure sustained behavior change over time
        
        **Program Graduation Pathways:** Channel empowered participants into leadership, advocacy, and crew leader roles
        """)
        
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Impact")

if __name__ == "__main__":
    main()
