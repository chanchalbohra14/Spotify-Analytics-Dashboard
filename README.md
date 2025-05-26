# Spotify Analytics Dashboard

A Streamlit app that visualizes Spotify data with interactive charts and insightful metrics, showcasing listeners, revenue, plays, and more.

## Features

- Upload Spotify data (CSV, XLS, JSON, TXT)
- View key metrics: Revenue, Plays, Listeners
- Interactive visualizations including:
  - Bar charts for plays by song and revenue by country
  - Choropleth map showing revenue distribution geographically
  - Scatter plots showing relationship between plays and listeners
  - Treemaps for top songs by listeners
  - Sunburst charts exploring genre and song relationships
- Customized UI with Spotify-themed design
- Fully responsive layout

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly Express

## Installation

Clone the repository:

   ```bash
   git clone https://github.com/yourusername/spotify-analytics-dashboard.git
   cd spotify-analytics-dashboard

Run the app locally with:

bash
Copy
Edit
streamlit run dashboard.py

Make sure your repo includes a requirements.txt file with:
Copy
Edit
streamlit
pandas
plotly
