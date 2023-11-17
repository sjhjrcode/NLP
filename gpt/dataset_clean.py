import csv
import json

# Function to convert CSV data to the specified JSON format, excluding the first row
def csv_to_json_exclude_first_row(csv_filepath):
    json_data = {"messages": []}

    # Adding the initial system message
    system_message = {
        "role": "system",
        "content": "Cassy is a home health care assistant that helps dementia patients by classifying their given sentences into intent and NER."
    }
    json_data["messages"].append(system_message)

    # Read CSV and convert to JSON, skipping the first row
    with open(csv_filepath, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row
        for row in reader:
            # Assuming the CSV format is: description, category, NER
            user_message = {"role": "user", "content": row[0]}
            assistant_message = {"role": "assistant", "content": f"{row[1]};{row[2]}"}

            json_data["messages"].append(user_message)
            json_data["messages"].append(assistant_message)

    return json_data

# Convert the uploaded CSV file to JSON
csv_filepath = './your_file.csv'
json_output_excluding_first = csv_to_json_exclude_first_row(csv_filepath)

# Displaying a part of the JSON for verification
json_output_part_excluding_first = json.dumps(json_output_excluding_first, indent=4)[:500]  # Display first 500 characters for brevity
json_output_part_excluding_first
json_filename = './converted_data.json'
def save_as_jsonl(json_data, jsonl_filepath):
    with open(jsonl_filepath, 'w', encoding='utf-8') as file:
        for message in json_data["messages"]:
            json.dump(message, file)
            file.write('\n')

# File path for JSONL file
jsonl_filepath = './converted_data.jsonl'

# Saving the data as JSONL
#save_as_jsonl(json_output_excluding_first, jsonl_filepath)

#jsonl_filepath

# Corrected function to save the JSON data as JSONL in the specified format
def save_as_jsonl_corrected_format(json_data, jsonl_filepath):
    with open(jsonl_filepath, 'w', encoding='utf-8') as file:
        for i in range(1, len(json_data["messages"]), 2):  # Skip the system message and process pairs of user and assistant messages
            combined_data = {
                "messages": [
                    json_data["messages"][0],  # System message
                    json_data["messages"][i],  # User message
                    json_data["messages"][i + 1]  # Assistant message
                ]
            }

            json.dump(combined_data, file)
            file.write('\n')

# File path for the corrected JSONL file
jsonl_corrected_format_filepath = './converted_data_corrected_format.jsonl'

# Saving the data as JSONL in the corrected format
save_as_jsonl_corrected_format(json_output_excluding_first, jsonl_corrected_format_filepath)

jsonl_corrected_format_filepath
#broken fix later 
import random

# Splitting the data into training (70%) and validation (30%)
def split_data(json_data, split_ratio=0.7):
    total_messages = len(json_data["messages"]) - 1  # Exclude the system message
    num_train = int(total_messages * split_ratio) // 2 * 2  # Ensure even number for pairs

    # Shuffle and split indices (starting from 1 to skip system message)
    indices = list(range(1, total_messages + 1))
    random.shuffle(indices)
    train_indices = indices[:num_train]
    validation_indices = indices[num_train:]

    # Splitting the data
    train_data = {"messages": [json_data["messages"][0]] + [json_data["messages"][i] for i in train_indices]}
    validation_data = {"messages": [json_data["messages"][0]] + [json_data["messages"][i] for i in validation_indices]}

    return train_data, validation_data

# Split the data
train_data, validation_data = split_data(json_output_excluding_first)

# Saving the training and validation data as JSONL
train_jsonl_filepath = './train_data.jsonl'
validation_jsonl_filepath = './validation_data.jsonl'

save_as_jsonl_corrected_format(train_data, train_jsonl_filepath)
save_as_jsonl_corrected_format(validation_data, validation_jsonl_filepath)
# Function to save the split data as JSONL while maintaining the original format
def save_split_data_as_jsonl(original_json_data, train_data, validation_data, train_filepath, validation_filepath):
    with open(train_filepath, 'w', encoding='utf-8') as train_file, \
         open(validation_filepath, 'w', encoding='utf-8') as validation_file:

        # Function to write data in specified format
        def write_data(file, data_indices):
            for i in data_indices:
                combined_data = {
                    "messages": [
                        original_json_data["messages"][0],  # System message
                        original_json_data["messages"][i],  # User message
                        original_json_data["messages"][i + 1]  # Assistant message
                    ]
                }
                json.dump(combined_data, file)
                file.write('\n')

        # Write training data
        write_data(train_file, range(1, len(train_data["messages"]), 2))

        # Write validation data
        write_data(validation_file, range(1, len(validation_data["messages"]), 2))

# Save the split data as JSONL in the correct format
save_split_data_as_jsonl(json_output_excluding_first, train_data, validation_data, train_jsonl_filepath, validation_jsonl_filepath)

