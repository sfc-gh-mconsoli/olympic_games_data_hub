import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, count, sum, avg
import pandas as pd


def get_snowflake_connection():
    return get_active_session()

# Initialize Snowflake connection
st.session_state.snowflake_connection = get_snowflake_connection()

# Function to run Snowflake queries
@st.cache_data
def run_query(query):
    try:
        conn = st.session_state.snowflake_connection
        return conn.sql(query).to_pandas()  # Fetch data and convert to Pandas DataFrame for Plotly
    except Exception as e:
        st.error(f"Error running query: {e}")
        return pd.DataFrame()

# Function to plot bar chart
def plot_bar_chart(df, x_col, y_col, title, labels):
    fig = px.bar(df, x=x_col, y=y_col, title=title, labels=labels)
    st.plotly_chart(fig)

# Function to plot line chart
def plot_line_chart(df, x_col, y_col, title, labels):
    fig = px.line(df, x=x_col, y=y_col, title=title, labels=labels)
    st.plotly_chart(fig)

# Function to plot pie chart
def plot_pie_chart(df, names_col, values_col, title, labels):
    fig = px.pie(df, names=names_col, values=values_col, title=title, labels=labels)
    st.plotly_chart(fig)

# Sidebar for selecting analysis
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg')
st.sidebar.title('Olympic Games Data Hub')
analysis = st.sidebar.selectbox('Select Analysis', [
    'App Info',
    'Gold Medal Comparison by Country',
    'Performance Trends by Country',
    'Olympic Medals Distribution Over Time',
    'Top Athletes by Medals',
    'Event Participation Analysis'
])

if analysis == 'App Info':
    st.title('Olympic Games Data Hub - Overview')
    st.image('https://upload.wikimedia.org/wikipedia/commons/b/b6/1896_Olympic_opening_ceremony.jpg')
    
    st.write('Welcome to the **Olympic Games Data Hub**! This application provides a comprehensive analysis of Olympic data, offering insights into medal distribution, athlete performance, and more. Explore various analyses to dive deep into the world of the Olympics.')

    st.write('### Available Analyses')
    
    st.write("""
    - **Gold Medal Comparison by Country**: Compare the gold medal counts across different countries and editions. Visualize the performance of selected countries in a grouped bar chart.

    - **Performance Trends by Country**: Analyze the performance trends of the selected country over the years, separate lines for summer and winter editions.

    - **Olympic Medals Distribution Over Time**: View the distribution of gold, silver, and bronze medals over the history of Olympic Games. Track the trends in medal counts through interactive line charts.

    - **Top Athletes by Medals**: Discover the top athletes based on their medal counts. This section highlights the athletes with the most medals across different events.

    - **Event Participation Analysis**: Examine the number of athletes competing in the Olympic Games history. Get insights into the participation patterns of Olympic athletes.
   """)
    
    st.write('### Dataset Summary')
    tables = ['OLYMPICS_COUNTRY', 'OLYMPIC_GAMES', 'OLYMPIC_ATHLETE_BIO', 'OLYMPIC_ATHLETE_EVENT_RESULTS', 'OLYMPIC_RESULTS', 'OLYMPIC_GAMES_MEDAL_TALLY']
    for table in tables:
        df = st.session_state.snowflake_connection.table(table).to_pandas()
        st.write(f"- **{table}**: (Rows: {len(df)} - Columns: {len(df.columns)})")
    
    st.write('### Credits')
    st.write('This application was developed by Matteo Consoli. Logo and photos used in the landing page are hosted on Wikimedia')
    st.write('All content and visuals provided are for educational and informational purposes. Please adhere to copyright and usage guidelines when sharing or using the data and images.')
    st.write('Dataset provided under a public license from Kaggle: [Olympic Historical Dataset](https://www.kaggle.com/datasets/josephcheng123456/olympic-historical-dataset-from-olympediaorg). Data was webscraped from Olymedia.org.')

    st.write('Thank you for exploring the Olympic Games Data Hub!')

elif analysis == 'Olympic Medals Distribution Over Time':
    st.title('Medal Distribution Over Time')
    
    # Load the data
    query = """
    SELECT YEAR, SUM(GOLD) AS total_gold, SUM(SILVER) AS total_silver, SUM(BRONZE) AS total_bronze
    FROM OLYMPIC_GAMES_MEDAL_TALLY
    WHERE EDITION like '%Summer%'
    GROUP BY YEAR
    ORDER BY YEAR
    """
    df = run_query(query)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['YEAR'], y=df['TOTAL_GOLD'], mode='lines+markers', name='Gold Medals'))
    fig.add_trace(go.Scatter(x=df['YEAR'], y=df['TOTAL_SILVER'], mode='lines+markers', name='Silver Medals'))
    fig.add_trace(go.Scatter(x=df['YEAR'], y=df['TOTAL_BRONZE'], mode='lines+markers', name='Bronze Medals'))
        
    fig.update_layout(title='Summer Olympics', xaxis_title='Year', yaxis_title='Number of Medals')
    st.plotly_chart(fig)
    
    # Load the data
    query = """
    SELECT YEAR, SUM(GOLD) AS total_gold, SUM(SILVER) AS total_silver, SUM(BRONZE) AS total_bronze
    FROM OLYMPIC_GAMES_MEDAL_TALLY
    WHERE EDITION like '%Winter%'
    GROUP BY YEAR
    ORDER BY YEAR
    """
    df = run_query(query)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['YEAR'], y=df['TOTAL_GOLD'], mode='lines+markers', name='Gold Medals'))
    fig.add_trace(go.Scatter(x=df['YEAR'], y=df['TOTAL_SILVER'], mode='lines+markers', name='Silver Medals'))
    fig.add_trace(go.Scatter(x=df['YEAR'], y=df['TOTAL_BRONZE'], mode='lines+markers', name='Bronze Medals'))
        
    fig.update_layout(title='Winter Olympics', xaxis_title='Year', yaxis_title='Number of Medals')
    st.plotly_chart(fig)


elif analysis == 'Top Athletes by Medals':
    st.title('Top Athletes by Medals')
    
    # Load the data
    query = """
    SELECT ATHLETE, COUNT(MEDAL) AS medal_count
    FROM OLYMPIC_ATHLETE_EVENT_RESULTS
    GROUP BY ATHLETE
    ORDER BY medal_count DESC
    LIMIT 10
    """
    df = run_query(query)
    
    # Plot
    plot_bar_chart(df, 'ATHLETE', 'MEDAL_COUNT', 'Top 10 Athletes by Number of Medals', {'ATHLETE': 'Athlete', 'medal_count': 'Number of Medals'})

 # Add a selectbox for athlete details
    selected_athlete = st.selectbox('Select an Athlete to View Details', df['ATHLETE'])
    
    if selected_athlete:
        # Query to get details of selected athlete
        query_details = f"""
        SELECT EDITION, SPORT, EVENT, MEDAL
        FROM OLYMPIC_ATHLETE_EVENT_RESULTS
        WHERE ATHLETE = '{selected_athlete}'
        """
        df_details = run_query(query_details)
        
        # Display athlete details
        st.write(f"### Details of {selected_athlete}")
        st.write(df_details)
elif analysis == 'Event Participation Analysis':
    st.title('Event Participation Analysis')
    
    # Load the data
    query = """
    SELECT EDITION, COUNT(DISTINCT ATHLETE_ID) AS NUM_PARTICIPANTS
    FROM OLYMPIC_ATHLETE_EVENT_RESULTS
    WHERE EDITION like '%Summer%'
    GROUP BY EDITION
    ORDER BY EDITION DESC
    """
    df = run_query(query)
    
    # Plot
    plot_bar_chart(df, 'EDITION', 'NUM_PARTICIPANTS', 'Number of Participants per Summer Event', {'EVENT': 'Event', 'num_participants': 'Number of Participants'})

    # Load the data
    query = """
    SELECT EDITION, COUNT(DISTINCT ATHLETE_ID) AS NUM_PARTICIPANTS
    FROM OLYMPIC_ATHLETE_EVENT_RESULTS
    WHERE EDITION like '%Winter%'
    GROUP BY EDITION
    ORDER BY EDITION DESC
    """
    df = run_query(query)
    
    # Plot
    plot_bar_chart(df, 'EDITION', 'NUM_PARTICIPANTS', 'Number of Participants per Winter Event', {'EVENT': 'Event', 'num_participants': 'Number of Participants'})

elif analysis == 'Performance Trends by Country':
    st.title('Performance Trends by Country')
    
    # Load the data
    query = """
    SELECT YEAR, CASE WHEN EDITION LIKE '%Summer%' THEN 'Summer' ELSE 'Winter' END as EDITION_TYPE, COUNTRY, SUM(GOLD) AS GOLD_MEDALS
    FROM OLYMPIC_GAMES_MEDAL_TALLY
    GROUP BY YEAR, COUNTRY, EDITION_TYPE
    ORDER BY YEAR, GOLD_MEDALS DESC
    """
    df = run_query(query)
    
    # User input for country selection
    country = st.selectbox('Select Country', df['COUNTRY'].unique())
    
    # Filter data for selected country
    country_df = df[df['COUNTRY'] == country]
    
    # Plot
    fig = go.Figure()
    
    # Plot Summer data
    summer_df = country_df[country_df['EDITION_TYPE'] == 'Summer']
    fig.add_trace(go.Scatter(x=summer_df['YEAR'], y=summer_df['GOLD_MEDALS'], mode='lines+markers', name='Summer Olympics'))
    
    # Plot Winter data
    winter_df = country_df[country_df['EDITION_TYPE'] == 'Winter']
    fig.add_trace(go.Scatter(x=winter_df['YEAR'], y=winter_df['GOLD_MEDALS'], mode='lines+markers', name='Winter Olympics'))
    
    fig.update_layout(
        title=f'Performance Trend of {country}',
        xaxis_title='Year',
        yaxis_title='Gold Medals',
        legend_title='Edition Type'
    )
    
    st.plotly_chart(fig)

elif analysis == 'Gold Medal Comparison by Country':
    st.title('Gold Medal Comparison by Country')
    
    # Load the data
    query = """
    SELECT OLYMPIC_GAMES.EDITION AS EDITION, OLYMPIC_GAMES_MEDAL_TALLY.COUNTRY, SUM(GOLD) AS TOTAL_GOLD
    FROM OLYMPIC_GAMES
    JOIN OLYMPIC_GAMES_MEDAL_TALLY ON OLYMPIC_GAMES.EDITION_ID = OLYMPIC_GAMES_MEDAL_TALLY.EDITION_ID
    GROUP BY OLYMPIC_GAMES.EDITION, OLYMPIC_GAMES_MEDAL_TALLY.COUNTRY
    ORDER BY TOTAL_GOLD DESC
    """
    df = run_query(query)
    
    # Multi-select for editions
    editions = st.multiselect('Select Editions', options=df['EDITION'].unique())
    if editions:
        filtered_df = df[df['EDITION'].isin(editions)]
    else:
        filtered_df = df
    
    # Multi-select for countries
    countries = st.multiselect('Select Countries', options=filtered_df['COUNTRY'].unique())
    if countries:
        filtered_df = filtered_df[filtered_df['COUNTRY'].isin(countries)]
    
    # Plot
    fig = px.bar(filtered_df, x='EDITION', y='TOTAL_GOLD', color='COUNTRY', barmode='group', 
                 title='Gold Medals by Country and Edition', labels={'EDITION': 'Edition', 'TOTAL_GOLD': 'Gold Medals'})
    st.plotly_chart(fig)
    
