import csv
import openai
import os 
# Load the CSV data
def load_data(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

# Use ChatGPT API for classification
def classify_sentence(sentence, api_key):
    response = openai.Completion.create(
        model="your-finetuned-model-name",  # Replace with your fine-tuned model name
        prompt=sentence,
        max_tokens=50,  # Adjust as necessary
        api_key=api_key
    )
    return response.choices[0].text.strip()

def main():
    filename = './your_file.csv'  # Replace with your CSV file path
    data = load_data(filename)
    api_key = os.getenv('OPENAI_API_KEY') # Replace with your OpenAI API key

    # Get input from user
    user_sentence = input("Enter a sentence for classification: ")

    # Classify the sentence using ChatGPT API
    classification_result = classify_sentence(user_sentence, api_key)

    # Output the result
    print(f"Classification Result: {classification_result}")

if __name__ == "__main__":
    main()