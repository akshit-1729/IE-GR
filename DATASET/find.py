# Description: This file contains the implementation of the find_in_json function,
# which is used to search for a key in a nested dictionary structure and return its value.
def find_in_json(data, key_to_find):
    """
    Search for a key in a nested dictionary structure 
    and return its value.
    Args:
    - data: The dictionary to search in.
    - key_to_find: The key to search for in the dictionary.

    Returns:
    - The value corresponding to the key if found, None otherwise.
    """
    # Base case: if data is not a dictionary, return None
    if not isinstance(data, dict):
        return None

    # Check if the key is in the current dictionary
    if key_to_find in data:
        return data[key_to_find]

    # Recursive case: search in nested dictionaries
    for key, value in data.items():
        if isinstance(value, dict):
            result = find_in_json(value, key_to_find)
            if result is not None:
                return result
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    result = find_in_json(item, key_to_find)
                    if result is not None:
                        return result
    # If key is not found in any level, return None
    return None

def find_all_in_json(data, key_to_find):
    """
    Search for all occurrences of a key in a nested dictionary structure 
    and return all unique values, or None if no matches are found.
    
    Args:
    - data: The dictionary to search in.
    - key_to_find: The key to search for in the dictionary.

    Returns:
    - A set of unique values corresponding to the key, or None if no matches are found.
    """
    found_values = set()

    # Base case: if data is not a dictionary, return an empty set
    if not isinstance(data, dict):
        return found_values

    # Check if the key is in the current dictionary
    if key_to_find in data:
        found_values.add(data[key_to_find])

    # Recursive case: search in nested dictionaries
    for key, value in data.items():
        if isinstance(value, dict):
            result = find_all_in_json(value, key_to_find)
            if result:  # Only update if result is not None or empty
                found_values.update(result)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    result = find_all_in_json(item, key_to_find)
                    if result:  # Only update if result is not None or empty
                        found_values.update(result)

    # Return None if no values were found, otherwise return the set of found values
    return found_values if found_values else None
