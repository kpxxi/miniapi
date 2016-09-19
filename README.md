# miniapi
Mini API setup for a tech challenge using Python and Tornado with SQLITE 3 database

Prerequisite
------------
- Install tornado using pip or easy_install <br />
  `<pip install tornado>`

Running the MINIAPI
---------------------
- Run apiserver.py <python apiserver.py> from command prompt/terminal (service will be run on localhost with port 8888)
- New db file "api.db" will be created in current working directory with "Listing" and "User" tables
- Create new user first before creating a listing

Usage
------
Open a new terminal, below are the available API calls__
Output in JSON format

Url | Function Description | Parameters | Parameters Description
--- | -------------------- | ---------- | -----------
/api/user/get_users/ | To list all users | - | -
/api/user/update_user/ | To update username of the given user id | id | User ID
 | | name | Username
/api/user/new_user/ | To add new user | name | username
/api/user/delete_user/ | To delete user of the given user id | id | User ID
/api/listing/get_listings/ | To list all listings | - | -
/api/listing/update_listing/ | To update details of given listing id | id | Listing ID
 | | userid | User ID (to be taken from User table)
 | | listing_type | Type of Listing ('rent' or 'sale')
 | | price | Price of listing
 | | postal_code | Postal Code of Listing
 | | status | Status of Listing ('active' or 'closed' or 'deleted')
/api/listing/new_listing/ | To add new listing | userid | User ID from User table
 | | listing_type | Type of Listing ('rent' or 'sale')
 | | price | Price of listing
 | | postal_code | Postal code of listing
 | | status | Status of Listing ('active' or 'closed' or deleted')
/api/listing/delete_listing/ | To delete listing of the given listing id | id | Listing ID

cURL examples:
- `<curl /api/user/get_users>`<br />
  Example Output <br />
`<[{"id":1,"name":"agenta"}]>`

- `<curl /api/listing/new_listing --data "userid=1&price=2400&listing_type=rent&postal_code=123456&status=active">`<br />
  Example output <br />
`<{"result": "New Listing Created"}>`

