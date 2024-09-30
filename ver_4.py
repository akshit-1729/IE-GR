'''Same as version 3 but have some minor ui changes'''
import requests
import os
from pdf2image import convert_from_path
import base64
from io import BytesIO
import json 
import sys


api_key = ""


# Function to convert a PDF file to images and save them to a folder
def pdf_to_images(pdf_path):
    # Convert each page of the PDF to an image
    images = convert_from_path(pdf_path, dpi=300, fmt='jpeg')
    return images

# Function to encode the images
def encode_image(image_path):
    # with open(image_path, "rb") as image_file:
    return base64.b64encode(image_path).decode('utf-8')

# Function to convert the each text file to string and in turn return the entire list of strings
def text_files_to_string_list(text_file_paths):
    """
    Reads each text file specified in the text_file_paths list,
    converts each file's content to a string, and appends it to a list.

    Parameters:
    - text_file_paths: List[str] - A list of file paths to text files.

    Returns:
    - List[str]: A list of strings where each string is the content of one text file.
    """
    strings_list = []  # Initialize an empty list to store file contents.
    for file_path in text_file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                strings_list.append(file.read())  # Read the entire file content and append to the list.
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            # You might want to handle the error differently depending on your needs.
            # For example, you could append a None, continue to the next file, etc.

    return strings_list

def extract_json_content(response_data):
    # Find the index of the first opening brace
    start_index = response_data.find('{')
    # Find the index of the last closing brace
    end_index = response_data.rfind('}') + 1  # Add 1 to include the brace itself

    # Extract the JSON string
    json_content = response_data[start_index:end_index]

    return json_content


# Function to convert the text strings to json files
def convert_text_to_json_and_save(text_file_paths, output_folder):
    """
    For each text file in text_file_paths, reads the content, sends it to an API, 
    and saves the API's JSON response to a file with the same name in the specified output folder.

    Parameters:
    - text_file_paths: List[str] - A list of file paths to text files.
    - output_folder: str - The path to the folder where JSON files should be saved.
    - api_key: str - The API key for authentication with the API.
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    ct = 0
    for text_file_path in text_file_paths:
        # Read text content from the file
        print("text: ", ct)
        try:
            with open(text_file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
        except Exception as e:
            print(f"Error reading file {text_file_path}: {e}")
            continue
        prompt = "Convert the below text file to json file with proper hierarchy and return only\
            the json file in response, I don't want python code to convert text to json give me\
            only the fully converted json file in the response and nothing else. Make sure to not\
            miss any detail and write all the key and values in full detail, give proper json file."
        current_prompt = prompt + text_content
        # Construct the API request
        # print(current_prompt)
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }   
        payload = {
        "model": "gpt-4",
        # "prompt": current_prompt,
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": current_prompt
            }
            ]
        }
        ],
        "max_tokens": 3000
        }
        
        # Send the request to the API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response.json())
        response.raise_for_status()  # Check for errors
        response_data = response.json()
        response_data = response.json()['choices'][0]['message']['content']
        # response_data = response_data.json()
        response_data_formatted = extract_json_content(response_data)
        print(response_data_formatted)
        response_data2 = json.loads(response_data_formatted)
        
        # Determine the output JSON file name (same as input but with .json extension)
        base_filename = os.path.basename(text_file_path)
        json_filename = os.path.splitext(base_filename)[0] + '.json'
        json_file_path = os.path.join(output_folder, json_filename)
        
        # Save the response data to a JSON file
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(response_data2, json_file, ensure_ascii=False, indent=4)
            
        print(f"Saved JSON response for {text_file_path} to {json_file_path}")
        ct += 1
        # except requests.RequestException as e:
        #     print(f"Error calling API for file {text_file_path}: {e}")




def concatenate_and_save_text_files(folder_path, output_file_path):
    """
    Concatenates all text files in the specified folder in alphabetical order of their names and saves to a new file.
    
    Args:
    folder_path (str): The path to the folder containing the text files.
    output_file_path (str): The path to the output file where the concatenated content will be saved.
    
    Returns:
    None: Saves the concatenated text to a file.
    """
    # Create a list of all files in the folder that are text files
    files = [f for f in sorted(os.listdir(folder_path)) if f.endswith('.txt')]
    
    # Initialize an empty string to store the concatenated content
    concatenated_content = ""
    
    # Iterate over each file in alphabetical order
    for file_name in files:
        # Create the full path to the file
        file_path = os.path.join(folder_path, file_name)
        # Open the file and read its content
        with open(file_path, 'r', encoding='utf-8') as file:
            concatenated_content += file.read() + "\n"  # Append content and a newline for separation
    
    # output_file_path += '/text_file_combined.txt'
    # Write the concatenated content to the output file
    with open(output_file_path, 'w', encoding='utf-8') as text_file_combined:
        text_file_combined.write(concatenated_content)



# Function to call the OpenAI API and store the response in a text file
def call_openai_and_save(image_paths, output_folder, text_file_paths, save_path, json_filename):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    text_content = ""
    counter = 0
    # Call the OpenAI API for each image and save the response
    for image_path in image_paths:
        print(counter)
        first_image = image_path
        buffer = BytesIO()
        first_image.save(buffer, format='JPEG')  # You can choose format as needed (e.g., PNG)

        # Now, buffer.getvalue() contains the binary data you would get from image.read()
        image_data = buffer.getvalue()
        base64_image = encode_image(image_data)


        prompt = "understand the image and convert the full description of the image into text file and return only the \
                text format for the current image use tables when necessary, the goal is to extract the contents of image in the form of text file \
                without missing any details, not missing any details is most important thing. Don't give any text except than text file. If this\
                image is continuation from last page then add a title named continue and the corresponding value that describes how it is continuation\
                from the previous image in the text file."
        current_prompt =  text_content +  " Above is the output from the previous prompt. (If there is no text before that means this is first prompt)" + prompt
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }   
        payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": current_prompt
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
            ]
        }
        ],
        "max_tokens": 3000
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response.json())
        response.raise_for_status()  # Raise an error if the request failed
        text_content = response.json()['choices'][0]['message']['content']
        text_content = text_content[3:-3]
        counter = counter + 1
        # Save the response to a json file
        filename = 'image_' + str(counter) + '.txt'
        text_file_path = os.path.join(output_folder, filename)
        text_file_paths.append(text_file_path)
        with open(text_file_path, 'w') as text_file:
            text_file.write(text_content)

    #save all the concatenated files at a given path
    save_path = save_path + get_filename_without_extension(json_filename) + '.txt'
    concatenate_and_save_text_files(output_folder, save_path)




# Getting the filename without extension 
def get_filename_without_extension(file_path):
    # Get the base name of the file (without directory path)
    base_name = os.path.basename(file_path)
    # Split the base name into name and extension
    name, extension = os.path.splitext(base_name)
    return name


# Function to combine all the json files
def combine_json_files(output_folder, pdf_path, save_path, json_filename):
    # Directory where the JSON files are located
    directory = output_folder

    # Placeholder for combining the JSON data
    combined_data = {}

    # Iterate over files in the specified directory
    for filename in sorted(os.listdir(directory)):
        # Check if the file is a JSON file and matches the naming pattern
        if filename.startswith('image_') and filename.endswith('.json'):
            # Construct the full file path
            filepath = os.path.join(directory, filename)
            # Open and read the JSON file
            with open(filepath, 'r') as file:
                data = json.load(file)
                # Append the data from this file into the combined_data list
                # combined_data.append(data)
                combined_data[filename] = data


    # Specify the file path for the combined JSON file
    combined_file_path = output_folder + get_filename_without_extension(pdf_path)

    # Write the combined data to a new JSON file
    with open(combined_file_path, 'w') as file:
        json.dump(combined_data, file, indent=4)

    results_folder = 'Experiments/'
    results_file_path = results_folder + 'ver_4_' + get_filename_without_extension(pdf_path) + '.json'
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    with open(results_file_path, 'w') as file:
        json.dump(combined_data, file, indent=4)

    print(f"Combined JSON data has been written to {combined_file_path}")
    #save the image with GUI
    save_file_path = save_path + json_filename
    with open(save_file_path, 'w') as file:
        json.dump(combined_data, file, indent=4)

# Function to call the entire end-to-end code
def call_end_to_end(pdf_path, save_path, json_filename):
    # return
    text_file_paths = []
    # output_folder = 'output_ver_4/'
    output_folder = 'output_ver_4/' + os.path.basename(pdf_path)[0:-4] + '/'
    image_paths = pdf_to_images(pdf_path)
    call_openai_and_save(image_paths, output_folder, text_file_paths, save_path, json_filename)
    convert_text_to_json_and_save(text_file_paths, output_folder)
    combine_json_files(output_folder, pdf_path, save_path, json_filename)

# Returns the path names of each text files in directory named directory in a list
def get_textfile_paths(directory):
    textfile_paths = []
    # Check if the directory exists
    if os.path.exists(directory):
        # Get all files and directories in the specified directory
        for file_name in os.listdir(directory):
            # Check if the file name starts with 'im' and ends with '.txt'
            if file_name.startswith('im') and file_name.endswith('.txt'):
                # If the file meets the criteria, append its path to the list
                textfile_paths.append(os.path.join(directory, file_name))
    else:
        print(f"The directory {directory} does not exist.")
    return textfile_paths

# # combine_json_files('output_ver_4/', '')
# pdf_path = ''  # Replace with the path to your PDF file

# # Check if a command line argument is provided
# if len(sys.argv) > 1:
#     pdf_path = sys.argv[1]  # Take the PDF path from the first command line argument
# else:
#     pdf_path = pdf_path  # Use the default path if no argument is provided

# print(f"Using PDF path: {pdf_path}")
# call_end_to_end(pdf_path)

# output_folder = 'output_ver_4/'
# text_file_paths = []
# image_paths = pdf_to_images(pdf_path)
# call_openai_and_save(image_paths, output_folder)
# # print(text_file_paths)
# text_file_paths = get_textfile_paths(output_folder)
# convert_text_to_json_and_save(text_file_paths, output_folder)

