with tab2:
    st.markdown('<h3 class="section-title">Recruitment & Engagement Metrics</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # New members by month
        month_data = {
            'Month': ['January', 'February', 'March', 'April'],
            'New Members': [591, 1574, 4382, 4809]
        }
        df_months = pd.DataFrame(month_data)
        
        fig_months = px.line(df_months, x='Month', y='New Members', 
                          title='New Members by Month',
                          markers=True)
        fig_months.update_traces(
            line=dict(color=primary_blue, width=3),
            marker=dict(color=primary_orange, size=10)
        )
        fig_months.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(fig_months, use_container_width=True)
    
    with col2:
        # New members by age
        new_age_data = {
            'Age Group': ['18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+', 'Unknown'],
            'New Members': [86, 477, 1771, 2163, 1898, 4961]
        }
        df_new_age = pd.DataFrame(new_age_data)
        
        fig_new_age = px.pie(df_new_age, values='New Members', names='Age Group', 
                         title='New Members by Age Group',
                         color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, 
                                                secondary_blue, secondary_orange, secondary_teal])
        fig_new_age.update_traces(textposition='inside', textinfo='percent+label')
        fig_new_age.update_layout(title_font=dict(color=primary_blue))
        st.plotly_chart(fig_new_age, use_container_width=True)
    
    # Engagement metrics
    st.markdown('<h4>Engagement Stats</h4>', unsafe_allow_html=True)
    
    engagement_col1, engagement_col2, engagement_col3 = st.columns(3)
    
    with engagement_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">ACTIVE VOLUNTEERS</p>'
            f'<p class="metric-value">3,348</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with engagement_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">DOCUMENTED CREW LEADERS</p>'
            f'<p class="metric-value">3,732</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with engagement_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">ACTIVE CREW LEADERS</p>'
            f'<p class="metric-value">1,846</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Campaign metrics
    st.markdown('<h4>Current Campaign: Self-Care Schools</h4>', unsafe_allow_html=True)
    
    campaign_col1, campaign_col2 = st.columns(2)
    
    with campaign_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL REGISTRANTS</p>'
            f'<p class="metric-value">7,500</p>'
            f'<p>Goal: 10,000</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with campaign_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL DOWNLOADS</p>'
            f'<p class="metric-value">32,000</p>'
            f'<p>Goal: 50,000</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Badges claimed
    badges_data = {
        'Week': ['Week 0', 'Week 1', 'Week 2'],
        'Badges Claimed': [3000, 2000, 1500]
    }
    df_badges = pd.DataFrame(badges_data)
    
    fig_badges = px.bar(df_badges, x='Week', y='Badges Claimed', 
                      title='Badges Claimed by Week',
                      color='Badges Claimed',
                      color_continuous_scale=[primary_yellow, primary_orange, secondary_orange])
    fig_badges.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(fig_badges, use_container_width=True)

with tab3:
    st.markdown('<h3 class="section-title">Development Metrics</h3>', unsafe_allow_html=True)
    
    # Financial summary
    financial_col1, financial_col2, financial_col3 = st.columns(3)
    
    with financial_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL DONATIONS</p>'
            f'<p class="metric-value">$1,094,048.68</p>'
            f'<p>Goal: $8,000,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with financial_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL REVENUE</p>'
            f'<p class="metric-value">$1,500,000</p>'
            f'<p>Goal: $400,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with financial_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">TOTAL EXPENSES</p>'
            f'<p class="metric-value">$1,200,000</p>'
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
            f'<p class="metric-value">$600,000</p>'
            f'<p>Goal: $1,000,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with grants_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">CORPORATE SPONSORSHIPS</p>'
            f'<p class="metric-value">$750,000</p>'
            f'<p>Goal: $1,500,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Financial breakdown chart
    finance_data = {
        'Category': ['Donations', 'Grants', 'Corporate Sponsorships', 'Store Sales', 'Other Revenue'],
        'Amount': [1094048.68, 600000, 750000, 25000, 125000]
    }
    df_finance = pd.DataFrame(finance_data)
    
    fig_finance = px.pie(df_finance, values='Amount', names='Category', 
                       title='Revenue Breakdown',
                       color_discrete_sequence=[primary_blue, primary_orange, primary_yellow, 
                                              secondary_blue, secondary_orange])
    fig_finance.update_traces(textposition='inside', textinfo='percent+label')
    fig_finance.update_layout(title_font=dict(color=primary_blue))
    st.plotly_chart(fig_finance, use_container_width=True)
    
    # Dummy data for financial trends
    months = ['January', 'February', 'March', 'April']
    revenue = [250000, 310000, 450000, 490000]
    expenses = [220000, 280000, 350000, 350000]
    donations = [180000, 240000, 300000, 374048.68]
    
    finance_trend_data = pd.DataFrame({
        'Month': months,
        'Revenue': revenue,
        'Expenses': expenses,
        'Donations': donations
    })
    
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

with tab4:
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
    activity_data = {
        'Period': ['30 day', '60 day', '90 day', '6 months'],
        'Openers': [221719, 266461, 272011, 295705],
        'Clickers': [13000, 21147, 22504, 26272]
    }
    df_activity = pd.DataFrame(activity_data)
    
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
    st.markdown('<h4>Email Engagement</h4>', unsafe_allow_html=True)
    
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

with tab5:
    st.markdown('<h3 class="section-title">Impact & Member Care Metrics</h3>', unsafe_allow_html=True)
    
    # Care Village metrics
    care_col1, care_col2 = st.columns(2)
    
    with care_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">CARE VILLAGE: POPULATION REACHED</p>'
            f'<p class="metric-value">2,869</p>'
            f'<p>Goal: 20,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with care_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">HEALTH WORKER TRAINING</p>'
            f'<p class="metric-value">450</p>'
            f'<p>Goal: 4,000</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # Member satisfaction metrics
    member_col1, member_col2 = st.columns(2)
    
    with member_col1:
        fig_satisfaction = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=95,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Member Satisfaction Rating", 'font': {'color': primary_blue}},
            delta={'reference': 85, 'increasing': {'color': primary_orange}},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': primary_orange},
                'steps': [
                    {'range': [0, 50], 'color': secondary_beige},
                    {'range': [50, 85], 'color': secondary_gold},
                    {'range': [85, 100], 'color': primary_yellow}
                ],
                'threshold': {
                    'line': {'color': secondary_orange, 'width': 4},
                    'thickness': 0.75,
                    'value': 85
                }
            }
        ))
        
        fig_satisfaction.update_layout(height=300)
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    with member_col2:
        fig_response = go.Figure(go.Indicator(
            mode="number+delta",
            value=2,
            number={'suffix': " hours", 'font': {'color': primary_blue}},
            title={'text': "Resolution/Responsiveness Rate", 'font': {'color': primary_blue}},
            delta={'reference': 48, 'decreasing': {'color': primary_orange}}
        ))
        
        fig_response.update_layout(height=300)
        st.plotly_chart(fig_response, use_container_width=True)
    
    # Health impact metrics (dummy data)
    st.markdown('<h4>Health Impact</h4>', unsafe_allow_html=True)
    
    health_data = {
        'Metric': [
            'Improved Mental Well-being', 
            'Feel More Connected', 
            'Weight Loss', 
            'Improved Management of Chronic Conditions',
            'Reduced Medication Dependency',
            'Fewer Symptoms of Depression or Anxiety'
        ],
        'Percentage': [78, 85, 65, 58, 42, 72]
    }
    df_health = pd.DataFrame(health_data)
    
    fig_health = px.bar(df_health, x='Metric', y='Percentage',
                     title='Self-Reported Health Improvements',
                     color='Percentage',
                     color_continuous_scale=[primary_blue, primary_orange, primary_yellow])
    
    fig_health.update_layout(
        xaxis_title='Health Outcome',
        yaxis_title='Percentage of Respondents (%)',
        height=500,
        title_font=dict(color=primary_blue)
    )
    
    st.plotly_chart(fig_health, use_container_width=True)
    
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
    
    # Operations metrics
    st.markdown('<h4>Operations</h4>', unsafe_allow_html=True)
    
    ops_col1, ops_col2, ops_col3 = st.columns(3)
    
    with ops_col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">STORE SALES</p>'
            f'<p class="metric-value">$25,000</p>'
            f'<p>Goal: $50,000</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with ops_col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">AUDIT COMPLIANCE</p>'
            f'<p class="metric-value">90%</p>'
            f'<p>Goal: 100%</p>'
            f'<p>{status_badge("On Track")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    with ops_col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="metric-title">CYBER SECURITY COMPLIANCE</p>'
            f'<p class="metric-value">60%</p>'
            f'<p>Goal: 90%</p>'
            f'<p>{status_badge("At Risk")}</p>'
            f'</div>', 
            unsafe_allow_html=True
        )

# Sidebar for filters
st.sidebar.markdown("# Filters")
st.sidebar.markdown("### Date Range")
start_date = st.sidebar.date_input("Start Date", datetime(2025, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime(2025, 4, 25))

st.sidebar.markdown("### Regions")
regions = ['All', 'Northeast', 'Southeast', 'Midwest', 'Southwest', 'West']
selected_region = st.sidebar.selectbox("Select Region", regions)

st.sidebar.markdown("### Age Groups")
age_groups = ['All', '18 to 24', '25 to 34', '35 to 49', '50 to 64', '65+']
selected_age = st.sidebar.multiselect("Select Age Groups", age_groups, default='All')

st.sidebar.markdown("### Dashboard Settings")
show_target_lines = st.sidebar.checkbox("Show Target Lines", value=True)
dark_mode = st.sidebar.checkbox("Dark Mode", value=False)

# Footer
st.markdown(
    f"""
    <div style="margin-top: 50px; padding: 20px; background-color: {secondary_beige}; border-radius: 10px; text-align: center;">
        <h3 style="color: {primary_blue};">GirlTREK - Inspiring Black Women to Walk for Better Health</h3>
        <p>Data last updated: April 25, 2025</p>
        <p>For more information, visit <a href="https://www.girltrek.org" target="_blank" style="color: {primary_blue};">girltrek.org</a></p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Add documentation for how to deploy this dashboard to GitHub
st.sidebar.markdown("---")
st.sidebar.markdown("### Deployment Instructions")
with st.sidebar.expander("How to deploy this dashboard on GitHub"):
    st.markdown(
        f"""
        ### Deploying to GitHub
        
        1. Create a new GitHub repository
        2. Add the following files to your repository:
            - `app.py` (this Streamlit app)
            - `requirements.txt` (with dependencies: streamlit, pandas, plotly)
            - `README.md` (basic documentation)
        3. Connect your repository to Streamlit Cloud:
            - Go to [Streamlit Cloud](https://streamlit.io/cloud)
            - Sign in with your GitHub account
            - Click "New app"
            - Select your repository, branch, and main file path
            - Click "Deploy"
        
        Your dashboard will be available at a public URL provided by Streamlit Cloud.
        """
    )

# Add GitHub repo structure
with st.sidebar.expander("GitHub Repository Structure"):
    st.code("""
├── app.py             # Main Streamlit application (this code)
├── requirements.txt   # Dependencies
│   ├── streamlit>=1.10.0
│   ├── pandas>=1.3.0
│   ├── plotly>=5.5.0
├── .streamlit/        # Configuration folder
│   ├── config.toml    # Streamlit configuration
├── README.md          # Documentation
├── LICENSE            # License information
    """)

# Sample requirements.txt
with st.sidebar.expander("Sample requirements.txt"):
    st.code("""
streamlit>=1.10.0
pandas>=1.3.0
plotly>=5.5.0
    """)

# Sample config.toml with GirlTREK colors
with st.sidebar.expander("Sample .streamlit/config.toml"):
    st.code(
        f"""
        [theme]
        primaryColor = "{primary_orange}"
        backgroundColor = "{secondary_white}"
        secondaryBackgroundColor = "{secondary_beige}"
        textColor = "{secondary_gray}"
        font = "sans serif"
        """
    )
