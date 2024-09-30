import json
import copy

for i in range(1 , 51):
    file_path = './synthetic_data2/' + f'gr2_{i}.json'
    key1 = 'Relevant Biomarkers'
    key2 = 'Gene variants of unknown significance'
    key4 = 'Chemotherapy clinical trials'
    output_dir = './synthetic_data2/'
    
    # Read the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)
        
        
    # Find the indices of the keys
    keys = list(data.keys())
    index1 = keys.index(key1)
    index2 = keys.index(key2)
    index4 = keys.index(key4)
    
    # Split the data into three parts
    part1 = {k: data[k] for k in keys[:index1]}
    part2 = {k: data[k] for k in keys[index1:index2]}
    part3 = {k: data[k] for k in keys[index2:index4]}
    part4 = copy.deepcopy(data["specimen information"])
    part4.pop("primary_tumor_site")
    part4.pop("specimen_site")
    part4["Pathological Diagnosis"] = part1["specimen information"].pop("Pathological Diagnosis")
    part4["Dissection Information"] = part1["specimen information"].pop("Dissection Information")
    part4 = {"specimen information": part4}
    part5 = {k: data[k] for k in keys[index4:]}

    # Define output file paths
    part1_file = output_dir + f'gr2_{i}_1.json'
    part2_file = output_dir + f'gr2_{i}_2.json'
    part3_file = output_dir + f'gr2_{i}_3.json'
    part4_file = output_dir + f'gr2_{i}_4.json'
    part5_file = output_dir + f'gr2_{i}_5.json'
    
    # Write each part to separate JSON files
    with open(part1_file, 'w') as file:
        json.dump(part1, file, indent=4)
    
    with open(part2_file, 'w') as file:
        json.dump(part2, file, indent=4)
    
    with open(part3_file, 'w') as file:
        json.dump(part3, file, indent=4)
        
    with open(part4_file, 'w') as file:
        json.dump(part4, file, indent=4)
    
    with open(part5_file, 'w') as file:
        json.dump(part5, file, indent=4)
    
    print("JSON data split into three/five files successfully.")
