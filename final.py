import csv
import json

def open_json_config(path):
    f=open(path)
    json_data=json.load(f)
    f.close()
    return json_data

def get_required_dict():
    """
    This function returns the required dimensions and metrics
    as an indexed dictionary

    """
    data=open('result.csv')
    csv_data=csv.reader(data)
    header_list=list(csv_data)[0]
    all_rows=list(csv_data)
    filtered_header_list=[]
    filtered_metrics_list=[]

    json_data=open_json_config('example.json')

    dimensions_list=json_data['dimensions']
    # print("dimensions_list",dimensions_list)

    metrics_list=json_data['metrics']
    # print("Metrics List",metrics_list)

    for i in dimensions_list:
        for j in header_list:
            if j==i:
                filtered_header_list.append(i)

    for i in metrics_list:
        for j in header_list:
            if j==i:
                filtered_metrics_list.append(i)

    required_filtered_list=filtered_header_list+filtered_metrics_list
    # print("required List",required_filtered_list)

    required_indices=[]
    for i in required_filtered_list:
        for j in header_list:
            if i.__eq__(j):
                x=header_list.index(j)
                required_indices.append(x)

    # print("Required indices",required_indices)

    count=0
    data_dict={}
    with open("./result.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            data_dict[count]=row
            count=count+1

        
    # print(data_dict)
    no_of_data_rows=count-1
    # print(no_of_data_rows)



    required_dict={}
    running_list=[]
    counter=0
    for i in data_dict:
        for j in required_indices:
            x=data_dict[i][j]
            # print(x)
            running_list.append(x)
        required_dict[counter]=running_list
        counter=counter+1
        running_list=[]

    list_of_lists=list(required_dict.values())
    # print(required_dict)

    required_columns=required_dict[0]

    final_dict={}

    f=open('result_json.json')
    json_data=json.load(f)



    for each in json_data:
        my_dict={}
        for y in json_data[each]:
            if y=='\ufeffDATE':
                my_dict[y]=json_data[each][y]
            else:
                if y in required_columns:
                    my_dict[y]=json_data[each][y]
        final_dict[each]=my_dict

    # print(final_dict)

    # final dict has the required columns mentioned in config json ie example.json
    return final_dict

# print(get_required_dict())

def apply_filters(dict):
    """
        Here dict is dictionary on which to apply filters
        dict from get_required_dict()
    """
    json_data=open_json_config('example.json')
    final_dict_after_filters={}
    length=len(json_data['filters'])
    # print(length)
    final_dict=dict
    for each in final_dict:
        # print("each",each)
        count=0
        for i in json_data['filters']:
            # print("i-------------->",i)
            # print(final_dict[each][i])
            # print(json_data['filters'][i])
            if final_dict[each][i] in json_data['filters'][i]:
                count=count+1
        # print(count)
        if count==length:
            final_dict_after_filters[each]=final_dict[each]

    # print(final_dict_after_filters)
    return(final_dict_after_filters)

def date_to_int(var):
    list=var.split('-')
    word=''
    for element in list:
        word+=str(element)
    return int(word)

def apply_date(dict):
    final_dict_after_filters=dict
    final_dict_after_date={}
    json_data=open_json_config('example.json')
    if json_data['date']:
        start_date=json_data['date']['start_date']
        end_date=json_data['date']['end_date']
    # print(start_date,end_date)

    
        start_date_as_int=date_to_int(start_date)
        end_date_as_int=date_to_int(end_date)

        # print(start_date_as_int,end_date_as_int)

        final_dict_after_date={}
        for each in final_dict_after_filters:
            row_date=date_to_int(final_dict_after_filters[each]['\ufeffDATE'])
            # print(row_date)
            if row_date>=start_date_as_int and row_date<=end_date_as_int:
                final_dict_after_date[each]=final_dict_after_filters[each]
    else:
        final_dict_after_date=dict
    return final_dict_after_date
    # print(final_dict_after_date)


def apply_search(dict):
    final_dict_after_search={}
    final_dict_after_date=dict
    json_data=open_json_config('example.json')
    if json_data['search']:
        search_text=json_data['search']['text']
        # print(search_text)
        search_columns=json_data['search']['columns']
        # print(search_columns)
        for each in final_dict_after_date:
            for i in search_columns:
                if final_dict_after_date[each][i].__contains__(search_text):
                    final_dict_after_search[each]=final_dict_after_date[each]
    else:
        final_dict_after_search=final_dict_after_date
    # print(final_dict_after_search)
    return final_dict_after_search


def apply_sort(dict):
    json_data=open_json_config('example.json')
    final_dict_after_sort={}
    sorted_dict={}
    passed_dict=dict
    list_of_sort_params=[json_data['sort']]
    # print(list_of_sort_params)
    for i in list_of_sort_params[0]:
        # print(i)
        order=i['order']
        name=i['name']
        # print(name)
        if order=="DESC":
            order=True
        else:
            order=False
        sorted_dict=sorted(passed_dict.items(), key=lambda x: x[1][name], reverse=order)
        # print(sorted_dict)

    final_dict_after_sort=sorted_dict
# apply_sort(final_dict)

 
# print(list(final_dict.values()))

def apply_pagination_and_write_to_csv(dict):
    json_data=open_json_config('example.json')
    limit=range(json_data['pagination']['limit'])
    print(limit)
    passed_dict=dict
    header_row=list(passed_dict['0'].keys())
    list_of_lists=list(passed_dict.values())
    final_list_of_lists=[]
    final_list_of_lists.append(header_row)
    # print(header_row)
    counter=0
    for x in limit:
        final_list_of_lists.append(list(list_of_lists[counter].values()))
        counter=counter+1
    print(final_list_of_lists)


    with open('output.csv','w') as f:
        writer=csv.writer(f)
        writer.writerows(final_list_of_lists)
    

final_dict=get_required_dict()
# print(final_dict)
final_dict_after_filters=apply_filters(final_dict)
# print(final_dict_after_filters)
final_dict_after_date=apply_date(final_dict_after_filters)
# print(final_dict_after_date)
final_dict_after_search=apply_search(final_dict_after_date)
# print(final_dict_after_search)
# print(apply_search(final_dict))  ----> u can pass final_dict as well it will search for you

# print(sorted(final_dict_after_search.items(), key=lambda x: x[1]['FOLLOWS'], reverse=True))
apply_pagination_and_write_to_csv(final_dict)



