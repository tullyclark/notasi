# *Welcome to Notasi!*

Notasi is designed for 2 different types of people:

 - People who want to care about data, but don't know what data they've got
 - People who don't want to care about data, but have to

 Roughly described as a data hub, Notasi deliberately does not care about what the data looks like going in. It does not try to format the data or make it conform to a standard. 

 Unlike most data warehouses, hubs or connectors, users only need to format the data when it is pulled out of Notasi. This delays decisions that are nearly impossible to make correctly when first starting out. 
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
Addresses, Ports, Usernames, Passwords, Database names, URLs, Headers and Bodies are encrypted using AES 128 bit encryption and a randomly generated key stored in config.py. If this is not strong enough for you, don't use Notasi. Better yet, let me know and help me improve Notasi!
<br></br>


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
A location can be a:
 - SQL Database
 - Folder containing CSV, XML or JSON files
 - HTTP address

### Queries: How you get your data

All queries need a name and a linked location. Beyond that, each different type on location requires different information:

| Location Type | Query Details |
|--|--|
| *SQL databases* | SQL databases need a standard SQL query in the **Request Body** field. For safety, it's best to use fully qualified table names |
|*Folder*|Folders are simple, they just need a file name in the **Endpoint** field|
|*HTTP*| HTTP locations need lots:<br></br>Endpoint<br></br>Request Method<br></br>Headers<br></br>Request Body|
 

### Views: What data is stored

All views need a name, a view name, and a linked query. 

Once a view is defined, a Postgres view is built. Views are defined by **business keys** and **information columns**:
| Column Type | Purpose |
|--|--|
| *Business Key* | Business keys make up a row's identifier. They are what makes a row unique |
| *Information Column* | Information columns contain the information you want to store. They are how Notasi knows when to store a change |

<br></br>
# Accessing Your Data

### Requests through Notasi
This is where the real power of Notasi is; **you can query the data lake and feed the results directly into another query.**

After you've defined a view, you can query the results in another query's *Data Lake Query* field.

If a data lake query is entered, the results can be used in curly brackets,`{variable_name}`, in the endpoint, header and body fields. The resulting query is run once per data lake query row.

![Feeding Notasi data to a query](screenshots/screenshot_1.png?raw=true "Feeding Notasi data to a query")

### Direct Database Connection
Notasi is built on PostgreSQL.
```
Database: notasi
Username: notasi
Password: In config.py, or printed at install
```

Views are built with their defined names.

<br></br>
# TO DO

 - Scheduling
 - SSO
 - Better handling of deleted views
 - Better handling of bad input
 - Better error messages
 - Exporting sync setups
 - Specific edit screens for location types
 - Ensure views return unique values when flattening JSON
