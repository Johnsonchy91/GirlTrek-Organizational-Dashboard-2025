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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch

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

def status_badge(status):
    if status == "On Track":
        return f'<span style="background-color: #4CAF50; color: white; padding: 3px 8px; border-radius: 4px;">On Track</span>'
    elif status == "At Risk":
        return f'<span style="background-color: #FF9800; color: white; padding: 3px 8px; border-radius: 4px;">At Risk</span>'
    elif status == "Achieved":
        return f'<span style="background-color: {achieved_green}; color: white; padding: 3px 8px; border-radius: 4px;">Achieved</span>'
    else:
        return f'<span style="background-color: #F44336; color: white; padding: 3px 8px; border-radius: 4px;">Off Track</span>'

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
            .model-header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
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
            .model-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

# Session State - Initialize with real data
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.total_membership = 1244476
    st.session_state.new_members = 15438
    st.session_state.total_contributions = 3109294.25
    st.session_state.total_grants = 3101133.09
    st.session_state.data_loaded = True

# Initialize dark mode
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Main App
def main():
    # Add print-friendly CSS
    st.markdown("""
    <style>
    @media print {
        header[data-testid="stHeader"] { display: none !important; }
        section[data-testid="stSidebar"] { display: none !important; }
        div[data-testid="stToolbar"] { display: none !important; }
        footer { display: none !important; }
        #MainMenu { display: none !important; }
        
        .main .block-container {
            max-width: 100% !important;
            padding: 1rem !important;
        }
        
        * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        .element-container, .metric-container {
            break-inside: avoid !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.image("https://www.girltrek.org/assets/images/logo.png", width=200)
    st.sidebar.markdown("### 🚶🏾‍♀️ GirlTREK Dashboard")
    st.sidebar.markdown("**Q3 2025 Metrics Overview**")
    st.sidebar.markdown("*Data updated: Aug 1, 2025*")
    st.sidebar.markdown("---")
    
    # Dashboard Settings
    st.sidebar.markdown("### ⚙️ Dashboard Settings")
    dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
    st.session_state.dark_mode = dark_mode
    apply_dark_mode(dark_mode)
    
    # Quick Stats in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    st.sidebar.metric("Total Membership", format_number(st.session_state.total_membership))
    st.sidebar.metric("New Members (2025)", format_number(st.session_state.new_members))
    st.sidebar.metric("Total Contributions", format_currency(st.session_state.total_contributions))
    st.sidebar.metric("Members Walking Daily", "5,634")
    
    # Export Options
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📥 Export Options")
    if st.sidebar.button("🖨️ Save as PDF"):
        print_js = """
        <script>
        setTimeout(function() {
            window.print();
        }, 500);
        </script>
        """
        st.components.v1.html(print_js, height=0)
        st.sidebar.success("✅ Print dialog opened!")

    # App Title with Model of Change Header
    st.markdown(
        """
        <div class="model-header">
            <h1 style="color: white; margin: 0;">🚶🏾‍♀️ GirlTREK Organizational Dashboard</h1>
            <p style="color: white; font-size: 18px; margin-top: 10px;">Model of Change: Walk • Talk • Solve Problems</p>
            <p style="color: white; font-size: 14px; margin-top: 5px;">Reducing Inactivity • Eliminating Isolation • Combating Injustice</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load all original data
    
    # New Members by Month - Real data
    df_extended = pd.DataFrame({
        'Month': ['Oct 2024', 'Nov 2024', 'Dec 2024', 'Jan 2025', 'Feb 2025', 'Mar 2025', 'Apr 2025', 'May 2025', 'Jun 2025'],
        'New Members': [1365, 1419, 182, 591, 1588, 4382, 6073, 2610, 123],
        'Date': [
            datetime(2024, 10, 1), datetime(2024, 11, 1), datetime(2024, 12, 1),
            datetime(2025, 1, 1), datetime(2025, 2, 1), datetime(2025, 3, 1),
            datetime(2025, 4, 1), datetime(2025, 5, 1), datetime(2025, 6, 1)
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

    # Historic Movement Growth Numbers - Real data
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
        'Revenue': [648705, 648705, 648705, 648705, 648706],
        'Expenses': [468772, 468772, 468772, 468773, 468773]
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
            'Radical care, family legacy & intergenerational healing',
            'Decarceration, gun safety & restorative justice',
            'Safety, self-defense & public resource access',
            'Mental health & emotional boundaries',
            'Self-esteem, celebration & personal empowerment',
            'Civic engagement & political participation',
            'Parenting, mentorship & end-of-life planning'
        ],
        'Members': [710, 695, 658, 645, 622, 602, 569, 536],
        'Percentage': [71.60, 67.34, 63.76, 64.40, 60.27, 58.33, 57.00, 51.94]
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
    
    # Grant Applications Data
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
    
    grants_df = pd.DataFrame(grants_data)
    
    # Create Tabs based on Model of Change
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Executive Summary",
        "🚶🏾‍♀️ WALK (Reduce Inactivity)", 
        "💬 TALK (Eliminate Isolation)",
        "✊🏾 SOLVE PROBLEMS (Combat Injustice)",
        "📊 Operational Excellence"
    ])
    
    # ---------------------------------
    # Executive Summary Tab
    # ---------------------------------
    with tab1:
        st.markdown('<h2 class="section-title">Executive Summary - Q3 2025</h2>', unsafe_allow_html=True)
        
        # Mission Statement
        st.info(
            """
            **Our Mission**: To increase the life expectancy of Black women by mobilizing 1 million women to walk, talk, and solve problems.
            
            **Our Model**: Walk (Reduce Inactivity) • Talk (Eliminate Isolation) • Solve Problems (Combat Injustice)
            """
        )
        
        # Key Performance Indicators
        st.markdown("### 🎯 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Membership", format_number(st.session_state.total_membership), "+15,438 YTD")
        with col2:
            st.metric("Walking Daily", "5,634", "Goal: 65,000")
        with col3:
            st.metric("Total Raised", format_currency(st.session_state.total_contributions), "31% of $10M goal")
        with col4:
            st.metric("Program Impact", "99.9%", "Mental well-being improvement")
        
        # Report Card Progress
        st.markdown("### 📋 2025 Report Card Progress")
        
        report_data = {
            "Goal": [
                "🚶🏾‍♀️ WALK: Support 65,000 walking daily",
                "🚶🏾‍♀️ WALK: Recruit 100,000 new members",
                "💬 TALK: Engage 250,000 members",
                "💬 TALK: Train 100 Blue Brigade leaders",
                "✊🏾 SOLVE: Unite 3 advocacy partners",
                "✊🏾 SOLVE: Establish Care Village (40k)",
                "💰 SUSTAIN: Raise $10M",
                "📊 EXCEL: Achieve 85% organizational health"
            ],
            "Current": ["5,634", "15,438", "13,119", "50", "0", "7,660", "$3.1M", "TBD"],
            "Progress": [8.67, 15.44, 5.25, 50.0, 0, 19.15, 31.09, 0],
            "Status": ["At Risk", "At Risk", "On Track", "On Track", "On Track", "On Track", "On Track", "On Track"]
        }
        
        for i in range(len(report_data["Goal"])):
            goal = report_data["Goal"][i]
            current = report_data["Current"][i]
            progress = report_data["Progress"][i]
            status = report_data["Status"][i]
            
            if status == "On Track":
                bar_color = "#4CAF50"
            elif status == "At Risk":
                bar_color = "#FF9800"
            else:
                bar_color = "#F44336"
            
            st.markdown(
                f"""
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <div><strong>{goal}</strong></div>
                        <div style="text-align: right;">
                            <span style="margin-right: 15px;">{current}</span>
                            <span style="margin-right: 15px;">{progress:.1f}%</span>
                            {status_badge(status)}
                        </div>
                    </div>
                    <div style="width: 100%; background-color: #f0f2f5; height: 12px; border-radius: 6px;">
                        <div style="width: {min(progress, 100)}%; height: 100%; background-color: {bar_color}; border-radius: 6px;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Model of Change Performance
        st.markdown("### 🔄 Model of Change Performance")
        
        model_col1, model_col2, model_col3 = st.columns(3)
        
        with model_col1:
            st.markdown(
                """
                <div style="background-color: #E8F5E8; border-radius: 10px; padding: 20px; text-align: center;">
                    <h3 style="color: #2E7D32;">🚶🏾‍♀️ WALK</h3>
                    <p style="font-size: 14px; color: #424242;">Reducing Inactivity</p>
                    <hr>
                    <p><strong>5,634</strong> walking daily</p>
                    <p><strong>727</strong> new crews formed</p>
                    <p><strong>12,037</strong> at life-saving level</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with model_col2:
            st.markdown(
                """
                <div style="background-color: #E3F2FD; border-radius: 10px; padding: 20px; text-align: center;">
                    <h3 style="color: #1565C0;">💬 TALK</h3>
                    <p style="font-size: 14px; color: #424242;">Eliminating Isolation</p>
                    <hr>
                    <p><strong>11,535</strong> trained volunteers</p>
                    <p><strong>673</strong> report social connection</p>
                    <p><strong>8</strong> knowledge topics delivered</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with model_col3:
            st.markdown(
                """
                <div style="background-color: #FFF3E0; border-radius: 10px; padding: 20px; text-align: center;">
                    <h3 style="color: #E65100;">✊🏾 SOLVE</h3>
                    <p style="font-size: 14px; color: #424242;">Combating Injustice</p>
                    <hr>
                    <p><strong>7</strong> advocacy briefs published</p>
                    <p><strong>7,660</strong> in Care Village</p>
                    <p><strong>907</strong> empowered to act</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Historic Growth
        st.markdown("### 📈 Historic Movement Growth")
        
        historic_fig = go.Figure()
        historic_fig.add_trace(go.Scatter(
            x=df_historic_growth['Year'],
            y=df_historic_growth['Trekkers'],
            mode='lines+markers',
            name='Total Trekkers',
            line=dict(color=primary_blue, width=3),
            marker=dict(size=8)
        ))
        
        historic_fig.update_layout(
            title='Historic Growth of Trekkers (2020-2025)',
            xaxis_title='Year',
            yaxis_title='Total Trekkers',
            title_font=dict(color=primary_blue),
            height=400
        )
        
        st.plotly_chart(historic_fig, use_container_width=True)
        
        # Demographics Overview
        st.markdown("### 👥 Membership Demographics")
        
        demo_col1, demo_col2 = st.columns(2)
        
        with demo_col1:
            # Top States
            states_fig = px.bar(
                df_top_states,
                x='State',
                y='Members',
                title='Top 5 States by Membership',
                color='Members',
                color_continuous_scale=[primary_blue, secondary_purple]
            )
            states_fig.update_layout(title_font=dict(color=primary_blue), height=350)
            st.plotly_chart(states_fig, use_container_width=True)
        
        with demo_col2:
            # Top Cities
            cities_fig = px.bar(
                df_top_cities,
                x='City',
                y='Members',
                title='Top 5 Cities by Membership',
                color='Members',
                color_continuous_scale=[primary_blue, secondary_orange]
            )
            cities_fig.update_layout(title_font=dict(color=primary_blue), height=350)
            st.plotly_chart(cities_fig, use_container_width=True)
        
        # Member Profile
        st.markdown('### 👩🏾 GirlTREK Member Profile: "The Everyday Health Activist"')
        
        profile_col1, profile_col2, profile_col3 = st.columns(3)
        
        with profile_col1:
            st.info(
                """
                **Demographics**
                - Age: 52 years old
                - Education: College degree
                - Income: $100K+ (69%)
                - Location: Southern states
                - Homeowner: 83.3%
                """
            )
        
        with profile_col2:
            st.info(
                """
                **Health Habits**
                - Walks 30 min/day, 5 days/week
                - Gardens (80.2%)
                - Reads (92.2%)
                - Travels (89.9%)
                - Fitness-focused (90.5%)
                """
            )
        
        with profile_col3:
            st.info(
                """
                **Engagement**
                - Email subscriber
                - SMS member
                - Podcast listener
                - Event participant
                - Social media sharer
                """
            )
    
    # ---------------------------------
    # WALK Tab (Reduce Inactivity)
    # ---------------------------------
    with tab2:
        st.markdown('<h2 class="section-title">🚶🏾‍♀️ WALK - Reducing Inactivity</h2>', unsafe_allow_html=True)
        
        st.markdown(
            """
            <div style="background-color: #E8F5E8; border-left: 5px solid #4CAF50; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <p style="color: #2E7D32; font-size: 16px; margin: 0;">
                <strong>Primary Outcome:</strong> Reduce inactivity by motivating members to adopt a daily habit of walking 30 minutes a day, 5 days a week.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Walking Metrics
        st.markdown("### 📊 Core Walking Metrics")
        
        walk_col1, walk_col2, walk_col3, walk_col4 = st.columns(4)
        
        with walk_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">MEMBERS WALKING DAILY</p>'
                f'<p class="metric-value">5,634</p>'
                f'<p style="font-style: italic; font-size: 12px;">30 min/day, 5 days/week</p>'
                f'<p>Goal: 65,000</p>'
                f'<p>{status_badge("At Risk")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with walk_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">AT LIFE-SAVING LEVEL</p>'
                f'<p class="metric-value">12,037</p>'
                f'<p style="font-style: italic; font-size: 12px;">From Self-Care School</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with walk_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">NEW WALKING CREWS</p>'
                f'<p class="metric-value">727</p>'
                f'<p style="font-style: italic; font-size: 12px;">Formed in 2025</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with walk_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">ACTIVE CREW LEADERS</p>'
                f'<p class="metric-value">1,846</p>'
                f'<p style="font-style: italic; font-size: 12px;">Leading walks</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Recruitment Section
        st.markdown("### 👥 Member Recruitment")
        
        recruit_col1, recruit_col2, recruit_col3 = st.columns(3)
        
        with recruit_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL NEW MEMBERS</p>'
                f'<p class="metric-value">{format_number(st.session_state.new_members)}</p>'
                f'<p>Goal: 100,000</p>'
                f'<p>{status_badge("At Risk")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with recruit_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">NEW MEMBERS AGE 18-25</p>'
                f'<p class="metric-value">316</p>'
                f'<p>Goal: 100,000</p>'
                f'<p>{status_badge("At Risk")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with recruit_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">RECRUITMENT PARTNERSHIPS</p>'
                f'<p class="metric-value">18</p>'
                f'<p>Goal: 10</p>'
                f'<p>{status_badge("Achieved")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Monthly Recruitment Chart
        st.markdown("### 📈 Monthly Recruitment Trends")
        
        recruit_monthly_fig = px.bar(
            df_extended,
            x='Month',
            y='New Members',
            title='New Member Recruitment by Month (Oct 2024 - Jun 2025)',
            color='New Members',
            color_continuous_scale=[secondary_blue, primary_blue, primary_orange]
        )
        recruit_monthly_fig.update_layout(title_font=dict(color=primary_blue), height=400)
        st.plotly_chart(recruit_monthly_fig, use_container_width=True)
        
        # Age Distribution
        st.markdown("### 👤 Member Age Distribution")
        
        age_col1, age_col2 = st.columns(2)
        
        with age_col1:
            # New Members by Age
            new_age_fig = px.pie(
                df_new_age,
                values='New Members',
                names='Age Group',
                title='New Members by Age Group',
                color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, secondary_pink, secondary_purple, secondary_green]
            )
            new_age_fig.update_traces(textposition='inside', textinfo='percent+label')
            new_age_fig.update_layout(title_font=dict(color=primary_blue), height=350)
            st.plotly_chart(new_age_fig, use_container_width=True)
        
        with age_col2:
            # Total Membership by Age
            total_age_fig = px.bar(
                df_total_age,
                x='Age Group',
                y='Members',
                title='Total Membership by Age Group',
                color='Members',
                color_continuous_scale=[secondary_purple, primary_blue, secondary_pink]
            )
            total_age_fig.update_layout(title_font=dict(color=primary_blue), height=350)
            st.plotly_chart(total_age_fig, use_container_width=True)
        
        # Walking Campaigns
        st.markdown("### 🎯 Walking Campaigns & Programs")
        
        # Self-Care School Campaign Metrics
        st.markdown("#### Self-Care School 2025")
        
        scs_col1, scs_col2, scs_col3 = st.columns(3)
        
        with scs_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">MEMBERS RECRUITED</p>'
                f'<p class="metric-value">5,377</p>'
                f'<p style="font-style: italic; font-size: 12px;">Through Self-Care School</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with scs_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">WALKING AT LIFE-SAVING</p>'
                f'<p class="metric-value">12,037</p>'
                f'<p style="font-style: italic; font-size: 12px;">30+ min/day, 5 days/week</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with scs_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">BADGES EARNED</p>'
                f'<p class="metric-value">22,903</p>'
                f'<p style="font-style: italic; font-size: 12px;">Total badges claimed</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Badge Week Performance
        st.markdown("#### Badge Achievement by Week")
        
        badge_fig = px.bar(
            badge_week_data,
            x='Week',
            y='Badges Claimed',
            title='Self-Care School Badge Achievement Progress',
            color='Badges Claimed',
            color_continuous_scale=['#E8F5E8', '#4CAF50']
        )
        badge_fig.update_layout(title_font=dict(color=primary_blue), height=350)
        st.plotly_chart(badge_fig, use_container_width=True)
        
        # Special Walking Programs
        st.markdown("### 🌟 Special Walking Programs")
        
        with st.expander("👩‍👧 Mommy and Me Walking Program", expanded=True):
            mommy_col1, mommy_col2, mommy_col3 = st.columns(3)
            
            with mommy_col1:
                st.metric("Mom Coaches Recruited", "45/50", "90% Complete")
            with mommy_col2:
                st.metric("Walks Completed", "8", "Goal: 100")
            with mommy_col3:
                st.metric("Community Engagement", "83", "Free tickets distributed")
            
            st.markdown(
                """
                **Program Impact:** Creating safe spaces for mothers and children to walk together
                
                **Schedule:**
                - Round 1: Completed July 5th ✅
                - Round 2: July 19, Aug 2 & 23, Sep 6
                """
            )
        
        with st.expander("🎓 College Crews Initiative", expanded=True):
            college_col1, college_col2, college_col3 = st.columns(3)
            
            with college_col1:
                st.metric("College Leads", "11/100", "11% of target")
            with college_col2:
                st.metric("Members 18-25", "316", "Goal: 100,000")
            with college_col3:
                st.metric("Campus Coverage", "11", "HBCUs prioritized")
            
            st.markdown(
                """
                **Mission:** Empowering the next generation to start self-care early
                
                **Solidarity Walks:**
                - Round 1: September 18, 2025
                - Round 2: January 22, 2026
                - Round 3: April 9, 2026
                """
            )
        
        # Walking Habit Development
        st.markdown("### 📈 Walking Habit Impact")
        
        habit_data = pd.DataFrame({
            'Metric': ['Built Stronger Walking Habit', 'Implemented New Habits', 'Shared Lessons with Others'],
            'Members': [709, 293, 819],
            'Percentage': [68.70, 34.92, 83.66]
        })
        
        habit_fig = px.bar(
            habit_data,
            x='Metric',
            y='Members',
            title='Self-Care School Behavior Change Outcomes',
            text='Percentage',
            color='Members',
            color_continuous_scale=['#E8F5E8', '#66BB6A', '#4CAF50']
        )
        habit_fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        habit_fig.update_layout(title_font=dict(color=primary_blue), height=400)
        st.plotly_chart(habit_fig, use_container_width=True)
    
    # ---------------------------------
    # TALK Tab (Eliminate Isolation)
    # ---------------------------------
    with tab3:
        st.markdown('<h2 class="section-title">💬 TALK - Eliminating Isolation</h2>', unsafe_allow_html=True)
        
        st.markdown(
            """
            <div style="background-color: #E3F2FD; border-left: 5px solid #2196F3; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <p style="color: #1565C0; font-size: 16px; margin: 0;">
                <strong>Primary Outcome:</strong> Foster social cohesion and eliminate isolation through training, dialogue, storytelling, and peer support.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Engagement Metrics
        st.markdown("### 🤝 Engagement & Connection Metrics")
        
        eng_col1, eng_col2, eng_col3, eng_col4 = st.columns(4)
        
        with eng_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL ENGAGED</p>'
                f'<p class="metric-value">13,119</p>'
                f'<p>Goal: 250,000</p>'
                f'<p>{status_badge("On Track")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with eng_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">ACTIVE VOLUNTEERS</p>'
                f'<p class="metric-value">3,348</p>'
                f'<p style="font-style: italic; font-size: 12px;">Hosted event this year</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with eng_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">DOCUMENTED CREW LEADERS</p>'
                f'<p class="metric-value">3,856</p>'
                f'<p style="font-style: italic; font-size: 12px;">Total crew leaders</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with eng_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">CREW LEADERS TRAINED</p>'
                f'<p class="metric-value">124</p>'
                f'<p style="font-style: italic; font-size: 12px;">Trained in 2025</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Training & Development
        st.markdown("### 🎓 Training & Leadership Development")
        
        train_col1, train_col2, train_col3 = st.columns(3)
        
        with train_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL TRAINED VOLUNTEERS</p>'
                f'<p class="metric-value">11,535</p>'
                f'<p style="font-style: italic; font-size: 12px;">All training programs</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with train_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">SPECIAL IMPACT PROGRAMS</p>'
                f'<p class="metric-value">100</p>'
                f'<p>Goal: 65,000</p>'
                f'<p>{status_badge("At Risk")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with train_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TRAINING WORKSHOPS</p>'
                f'<p class="metric-value">8</p>'
                f'<p style="font-style: italic; font-size: 12px;">8 more scheduled</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Impact Metrics
        st.markdown("### 💝 Social & Emotional Impact")
        
        impact_col1, impact_col2, impact_col3, impact_col4 = st.columns(4)
        
        with impact_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">MENTAL WELL-BEING</p>'
                f'<p class="metric-value">998</p>'
                f'<p style="font-style: italic; font-size: 12px;">99.90% improvement</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with impact_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">SOCIAL CONNECTION</p>'
                f'<p class="metric-value">673</p>'
                f'<p style="font-style: italic; font-size: 12px;">68.53% feel connected</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with impact_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">EMPOWERED TO ACT</p>'
                f'<p class="metric-value">907</p>'
                f'<p style="font-style: italic; font-size: 12px;">90.52% empowered</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with impact_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">SHARED WITH OTHERS</p>'
                f'<p class="metric-value">819</p>'
                f'<p style="font-style: italic; font-size: 12px;">83.66% sharing</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Knowledge Impact
        st.markdown("### 📚 Knowledge & Education Impact")
        
        # Knowledge impact chart with percentages
        fig_knowledge = px.bar(
            knowledge_data,
            x='Members',
            y='Topic',
            orientation='h',
            title='Self-Care School Knowledge Impact by Topic',
            color='Percentage',
            color_continuous_scale=['#E3F2FD', '#2196F3', '#1565C0'],
            text='Percentage'
        )
        fig_knowledge.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_knowledge.update_layout(height=400, title_font=dict(color=primary_blue))
        st.plotly_chart(fig_knowledge, use_container_width=True)
        
        # Special Impact Groups
        st.markdown("### 👥 Special Impact Groups")
        
        # Blue Brigade
        with st.expander("🧠 Blue Brigade - Mental Health Initiative", expanded=True):
            blue_col1, blue_col2, blue_col3, blue_col4 = st.columns(4)
            
            with blue_col1:
                st.metric("Fully Certified", "7/100", "7% complete")
            with blue_col2:
                st.metric("In Training", "50/100", "50% in pipeline")
            with blue_col3:
                st.metric("Wellness Walks", "4", "Monthly walks")
            with blue_col4:
                st.metric("Community Care Walks", "1", "Aug 23, Chicago")
            
            st.markdown(
                """
                **Training Schedule:**
                - Virtual: Aug 9, 17 | Sep 6, 26
                - In-person: Sep 13 (Montgomery, AL)
                
                **2026 Goal:** 1,000 MHFA Responders certified
                """
            )
        
        # Caregiver Tribe
        with st.expander("💜 Caregiver Tribe Program", expanded=True):
            care_col1, care_col2, care_col3, care_col4 = st.columns(4)
            
            with care_col1:
                st.metric("Caregivers Engaged", "649", "Total reached")
            with care_col2:
                st.metric("Workshops Complete", "2/4", "50% done")
            with care_col3:
                st.metric("Self-Care Assessments", "15", "Completed")
            with care_col4:
                st.metric("Resources Developed", "4+", "Materials created")
            
            st.markdown(
                """
                **Completed Workshops:**
                ✅ Medicaid for Caregivers (Apr 16)
                ✅ Mental Health First Aid (Jun 18)
                
                **Upcoming:**
                📅 Self-Care Practices (Aug 20)
                📅 Time Management & Nutrition (Oct 15)
                """
            )
        
        # Justice-Impacted
        with st.expander("⚖️ Justice-Impacted Women's Initiative", expanded=True):
            justice_col1, justice_col2, justice_col3 = st.columns(3)
            
            with justice_col1:
                st.metric("Walks Completed", "21/40", "52.5% complete")
            with justice_col2:
                st.metric("Active Locations", "2", "Atlanta + Virtual")
            with justice_col3:
                st.metric("Partner Facility", "Breakthru House", "Active")
            
            st.markdown(
                """
                **August 2025 Events:**
                - Connections & Conversations
                - Beyond the Bars Workshop
                - "I am walking for..." Walk
                """
            )
        
        # Garden Club
        with st.expander("🌱 Garden Club", expanded=True):
            st.markdown(
                """
                **Activities Completed:**
                - 2 seed mailings completed
                - Heirloom collard greens distribution
                - Seed saving education
                - Community seed distribution program
                
                **Impact:** Building food sovereignty knowledge and addressing food insecurity
                """
            )
        
        # Faith Initiative
        with st.expander("⛪ Faith Initiative", expanded=True):
            st.markdown(
                """
                **Progress:**
                - Multiple faith gatherings hosted
                - New faith communities recruited
                - On track for 500 faith communities engaged in 2025
                
                **Impact:** Building spiritual connections and community support through faith-based walking groups
                """
            )
        
        # Communication & Marketing
        st.markdown("### 📱 Communication & Storytelling")
        
        comm_col1, comm_col2, comm_col3, comm_col4 = st.columns(4)
        
        with comm_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">EMAIL SUBSCRIBERS</p>'
                f'<p class="metric-value">931,141</p>'
                f'<p>Goal: 1,300,000</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with comm_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">ACTIVE SUBSCRIBERS</p>'
                f'<p class="metric-value">320,463</p>'
                f'<p style="font-style: italic; font-size: 12px;">34.4% of total</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with comm_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">OPEN RATE</p>'
                f'<p class="metric-value">18.54%</p>'
                f'<p style="font-style: italic; font-size: 12px;">Industry: 28.59%</p>'
                f'{status_badge("At Risk")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with comm_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">CLICK RATE</p>'
                f'<p class="metric-value">1.06%</p>'
                f'<p style="font-style: italic; font-size: 12px;">Industry: 3.29%</p>'
                f'{status_badge("At Risk")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Email Performance Comparison
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
            title='Email Performance vs Industry Standards',
            yaxis_title='Percentage (%)',
            barmode='group',
            title_font=dict(color=primary_blue),
            height=350
        )
        st.plotly_chart(comparison_fig, use_container_width=True)
        
        # META Advertising
        st.markdown("### 📱 META Advertising Performance")
        
        meta_col1, meta_col2, meta_col3 = st.columns(3)
        
        with meta_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL AD SPEND</p>'
                f'<p class="metric-value">$11,180.19</p>'
                f'<p style="font-style: italic; font-size: 12px;">WNBA + Underground App</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with meta_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL IMPRESSIONS</p>'
                f'<p class="metric-value">858,890</p>'
                f'<p style="font-style: italic; font-size: 12px;">Combined reach</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with meta_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL CLICKS</p>'
                f'<p class="metric-value">5,060</p>'
                f'<p style="font-style: italic; font-size: 12px;">Combined clicks</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Campaign Details
        with st.expander("View Campaign Details"):
            st.markdown("**WNBA Campaign:**")
            st.info(f"Spend: $3,901.12 | CTR: 1.23% | CPC: $0.94 | Clicks: 1,986")
            
            st.markdown("**Underground App Campaign:**")
            st.info(f"Spend: $7,279.07 | CTR: 1.30% | CPC: $2.37 | Clicks: 3,074 | Leads: 281 | CPL: $25.90")
        
        # Member Testimonials
        st.markdown("### 💭 Member Voices")
        
        with st.expander("📖 Read Member Testimonials", expanded=True):
            st.markdown(
                """
                **Karen Laing - Finding Joy Through Community**
                > "I have found more joy and healing spaces during these weeks. GirlTrek's self-care school has been mission critical when I was fired and faced housing challenges."
                
                **Angelia Taylor - 106 Pound Transformation**
                > "Eating what the earth provides helped me lose 106 pounds! I taught plant-based meals to kids, complete with 'chocolate pudding' made from eggplant. You should have seen them lick the bowls. PRICELESS!!"
                
                **Alicia Cross - Perseverance Through Recovery**
                > "I've walked with GirlTrek since 2019, had knee replacement in 2024, but I'm taking one day at a time. Seven weeks of GirlTrek has been a lifesaver."
                """
            )
        
        # Member Care
        st.markdown("### 🤝 Member Care & Support")
        
        care_col1, care_col2 = st.columns(2)
        
        with care_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">MEMBER SATISFACTION</p>'
                f'<p class="metric-value">93%</p>'
                f'<p>Goal: 95%</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with care_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">RESPONSE TIME</p>'
                f'<p class="metric-value">2 hours</p>'
                f'<p>Goal: 48 hours</p>'
                f'{status_badge("Achieved")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        st.info(
            """
            **Top Member Issues:**
            - SCS Registration Error Message
            - Connecting to the Movement
            """
        )
    
    # ---------------------------------
    # SOLVE PROBLEMS Tab (Combat Injustice)
    # ---------------------------------
    with tab4:
        st.markdown('<h2 class="section-title">✊🏾 SOLVE PROBLEMS - Combating Injustice</h2>', unsafe_allow_html=True)
        
        st.markdown(
            """
            <div style="background-color: #FFF3E0; border-left: 5px solid #FF9800; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <p style="color: #E65100; font-size: 16px; margin: 0;">
                <strong>Primary Outcome:</strong> Combat injustice through collective impact, community projects, advocacy, and systems transformation.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Advocacy Metrics
        st.markdown("### 📢 Advocacy & Policy Impact")
        
        adv_col1, adv_col2, adv_col3, adv_col4 = st.columns(4)
        
        with adv_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">ADVOCACY BRIEFS</p>'
                f'<p class="metric-value">7/10</p>'
                f'<p style="font-style: italic; font-size: 12px;">Joy & Justice agenda</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with adv_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">ADVOCACY PARTNERS</p>'
                f'<p class="metric-value">0/3</p>'
                f'<p style="font-style: italic; font-size: 12px;">Partner activations</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with adv_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">LISTENING SESSIONS</p>'
                f'<p class="metric-value">0/5</p>'
                f'<p style="font-style: italic; font-size: 12px;">Key geographies</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with adv_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">CASE STUDIES</p>'
                f'<p class="metric-value">0/4</p>'
                f'<p style="font-style: italic; font-size: 12px;">Local impact stories</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Strategic Timeline Note
        st.warning(
            """
            **Timeline Adjustment:** Given c-suite conversations, external conditions, and internal priorities, we have been reevaluating the pacing of advocacy goals. 
            Timeline shifted to Q1 2026. Currently building relationships with 1K Women Strong and Health in Partnership (HiP).
            """
        )
        
        # Care Village Initiative
        st.markdown("### 🏘️ Care Village Initiative - Montgomery, AL")
        
        care_col1, care_col2 = st.columns(2)
        
        with care_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">CARE VILLAGE POPULATION</p>'
                f'<p class="metric-value">7,660</p>'
                f'<p style="font-style: italic; font-size: 12px;">Women reached in AL</p>'
                f'<p>Goal: 40,000 (19.15%)</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with care_col2:
            st.info(
                """
                **Care Village Components:**
                - Bricklayers Hall restoration
                - Mother Garden for food access
                - Community gathering spaces
                - Health and wellness programs
                - Place-based interventions
                """
            )
        
        # Development & Fundraising
        st.markdown("### 💰 Resource Development")
        
        dev_col1, dev_col2, dev_col3, dev_col4 = st.columns(4)
        
        with dev_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">TOTAL RAISED</p>'
                f'<p class="metric-value">{format_currency(st.session_state.total_contributions)}</p>'
                f'<p>Goal: $10M</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with dev_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">GRANT FUNDING</p>'
                f'<p class="metric-value">{format_currency(st.session_state.total_grants)}</p>'
                f'<p>17 of 48 grants</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with dev_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">CORPORATE SPONSORS</p>'
                f'<p class="metric-value">$130,000</p>'
                f'<p>Goal: $1.5M</p>'
                f'{status_badge("At Risk")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with dev_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">BRICKLAYERS</p>'
                f'<p class="metric-value">$2,500</p>'
                f'<p>Goal: $500K</p>'
                f'{status_badge("At Risk")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Grant Pipeline Table
        st.markdown("### 📋 2025 Grant Applications Pipeline")
        
        # Summary boxes
        grant_col1, grant_col2, grant_col3, grant_col4 = st.columns(4)
        
        with grant_col1:
            st.info("**Total Applications:** 22")
        with grant_col2:
            st.info("**Total Requested:** $8,519,750")
        with grant_col3:
            st.info("**Total Funded:** $14,500")
        with grant_col4:
            st.info("**Success Rate:** 18.2%")
        
        # Detailed grant table
        with st.expander("View Detailed Grant Pipeline"):
            # Create styled table
            grant_html = """
            <style>
            .grant-table { width: 100%; border-collapse: collapse; font-size: 12px; }
            .grant-table th { background-color: #4A90E2; color: white; padding: 8px; text-align: left; }
            .grant-table td { padding: 8px; border: 1px solid #ddd; }
            .status-pending { background-color: #E3F2FD; }
            .status-funded { background-color: #E8F5E8; }
            .status-declined { background-color: #FFEBEE; }
            .status-prepare { background-color: #FFF3E0; }
            </style>
            <table class="grant-table">
            <thead><tr>
            <th>Account</th><th>Grant Name</th><th>Amount Requested</th><th>Status</th>
            </tr></thead><tbody>
            """
            
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
                
                grant_html += f'<tr class="{status_class}">'
                grant_html += f'<td>{row["Account"]}</td>'
                grant_html += f'<td>{row["Grant Name"]}</td>'
                grant_html += f'<td>{row["Amount Requested"]}</td>'
                grant_html += f'<td><strong>{row["Status"]}</strong></td>'
                grant_html += '</tr>'
            
            grant_html += '</tbody></table>'
            st.markdown(grant_html, unsafe_allow_html=True)
        
        # Revenue Breakdown
        st.markdown("### 📊 Revenue Sources")
        
        revenue_fig = px.pie(
            df_finance,
            values='Amount',
            names='Category',
            title='Total Contributions Breakdown',
            color_discrete_sequence=[primary_blue, primary_orange]
        )
        revenue_fig.update_traces(textposition='inside', textinfo='percent+label')
        revenue_fig.update_layout(title_font=dict(color=primary_blue), height=350)
        st.plotly_chart(revenue_fig, use_container_width=True)
        
        # Earned Revenue
        st.markdown("### 🛍️ Earned Revenue & Store Performance")
        
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
        
        # Joy & Justice Agenda
        st.markdown("### ⚖️ Joy & Justice 10-Point Plan")
        
        with st.expander("View 10-Point Plan Details", expanded=True):
            # Create data for the 10-point plan
            joy_justice_data = pd.DataFrame({
                'Point': [
                    '1. Land rights & environmental justice',
                    '2. Healthy minds (Mental health)',
                    '3. Radical care & healing',
                    '4. Decarceration & restorative justice',
                    '5. Safety & public resources',
                    '6. Mental health & boundaries',
                    '7. Self-esteem & empowerment',
                    '8. Civic engagement',
                    '9. Parenting & mentorship',
                    '10. Community care models'
                ],
                'Members Engaged': [710, 998, 695, 658, 645, 622, 602, 569, 536, 7660],
                'Progress': ['71.60%', '99.90%', '67.34%', '63.76%', '64.40%', '60.27%', '58.33%', '57.00%', '51.94%', '19.15%']
            })
            
            for _, row in joy_justice_data.iterrows():
                st.markdown(f"**{row['Point']}**")
                col1, col2 = st.columns([3, 1])
                with col1:
                    progress_val = float(row['Progress'].strip('%'))
                    st.progress(progress_val / 100)
                with col2:
                    st.metric("", f"{row['Members Engaged']} ({row['Progress']})")
        
        # Collective Impact Flow
        st.markdown("### 🔄 From Individual Change to Collective Impact")
        
        impact_data = pd.DataFrame({
            'Stage': ['Health Knowledge', 'Behavior Change', 'Community Action', 'Policy Influence'],
            'Members Impacted': [999, 907, 819, 569],
            'Percentage': [99.9, 90.5, 83.7, 57.0]
        })
        
        fig_impact = px.funnel(
            impact_data,
            x='Members Impacted',
            y='Stage',
            title='Impact Progression: Individual → Systems Change',
            color='Percentage',
            color_continuous_scale=['#FFF3E0', '#FF9800', '#E65100']
        )
        fig_impact.update_layout(height=350, title_font=dict(color=primary_blue))
        st.plotly_chart(fig_impact, use_container_width=True)
        
        # Strategic Partnerships
        st.markdown("### 🤝 Strategic Partnerships & Coalitions")
        
        st.info(
            """
            **Active Partnership Development:**
            - **1K Women Strong** - Coalition building for collective impact
            - **Health in Partnership (HiP)** - Health equity collaboration
            - **Youth-serving organizations** - Next generation leadership (20 contacts made)
            - **Faith-based institutions** - North Star initiative (500 faith communities target)
            - **Civic organizations** - Including Zeta Phi Beta Sorority
            
            **Partnership Metrics:**
            - Total Recruitment Partnerships: 18 (Goal: 10) ✅
            - Advocacy Partnerships: 0 (Goal: 3) - In Development
            - Faith Communities: On track for 500 engaged
            - Care Village Coalition Partners: Building in Montgomery
            """
        )
        
        # Major Fundraising Event
        st.markdown("### 🎯 Major Fundraising Initiative")
        
        st.warning(
            """
            **October 10, 2025 - Exclusive Investment Opportunity**
            
            Invite-only event for Care Village model investment featuring:
            - Key co-hosts secured
            - Strategic partner: NationSwell
            - Focus: Mission-aligned investors and champions
            - Goal: Major gifts for Care Village expansion
            """
        )
    
    # ---------------------------------
    # Operational Excellence Tab
    # ---------------------------------
    with tab5:
        st.markdown('<h2 class="section-title">📊 Operational Excellence</h2>', unsafe_allow_html=True)
        
        st.markdown(
            """
            <div style="background-color: #F3F9FF; border-left: 5px solid #0088FF; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <p style="color: #0088FF; font-size: 16px; margin: 0;">
                <strong>Supporting Our Mission:</strong> Ensuring organizational health, financial sustainability, and operational efficiency to power our model of change.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Financial Performance
        st.markdown("### 💰 Financial Performance (YTD May 2025)")
        
        ytd_revenue = finance_trend_data['Revenue'].sum()
        ytd_expenses = finance_trend_data['Expenses'].sum()
        
        fin_col1, fin_col2, fin_col3, fin_col4 = st.columns(4)
        
        with fin_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">YTD REVENUE</p>'
                f'<p class="metric-value">{format_currency(ytd_revenue)}</p>'
                f'<p>Budget: $1,237,419</p>'
                f'{status_badge("Achieved")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with fin_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">YTD EXPENSES</p>'
                f'<p class="metric-value">{format_currency(ytd_expenses)}</p>'
                f'<p>Budget: $1,608,765</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with fin_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">NET SURPLUS</p>'
                f'<p class="metric-value">{format_currency(ytd_revenue - ytd_expenses)}</p>'
                f'<p style="font-style: italic; font-size: 12px;">YTD Net Income</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with fin_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">BUDGET VARIANCE</p>'
                f'<p class="metric-value">262%</p>'
                f'<p style="font-style: italic; font-size: 12px;">Revenue vs Budget</p>'
                f'{status_badge("Achieved")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Financial Trend Chart
        st.markdown("### 📈 Financial Trends")
        
        finance_fig = go.Figure()
        finance_fig.add_trace(go.Bar(
            name='Revenue',
            x=finance_trend_data['Month'],
            y=finance_trend_data['Revenue'],
            marker_color=primary_blue
        ))
        finance_fig.add_trace(go.Bar(
            name='Expenses',
            x=finance_trend_data['Month'],
            y=finance_trend_data['Expenses'],
            marker_color=secondary_orange
        ))
        finance_fig.update_layout(
            title='Monthly Revenue vs Expenses (YTD May 2025)',
            barmode='group',
            title_font=dict(color=primary_blue),
            height=350
        )
        st.plotly_chart(finance_fig, use_container_width=True)
        
        # People & Culture
        st.markdown("### 👥 People & Culture")
        
        people_col1, people_col2, people_col3, people_col4 = st.columns(4)
        
        with people_col1:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">STAFF RETENTION</p>'
                f'<p class="metric-value">94%</p>'
                f'<p>Industry: 86%</p>'
                f'{status_badge("Achieved")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with people_col2:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">SATISFACTION</p>'
                f'<p class="metric-value">88%</p>'
                f'<p>Target: 85%</p>'
                f'{status_badge("Achieved")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with people_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">BOARD DIVERSITY</p>'
                f'<p class="metric-value">73%/82%</p>'
                f'<p style="font-style: italic; font-size: 12px;">Black/Women</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with people_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">STAFF DIVERSITY</p>'
                f'<p class="metric-value">96%/100%</p>'
                f'<p style="font-style: italic; font-size: 12px;">Black/Women</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Systems & Technology
        st.markdown("### 💻 Systems & Technology")
        
        sys_col1, sys_col2, sys_col3, sys_col4 = st.columns(4)
        
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
                f'<p class="metric-title">CYBERSECURITY</p>'
                f'<p class="metric-value">70%</p>'
                f'<p>Goal: 90%</p>'
                f'{status_badge("On Track")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with sys_col3:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">AUDIT COMPLIANCE</p>'
                f'<p class="metric-value">100%</p>'
                f'<p>Goal: 100%</p>'
                f'{status_badge("Achieved")}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with sys_col4:
            st.markdown(
                f'<div class="metric-box">'
                f'<p class="metric-title">ORG HEALTH</p>'
                f'<p class="metric-value">TBD</p>'
                f'<p style="font-style: italic; font-size: 12px;">Survey Nov 2025</p>'
                f'<p>Goal: 85%</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Operational Priorities
        st.markdown("### 🎯 Operational Priorities")
        
        ops_col1, ops_col2 = st.columns(2)
        
        with ops_col1:
            st.success(
                """
                **✅ What's Working Well:**
                - **People First Wins:** 94% retention vs 86% industry avg
                - **Financial Strength:** $3.24M revenue vs $1.24M budget
                - **Member Care Excellence:** 2-hour response vs 48-hour goal
                - **Audit Perfection:** 100% compliance achieved
                - **Cybersecurity Progress:** 70% on path to 90% goal
                - **Employee Happiness:** 88% satisfaction vs 85% target
                """
            )
        
        with ops_col2:
            st.warning(
                """
                **⚠️ Areas Needing Focus:**
                - **Tech Adoption:** Asana at 38% vs 85% goal
                - **Store Operations:** $99.8K vs $400K goal (25%)
                - **Corporate Sponsorships:** $130K vs $1.5M goal (8.7%)
                - **Grant Success Rate:** 18.2% needs improvement
                - **Email Engagement:** Below industry standards
                - **Bricklayers Program:** $2.5K vs $500K goal
                """
            )
        
        # Summary Stats
        st.markdown("### 📊 Quick Summary Statistics")
        
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            st.info(
                """
                **Membership Stats:**
                - Total: 1,244,476
                - New (2025): 15,438
                - Walking Daily: 5,634
                - Life-Saving Level: 12,037
                """
            )
        
        with summary_col2:
            st.info(
                """
                **Financial Stats:**
                - Total Raised: $3.1M
                - Grants: $3.1M
                - Store: $99.8K
                - Corporate: $130K
                """
            )
        
        with summary_col3:
            st.info(
                """
                **Impact Stats:**
                - Mental Well-being: 99.9%
                - Social Connection: 68.5%
                - Empowered: 90.5%
                - Knowledge Gain: 61.1%
                """
            )

if __name__ == "__main__":
    main()
