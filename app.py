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

def add_board_update(tab_name, update_content):
    """
    Add a leadership update section to the top of a tab
    
    Parameters:
    tab_name (str): The name of the tab
    update_content (str): The HTML content to display
    """
    # Check if dark mode is enabled in session state
    dark_mode = st.session_state.dark_mode if 'dark_mode' in st.session_state else False
    
    if dark_mode:
        # Dark mode styling
        board_update_html = f'''
        <div style="background-color: #1E2130; border-left: 5px solid #0088FF; 
             padding: 20px; border-radius: 5px; margin: 15px 0 25px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">
            <h4 style="color: #4DA6FF; margin-top: 0; margin-bottom: 15px; font-size: 18px;">Leadership Update: {tab_name}</h4>
            <div style="color: #E0E0E0; line-height: 1.5;">
                {update_content}
        </div>
        '''
    else:
        # Light mode styling (default)
        board_update_html = f'''
        <div style="background-color: #F3F9FF; border-left: 5px solid #0088FF; 
             padding: 20px; border-radius: 5px; margin: 15px 0 25px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h4 style="color: #0088FF; margin-top: 0; margin-bottom: 15px; font-size: 18px;">Leadership Update: {tab_name}</h4>
            <div style="color: #333333; line-height: 1.5;">
                {update_content}
        </div>
        '''
    
    # Use st.markdown with unsafe_allow_html=True to render the HTML
    st.markdown(board_update_html, unsafe_allow_html=True)

# Modify the create_notes_section function to use persistent state
def create_notes_section(tab_name):
    """Create a notes section for any tab with persistence"""
    
    notes_key = f"notes_{tab_name}"
    
    # Initialize notes in session state if they don't exist
    if notes_key not in st.session_state:
        # Try to load from disk if available
        try:
            with open(f"{notes_key}.txt", "r") as f:
                st.session_state[notes_key] = f.read()
        except FileNotFoundError:
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
                
                # Save to disk for persistence
                with open(f"{notes_key}.txt", "w") as f:
                    f.write(notes)
                
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
                    
                # Remove the file to reflect cleared notes
                try:
                    import os
                    os.remove(f"{notes_key}.txt")
                except FileNotFoundError:
                    pass
                    
                st.experimental_rerun()

# Also update the global notes saving logic
def save_global_notes(global_notes):
    previous_notes = st.session_state.global_notes
    st.session_state.global_notes = global_notes
    
    # Save to disk for persistence
    with open("global_notes.txt", "w") as f:
        f.write(global_notes)
    
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

# PDF Generation Function
def generate_pdf(section_name, dark_mode=False):
    """Generate a PDF report for the selected dashboard section"""
    
    # Buffer to store the PDF
    buffer = io.BytesIO()
    
    # Set PDF styling based on dark mode
    if dark_mode:
        background_color = colors.HexColor('#121212')
        text_color = colors.white
        accent_color = colors.HexColor('#0088FF')
    else:
        background_color = colors.white
        text_color = colors.black
        accent_color = colors.HexColor('#0088FF')
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Define styles
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
    
    # Create document elements
    elements = []
    
    # Dashboard title and date
    elements.append(Paragraph(f"GirlTREK Organizational Dashboard", title_style))
    elements.append(Paragraph(f"Q2 2025 Metrics Overview - {section_name}", heading_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add section-specific content
    if section_name == "Executive Summary":
        elements.append(Paragraph("Key Metrics", heading_style))
        
        # Key metrics table
        data = [
            ["Metric", "Current Value", "Goal", "Status"],
            ["Total Membership", f"{format_number(st.session_state.total_membership)}", "2,000,000", "On Track"],
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
        
        # Report Card Progress
        elements.append(Paragraph("Report Card Progress", heading_style))
        report_data = [
            ["Goal", "Current Total", "Percent Progress", "Status"],
            ["Recruit 100,000 new members (Age 18-25)", "130", ".13%", "Off Track"],
            ["Engage 250,000 members", "11,769", "5%", "On Track"],
            ["Support 65,000 walking daily", "4,858", "7%", "At Risk"],
            ["Unite 20 advocacy partners", "2", "10%", "At Risk"],
            ["Raise $10M", "3,061,104.78", "31%", "On Track"],
            ["Establish Care Village", "2,869", "7%", "At Risk"],
            ["Achieve 85% organizational health", "Pending", "Pending", "Pending"]
        ]
        
        t2 = Table(report_data, colWidths=[2.5*inch, 1.5*inch, 1*inch, 1*inch])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (3, 1), (3, 1), colors.green),
            ('BACKGROUND', (3, 2), (3, 2), colors.green),
            ('BACKGROUND', (3, 3), (3, 3), colors.orange),
            ('BACKGROUND', (3, 4), (3, 4), colors.orange),
            ('BACKGROUND', (3, 5), (3, 5), colors.green),
            ('BACKGROUND', (3, 6), (3, 6), colors.orange),
            ('TEXTCOLOR', (3, 1), (3, 6), colors.white),
        ]))
        elements.append(t2)
        
    elif section_name == "Recruitment":
        elements.append(Paragraph("Recruitment Metrics", heading_style))
        
        # Recruitment metrics table
        data = [
            ["Metric", "Current Value", "Goal", "Status"],
            ["Total New Members", f"{format_number(st.session_state.new_members)}", "100,000", "On Track"],
            ["New Members Age 18-25", "130", "100,000", "Off Track"],
            ["Total Recruitment Partnerships", "2", "10", "On Track"]
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
        
        # Add new members by age group
        elements.append(Paragraph("New Members by Age Group", heading_style))
        elements.append(Paragraph("18 to 24: 86 members", normal_style))
        elements.append(Paragraph("25 to 34: 477 members", normal_style))
        elements.append(Paragraph("35 to 49: 1,771 members", normal_style))
        elements.append(Paragraph("50 to 64: 2,163 members", normal_style))
        elements.append(Paragraph("65+: 1,898 members", normal_style))
        elements.append(Paragraph("Unknown: 4,961 members", normal_style))
                
    elif section_name == "Development":
        elements.append(Paragraph("Development Metrics", heading_style))
        
        # Development metrics table
        data = [
            ["Metric", "Current Value", "Goal", "Status"],
            ["Total Contributions", f"{format_currency(st.session_state.total_contributions)}", "$10,000,000", "On Track"],
            ["Total Grants", f"{format_currency(st.session_state.total_grants)}", "48 grants", "On Track"],
            ["Corporate Sponsorships", "$130,000", "$1,500,000", "At Risk"]
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
        
        # Revenue breakdown
        elements.append(Paragraph("Revenue Distribution", heading_style))
        elements.append(Paragraph("Donations: $1,094,048.68", normal_style))
        elements.append(Paragraph("Grants: $3,055,250.00", normal_style))
        
    elif section_name == "Engagement":
        elements.append(Paragraph("Engagement Metrics", heading_style))
        
        # Engagement metrics table
        data = [
            ["Metric", "Current Value", "Goal", "Status"],
            ["Total New Crews (2025)", "603", "-", "-"],
            ["Members Walking Daily", "4,788", "50,000", "At Risk"],
            ["Active Volunteers", "3,348", "-", "-"],
            ["Documented Crew Leaders", "3,732", "-", "-"],
            ["Active Crew Leaders", "1,846", "-", "On Track"]
        ]
        
        t = Table(data, colWidths=[2*inch, 1.5*inch, 1*inch, 1*inch])
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
        
        # Self-Care School Campaign
        elements.append(Paragraph("Self-Care School Campaign", heading_style))
        elements.append(Paragraph("Goal: 10,000 Registrants | Current: 11,985 Registrants", normal_style))
        elements.append(Paragraph("Status: Achieved (119.9% of goal)", normal_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Campaign Metrics
        elements.append(Paragraph("Campaign Metrics", heading_style))
        elements.append(Paragraph("New Members: 4,808", normal_style))
        elements.append(Paragraph("Downloads: 22,186 (Goal: 100,000)", normal_style))
        elements.append(Paragraph("Stories Submitted: 234 (Goal: 100)", normal_style))
        elements.append(Paragraph("Registrants Age 18-25: 101", normal_style))
        
    elif section_name == "Marketing":
        elements.append(Paragraph("Marketing Metrics", heading_style))
        
        # Marketing metrics table
        data = [
            ["Metric", "Current Value", "Goal/Percentage"],
            ["Total Subscribers", "931,141", "Goal: 1,300,000"],
            ["Active Subscribers", "297,283", "31.9% of Total"]
        ]
        
        t = Table(data, colWidths=[2*inch, 1.5*inch, 2*inch])
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
        
        # Social Media Following
        elements.append(Paragraph("Social Media Following", heading_style))
        elements.append(Paragraph("Facebook: 382,000 Followers", normal_style))
        elements.append(Paragraph("Instagram: 194,041 Followers", normal_style))
        elements.append(Paragraph("LinkedIn: 5,034 Followers", normal_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Self-Care School Social Media Performance
        elements.append(Paragraph("Self-Care School Social Media Performance", heading_style))
        elements.append(Paragraph("Impressions: 338K", normal_style))
        elements.append(Paragraph("Clicks to Site: 39K", normal_style))
        elements.append(Paragraph("Video Views: 70.7K", normal_style))
        elements.append(Paragraph("Reactions: 3.2K", normal_style))
        elements.append(Paragraph("Comments: 74", normal_style))
        elements.append(Paragraph("Shares: 217", normal_style))
        elements.append(Paragraph("Saves: 66", normal_style))
        elements.append(Paragraph("New FB Page Likes: 67", normal_style))
        
    elif section_name == "Operations":
        elements.append(Paragraph("Operations Metrics", heading_style))
        
        # Systems Performance metrics
        elements.append(Paragraph("Systems Performance", heading_style))
        data = [
            ["Metric", "Current Value", "Goal", "Status"],
            ["ASANA Adoption", "38%", "85%", "At Risk"],
            ["Audit Compliance", "Pending", "100%", "On Track"],
            ["Cybersecurity Compliance", "Pending", "70%", "On Track"]
        ]
        
        t = Table(data, colWidths=[2*inch, 1.5*inch, 1*inch, 1*inch])
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
        
        # Budget Performance
        elements.append(Paragraph("Budget Performance", heading_style))
        elements.append(Paragraph("Note: All financial data is dummy data for presentation purposes only.", normal_style))
        elements.append(Spacer(1, 0.1*inch))
        
        budget_data = [
            ["Category", "Budget", "Actual", "Percent"],
            ["Personnel", "$2,100,000", "$1,950,000", "92.9%"],
            ["Technology", "$850,000", "$790,000", "92.9%"],
            ["Facilities", "$320,000", "$295,000", "92.2%"],
            ["Marketing", "$750,000", "$710,000", "94.7%"],
            ["Programs", "$1,200,000", "$1,050,000", "87.5%"],
            ["Admin", "$280,000", "$265,000", "94.6%"]
        ]
        
        t2 = Table(budget_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t2)
        
    elif section_name == "Member Care":
        elements.append(Paragraph("Member Care Metrics", heading_style))
        
        # Member Care metrics table
        data = [
            ["Metric", "Current Value", "Goal"],
            ["Member Satisfaction Rating", "95%", "85%"],
            ["Resolution/Responsiveness Rate", "2 hours", "48 hours"]
        ]
        
        t = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
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
        
        # Top Member Issues
        elements.append(Paragraph("Top Member Issues/Concerns", heading_style))
        elements.append(Paragraph("- The App & Join the Movement", normal_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Inspirational Stories (summary)
        elements.append(Paragraph("Inspirational Stories", heading_style))
        elements.append(Paragraph("The dashboard contains three inspirational stories: Crew Leader Nicole Crooks and the South Florida crew, Amazing Ted Talk used in class, and My Sister's Keeper. See the interactive dashboard for the full stories.", normal_style))
        
    elif section_name == "Advocacy":
        elements.append(Paragraph("Advocacy Metrics", heading_style))
        
        # Advocacy metrics table
        data = [
            ["Metric", "Current Value", "Goal", "Status"],
            ["Advocacy Briefs Published", "4", "10", "On Track"],
            ["Advocacy Partnerships", "2", "20", "On Track"]
        ]
        
        t = Table(data, colWidths=[2*inch, 1.5*inch, 1*inch, 1*inch])
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
        
        # Current Focus Areas
        elements.append(Paragraph("Current Focus Areas", heading_style))
        elements.append(Paragraph("- Produce advocacy briefs establishing research basis for why each J&J agenda item leads to an increase in Black women's life expectancy", normal_style))
        elements.append(Paragraph("- Uplift best-in-class organizations", normal_style))
        elements.append(Paragraph("- Secure advocacy partners that align with GirlTREK's Joy & Justice Agenda through signed MOUs", normal_style))
        
    elif section_name == "Impact":
        elements.append(Paragraph("Impact Metrics", heading_style))
        
        elements.append(Paragraph("Note: GirlTREK's community health impact reporting will be updated following Self-Care School 2025 outcomes.", normal_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Upcoming Impact Metrics
        elements.append(Paragraph("Upcoming Impact Metrics", heading_style))
        elements.append(Paragraph("The following metrics will be reported post Self-Care School 2025:", normal_style))
        elements.append(Paragraph("- Women who have reported a change in health knowledge", normal_style))
        elements.append(Paragraph("- Changes in self-reported mental well-being", normal_style))
        elements.append(Paragraph("- Number of women who report feeling more connected and less isolated as a result of GirlTREK programming", normal_style))
        elements.append(Paragraph("- % of participants reporting weight loss", normal_style))
        elements.append(Paragraph("- % of participants reporting improved management of chronic conditions (e.g., diabetes, hypertension)", normal_style))
        elements.append(Paragraph("- % of participants reporting reduced medication dependency", normal_style))
        elements.append(Paragraph("- % of participants reporting fewer symptoms of depression or anxiety", normal_style))
    
    # Complete Dashboard section
    elif section_name == "Complete Dashboard":
        # Include summaries from all sections
        elements.append(Paragraph("This report contains all sections of the GirlTREK dashboard.", normal_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Executive Summary
        elements.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
        elements.append(Paragraph(f"Total Membership: {format_number(st.session_state.total_membership)}", normal_style))
        elements.append(Paragraph(f"Total New Members: {format_number(st.session_state.new_members)}", normal_style))
        elements.append(Paragraph(f"Total Contributions: {format_currency(st.session_state.total_contributions)}", normal_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Recruitment
        elements.append(Paragraph("RECRUITMENT", heading_style))
        elements.append(Paragraph("Total New Members: 11,356", normal_style))
        elements.append(Paragraph("New Members Age 18-25: 130", normal_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Engagement
        elements.append(Paragraph("ENGAGEMENT", heading_style))
        elements.append(Paragraph("Total New Crews: 603", normal_style))
        elements.append(Paragraph("Members Walking Daily: 4,788", normal_style))
        elements.append(Paragraph("Self-Care School Registrants: 11,985", normal_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Development
        elements.append(Paragraph("DEVELOPMENT", heading_style))
        elements.append(Paragraph(f"Total Contributions: {format_currency(st.session_state.total_contributions)}", normal_style))
        elements.append(Paragraph(f"Total Grants: {format_currency(st.session_state.total_grants)}", normal_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Additional sections summarized
        elements.append(Paragraph("MARKETING", heading_style))
        elements.append(Paragraph("Total Subscribers: 931,141", normal_style))
        elements.append(Paragraph("Active Subscribers: 297,283", normal_style))
        elements.append(Spacer(1, 0.25*inch))
        
        elements.append(Paragraph("MEMBER CARE", heading_style))
        elements.append(Paragraph("Member Satisfaction Rating: 95%", normal_style))
        elements.append(Paragraph("Resolution/Responsiveness Rate: 2 hours", normal_style))
        elements.append(Spacer(1, 0.25*inch))
        
        elements.append(Paragraph("ADVOCACY", heading_style))
        elements.append(Paragraph("Advocacy Briefs Published: 4/10", normal_style))
        elements.append(Paragraph("Advocacy Partnerships: 2/20", normal_style))
    
    else:
        # Generic content for other sections
        elements.append(Paragraph(f"{section_name} Metrics", heading_style))
        elements.append(Paragraph("This report section contains key metrics for the selected dashboard area.", normal_style))
        elements.append(Paragraph("For more detailed information, please refer to the interactive dashboard.", normal_style))
    
    # Add any notes from the dashboard
    if section_name in ["Executive Summary", "Recruitment", "Engagement", "Development", "Marketing", "Operations", "Member Care", "Advocacy", "Impact"]:
        notes_key = f"notes_{section_name}"
        if notes_key in st.session_state and st.session_state[notes_key]:
            elements.append(Spacer(1, 0.5*inch))
            elements.append(Paragraph("Notes", heading_style))
            elements.append(Paragraph(st.session_state[notes_key], normal_style))
    
    # Add global notes if they exist
    if 'global_notes' in st.session_state and st.session_state.global_notes:
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("Global Dashboard Notes", heading_style))
        elements.append(Paragraph(st.session_state.global_notes, normal_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get the PDF data and return as base64
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

# Session State
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'total_membership' not in st.session_state:
    st.session_state.total_membership = 1240394
    st.session_state.new_members = 11356
    st.session_state.total_contributions = 3061104  # Corrected total contributions value
    st.session_state.total_grants = 3055250
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

    # Fixed PDF generation section
    if st.sidebar.button("Generate PDF for Download"):
        with st.sidebar:
            with st.spinner("Generating PDF..."):
                # Generate PDF using the new function
                pdf_base64 = generate_pdf(selected_download, dark_mode=st.session_state.dark_mode)
                
                # Create download link
                filename = f"{selected_download.replace(' ', '_')}_report.pdf"
                download_link = f'<a href="data:application/pdf;base64,{pdf_base64}" download="{filename}">Download {selected_download} PDF</a>'
                
                st.success(f"PDF for {selected_download} has been generated!")
                st.markdown(download_link, unsafe_allow_html=True)

    # Add dashboard notes section after settings
    st.sidebar.markdown("---")
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

    # Add dashboard notes section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Dashboard Notes")

    # Add a section for global notes that apply to all tabs
    global_notes = st.sidebar.text_area(
        "Add global notes for the entire dashboard:",
        value=st.session_state.global_notes,
        height=100,
        key="textarea_global_notes"
    )

    # Save button for global notes
    if st.sidebar.button("Save Global Notes"):
        save_global_notes(global_notes)

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

    # Create Tabs - Fixed: Define 9 tabs only since that's what's used
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
        # Add Board Update first
        executive_update = """

        <p style="margin-bottom: 0;"><strong>Mission Priority:</strong> Our every action is in service of our mission to 
        <strong>extend the life expectancy of Black women by 10 years in 10 years.</strong></p>
        """
        add_board_update("Executive Summary", executive_update)
        
        st.markdown('<h3 class="section-title">Executive Summary</h3>', unsafe_allow_html=True)

        # --- Key Metrics ---
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
                "Recruit 100,000 new members (Age 18-25)",
                "Engage 250,000 members",
                "Support 65,000 walking daily",
                "Unite 20 advocacy partners",
                "Raise $10M",
                "Establish Care Village",
                "Achieve 85% organizational health"
            ],
            "Current Total": [
                "130", "11,769", "4,858", "2",
                "3,061,104.78", "2,869", "Pending"
            ],
            "Percent Progress": [
                ".13%", "5%", "7%", "10%", "31%", "7%", "Pending"
            ],
            "Status": [
                "Off Track", "On Track", "At Risk", "At Risk",
                "On Track", "At Risk", "Pending"
            ],
            "Progress": [
                .13, 4.7, 7.5, 10, 30.6, 7.2, 0
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

        # Continuation of the GirlTREK dashboard code:
# Picking up in the recruitment tab:
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
                f'<p class="metric-title">NEW MEMBERS AGE 18-25</p>'
                f'<p class="metric-value">130</p>'
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
        
        # Fixed: Added chart display that was missing
        st.plotly_chart(new_age_fig, use_container_width=True, key="new_age_fig")

            # Recruitment Metrics that need updates

        st.markdown("<br>", unsafe_allow_html=True)

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

        # Add Notes Section for Recruitment
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Recruitment")

    # ---------------------------------
    # Engagement Tab
    # ---------------------------------
    with tab3:
        # Add Board Update first
        engagement_update = """
        <p style="margin-bottom: 15px;"><strong>Programming Focus:</strong> Mental health is our first priority. We've launched a 
        nationwide effort to train a corps of women in <em>Mental Health First Aid</em>. This is an investment in both 
        immediate healing and long-term life extension.</p>
        
        <p style="margin-bottom: 0;"><strong>On-the-Ground Impact:</strong> In Montgomery, we've made targeted investments to serve 
        Black women at their point of need. These efforts align with our vision to increase longevity through 
        localized public health services and deepen trust with the communities we serve.</p>
        """
        add_board_update("Engagement", engagement_update)
        
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
        
        # Age demographics and Badges claimed  
        st.markdown('<h4>Campaign Metrics</h4>', unsafe_allow_html=True)

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
                    <div style="font-size: 36px; font-weight: bold; color: #0277BD; margin: 8px 0;">234</div>
                    <p style="color: #0277BD;">Goal: 100</p>
                    <p>{status_badge("Achieved")}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
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
        
        # Fixed: Added missing chart display
        st.plotly_chart(engage_badges_fig, use_container_width=True, key="engage_badges_fig")

        # Add Notes Section
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Engagement")

    # ---------------------------------
    # Development Tab
    # ---------------------------------
    with tab4:
        # Add Board Update first
        development_update = """
        <p style="margin-bottom: 15px;"><strong>Development Update:</strong> A major funder will be <strong>doubling their donation this year</strong>. 
        This strengthens our already solid financial position heading into Q3-Q4.</p>
        """
        add_board_update("Development", development_update)
        
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
                f'<p>{status_badge("On Track")}</p>'
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
        
        # Add Notes Section for Development
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Development")

    # ---------------------------------
    # Marketing Tab
    # ---------------------------------
    with tab5:
        # Add Board Update first
        marketing_update = """
        <p style="margin-bottom: 15px;"><strong>Communications & Messaging:</strong> Our values have been boldly rearticulated and published in our new 
        <strong>Field Guide</strong>:
        <ol style="margin-top: 10px; margin-bottom: 15px;">
            <li>We practice <strong>Radical Welcome</strong>.</li>
            <li>We focus on <strong>Black women disproportionately affected by health disparities</strong>.</li>
            <li>We walk with <strong>diverse communities</strong>—and we welcome all to walk with us.</li>
        </ol></p>
        
        <p style="margin-bottom: 0;"><strong>Public Relations:</strong> We're developing unified talking points for internal and external use, 
        with upcoming training sessions led by our incoming PR firm: <strong>Black Alders</strong>.</p>
        """
        add_board_update("Marketing", marketing_update)
        
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
        
        # Add Notes Section for Marketing
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Marketing")

    # ---------------------------------
    # Operations Tab (Improved)
    # ---------------------------------
    with tab6:
        # Add Board Update first
        operations_update = """
        
        <p style="margin-bottom: 15px;"><strong>Financial Stewardship Update:</strong> We recently received word that a major funder will be 
        <strong>doubling their donation this year</strong>. We are in a solid financial position.</p>
        
        <p style="margin-bottom: 15px;">We are moving forward with fiscal prudence given the economic climate and will adopt an 
        <em>austerity budget</em> while maintaining mission-critical programming that supports Black women's longevity and ensuring our team remains 
        gainfully and justly employed.</p>
        
        <p style="margin-bottom: 15px;"><strong>Technology & Security:</strong> In March, we engaged an external technology expert to audit our systems. 
        We are currently migrating member records to a more secure platform. Through our partnership with 
        RoundTable Technology, we've implemented 24/7 cybersecurity monitoring and completed digital safety 
        training for 100% of staff.</p>
        
        <p style="margin-bottom: 15px;"><strong>Compliance & Governance:</strong> GirlTREK has updated and legally vetted policies covering hiring, 
        procurement, and non-discrimination. We've revised our IRS Form 990 to reflect our commitment to 
        <em>radical welcome</em> while ensuring 501(c)(3) compliance. We're also hiring a PR firm to audit 
        our public-facing platforms.</p>
        
        <p style="margin-bottom: 0;"><strong>Legal Strategy:</strong> We are represented by <em>Orrick, Herrington & Sutcliffe LLP</em>—a powerhouse 
        in civil rights law. Our operations team meets with them bi-monthly to stay ahead of the curve.</p>
        """
        add_board_update("Operations", operations_update)
        
        st.markdown('<h3 class="section-title">Operations Metrics</h3>', unsafe_allow_html=True)

        # --- Financial Trends (moved to top of tab) ---
        st.markdown('<h4>Financial Trends Overview</h4>', unsafe_allow_html=True)
        
        # Add disclaimer about dummy data
        st.markdown(
            """
            <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-style: italic; font-size: 18px;">
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

        ops_trend_fig.update_layout(
            title='Revenue vs Expenses',
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
            <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-style: italic; font-size: 18px;">
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
                f'<p>Goal: 70%</p>'
                f'{status_badge("On Track")}'
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
        # Add Board Update first
        member_care_update = """
        <p style="margin-bottom: 0;"><strong>Mental Health Initiative:</strong> We've launched a nationwide effort to train a corps of women in 
        <em>Mental Health First Aid</em>. This program represents our commitment to both immediate healing and 
        long-term life extension through community-based mental health support.</p>
        """
        add_board_update("Member Care", member_care_update)
        
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
                """
            )
        
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
        
        # Fixed: Moved notes section outside of the expander
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Member Care")

    # ---------------------------------
    # Advocacy Tab (real data from PDF)
    # ---------------------------------
    with tab8:
        # Add Board Update first
        advocacy_update = """
        <p style="margin-bottom: 15px;"><strong>Coalition Building:</strong> We are actively deepening our relationships with national coalitions to:
        <ul style="margin-top: 10px; margin-bottom: 15px;">
            <li>Share legal resources</li>
            <li>Coordinate responses to external threats</li>
            <li>Build collective readiness and resilience</li>
        </ul></p>
        
        <p style="margin-bottom: 0;">This summer, we'll engage partners in meaningful dialogue to strengthen cross-sector relationships, 
        culminating in a convening of our coalition partners in late 2025.</p>
        """
        add_board_update("Advocacy", advocacy_update)
        
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
        
        # Add Notes Section for Impact
        st.markdown('<hr>', unsafe_allow_html=True)
        create_notes_section("Impact")

if __name__ == "__main__":
    main()
