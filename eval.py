
import json
import os
import re
from typing import Any, Dict, List, Union

# Key mappings
KEY_MAPPING = {
    "Patient Name": "Name",
    "Doctor Name": "Doctor's Name",
    "Laboratory Medical Director ": "Laboratory Medical Director",
    "Low-Coverage Regions": "List of Low-Coverage Regions",
    "Variant Allele Fraction": "Variant Allele Fraction (VAF)",
    "DNA Mutation Description": "DNA Mutation Description",
    "Method of Detection ": "Method of Detection",
    "FDA-Approved Therapies for Current Diagnosis": "FDA-Approved Therapies for Current Diagnosis",
    "FDA-Approved Therapies for Other Indications": "FDA-Approved Therapies for Other Indications",
    "DNA Alteration": "DNA Alteration",
    
}

EQUIVALENT_VALUES = {
    "N/A": ["Not provided", "Not explicitly stated", "N/A", "Null", "None", "Not applicable"],
    "Method Undefined": ["Not explicitly stated, assumed NGS", "Assumed NGS"],
    "GOF": ["Gain of Function", "Gain of Function (GOF)", "GOF"],
    "LOF": ["Loss of Function", "Loss of Function (LOF)", "LOF"],
    "targeted therapy": ["Targeted Therapy"],
}

def load_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        content = file.read()
        # Find the content between the first { and the last }
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            json_content = match.group()
            return json.loads(json_content)
        else:
            raise ValueError(f"No valid JSON object found in {file_path}")

def get_mapped_key(key: str) -> str:
    return KEY_MAPPING.get(key, key)

def normalize_value(value: Any) -> Any:
    str_value = str(value).strip().lower()
    str_value = str_value.rstrip('%')
    if isinstance(value, str):
        for norm_value, equiv_values in EQUIVALENT_VALUES.items():
            if value in equiv_values:
                return norm_value
    return str_value

def are_values_equivalent(value1: Any, value2: Any) -> bool:
    norm_value1 = normalize_value(value1)
    norm_value2 = normalize_value(value2)
    return norm_value1 == norm_value2

def compare_json(gt_data: Dict[str, Any], op_data: Dict[str, Any]) -> Dict[str, Union[int, float, List[str]]]:
    total_pairs = 0
    correct_pairs = 0
    incorrect_pairs = []

    def recursive_compare(gt_obj: Any, op_obj: Any, path: str = ""):
        nonlocal total_pairs, correct_pairs, incorrect_pairs

        if isinstance(gt_obj, dict):
            if not isinstance(op_obj, dict):
                total_pairs += 1
                incorrect_pairs.append(f"{path}: Expected dict, got {type(op_obj).__name__}")
                return
            for key, gt_value in gt_obj.items():
                mapped_key = get_mapped_key(key)
                new_path = f"{path}.{key}" if path else key
                op_value = op_obj.get(mapped_key)

                if op_value is None:
                    total_pairs += 1
                    incorrect_pairs.append(f"{new_path}: Missing in output")
                elif isinstance(gt_value, (dict, list)):
                    recursive_compare(gt_value, op_value, new_path)
                else:
                    total_pairs += 1
                    if are_values_equivalent(gt_value, op_value):
                        correct_pairs += 1
                    else:
                        incorrect_pairs.append(f"{new_path}: Expected {gt_value}, got {op_value}")

        elif isinstance(gt_obj, list):
            if not isinstance(op_obj, list):
                total_pairs += 1
                incorrect_pairs.append(f"{path}: Expected list, got {type(op_obj).__name__}")
                return
            for i, (gt_item, op_item) in enumerate(zip(gt_obj, op_obj)):
                recursive_compare(gt_item, op_item, f"{path}[{i}]")
            if len(gt_obj) > len(op_obj):
                for i in range(len(op_obj), len(gt_obj)):
                    total_pairs += 1
                    incorrect_pairs.append(f"{path}[{i}]: Missing in output")

    recursive_compare(gt_data, op_data)

    accuracy = (correct_pairs / total_pairs) * 100 if total_pairs > 0 else 0

    return {
        "total_pairs": total_pairs,
        "correct_pairs": correct_pairs,
        "accuracy": round(accuracy, 2),
        "incorrect_pairs": incorrect_pairs
    }

def main():
    gt_dir = "" #Ground truth directory
    op_dir = "" #Output directory

    total_accuracy = 0
    processed_files = 0
    skipped_files = []

    for i in range(1, 51):  
        gt_file = os.path.join(gt_dir, f"fgr2_{i}.json")
        op_file = os.path.join(op_dir, f"doc2_{i}.json")

        print(f"\nProcessing pair {i}:")
        if not os.path.exists(gt_file):
            print(f"  Error: Ground truth file not found at {gt_file}")
            skipped_files.append(i)
            continue
        if not os.path.exists(op_file):
            print(f"  Error: Output file not found at {op_file}")
            skipped_files.append(i)
            continue

        try:
            gt_data = load_json(gt_file)
            op_data = load_json(op_file)

            result = compare_json(gt_data, op_data)

            print(f"  Total key-value pairs: {result['total_pairs']}")
            print(f"  Correctly matched pairs: {result['correct_pairs']}")
            print(f"  Accuracy: {result['accuracy']}%")
            print(f"  Number of incorrect pairs: {len(result['incorrect_pairs'])}")

            if result['incorrect_pairs']:
                print("\n  Incorrect pairs:")
                for pair in result['incorrect_pairs'][:]:  # Print only first 5 incorrect pairs
                    print(f"    {pair}")
                if len(result['incorrect_pairs']) > 5:
                    print(f"    ... and {len(result['incorrect_pairs']) - 5} more.")

            total_accuracy += result['accuracy']
            processed_files += 1

        except Exception as e:
            print(f"  Error processing file pair {i}: {str(e)}")
            skipped_files.append(i)

    if processed_files > 0:
        average_accuracy = total_accuracy / processed_files
        print(f"\nAverage accuracy across {processed_files} file pairs: {average_accuracy:.2f}%")
    else:
        print("\nNo files were successfully processed.")

    if skipped_files:
        print(f"\nSkipped file pairs: {', '.join(map(str, skipped_files))}")

if __name__ == "__main__":
    main()