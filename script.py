import json
import re

def sort_region_keys(json_data):
    """
    Sort regions in format A-1, A-2, B-1, etc. alphabetically and numerically
    and ensure consistent property ordering within each region
    """
    regions = json_data["regions"]
    
    # Define a custom key function for sorting region keys
    def sort_key(key):
        # Split the key into letter and number parts
        parts = key.split('-')
        if len(parts) == 2:
            letter, number = parts
            # Return a tuple of the letter and the number as an integer
            return (letter, int(number))
        return key
    
    # Define property order to ensure consistency
    property_order = [
        "name",
        "points",
        "full_fill_percent",
        "empty_fill_percent",
        "brightness_threshold",
        "draw_bounding_box"
    ]
    
    # Get all keys and sort them
    sorted_keys = sorted(regions.keys(), key=sort_key)
    
    # Create a new dictionary with sorted keys and ordered properties
    sorted_regions = {}
    for key in sorted_keys:
        # Create a new ordered dict for this region
        region = regions[key]
        ordered_region = {}
        
        # Add properties in the defined order
        for prop in property_order:
            if prop in region:
                # Special handling for the points array to standardize x/y order
                if prop == "points" and isinstance(region[prop], list):
                    ordered_region[prop] = sort_points(region[prop])
                else:
                    ordered_region[prop] = region[prop]
        
        # Add any remaining properties that weren't in our predefined order
        for prop in region:
            if prop not in ordered_region:
                ordered_region[prop] = region[prop]
        
        sorted_regions[key] = ordered_region
    
    # Return a new JSON object with sorted regions and root properties
    # Define root property order
    root_property_order = [
        "camera",
        "enable_raw_readings",
        "person_detector",
        "draw_person_boxes",
        "regions"
    ]
    
    # Create new ordered root object
    result = {}
    
    # Add properties in the defined order
    for prop in root_property_order:
        if prop in json_data:
            result[prop] = json_data[prop] if prop != "regions" else sorted_regions
    
    # Add any remaining properties that weren't in our predefined order
    for prop in json_data:
        if prop not in result:
            result[prop] = json_data[prop]
            
    return result

def sort_points(points_list):
    """
    Ensure consistent ordering of coordinates within each point.
    This preserves the order of points in the array (which is important),
    but standardizes the order of x/y within each point.
    """
    standardized_points = []
    
    for point in points_list:
        # Create a new point with standardized key order
        new_point = {
            "x": point["x"],
            "y": point["y"]
        }
        standardized_points.append(new_point)
    
    return standardized_points

if __name__ == "__main__":
    import sys
    
    # Check if file name was provided as argument
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = f"sorted-{input_file}"
    else:
        input_file = 'config.json'
        output_file = 'sorted-config.json'
    
    # Read the JSON file
    with open(input_file, 'r') as file:
        json_data = json.load(file)
    
    # Sort the regions
    sorted_data = sort_region_keys(json_data)
    
    # Write the sorted data to a new file
    with open(output_file, 'w') as file:
        json.dump(sorted_data, file, indent=2)
    
    print(f'Sorted JSON saved to {output_file}')