# Genomic Report Data Generation and Processing

## Project Overview

This project aims to generate synthetic genomic reports, process them, convert them into a standardized format, and extract information from PDF reports using AI. The system is designed for research and development purposes in the fields of medical informatics and bioinformatics.

## Key Components

1. **Data Generation (`generate_json.py`)**: Creates synthetic genomic report data in JSON format.
2. **PDF Report Generation (`reportlab_doc.py` and `reportlab_doc2.py`)**: Converts JSON data into visually rich PDF reports.
3. **Data Processing (`generate_data.py`)**: Orchestrates the overall process of generating and processing data.
4. **JSON Splitting (`split_json.py`)**: Splits the generated JSON files into multiple parts for easier handling.
5. **Standardization (`to_std_format.py`)**: Converts the generated data into a standardized format for consistency and easier analysis.
6. **PDF Information Extraction (`icon.ipynb`)**: Extracts key-value pairs from PDF reports using OpenAI's GPT-4 vision model.
7. **Utility Functions (`find.py`)**: Provides functions for searching and extracting data from nested JSON structures.

## Detailed Component Description

### 1. Data Generation (`generate_json.py`)

This script generates synthetic genomic report data in JSON format. It includes:

- Patient details
- Specimen information
- Genomic variants
- Immunotherapy markers
- FDA-approved therapies
- Clinical trials
- Variants of unknown significance

The script uses the Faker library to generate realistic-looking data and custom providers for medical-specific information.

### 2. PDF Report Generation (`reportlab_doc.py` and `reportlab_doc2.py`)

These components take the JSON data and create visually rich PDF reports that mimic real genomic reports. They use the ReportLab library to:

- Create a structured layout
- Add patient and diagnosis information
- Include genomic variant details
- Display biomarkers and clinical trial information

### 3. Data Processing (`generate_data.py`)

This script coordinates the entire process:

- Generates JSON files using `generate_json.py`
- Creates PDF reports using `reportlab_doc.py` or `reportlab_doc2.py`
- Processes a specified number of reports (default: 50)

### 4. JSON Splitting (`split_json.py`)

This utility script splits the generated JSON files into three parts based on specific keys. This can be useful for handling large datasets or focusing on specific sections of the reports.

### 5. Standardization (`to_std_format.py`)

This script converts the generated data into a standardized format. It extracts and reorganizes information from the original JSON files into a consistent structure, including:

- Patient information
- Diagnosis details
- Cancer information
- Biomarkers
- Therapeutic information
- Clinical trials
- Variants of unknown significance

### 6. PDF Information Extraction (`icon.ipynb`)

This Jupyter notebook provides functionality to extract information from PDF genomic reports using OpenAI's GPT-4 vision model. Key features include:

- Conversion of PDF pages to images
- Sending images to OpenAI's API for analysis
- Extracting key-value pairs from the AI's response
- Converting the extracted information into a structured JSON format

### 7. Utility Functions (`find.py`)

This module contains utility functions for searching and extracting data from nested JSON structures:

- `find_in_json`: Searches for a specific key in a nested dictionary and returns its value.
- `find_all_in_json`: Searches for all occurrences of a key in a nested dictionary and returns all unique values.

## Usage

1. Set up the required environment (Python 3.x with necessary libraries).
2. Run `generate_data.py` to start the data generation and processing pipeline.
3. Use `split_json.py` if you need to split the generated JSON files.
4. Run `to_std_format.py` to convert the data into the standardized format.
5. For PDF information extraction:
   - Ensure you have the required libraries installed (`openai`, `pdf2image`, etc.)
   - Set up your OpenAI API key in the `icon.ipynb` notebook
   - Run the notebook, providing the path to the folder containing PDF reports
   - The script will process each PDF, extract information, and save it as both text and JSON files

## Data Dictionary

The project uses various medical terminologies and concepts. Key terms include:

- Somatic and Germline variants
- Tumor Mutational Burden (TMB)
- Microsatellite Instability (MSI)
- FDA-approved therapies
- Clinical trial phases
- Variants of Unknown Significance (VUS)
- Immunotherapy markers

## Limitations and Considerations

- The generated data is synthetic and should not be used for real medical decisions.
- The system aims to mimic real genomic reports but may not capture all complexities of actual clinical data.
- The standardized format may need adjustments based on specific research or analysis needs.
- The PDF information extraction process relies on the accuracy of the AI model and may require human verification for critical applications.

## Future Enhancements

- Incorporate more diverse and complex genomic profiles
- Enhance the realism of generated clinical trials and therapies
- Implement more sophisticated data validation and quality checks
- Develop a user interface for easier data generation and customization
- Improve the accuracy and robustness of the PDF information extraction process
- Integrate the PDF extraction process with the existing data generation pipeline

## Contributors

Akshit Varmora, Jay Gorakhiya, Tamali Banerjee
