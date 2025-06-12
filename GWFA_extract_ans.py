import re

def extract_data_from_file(file_path):
    # Initialize a dictionary to store the extracted values
    data = {}

    # Open and read the file
    with open(file_path, 'r') as file:
        content = file.read()

        # Extract Final Edit Distance using regex
        final_edit_distance_match = re.search(r"Final Edit Distance\s+:\s+(\d+)", content)
        if final_edit_distance_match:
            data['final_edit_distance'] = int(final_edit_distance_match.group(1))

        # Extract Final Ending Position
        final_ending_position_match = re.search(r"Final Ending Position\s+:\s+\((\d+),\s*(\d+)\)", content)
        if final_ending_position_match:
            data['final_ending_position'] = (int(final_ending_position_match.group(1)),
                                              int(final_ending_position_match.group(2)))

        # Extract Precision
        precision_match = re.search(r"Precision\s+=\s+abs\(Golden-Yours\) / Golden\s+:\s+([\d\.]+)", content)
        if precision_match:
            data['precision'] = float(precision_match.group(1))

        # Extract MIS/INS/DEL times
        mis_ins_del_match = re.search(r"Your MIS/INS/DEL times\s+:\s+(\d+)", content)
        if mis_ins_del_match:
            data['mis_ins_del_times'] = int(mis_ins_del_match.group(1))

        # Extract Traceback result (optional)
        traceback_result_match = re.search(r"Your traceback result\s+:\s+(.*)", content)
        if traceback_result_match:
            data['traceback_result'] = traceback_result_match.group(1).strip()

    return data

# Example usage
file_path = 'your_file.txt'  # Replace with your actual file path
extracted_data = extract_data_from_file(file_path)

# Print the extracted data
for key, value in extracted_data.items():
    print(f"{key}: {value}")
    