# This python script pull raw data from cAdvisor using the REST API for each active container.
# It then stores the JSON files in a mongoDB database, with a collection for each container. 

# usage: python task-05-pipeline.py <database> 
# returns: prints the collection names within the database 

# loading modules
import docker
import requests
import json
import pymongo
import argparse
import sys
from pymongo import MongoClient
from task03 import simulate_load
from util import get_args

if __name__ == '__main__':

    # setting up client 
    client = docker.from_env()

    # defining database 
    args = get_args()

    # connecting to mongoDB 
    mclient = MongoClient(args.mongo_client, 3306)

    # simulate load
    if args.simulate_load == "True":
        simulate_load(args)

    name = args.database
    db = mclient[name] 

    # open file for writing
    if args.write_to_file == "True":
        f = open(name+".collections.txt","w+")

    # for each container in the web application
    for item in client.containers.list():
        
        # get id and name 
        cont_id = item.id 
        cont_name = item.name
        if args.write_to_file == "True":
            f.write(cont_name+"\n")
        print(cont_name)
        
        # cadvisor url
        url = args.api_url + cont_id
        print(url)
        
        # pull raw data 
        res = requests.get(url).json()
        parsed = res
        
        # creating collection   
        records = db[cont_name]
        
        # unique container search parameter 
        search = '/docker/' + cont_id

        # storing each stats record in container's collection in the database
        for p in parsed:
            if p["name"] == search:
                for record in p["stats"]:
                    records.insert(record)




   
