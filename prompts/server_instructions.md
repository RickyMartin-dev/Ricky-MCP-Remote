# RickyBot MCP Server

This server provides tools and processes that may be asked for by user. User may imply usage of available tools or explicitly ask for a "RickyBot" tool to be used.

## Available Tools

### fetch_ricky_martin_data
Retrieves the resume of an individual named Ricky Martin who built this MCP and resume will tell more about who this person is

**Returns:** Text pdf of resume to allow answering of questions.

**Usage:** Call this tool whenever user asks for information about Ricky or Ricky Martin. 

### fetch_instructions
Retrieves specialized writing instruction templates for working through different processes.

**Parameters:**
- `prompt_name` (string): Must be one of:
  - `write_complete_ppr.md` - Guidelines for creating a document referred to as a "PPR" that you will generate for the user.

**Returns:** Detailed instructions and formatting requirements for the requested content type

**Usage:** Fetch these instructions before performing tasks that relate to one of the use cases outlined.


### get_alerts
Get weather alerts for a US state.

**Parameters:**
- `state` (string): Two-letter US state code (e.g. CA, NY)

**Returns:** String of Alert Data

**Usage:** Use when user asks for alert data, may have to prompt for parameter.


### get_forecast
Get weather forecast for a location.

**Parameters:**
- `latitude` (float): Latitude of the location
- `longitude` (float): Longitude of the location

**Returns:** String of weather forcast for specified location.

**Usage:** Use when user asks for forcast for a specific location. May have to prompt user for parameter.