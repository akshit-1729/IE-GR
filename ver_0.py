import requests
import os
from pdf2image import convert_from_path
import json
import sys
import base64
from io import BytesIO

api_token = ""


# Function to convert a PDF file to images and save them to a folder
def pdf_to_images(pdf_path):
    # Convert each page of the PDF to an image
    images = convert_from_path(pdf_path, dpi=300, fmt='jpeg')
    return images


# Function to encode the images
def encode_image(image_path):
    # with open(image_path, "rb") as image_file:
    return base64.b64encode(image_path).decode('utf-8')

def extract_json_content(response_data):
    # Find the index of the first opening brace
    start_index = response_data.find('{')
    # Find the index of the last closing brace
    end_index = response_data.rfind('}') + 1  # Add 1 to include the brace itself

    # Extract the JSON string
    json_content = response_data[start_index:end_index]

    return json_content



# Function to call the OpenAI API and store the response in a text file
def call_openai_and_save(image_paths, output_folder, api_token):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    counter = 0
    for image_path in image_paths:
        print(counter)
        first_image = image_path
        buffer = BytesIO()
        first_image.save(buffer, format='JPEG')  # You can choose format as needed (e.g., PNG)
        # Now, buffer.getvalue() contains the binary data you would get from image.read()
        image_data = buffer.getvalue()
        base64_image = encode_image(image_data)
        prompt = "understand the image and give full description of the image, if necessary make tables, the goal is to extract the contents of image in the form of JSON file and return only JSON file without missing any details."
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        } 
        payload0 = {
            "model": "gpt-4-vision-preview",
            "messages": [
            {
                "role": "user",
                
                "content": [
                {
                    "type": "text",
                    "text": prompt
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

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload0)

        response.raise_for_status()  # Raise an error if the request failed
        # text_content = response.text
        # response = response.json()
        # print(response)
        response = response.json()['choices'][0]['message']['content']
        response_data_formatted = extract_json_content(response)
        response_data2 = json.loads(response_data_formatted)
        counter += 1
        filename = 'image_' + str(counter) + '.json'
        json_file_path = os.path.join(output_folder, filename)
        # text_file_paths.append(text_file_path)
        # with open(text_file_path, 'w') as text_file:
        #     text_file.write(response_data2)
        
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(response_data2, json_file, ensure_ascii=False, indent=4)

        print(f"Saved JSON response for {image_path} to {json_file_path}")
        # Save the response to a text file
        # filename = os.path.splitext(os.path.basename(image_path))[0] + '.json'
        # text_file_path = os.path.join(output_folder, filename)
        # with open(text_file_path, 'w') as text_file:
        #     text_file.write(text_content)


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
    results_file_path = results_folder + 'ver_0_' + get_filename_without_extension(pdf_path) + '.json'
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
def call_end_to_end(pdf_path,save_path, json_filename):
    # return
    text_file_paths = []
    text_descriptions = []
    output_folder = 'output_ver_0/' + os.path.basename(pdf_path)[0:-4] + '/'
    images_folder = 'images/'  # Replace with your images directory path
    image_paths = pdf_to_images(pdf_path, images_folder)
    call_openai_and_save(image_paths, output_folder, api_token)
    combine_json_files(output_folder, pdf_path, save_path, json_filename)


# Main code
# Paths for the PDF, images folder, and output folder
pdf_path = ''  # Replace with the path to your PDF file

# Check if a command line argument is provided
if len(sys.argv) > 1:
    pdf_path = sys.argv[1]  # Take the PDF path from the first command line argument
else:
    pdf_path = pdf_path  # Use the default path if no argument is provided

print(f"Using PDF path: {pdf_path}")


output_folder = 'output_ver_0/'  + os.path.basename(pdf_path)[0:-4] + '/' # Replace with your output directory path

# Convert the PDF to images
image_paths = pdf_to_images(pdf_path)

print(image_paths)
# Call the OpenAI API and save the responses
call_openai_and_save(image_paths, output_folder, api_token)
combine_json_files(output_folder, pdf_path)
# Note: Replace the placeholder paths and API token with your actual data and credentials.
