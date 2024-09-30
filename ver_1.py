
import requests
import os
from pdf2image import convert_from_path
import base64
import json
import sys

api_key = ""

# Function to convert a PDF file to images and save them to a folder
def pdf_to_images(pdf_path, images_folder):
    # Ensure the images folder exists
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    
    # Convert each page of the PDF to an image
    images = convert_from_path(pdf_path, dpi=300, fmt='jpeg')
    
    # Save images to the folder
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(images_folder, f'image_{i+1}.jpeg')
        image.save(image_path, 'JPEG')
        image_paths.append(image_path)
    
    return image_paths

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_json_content(response_data):
    # Find the index of the first opening brace
    start_index = response_data.find('{')
    # Find the index of the last closing brace
    end_index = response_data.rfind('}') + 1  # Add 1 to include the brace itself

    # Extract the JSON string
    json_content = response_data[start_index:end_index]

    return json_content

# Function to call the OpenAI API and store the response in a text file
def call_openai_and_save(image_paths, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Call the OpenAI API for each image and save the response
    text_content = ""
    for image_path in image_paths:
        print(image_path)
        base64_image = encode_image(image_path)
        prompt = "understand the image and convert the full description of the image into key-value pairs and return only the \
                json format of key-value pairs, if there is any additional details include them inside json file only, send no other text, the goal is to extract the contents of image in the form of json format \
                without missing any details and write all the key and values in full detail. In addition if it seems that the current image is continuous from the previous \
                output then make the json file accordingly."
        current_prompt =  text_content +  " Above is the output from the previous prompt. (If there is no text before that means\
                this is first prompt)" + prompt
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
        # prompt = "understand the image and give full description of the image, if necessary make tables, the goal is to extract the contents of image in the form of text without missing any details."

        
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        response.raise_for_status()  # Raise an error if the request failed
        # text_content = response.text
        text_content = response.json()['choices'][0]['message']['content']
        # text_content = text_content[7:-3]
        text_content = extract_json_content(text_content)

        
        
        # Save the response to a text file
        filename = os.path.splitext(os.path.basename(image_path))[0] + '.json'
        text_file_path = os.path.join(output_folder, filename)
        # with open(text_file_path, 'w') as text_file:
        #     text_file.write(text_content)
        # Save the response data to a JSON file
        with open(text_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(text_content, json_file, ensure_ascii=False, indent=4)



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
    results_file_path = results_folder + 'ver_1_' + get_filename_without_extension(pdf_path) + '.json'
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    with open(results_file_path, 'w') as file:
        json.dump(combined_data, file, indent=4)

    print(f"Combined JSON data has been written to {combined_file_path}")
    #save the image with GUI
    save_file_path = save_path + json_filename
    with open(save_file_path, 'w') as file:
        json.dump(combined_data, file, indent=4)


# Getting the filename without extension 
def get_filename_without_extension(file_path):
    # Get the base name of the file (without directory path)
    base_name = os.path.basename(file_path)
    # Split the base name into name and extension
    name, extension = os.path.splitext(base_name)
    return name


# Function to call the entire end-to-end code
def call_end_to_end(pdf_path,save_path, json_filename):
    # return
    text_file_paths = []
    text_descriptions = []
    output_folder = 'output_ver_1/' + os.path.basename(pdf_path)[0:-4] + '/'
    images_folder = 'images_ver_1/'
    image_paths = pdf_to_images(pdf_path, images_folder)
    call_openai_and_save(image_paths, output_folder)
    combine_json_files(output_folder, pdf_path, save_path, json_filename)


# # Main code
# # Paths for the PDF, images folder, and output folder
# pdf_path = ''  # Replace with the path to your PDF file
# images_folder = 'images_ver_1/'  # Replace with your images directory path
# # output_folder = 'output_ver_1/'  # Replace with your output directory path

# # Check if a command line argument is provided
# if len(sys.argv) > 1:
#     pdf_path = sys.argv[1]  # Take the PDF path from the first command line argument
# else:
#     pdf_path = pdf_path  # Use the default path if no argument is provided

# print(f"Using PDF path: {pdf_path}")

# output_folder = 'output_ver_1/' + os.path.basename(pdf_path)[0:-4] + '/'

# # Convert the PDF to images
# image_paths = pdf_to_images(pdf_path, images_folder)
# # print(image_paths)
# # image_paths = ['images/image_14.jpeg', 'images/image_15.jpeg', 'images/image_16.jpeg']
# # image_paths = image_paths[1:3]
# # Call the OpenAI API and save the responses
# call_openai_and_save(image_paths, output_folder)
# combine_json_files(output_folder, pdf_path)

