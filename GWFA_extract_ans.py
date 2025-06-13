import re
import argparse

def extract_data_from_file(file_path):
    # Initialize a list to store the extracted values for each execution
    all_data = []

    # Open and read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # Split the content by "Final Edit Distance" to separate each execution's result
        # Assuming "Final Edit Distance" is present at the start of each execution
        executions = content.split("Final Edit Distance ")
        
        # Iterate through each execution (excluding the first part before the first result)
        for execution in executions[1:]:
            data = {}

            # Extract Final Edit Distance using regex
            final_edit_distance_match = re.search(r"Final Edit Distance\s+:\s+(\d+)", execution)
            if final_edit_distance_match:
                data['final_edit_distance'] = int(final_edit_distance_match.group(1))

            # Extract Final Ending Position
            final_ending_position_match = re.search(r"Final Ending Position\s+:\s+\((\d+),\s*(\d+)\)", execution)
            if final_ending_position_match:
                data['final_ending_position'] = (int(final_ending_position_match.group(1)),
                                                  int(final_ending_position_match.group(2)))

            # Extract Precision
            precision_match = re.search(r"Precision\s+=\s+abs\(Golden-Yours\) / Golden\s+:\s+([\d\.]+)", execution)
            if precision_match:
                data['precision'] = float(precision_match.group(1))

            # Extract MIS/INS/DEL times
            mis_ins_del_match = re.search(r"Your MIS/INS/DEL times\s+:\s+(\d+)", execution)
            if mis_ins_del_match:
                data['mis_ins_del_times'] = int(mis_ins_del_match.group(1))

            # Extract Traceback result 
            traceback_result_match = re.search(r"Your Traceback result matches with your edit distance!", execution)
            if traceback_result_match:
                data['traceback_result'] = True  # Indicates that the traceback result matches with the edit distance

            # Append the extracted data for this execution to the list
            all_data.append(data)

    return all_data




parser = argparse.ArgumentParser(description="which folder")
parser.add_argument('len', type=str, help="length of pbsim3 sequence")

args     = parser.parse_args()
length   = args.len


file_path = f"GWFA_{length}.txt"  # Replace with your actual file path
all_extracted_data = extract_data_from_file(file_path)


# Extract the precision values from the data
precisions = [data['precision'] for data in all_extracted_data if 'precision' in data]

# Calculate average, max, and min precision
average_precision = sum(precisions) / len(precisions) if precisions else 0
max_precision = max(precisions) if precisions else 0
min_precision = min(precisions) if precisions else 0

print("-" * 50)
# Print the extracted data for each execution
for idx, data in enumerate(all_extracted_data, start=1):
    print(f"Data for execution {idx}:")
    for key, value in data.items():
        print(f"  {key}: {value}")
    print("-" * 50)

# Print average, max, and min precision
print(f"Average Precision: {average_precision:.4f}")
print(f"Max Precision: {max_precision:.4f}")
print(f"Min Precision: {min_precision:.4f}")
print("-" * 50)

# Optionally, write all extracted data to a new file
output_file = f"GWFA_{length}_extracted_results.txt"


with open(output_file, 'w') as f:
    for idx, data in enumerate(all_extracted_data, start=1):
        f.write(f"Execution {idx}:\n")
        for key, value in data.items():
            f.write(f"  {key}: {value}\n")
        f.write("-" * 50 + "\n")

print(f"All extracted data has been written to {output_file}")


