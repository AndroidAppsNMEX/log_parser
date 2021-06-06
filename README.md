# Log Parser

Log Parser is a container application to parse host logs and make them available through a Flask application

## Prerequisites

Install Docker engine either on Windows or Linux

## Installation

Use docker-compose to build and run the application.

```bash
docker-compose up
```
## Architecture

The application contains 4 different modules:
 - MySQL 8 Database
 - Parser 
 - Web Application
 - Scheduler

Each one of the previous module works independently of each other.

## Parser
Loads all available files at /data/logs volume, connected to ./logs folder locally. Each file is loaded separately and handled by a separate process.

## Web Application
Flask application to perform a search by given timestamps and host.

## Scheduler
Writes at the output folder the last hour logs:
 - Hostname list connected to a given host
 - Hostname list with connections received from a given host
 - Hostname with most connections

The given hostname can be configured or changed by changing the JSON file located at the config folder.

## Usage

Once the application is up & running go to 
```bash
localhost:5000
```
![Main Screen](https://github.com/AndroidAppsNMEX/log_parser/blob/main/images/main_screen.PNG)


Click on Search Logs and introduce start and end timestamp, as well as origin host.

![Search Engine](https://github.com/AndroidAppsNMEX/log_parser/blob/main/images/search_engine.PNG)

![Results](https://github.com/AndroidAppsNMEX/log_parser/blob/main/images/results.PNG)

Every hour at the output folder the summary can be found

The following folders are mounted inside all containers:
   - logs --> /data/logs
   - config --> /config
   - output --> /data/output

```bash
Time 2021-06-06 17:00:32.754652+00:00
From Host to Carlos
Carlos
To Host from Carlos
ppp
ttt
ttt2
ttt3
Carlos
From Host with more connections
Carlos
-------------------------
Time 2021-06-06 17:00:52.817316+00:00
```