import csv
import openai
import os 
# Set your API key
openai.api_key =  os.getenv('OPENAI_API_KEY')



def query_model(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-1106:oklahoma-state-university::8LjAus7L",
            temperature=0.6,
            messages=[
                {"role": "system", "content":  "Cassy is a home health care assistant that helps dementia patients by classifying their given sentences into intent and NER."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    # Replace this with your actual prompt or data retrieval logic
prompt = "Where am I?"
    
    # Query the model
result = query_model(prompt)
    
    # Process the result as needed
print(result)