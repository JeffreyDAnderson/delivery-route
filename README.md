# delivery-route

### Project Description
This project is an application for reading package delivery data, assigning shortest routes, and delivering packages.

### Languages
Python

### User Interactions
Users have 3 options to interact with this application
1. Get information about a certain package given its ID
2. Get information about all packages given a specific time
3. Exit the application

### How the Application Works
* This application **requires** a .csv file of package data
* Packages from the file are read and stored in internal memory
* Packages are assigned routes based on shortest path
* Delivery Routes are assigned to available trucks
* Trucks "deliver" packages by calculating delivery time
