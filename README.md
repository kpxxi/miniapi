# miniapi
Mini API setup for a tech challenge using Python and Tornado with SQLITE 3 database

Prerequisite
------------
- Install tornado using pip or easy_install
  pip install tornado

Running the MINIAPI
---------------------
- Run apiserver.py <python apiserver.py> from command prompt/terminal (service will be run on localhost with port 8888)
- New db file "api.db" will be created in current working directory with "Listing" and "User" tables

Usage
------
Open a new terminal, below are the available API calls
Output in JSON format

1. /api/user/get_users/ (to list all users)
2. /api/user/update_user/  (to update user)
  - Required parameters: id, name
3. /api/user/new_user/ (to create new user)
  - Required paramaters: name
4. /api/user/delete_user/ (to delete user)
  - Required parameters: id
5. /api/listing/get_listings/ (to list all listings)
6. /api/listing/new_listing/ (to create new listing)
  - Required parameters: userid, price,listing_type('rent' OR 'sale'),postal_code,status('active' or 'closed' or 'deleted')
7. /api/listing/update_listing/ (to edit listing)
  - Required parameters: userid,price,listing_type,postal_code,status
8. /api/listing/delete_listing/ (to delete listing)
  - Required parameters: id

cURL examples:
- curl /api/user/get_users
- OUTPUT
  [{"id":1,"name":"agenta"}]

- curl /api/listing/new_listing --data "userid=1&price=2400&listing_type=rent&postal_code=123456&status=active"
- OUTPUT
  {"result": "New Listing Created"}

