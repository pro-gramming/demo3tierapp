#!/bin/bash
set -e

# Create MongoDB log directory and set permissions
mkdir -p /var/log/mongodb
chmod 777 /var/log/mongodb
chown -R root:root /data/db

# Start MongoDB
mongod --fork --logpath /var/log/mongodb/mongod.log

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to start..."
sleep 10

# Import mock data
echo "Importing mock data..."
mongoimport --db=employees_DB --collection=employees --file=./MOCK_DATA.json --jsonArray --drop

# Create indexes
echo "Creating indexes..."
mongosh --eval "
  use employees_DB;
  db.employees.createIndex( { 'emp_id': 1}, { unique: true} );
  db.employees.createIndex( { first_name: 1, last_name: 1 }, { unique: true } );
"

# Start Nginx explicitly
echo "Starting Nginx..."
service nginx start

# Start Supervisor to manage the FastAPI app
echo "Starting Supervisor..."
/usr/bin/supervisord -n 