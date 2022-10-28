import csv
import json
 
def csv_to_json(csv_file_path, json_file_path):
    data_dict = {}

    with open('result.csv', encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
 
        count=0
        for rows in csv_reader:

            data_dict[count] = rows
            count=count+1
 
    
    with open(json_file_path, 'w', encoding = 'utf-8') as json_file_handler:
        json_file_handler.write(json.dumps(data_dict, indent = 4))
 

csv_file_path = 'result.csv'
json_file_path = 'result_json.json'
 
csv_to_json(csv_file_path, json_file_path)