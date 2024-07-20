-- Create a dedicated DB, Schema and WH
CREATE DATABASE IF NOT EXISTS OLYMPIC_GAMES;
CREATE SCHEMA IF NOT EXISTS OLYMPIC_GAMES.RAW_DATA;
CREATE OR REPLACE WAREHOUSE OLYMPICS_GAMES_WH
  WAREHOUSE_SIZE = 'X-Small'
  AUTO_SUSPEND = 60;

-- Create a network policy rule for GitHub
CREATE OR REPLACE NETWORK RULE GITHUB_NETWORK_RULE
  MODE = EGRESS 
  TYPE = HOST_PORT VALUE_LIST = ('github.com', 'raw.githubusercontent.com','media.githubusercontent.com')
  COMMENT = 'Allow access to GitHub';

-- Create External Access Integration that we'll use in the Notebook Functions
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION GITHUB_EXTERNAL_ACCESS_INTEGRATION
    ALLOWED_NETWORK_RULES = ('GITHUB_NETWORK_RULE')
    ENABLED = TRUE
    COMMENT = 'External access integration for GitHub';
