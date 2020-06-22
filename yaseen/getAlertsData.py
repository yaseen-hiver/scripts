#!/usr/bin/python

import requests
import json 
import csv 
import argparse
from csv import writer


def req_api(fdate,edate,team):
    response = requests.get("https://api.opsgenie.com/v2/alerts?query=teams:{team} AND createdAt>{fdate}".format(team=team,fdate=fdate),headers={'Authorization': 'GenieKey 1791b974-76c0-439e-8b6f-13f2a41caa60'})
    if response.status_code==200:
        json_response = response.json()
        print "data fetched"
        # make_json(json_response)
        create_csv(json_response,team)
    else:
        print "unable to fetch data"
        
def make_json(json_response):
    try:
        with open('b.json', 'w') as json_file:
            json.dump(json_response, json_file)       
    except:
        raise Exception("unable to make json file")
    print "json file created successfully" 
 

def create_csv(json_response,team):
    try:
        data_file = open('data1.csv', 'a') 
    except:
        raise Exception ("unable to open csv file")
    
    header=["tinyId","message","createdAt","owner","team","notes"]
    data = json_response['data']
    
    csv_writer = csv.writer(data_file) 
    csv_writer.writerow(header)

    writer = csv.DictWriter(data_file, fieldnames=header)
    for record in data:
        notes_request=requests.get("https://api.opsgenie.com/v2/alerts/{id}/notes?identifierType=id".format(id=record["id"]),headers={'Authorization': 'GenieKey 1791b974-76c0-439e-8b6f-13f2a41caa60'})
        if notes_request.status_code==200: 
            notes_json=notes_request.json()
            if len(notes_json['data'])!=0:
                note = notes_json['data'][0]['note']
            else:
                note='none'  
        # print note
        note_dict={
            "tinyId":record["tinyId"],
            "message":record["message"],
            "createdAt":record["createdAt"],
            "owner":record["owner"],
            "team":team,
            "notes":note
        }
        # print note_dict
        if(note_dict):
            writer.writerow(note_dict) 

    data_file.close() 
    print "csv file created successfully"


if __name__ == '__main__':   
    parser = argparse.ArgumentParser(description='Enter start date, end date and team name ')
    parser.add_argument("-s", action="store",dest="fdate")
    parser.add_argument("-e", action="store",dest="edate")
    parser.add_argument("-t","--team",action="store")
    args = parser.parse_args()
    if args:
        req_api(args.fdate,args.edate,args.team)
    # print args.date
    