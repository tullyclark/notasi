# *Welcome to Notasi!*

Notasi is designed for 2 different types of people:

 - People who want to care about data, but don't know what data they've got
 - People who don't want to care about data, but have to
<br></br>
# Design Principles

### Ease of use over performance
Instead of stressing about perfectly structuring their data, they tell Notasi how a piece of information is identified (business keys) and what changes to the information they care about (e.g. email address but not last read time). Notasi handles the rest.  
        
### Designed to be outgrown 
Notasi has been built to have the lowest possible barrier of entry. While scaling Notasi should be possible, it’s designed to help users solve their problems until they’re ready for other enterprise solutions.  
        
### Only basic SQL skills needed
if you understand:

```SQL
SELECT 
	column 
FROM 
	tab1 
	inner join tab2 on tab1.x = tab2.y
```

then you can implement and use Notasi
<br></br>



# Disclaimers
Addresses, Ports, Usernames, Passwords, Database names, URLs, Headers and Bodies are encrypted using AES 128 bit encryption and a randomly generated key stored in config.py. If this is not strong enough for you, don't use Notasi. Better yet, let me and and help me improve Notasi!


# Installation
*Tested on a fresh Ubuntu 18.04 EC2 instance*

Run:
```bash
wget https://raw.githubusercontent.com/tullyclark/notasi/master/install/install.sh
chmod +x install.sh
sudo ./install.sh
```

You will then be stepped through the setup process 
<br></br>
# Data Structure

### Locations: Where you get your data

All locations need a name, a type and an address, as well as:
|Type| Name |Address | Port | Database | Username | Password | SQL Type |
|--|--|--|--|--|--|--|--|
| Folder |✓|✓| 
| HTTP |✓|✓|?|
| SQL |✓|✓|✓|✓|✓|✓|✓| 


 - SQL Database
 - Folder containing CSV, XML or JSON files
 - HTTP

### Queries: How you get your data

All queries need a name and a linked location. Beyond that, each different type on location requires different information:

| Location Type | Query Details |
|--|--|
| *SQL databases* | SQL databases need a standard SQL query in the **Request Body** field. For safety, it's best to use fully qualified table names |
|*Folder*|Folders are simple, they just need a file name in the **Request Body** field|
|*HTTP*| HTTP locations need lots:<br></br>**Endpoint**<br></br>**Request Method**<br></br>**Headers**<br></br>**Request Body**|
 

### Views: What data is stored

All views need a name, a view name, and a linked query. 

Once a view is defined, a Postgres view is built. Views are defined by business keys and information columns:
| Column Type | Purpose |
|--|--|
| *Business Key* | Business keys make up a row's identifier; they are what makes a column unique |
| *Information Column* | Information columns contain the information you want to store. They are how Notasi knows when to store a change |

# Accessing Your Data

### Requests through Notasi

### Direct Database Connection
Notasi is built on PostgreSQL.
```
Database: notasi
Username: notasi
Password: In config.py, or printed at install
```

Views are built with their defined names.

# TO DO

 - Scheduling
 - SSO
 - Better handling of deleted views
 - Better handling of bad input
 - Better error messages
 - Exporting sync setups
 - Specific edit screens for location types
 - Ensure views return unique values when flattening JSON
