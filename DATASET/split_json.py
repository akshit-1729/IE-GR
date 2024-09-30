import json

for i in range(1 , 51):
    file_path = './synthetic_data/' + f'gr_{i}.json'
    key1 = 'Additional Indicators'
    key2 = 'low coverage regions'
    output_dir = './synthetic_data/'
    
    # Read the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)
        
    # Find the indices of the keys
    keys = list(data.keys())
    index1 = keys.index(key1)
    index2 = keys.index(key2) 
    
    # Split the data into three parts
    part1 = {k: data[k] for k in keys[:index1]}
    part2 = {k: data[k] for k in keys[index1:index2]}
    part3 = {k: data[k] for k in keys[index2:]}

    # Define output file paths
    part1_file = output_dir + f'gr_{i}_1.json'
    part2_file = output_dir + f'gr_{i}_2.json'
    part3_file = output_dir + f'gr_{i}_3.json'
    
    # Write each part to separate JSON files
    with open(part1_file, 'w') as file:
        json.dump(part1, file, indent=4)
    
    with open(part2_file, 'w') as file:
        json.dump(part2, file, indent=4)
    
    with open(part3_file, 'w') as file:
        json.dump(part3, file, indent=4)
    
    print("JSON data split into three files successfully.")
