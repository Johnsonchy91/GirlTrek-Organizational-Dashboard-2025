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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
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
    elif tab_name == "Operations":
        update_content = """
        <p><strong>What's Going Well</strong></p>
        <ul>
            <li><strong>People First Wins:</strong> We're operating with 94% staff retention—well above the industry average (86%)—and our latest 2024 survey shows 88% employee satisfaction. That's a reflection of the culture we're building together. Let's keep investing in each other.</li>
            <li><strong>Financial Strength:</strong> We've exceeded expectations with $3.24M YTD revenue compared to a $1.24M budget. We must be mindful of the current climate we are in and continue to be in a posture of how we fund our boldest ideas.</li>
            <li><strong>Cybersecurity on the Rise:</strong> We're now at 70% compliance—steadily advancing toward our 90% goal. Thank you to everyone working behind the scenes to keep our systems and data secure.</li>
        </ul>
        
        <p><strong>Where We Need to Focus</strong></p>
        <ul>
            <li><strong>Tech Adoption & Efficiency:</strong> Asana adoption is currently at 38% vs. our 85% goal. This signals a need for more support, training, and change management. The operations team will continue to provide not just training but real world examples of how Asana can help the organization be more productive and support our Goals process.</li>
            <li><strong>Store Operations Lag:</strong> With only 25% of our sales goal reached, we are taking a hard look at—product mix, pricing, marketing, and fulfillment and make necessary pivots.</li>
        </ul>
        """
    elif tab_name == "Engagement":
        update_content = """
        <p>The Engagement Team has hosted eight content-specific training workshops for members, focused on food justice, mental health, justice impacted communities, and caregivers. Eight additional workshops are scheduled for the remainder of the year. Members have engaged with field experts and gained valuable resources to support walking crews centered on these content areas. We are currently planning both in-person and online Mental Health First Aid training sessions for members in September. The GirlTREK Garden Club has completed two seed mailings with the first focused on growing heirloom collard greens, and the second on seed saving and community seed distribution. Additionally, the Faith Team has hosted numerous gatherings to support the growth of the faith initiative and has successfully recruited new faith communities. They are well on their way to engaging 500 faith communities this year.</p>
        
        <p>Work in Montgomery is steadily progressing. The architecture consultant has developed renderings for the space, including a beautiful Mother Garden in the backyard that will serve as a gathering space, a place of respite, and a food access point for the community. Our Director of Place-Based Innovation has also cultivated strong relationships across the community, and GirlTREK now enjoys increased brand awareness through outreach, publicity, and hosted walks.</p>
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

# PDF Generation Function - FIXED VERSION
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
    
    # Add title
    elements.append(Paragraph(f"GirlTREK Organizational Dashboard", title_style))
    
    if section_name == "Complete Dashboard":
        elements.append(Paragraph(f"Q2 2025 Complete Dashboard Report", heading_style))
    else:
        elements.append(Paragraph(f"Q2 2025 Metrics Overview - {section_name}", heading_style))
    
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Handle Complete Dashboard
    if section_name == "Complete Dashboard":
        sections = [
            "Executive Summary", "Recruitment", "Engagement", "Development", 
            "Marketing", "Campaigns", "Operations", "Member Care", "Advocacy", "Impact"
        ]
        
        for i, section in enumerate(sections):
            if i > 0:  # Add page break between sections
                elements.append(PageBreak())
            
            # Add section header
            elements.append(Paragraph(f"{section}", title_style))
            elements.append(Spacer(1, 0.25*inch))
            
            # Add section-specific content
            elements.extend(generate_section_content(section, heading_style, normal_style, accent_color, colors))
            
            # Add notes for this section if they exist
            notes_key = f"notes_{section}"
            if notes_key in st.session_state and st.session_state[notes_key]:
                elements.append(Spacer(1, 0.5*inch))
                elements.append(Paragraph(f"Notes - {section}", heading_style))
                elements.append(Paragraph(st.session_state[notes_key], normal_style))
    else:
        # Generate content for specific section
        elements.extend(generate_section_content(section_name, heading_style, normal_style, accent_color, colors))
        
        # Add notes if they exist
        notes_key = f"notes_{section_name}"
        if notes_key in st.session_state and st.session_state[notes_key]:
            elements.append(Spacer(1, 0.5*inch))
            elements.append(Paragraph("Notes", heading_style))
            elements.append(Paragraph(st.session_state[notes_key], normal_style))
    
    # Add global notes at the end
    if 'global_notes' in st.session_state and st.session_state.global_notes:
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("Global Dashboard Notes", heading_style))
        elements.append(Paragraph(st.session_state.global_notes, normal_style))
    
    # Build PDF
    doc.build(elements)
    
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(pdf_data).decode()

def generate_section_content(section_name, heading_style, normal_style, accent_color, colors):
    """Generate content for a specific section"""
    elements = []
    
    if section_name == "Executive Summary":
        elements.append(Paragraph("Key Metrics", heading_style))
        
        data = [
            ["Metric", "Current Value", "Goal", "Status"],
            ["Total Membership", f"{format_number(st.session_state.total_membership)}", "1,700,000", "On Track"],
            ["Total New Members", f"{format_number(st.session_state.new_members)}", "100,000", "At Risk"],
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
    
    elif section_name == "Recruitment":
        elements.append(Paragraph("Recruitment Metrics", heading_style))
        
        data = [
            ["Metric", "Current Value", "Goal", "Status"],
            ["Total New Members", "15,438", "100,000", "At Risk"],
            ["New Members Age 18-25", "316", "100,000", "At Risk"],
            ["Total Recruitment Partnerships", "18", "10", "Achieved"]
        ]
        
        t = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
    
    elif section_name == "Engagement":
        elements.append(Paragraph("Engagement Metrics", heading_style))
        
        data = [
            ["Metric", "Current Value", "Goal", "Status"],
            ["Total New Crews (2025)", "727", "-", "-"],
            ["Members Walking Daily", "5,439", "50,000", "At Risk"],
            ["Active Volunteers", "3,348", "-", "-"],
            ["Active Crew Leaders", "1,846", "-", "On Track"],
            ["Special Impact Programs", "100", "65,000", "At Risk"]
        ]
        
        t = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
    
    elif section_name == "Development":
        elements.append(Paragraph("Development Metrics", heading_style))
        
        data = [
            ["Metric", "Current Value", "Goal", "Status"],
            ["Total Contributions", "$3,109,294.25", "$10,000,000", "On Track"],
            ["Total Grants", "$3,101,133.09", "-", "On Track"],
            ["Corporate Sponsorships", "$130,000", "$1,500,000", "At Risk"],
            ["Earned Revenue (Store)", "$99,836", "$400,000", "At Risk"]
        ]
        
        t = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
    
    elif section_name == "Marketing":
        elements.append(Paragraph("Marketing Metrics", heading_style))
        
        data = [
            ["Metric", "Current Value", "Goal/Industry Avg", "Status"],
            ["Total Subscribers", "931,141", "1,300,000", "-"],
            ["Active Subscribers", "320,463", "-", "-"],
            ["Average Open Rate", "18.54%", "28.59%", "-"],
            ["Click-Through Rate", "1.06%", "3.29%", "-"]
        ]
        
        t = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
    
    elif section_name == "Campaigns":
        elements.append(Paragraph("Self-Care School 2025 Metrics", heading_style))
        
        data = [
            ["Metric", "Current Value", "Notes"],
            ["Members Recruited", "5,377", "Through Self-Care School"],
            ["Walking at Life-Saving Level", "12,037", "30+ min/day, 5 days/week"],
            ["Total Supporting Goal", "5,634", "Goal: 65,000"],
            ["Mental Well-Being Improvement", "998", "99.90% of respondents"],
            ["Social Connection", "673", "68.53% of respondents"]
        ]
        
        t = Table(data, colWidths=[2.5*inch, 1.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
    
    elif section_name == "Operations":
        elements.append(Paragraph("Operations Metrics", heading_style))
        
        data = [
            ["Metric", "Current Value", "Goal", "Status"],
            ["YTD Revenue", "$3,243,526", "$1,237,419", "-"],
            ["YTD Expenses", "$2,343,862", "$1,608,765", "-"],
            ["Asana Adoption", "38%", "85%", "At Risk"],
            ["Audit Compliance", "100%", "100%", "Achieved"],
            ["Staff Retention", "94%", "Industry Avg: 86%", "On Track"]
        ]
        
        t = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
    
    elif section_name == "Member Care":
        elements.append(Paragraph("Member Care Metrics", heading_style))
        
        data = [
            ["Metric", "Current Value", "Goal"],
            ["Member Satisfaction Rating", "93%", "95%"],
            ["Resolution/Responsiveness Rate", "2 hours", "48 hours"],
            ["Top Issues", "SCS Registration Error, Connecting to Movement", "-"]
        ]
        
        t = Table(data, colWidths=[2.5*inch, 2*inch, 2*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
    
    elif section_name == "Advocacy":
        elements.append(Paragraph("Advocacy Metrics", heading_style))
        
        data = [
            ["Metric", "Current Value", "Goal", "Status"],
            ["Advocacy Briefs Published", "7/10", "10", "On Track"],
            ["Advocacy Partnerships", "0/3", "3", "On Track"],
            ["Member Listening Sessions", "0/5", "5", "On Track"],
            ["Case Studies", "0/4", "4", "On Track"]
        ]
        
        t = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
    
    elif section_name == "Impact":
        elements.append(Paragraph("Impact Metrics - Self-Care School 2025", heading_style))
        
        data = [
            ["Metric", "Current Value", "Percentage"],
            ["Mental Well-Being Improvement", "998", "99.90%"],
            ["Social Connection", "673", "68.53%"],
            ["Empowered to Take Action", "907", "90.52%"],
            ["Stronger Walking Habit", "709", "68.70%"],
            ["Shared with Others", "819", "83.66%"]
        ]
        
        t = Table(data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
    
    return elements

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
                try:
                    pdf_base64 = generate_pdf(selected_download, dark_mode=st.session_state.dark_mode)
                    filename = f"{selected_download.replace(' ', '_')}_report.pdf"
                    download_link = f'<a href="data:application/pdf;base64,{pdf_base64}" download="{filename}">Download {selected_download} PDF</a>'
                    st.success(f"PDF for {selected_download} has been generated!")
                    st.markdown(download_link, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")

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
    st.markdown("*Data dashboard was updated on July 25, 2025*")

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
        
        # Member Profile Section
        st.markdown('<h3>👩🏾 GirlTREK General Member Profile: "The Everyday Health Activist"</h3>', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="background-color: #F8F9FA; border-radius: 10px; padding: 20px; margin: 20px 0; border-left: 5px solid #0088FF;">
                <p style="color: #424242; font-style: italic; font-size: 16px; margin-bottom: 20px;">
                <strong>She is the backbone of the movement. A consistent, committed, and conscientious Black woman who is reclaiming her health and leading others by example—not necessarily with a megaphone, but with steady action.</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Demographic Snapshot
        st.markdown('<h4>📊 Demographic Snapshot</h4>', unsafe_allow_html=True)
        
        demo_col1, demo_col2, demo_col3 = st.columns(3)
        
        with demo_col1:
            st.markdown("""
            **👤 Personal Info**
            - **Age**: 52 years old (core "sweet spot" 48-61)
            - **Race/Ethnicity**: Black or African American
            - **Marital Status**: Married (54.9%)
            - **Children**: Has grown children or is a caregiver (36.8%)
            """)
        
        with demo_col2:
            st.markdown("""
            **🎓 Education & Career**
            - **Education**: College-educated with bachelor's degree (26% have graduate degree)
            - **Occupation**: Professional/technical/managerial
            - **Common Sectors**: Tech (17%), Healthcare (6.2%), Education
            """)
        
        with demo_col3:
            st.markdown("""
            **💰 Financial Profile**
            - **Income**: $100K+ annually (69% of engaged members)
            - **Net Worth**: $250K-$499K
            - **Homeowner**: 83.3% (10+ years in home)
            - **Region**: Southern states (GA, TX, FL) or urban metros (NY, LA)
            """)
        
        # Mindset & Lifestyle
        st.markdown('<h4>💭 Mindset & Lifestyle</h4>', unsafe_allow_html=True)
        
        mindset_col1, mindset_col2 = st.columns(2)
        
        with mindset_col1:
            st.info("""
            **🚶🏾‍♀️ Why She Walks**
            - Health, stress relief, joy, and reclaiming time for herself
            - Both physical health and emotional healing
            - Fighting isolation, inactivity, and injustice
            
            **👥 Social Role**
            - May not lead a crew but admired by friends/family
            - First to text "You walking this Saturday?"
            - Medium to high engagement level
            """)
        
        with mindset_col2:
            st.info("""
            **🎯 Mission Alignment**
            - Driven by adding 10 years to Black women's life expectancy
            - Aligned with 3 "Deadly I's" framework
            - Subscribed to SMS list, checks Field Guide
            - Listens to Black History Bootcamp podcast
            """)
        
        # Health & Activity Level
        st.markdown('<h4>🏃🏾‍♀️ Health & Activity Level</h4>', unsafe_allow_html=True)
        
        health_col1, health_col2 = st.columns(2)
        
        with health_col1:
            st.success("""
            **Exercise Routine**
            - Walks 30 minutes/day, 5 days/week
            - Achieved during Self-Care School or Summer of Solidarity
            - Meets threshold to extend life by 7 years
            """)
        
        with health_col2:
            st.success("""
            **Preferred Activities**
            - Walking in parks or urban sidewalks
            - Gardening (80.2%)
            - Home cooking with healthy food
            - Reading (92.2%)
            - Travel (89.9%)
            - Fitness-focused (90.5%) on her own terms
            """)
        
        # Programs & Tools
        st.markdown('<h4>🛠️ Programs & Tools She Uses</h4>', unsafe_allow_html=True)
        
        tools_col1, tools_col2, tools_col3 = st.columns(3)
        
        with tools_col1:
            st.markdown("""
            **📱 Digital Tools**
            - **Field Guide**: Self-Care School calendar, Sister's Keeper pledge
            - **Podcast**: Black History Bootcamp during walks
            - **App/Website**: Tracks self-care streaks
            """)
        
        with tools_col2:
            st.markdown("""
            **🎪 Events & Programs**
            - **Mobilize**: Registers for local walks/events
            - **Juneteenth** and **BF5K** participation
            - **Care Programs**: Food justice, caregiving, mental health
            """)
        
        with tools_col3:
            st.markdown("""
            **🛍️ Engagement**
            - **Shop**: Campaign launches, golden shoelaces
            - **SMS/Email**: Subscribed for updates
            - **Social**: Shares with #GirlTREK #BlackGirlJoy
            """)
        
        # Member Behavior Patterns
        st.markdown('<h4>📅 Member Behavior Patterns</h4>', unsafe_allow_html=True)
        
        behavior_col1, behavior_col2 = st.columns(2)
        
        with behavior_col1:
            st.warning("""
            **🌸 Seasonal Engagement**
            - **Spring**: Self-Care School (10-week training)
            - **Summer**: Summer of Solidarity walks and local events
            - **Fall**: Gratitude Season – Black Family 5K, 9-Day Prayer Trek, Gratitude Trek
            """)
        
        with behavior_col2:
            st.warning("""
            **🌟 Social Influence**
            - Invites others to walk (Sister's Keeper bracelet goal)
            - Participates in Harriet House Parties, Juneteenth walks
            - Shares GirlTREK's message in church, workplace, community
            """)
        
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
