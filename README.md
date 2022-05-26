# ELIDEK_Database
A full stack web application created for the 6th semester course "Database Systems", course code 3123,  of the school of Electrical & Computer Engineering of NTUA. The database contains dummy data generated using https://filldb.io that were further edited by us to fit certain specifications provided, which is accessed by a Python backend server and is then presented in a NodeJS frontend. 

## Installation
### Prerequisites
  The following software is required for the installation and execution of this application:
* **Python 3.10**, preferably installed under "C:\Program Files\Python310" (see below)
* **Node.js 16.15.0** with **npm 8.10**, along with the package vue ^2.6.14 (npm install vue)
* XAMPP or your choice of stack manager that runs a MySQL server on port 3306.

### Installation Steps - Development Server, release not final
#### XAMPP & MySQL Server
  * Start up the MySQL server through XAMPP.
  * Either from a terminal or your DBMS software of choice, execute the DDL and DML .sql scripts **IN THAT ORDER**. The files are found in the project's  directory.

#### Flask Server
 * From a terminal in the project's main directory, execute the following commands:
    *     .\server\env\Scripts\activate
    *     python .\server\app.py
  In case you get an error about Python not being found in a certain directory, see "Reconfiguring Flask's Virtual Environment" below.
#### Vue Client
* From a terminal in the project's main folder, execute the following commands:
    *     cd client
    *     npm run serve
You should then be able to access the application on http://localhost:8080/.

##### Reconfiguring Flask's Virtual Environment
In case it is impossible or inconvenient to install Python under the required directory, you may configure a new virtual environment for the application to use that will be configured to your device's Python directory by executing the following commands from a terminal in the project's "server" folder:   
*     python -m venv env2  
*     .\env2\Scripts\activate  
*     pip install Flask Flask-Cors mysql-connector  
*     python ./app.py  
