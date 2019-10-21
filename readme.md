# *Welcome to Notasi!*

Notasi is designed for 2 different types of people:

 - People who want to care about data, but don't know what data they've got
 - People who don't want to care about data, but have to
<br></br>
# Design Principles

#### Ease of use over performance
Instead of stressing about perfectly structuring their data, they tell Notasi how a piece of information is identified (business keys) and what changes to the information they care about (e.g. email address but not last read time). Notasi handles the rest.  
        
#### Designed to be outgrown 
Notasi has been built to have the lowest possible barrier of entry. While scaling Notasi should be possible, it’s designed to help users solve their problems until they’re ready for other enterprise solutions.  
        
#### Only basic SQL skills needed
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

### Locations
Locations are **where you get your data**. 

Locations can be a:

 - SQL Database
 - Folder containing CSV, XML or JSON files
 - HTTP address

### Queries
Queries are **how you get your data**. 

All Queries **need to be linked to a Location**. Beyond that, each different type on location requires different information in their respective queries:

| Location Type | Query Details |
|--|--|
| *SQL databases* | SQL databases need a standard SQL query in the **Request Body** field. For safety, it's best to use fully qualified table names |
|*Folder*|Folders are simple, they just need a file name in the **Request Body** field|
|*HTTP address*| **Endpoint**<br></br>**Request Method**<br></br>**Headers**<br></br>**Request Body**|
 

### Views
Views are **what data is stored**
# Accessing Your Data

#### Requests through Notasi

#### Direct Database Connection

# TO DO

 - Scheduling
 - SSO
 - Better handling of deleted views
 - Better handling of bad input
 - Better error messages
 - Exporting sync setups
 - Specific edit screens for location types
