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

# Create a function to add board updates at the top of relevant tabs
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
        board_update_html = f"""
        <div style="background-color: #1E2130; border-left: 5px solid #0088FF; 
             padding: 20px; border-radius: 5px; margin: 15px 0 25px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">
            <h4 style="color: #4DA6FF; margin-top: 0; margin-bottom: 15px; font-size: 18px;">Leadership Update: {tab_name}</h4>
            <div style="color: #E0E0E0; line-height: 1.5;">
                {update_content}
            </div>
            <div style="text-align: right; font-style: italic; font-size: 12px; color: #BBBBBB; margin-top: 10px;">
                Updated: April 25, 2025
            </div>
        </div>
        """
    else:
        # Light mode styling (default)
        board_update_html = f"""
        <div style="background-color: #F3F9FF; border-left: 5px solid #0088FF; 
             padding: 20px; border-radius: 5px; margin: 15px 0 25px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h4 style="color: #0088FF; margin-top: 0; margin-bottom: 15px; font-size: 18px;">Leadership Update: {tab_name}</h4>
            <div style="color: #333333; line-height: 1.5;">
                {update_content}
            </div>
            <div style="text-align: right; font-style: italic; font-size: 12px; color: #666; margin-top: 10px;">
                Updated: April 25, 2025
            </div>
        </div>
        """
    
    # Use st.markdown with unsafe_allow_html=True to render the HTML
    st.markdown(board_update_html, unsafe_allow_html=True)

# Example usage in tab sections:

# Executive Summary Tab
def executive_summary_tab():
    # Define the update content with proper HTML formatting
    executive_update = """
    <p style="margin-bottom: 15px;"><strong>Financial Stewardship Update:</strong> We recently received word that a major funder will be 
    <strong>doubling their donation this year</strong>. We are in a solid financial position.</p>
    
    <p style="margin-bottom: 15px;">We are moving forward with fiscal prudence given the economic climate and will adopt an 
    <em>austerity budget</em> while maintaining mission-critical programming and ensuring our team remains 
    gainfully and justly employed.</p>
    
    <p style="margin-bottom: 0;"><strong>Mission Priority:</strong> Our every action is in service of our mission to 
    <strong>extend the life expectancy of Black women by 10 years in 10 years.</strong></p>
    """
    
    # Add the board update to the tab
    add_board_update("Executive Summary", executive_update)
    
    # Rest of executive summary tab content...

# Development Tab
def development_tab():
    # Define the update content with proper HTML formatting
    development_update = """
    <p style="margin-bottom: 15px;"><strong>Financial Update:</strong> A major funder will be <strong>doubling their donation this year</strong>. 
    This strengthens our already solid financial position heading into Q3-Q4.</p>
    
    <p style="margin-bottom: 0;">Teams are evaluating where cost-saving measures can be applied while preserving:
    <ul style="margin-top: 10px; margin-bottom: 0;">
        <li>Mission-critical programming that supports Black women's longevity</li>
        <li>Ensuring our team remains gainfully and justly employed</li>
    </ul></p>
    """
    
    # Add the board update to the tab
    add_board_update("Development", development_update)
    
    # Rest of development tab content...

# Engagement Tab
def engagement_tab():
    # Define the update content with proper HTML formatting
    engagement_update = """
    <p style="margin-bottom: 15px;"><strong>Programming Focus:</strong> Mental health is our first priority. We've launched a 
    nationwide effort to train a corps of women in <em>Mental Health First Aid</em>. This is an investment in both 
    immediate healing and long-term life extension.</p>
    
    <p style="margin-bottom: 0;"><strong>On-the-Ground Impact:</strong> In Montgomery, we've made targeted investments to serve 
    Black women at their point of need. These efforts align with our vision to increase longevity through 
    localized public health services and deepen trust with the communities we serve.</p>
    """
    
    # Add the board update to the tab
    add_board_update("Engagement", engagement_update)
    
    # Rest of engagement tab content...

# Marketing Tab
def marketing_tab():
    # Define the update content with proper HTML formatting
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
    
    # Add the board update to the tab
    add_board_update("Marketing", marketing_update)
    
    # Rest of marketing tab content...

# Operations Tab
def operations_tab():
    # Define the update content with proper HTML formatting
    operations_update = """
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
    
    # Add the board update to the tab
    add_board_update("Operations", operations_update)
    
    # Rest of operations tab content...

# Member Care Tab
def member_care_tab():
    # Define the update content with proper HTML formatting
    member_care_update = """
    <p style="margin-bottom: 0;"><strong>Mental Health Initiative:</strong> We've launched a nationwide effort to train a corps of women in 
    <em>Mental Health First Aid</em>. This program represents our commitment to both immediate healing and 
    long-term life extension through community-based mental health support.</p>
    """
    
    # Add the board update to the tab
    add_board_update("Member Care", member_care_update)
    
    # Rest of member care tab content...

# Advocacy Tab
def advocacy_tab():
    # Define the update content with proper HTML formatting
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
    
    # Add the board update to the tab
    add_board_update("Advocacy", advocacy_update)
    
    # Rest of advocacy tab content...

# Main App Structure (Example)
def main():
    # Sidebar with dark mode toggle
    st.sidebar.markdown("### Dashboard Settings")
    
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
        
    dark_mode = st.sidebar.checkbox("Dark Mode", value=st.session_state.dark_mode, key="dark_mode_checkbox")
    
    # Update session state
    st.session_state.dark_mode = dark_mode
    
    # Apply dark mode
    apply_dark_mode(dark_mode)
    
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
    
    # Fill tab content
    with tab1:
        executive_summary_tab()
        
    # Other tab content...
    with tab3:
        engagement_tab()
        
    with tab4:
        development_tab()
        
    with tab5:
        marketing_tab()
        
    with tab6:
        operations_tab()
        
    with tab7:
        member_care_tab()
        
    with tab8:
        advocacy_tab()

# Apply dark mode function (already in your code)
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

if __name__ == "__main__":
    main()
