from openai import OpenAI
client = OpenAI()

client.files.create(
  file=open("converted_data.json", "rb"),
  purpose="fine-tune"
)


client.fine_tuning.jobs.create(
  training_file="converted_data.json", 
  model="gpt-4"
)