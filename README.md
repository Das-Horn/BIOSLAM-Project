# BIOSLAM Project
By Craig Doyle
Supervised by Micheal Core

# Python
Inside the python folder is a program to read, analyze & store waveform data. It is also configured to perform actions based on the waveform data that it is reading.

# Backend
In the back end for this project a docker compose file is provided this can be used to download and install InfluxDB & Grafana using docker. This however is only the default and can be changed depending on the needs of the user. These are used to store and visualize the waveform data coming from the python program.
# Docker
The "*docker-compose.yml*" file in this repository will download and run a pre configured instance of Grafana & InfluxDB.