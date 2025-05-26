import streamlit as st
import pandas as pd
import plotly.express as px

# Initialize session state
if 'section' not in st.session_state:
    st.session_state.section = 'Landing'
if 'df' not in st.session_state:
    st.session_state.df = None
if 'conclusion_shown' not in st.session_state:
    st.session_state.conclusion_shown = False

# Layout
st.set_page_config(page_title="Spotify Analytics Dashboard", page_icon=":musical_note:", layout="wide")

# Custom CSS for Styling
st.markdown("""
    <style>
    .header {
        color: #1DB954;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        padding: 20px;
    }
    .title-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 0;
    }
    .title {
        color: #1DB954;
        font-size: 3em;
        font-weight: bold;
        margin: 0 20px;
    }
    .logo {
        width: 50px;
        height: 50px;
    }
    .description {
        font-size: 1.2em;
        color: #555555;
        margin-bottom: 20px;
        text-align: left;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #121212;
        color: white;
        text-align: center;
        padding: 10px;
    }
    .full-page-container {
        text-align: center;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .custom-button {
        background-color: #1DB954;
        color: white;
        font-size: 1.2em;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .custom-button:hover {
        background-color: #1DB954;
    }
    </style>
    """, unsafe_allow_html=True)

# Title with Logo
st.markdown('''
<div class="title-container">
    <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" class="logo">
    <div class="title"><u>Spotify Analytics Dashboard</u></div>
</div>
''', unsafe_allow_html=True)

# Display content based on the selected section
if st.session_state.section == 'Landing':
    st.markdown("""
    <div class="description">
        <u>Discover Insights from Spotify Data</u>
        <br>
        Welcome to the Music Analytics Dashboard! This application provides you with a 
        comprehensive view of various music trends, listener statistics, and song popularity.

        Features Include:
        ‣ Key Performance Indicators (KPIs) for revenue, plays, and listeners
        ‣ Visualization of plays by song with bar charts
        ‣ Geographic distribution of listeners through choropleth maps
        ‣ Revenue insights by country with bar chart
        ‣ Analysis of plays and listeners with scatter plots
        ‣ Interactive exploration of top songs by listeners with treemaps
        ‣ Relationship between genres and top songs visualized with sunburst charts

        Get Started:
        Click the button below to dive into your analytics.
    </div>
    """, unsafe_allow_html=True)

    if st.button('Click here to dive into your analytics', key='start_button'):
        st.session_state.section = 'Upload'

elif st.session_state.section == 'Upload':
    st.markdown("""
    <div class="description">
        Upload your file and generate analytics

        Please upload your Spotify data file and then click 'Generate' to create the analytics charts.
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload your file", type=["csv", "xls", "json", "txt"])

    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)

        # Display the "Generate" button only if a file is uploaded
        if st.button('Generate'):
            st.session_state.section = 'Explore Now'
            st.session_state.conclusion_shown = False

elif st.session_state.section == 'Explore Now':
    # Add a back button to return to the Upload page
    if st.button("← ", key='back_to_upload', help='Go back to the upload page'):
        st.session_state.section = 'Upload'

    df = st.session_state.df

    # Check if 'Genre' column exists
    if 'Genre' in df.columns:
        genres = ["All"] + sorted(df['Genre'].dropna().unique())
        selected_genre = st.selectbox("Select Genre", genres)

        if selected_genre != "All":
            df = df[df['Genre'] == selected_genre]
    else:
        st.warning("The dataset does not contain a 'Genre' column. Please upload a dataset with a 'Genre' column to filter by genre.")

    # Key Performance Indicators (KPIs)
    col1, col2, col3 = st.columns(3)
    total_revenue = df['Revenue'].sum() if 'Revenue' in df.columns else 0
    total_plays = df['Plays'].sum() if 'Plays' in df.columns else 0
    total_listeners = df['Listeners'].sum() if 'Listeners' in df.columns else 0

    col1.metric("Revenue", f"${total_revenue:,.2f}", "Last 30 days")
    col2.metric("Plays", f"{total_plays:,}", "Last 30 days")
    col3.metric("Listeners", f"{total_listeners:,}", "Last 30 days")

    # Plays by Song
    if 'Top Songs' in df.columns and 'Plays by Song' in df.columns:
        st.markdown('<p class="description"></p>', unsafe_allow_html=True)
        fig_plays = px.bar(df, x='Top Songs', y='Plays by Song', title='Plays by Song')
        st.plotly_chart(fig_plays, use_container_width=True)
        st.markdown("""
        <div class="description">
            This bar chart illustrates the number of plays for each top song, highlighting the most popular tracks based on play count.
        </div>
        """, unsafe_allow_html=True)
        
    # Map of Revenue by Country
    if 'Country' in df.columns and 'Revenue' in df.columns:
        st.markdown('<p class="description"></p>', unsafe_allow_html=True)
        fig_map = px.choropleth(df,
                               locations="Country",
                               locationmode="country names",
                               color="Country",
                               hover_name="Revenue",
                               color_continuous_scale=px.colors.sequential.Plasma,
                               title="Revenue Distribution by Country")
        st.plotly_chart(fig_map, use_container_width=True)
        st.markdown("""
        <div class="description">
            This choropleth map visualizes the revenue distribution across countries, highlighting the regions with higher revenue contributions.
        </div>
        """, unsafe_allow_html=True)

    # Revenue by Country
    if 'Country' in df.columns and 'Revenue' in df.columns:
        st.markdown('<p class="description"></p>', unsafe_allow_html=True)
        fig_revenue_country = px.bar(df, x='Country', y='Revenue', title='Revenue by Country')
        st.plotly_chart(fig_revenue_country, use_container_width=True)
        st.markdown("""
        <div class="description">
            This bar chart shows the revenue generated from each country, providing insights into the financial contributions of different regions.
        </div>
        """, unsafe_allow_html=True)
        
    # Plays and Listeners Scatter Plot
    if 'Plays by Song' in df.columns and 'Listeners' in df.columns and 'Top Songs' in df.columns:
        st.markdown('<p class="description"></p>', unsafe_allow_html=True)
        fig_scatter = px.scatter(df, x='Plays by Song', y='Listeners', color='Top Songs',
                                 hover_name='Top Songs', title='Relationship between Plays and Listeners')
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown("""
        <div class="description">
            This scatter plot shows the relationship between the number of plays and listeners for each top song, revealing the correlation between these metrics.
        </div>
        """, unsafe_allow_html=True)

    # Revenue Over Time
    if 'Date' in df.columns and 'Revenue' in df.columns:
        st.markdown('<p class="description"></p>', unsafe_allow_html=True)
        fig_revenue_time = px.line(df, x='Date', y='Revenue', title='Revenue Over Time')
        st.plotly_chart(fig_revenue_time, use_container_width=True)
        st.markdown("""
        <div class="description">
            This line chart illustrates the trend of revenue over time, helping to identify peaks and troughs in earnings.
        </div>
        """, unsafe_allow_html=True)

    # Top Songs by Listeners
    if 'Top Songs' in df.columns and 'Listeners' in df.columns:
        st.markdown('<p class="description"></p>', unsafe_allow_html=True)
        fig_top_songs = px.treemap(df, path=['Top Songs'], values='Listeners', title='Top Songs by Listeners')
        st.plotly_chart(fig_top_songs, use_container_width=True)
        st.markdown("""
        <div class="description">
            This treemap visualizes the top songs by listeners, providing a clear view of the most popular tracks.
        </div>
        """, unsafe_allow_html=True)

    # Sunburst Chart for Genre and Top Songs
    if 'Genre' in df.columns and 'Top Songs' in df.columns:
        st.markdown('<p class="description"></p>', unsafe_allow_html=True)
        fig_sunburst = px.sunburst(df, path=['Genre', 'Top Songs'], values='Listeners', title='Genre and Top Songs')
        st.plotly_chart(fig_sunburst, use_container_width=True)
        st.markdown("""
        <div class="description">
            This sunburst chart visualizes the relationship between genres and top songs, highlighting the distribution of listeners across different genres and songs.
        </div>
        """, unsafe_allow_html=True)

    # Show Conclusion Button
    if st.button('Show Conclusion'):
        st.session_state.conclusion_shown = True

    # Display Conclusion
    if st.session_state.conclusion_shown:
        st.markdown('<p class="description"></p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="description">
            Based on the visualizations, here are the key insights:

            ‣ Revenue Distribution: The choropleth map and bar charts reveal the global distribution of revenue, highlighting regions with significant financial contributions
            
            ‣ Plays by Song: The bar chart for plays by song identifies which tracks are the most popular, showing the total number of plays each song has received.

            ‣ Correlation Analysis: The scatter plot demonstrates the relationship between the number of plays and the number of listeners, providing insights into how play counts correlate with listener numbers.

            ‣ Top Songs Insights: The treemap visualizes which songs have the highest listener counts, offering insights into the most popular tracks.

            ‣ Genre Analysis: The sunburst chart shows the distribution of listeners across different genres and top songs, providing a comprehensive view of genre popularity and song performance within each genre.

            These visualizations offer a deep dive into the dataset, enabling users to make informed decisions based on the trends and distributions observed.
        </div>
        """, unsafe_allow_html=True)

# Footer with Spotify link
st.markdown("""
    <div class="footer">
        <p>Powered by Spotify Data | <a href="https://www.spotify.com" target="_blank">Visit Spotify</a></p>
    </div>
""", unsafe_allow_html=True)