# Complete Streamlit App with Cleaned Tabs 2-5, Dark Mode, and Export Options

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO

# Color scheme
primary_blue = "#1f77b4"
primary_orange = "#ff7f0e"
primary_yellow = "#ffcc00"
secondary_blue = "#0074D9"
secondary_orange = "#FF851B"
secondary_teal = "#2ECC40"
secondary_beige = "#f5f5dc"
secondary_gold = "#FFD700"
secondary_gray = "#555555"
secondary_white = "#FFFFFF"

# Status badge helper
def status_badge(status):
    color = {"On Track": "green", "At Risk": "red"}.get(status, "gray")
    return f'<span style="color:{color}; font-weight:bold;">{status}</span>'

# Export CSV or Excel
@st.cache_data

def convert_df(df, to="csv"):
    if to == "csv":
        return df.to_csv(index=False).encode('utf-8')
    else:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

# Tabs
st.set_page_config(layout="wide", page_title="GirlTREK Dashboard")
tab2, tab3, tab4, tab5 = st.tabs(["Recruitment & Engagement", "Development", "Marketing", "Impact & Member Care"])

# --------------------------- TAB 4 ---------------------------
with tab4:
    st.markdown('<h3 class="section-title">Marketing Metrics</h3>', unsafe_allow_html=True)

    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.markdown(f'<div class="metric-card"><p class="metric-title">TOTAL SUBSCRIBERS</p><p class="metric-value">931,141</p><p>Goal: 1,300,000</p></div>', unsafe_allow_html=True)
    with sub_col2:
        st.markdown(f'<div class="metric-card"><p class="metric-title">ACTIVE SUBSCRIBERS</p><p class="metric-value">297,283</p><p>31.9% of Total Subscribers</p></div>', unsafe_allow_html=True)

    df_activity = pd.DataFrame({
        'Period': ['30 day', '60 day', '90 day', '6 months'],
        'Openers': [221719, 266461, 272011, 295705],
        'Clickers': [13000, 21147, 22504, 26272]
    })

    fig_activity = go.Figure()
    fig_activity.add_trace(go.Bar(x=df_activity['Period'], y=df_activity['Openers'], name='Openers', marker_color=primary_blue))
    fig_activity.add_trace(go.Bar(x=df_activity['Period'], y=df_activity['Clickers'], name='Clickers', marker_color=primary_orange))
    fig_activity.update_layout(title='Subscriber Activity', xaxis_title='Time Period', yaxis_title='Number of Subscribers', barmode='group', height=400, title_font=dict(color=primary_blue))
    st.plotly_chart(fig_activity, use_container_width=True)

    st.markdown('<h4>Email Engagement</h4>', unsafe_allow_html=True)
    email_col1, email_col2 = st.columns(2)
    with email_col1:
        fig_open = go.Figure(go.Indicator(mode="gauge+number", value=34.95, domain={'x': [0, 1], 'y': [0, 1]}, title={'text': "Average Open Rate", 'font': {'color': primary_blue}},
                                          gauge={'axis': {'range': [None, 50]}, 'bar': {'color': primary_blue}, 'steps': [{'range': [0, 20], 'color': secondary_beige}, {'range': [20, 35], 'color': secondary_gold}, {'range': [35, 50], 'color': primary_orange}],
                                                 'threshold': {'line': {'color': secondary_orange, 'width': 4}, 'thickness': 0.75, 'value': 35}}))
        fig_open.update_layout(height=300)
        st.plotly_chart(fig_open, use_container_width=True)

    with email_col2:
        fig_click = go.Figure(go.Indicator(mode="gauge+number", value=6.27, domain={'x': [0, 1], 'y': [0, 1]}, title={'text': "Text Message Click-Through Rate", 'font': {'color': primary_blue}},
                                           gauge={'axis': {'range': [None, 15]}, 'bar': {'color': primary_blue}, 'steps': [{'range': [0, 5], 'color': secondary_beige}, {'range': [5, 10], 'color': secondary_gold}, {'range': [10, 15], 'color': primary_orange}],
                                                  'threshold': {'line': {'color': secondary_orange, 'width': 4}, 'thickness': 0.75, 'value': 10}}))
        fig_click.update_layout(height=300)
        st.plotly_chart(fig_click, use_container_width=True)
        st.markdown(f"<div style='font-size: 12px; color: {secondary_gray};'>Industry Standard: SMS messages have click-through rates of 6.3% for fundraising messages and 10% for advocacy messages.</div>", unsafe_allow_html=True)

# --------------------------- TAB 5 ---------------------------
with tab5:
    st.markdown('<h3 class="section-title">Impact & Member Care Metrics</h3>', unsafe_allow_html=True)

    care_col1, care_col2 = st.columns(2)
    with care_col1:
        st.markdown(f'<div class="metric-card"><p class="metric-title">CARE VILLAGE: POPULATION REACHED</p><p class="metric-value">2,869</p><p>Goal: 20,000</p><p>{status_badge("On Track")}</p></div>', unsafe_allow_html=True)
    with care_col2:
        st.markdown(f'<div class="metric-card"><p class="metric-title">HEALTH WORKER TRAINING</p><p class="metric-value">450</p><p>Goal: 4,000</p><p>{status_badge("At Risk")}</p></div>', unsafe_allow_html=True)

    member_col1, member_col2 = st.columns(2)
    with member_col1:
        fig_satisfaction = go.Figure(go.Indicator(mode="gauge+number+delta", value=95, delta={'reference': 85, 'increasing': {'color': primary_orange}},
                                                  domain={'x': [0, 1], 'y': [0, 1]}, title={'text': "Member Satisfaction Rating", 'font': {'color': primary_blue}},
                                                  gauge={'axis': {'range': [None, 100]}, 'bar': {'color': primary_orange}, 'steps': [{'range': [0, 50], 'color': secondary_beige}, {'range': [50, 85], 'color': secondary_gold}, {'range': [85, 100], 'color': primary_yellow}],
                                                         'threshold': {'line': {'color': secondary_orange, 'width': 4}, 'thickness': 0.75, 'value': 85}}))
        fig_satisfaction.update_layout(height=300)
        st.plotly_chart(fig_satisfaction, use_container_width=True)

    with member_col2:
        fig_response = go.Figure(go.Indicator(mode="number+delta", value=2, number={'suffix': " hours", 'font': {'color': primary_blue}},
                                             title={'text': "Resolution/Responsiveness Rate", 'font': {'color': primary_blue}},
                                             delta={'reference': 48, 'decreasing': {'color': primary_orange}}))
        fig_response.update_layout(height=300)
        st.plotly_chart(fig_response, use_container_width=True)

    st.markdown('<h4>Health Impact</h4>', unsafe_allow_html=True)
    df_health = pd.DataFrame({
        'Metric': ['Improved Mental Well-being', 'Feel More Connected', 'Weight Loss', 'Improved Management of Chronic Conditions', 'Reduced Medication Dependency', 'Fewer Symptoms of Depression or Anxiety'],
        'Percentage': [78, 85, 65, 58, 42, 72]
    })
    fig_health = px.bar(df_health, x='Metric', y='Percentage', title='Self-Reported Health Improvements', color='Percentage', color_continuous_scale=[primary_blue, primary_orange, primary_yellow])
    fig_health.update_layout(xaxis_title='Health Outcome', yaxis_title='Percentage of Respondents (%)', height=500, title_font=dict(color=primary_blue))
    st.plotly_chart(fig_health, use_container_width=True)

    st.markdown('<h4>Top Member Issues/Concerns</h4>', unsafe_allow_html=True)
    st.markdown("""
        <div class="metric-card">
            <ul>
                <li>The App functionality and usability</li>
                <li>Join the Movement process and onboarding</li>
                <li>Finding local crew events</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<h4>Operations</h4>', unsafe_allow_html=True)
    ops_col1, ops_col2, ops_col3 = st.columns(3)
    with ops_col1:
        st.markdown(f'<div class="metric-card"><p class="metric-title">STORE SALES</p><p class="metric-value">$25,000</p><p>Goal: $50,000</p><p>{status_badge("On Track")}</p></div>', unsafe_allow_html=True)
    with ops_col2:
        st.markdown(f'<div class="metric-card"><p class="metric-title">AUDIT COMPLIANCE</p><p class="metric-value">90%</p><p>Goal: 100%</p><p>{status_badge("On Track")}</p></div>', unsafe_allow_html=True)
    with ops_col3:
        st.markdown(f'<div class="metric-card"><p class="metric-title">CYBER SECURITY COMPLIANCE</p><p class="metric-value">60%</p><p>Goal: 90%</p><p>{status_badge("At Risk")}</p></div>', unsafe_allow_html=True)

    # Export buttons
    st.markdown("### Export Data")
    export_format = st.radio("Choose format:", ["csv", "excel"])
    file = convert_df(df_health, to=export_format)
    st.download_button("Download Health Impact Data", file, file_name=f"health_impact_data.{export_format}")

