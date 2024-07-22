# 🏅 Olympic Games Data Hub 🏅

Welcome to the Olympic Games Data Hub! This project provides a comprehensive dataset of the Olympic Games from 1896 to 2022. The goal is to load, explore, and visualize this data using Snowflake, Snowflake Notebooks, and Streamlit. Fun fact: we'll load the dataset stored in this GitHub repository using External Integration Access. There's no need to download the dataset locally; we'll pull it directly from GitHub to Snowflake.

**NOTE:** As soon as Cortex Analyst will be released in Public Preview, we'll use this dataset to build our Olympic Chat Bot! ... Stay Tuned ;) 
<p align="center">
  <br>
  <img src="https://github.com/sfc-gh-mconsoli/olympic_games_data_hub/blob/main/images/streamlit_app.gif?raw=true" alt="Olympic Rings"/>
</p>

## Getting Started

To get started with the Olympic Games Data Hub, follow these steps:

### 1. Run Setup Script

First, run the setup script to create the necessary database objects. This script sets up the database, schema, warehouse, and external access integration needed for the project.

- [Run setup.sql](https://github.com/sfc-gh-mconsoli/olympic_games_data_hub/blob/main/setup.sql)

### 2. Push Data from GitHub to Tables

Next, use the provided notebook to fetch the Olympic Games data from GitHub and push it into Snowflake tables. The notebook will handle the data ingestion and table creation.

- [Download & Import the notebook](https://github.com/sfc-gh-mconsoli/olympic_games_data_hub/blob/main/olympic_games_ingest_explore.ipynb)
- Import `plotly` package in the top right "Packages" button.
- Enable the External Access for GitHub (created in the previous step) from the Notebook Settings (three dots menu, top right).
  
### 3. Import the Streamlit App into Snowflake

To explore and visualize the data using the Streamlit app, follow these steps:

- **Create a New Streamlit App:**
  - Click on **New Streamlit**.
  - Enter a name for your app, such as **Olympic Games Data Hub**.
  
- **Configure Your App:**
  - Choose the **Database**: `OLYMPIC_GAMES`
  - Select the **Schema**: `RAW_DATA`
  - Choose the **Warehouse**: `OLYMPIC_GAMES_WH`

<p align="center">
  <br>
  <img src="https://github.com/sfc-gh-mconsoli/olympic_games_data_hub/blob/main/images/screenshot_create_app.png?raw=true" alt="Olympic Rings"/>
</p>

- **Add the App Code:**
  - [Download or Copy-Paste](https://github.com/sfc-gh-mconsoli/olympic_games_data_hub/blob/main/olympic_games_data_hub.py) the content of `olympic_games_data_hub.py`.
  - Import `plotly` package in the top left "Packages" button.


- **Run the App:**
  - Click on the **Run** button to start the app and begin exploring the data!


## Project Overview

The Olympic Games Data Hub consists of the following components:

- **setup.sql**: Script to set up the database, schema, warehouse, and external access integration.
- **olympic_games_ingest_explore.ipynb**: Notebook to fetch data from GitHub and push it into Snowflake tables.
- **olympics_games_data_hub.py**: Streamlit app for exploring and visualizing the Olympic Games data.
- **dataset**: folder containing csv dataset that will be uploaded in your Snowflake account.

## Requirements

- Snowflake Trial Account

---

Enjoy exploring the Olympic Games data!
