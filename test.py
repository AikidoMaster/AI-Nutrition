

import pandas as pd
import requests
import openai
import os

# Load the OpenAI API key from environment variables for security
openai.api_key = os.getenv("OPENAI_API_KEY", "Your_Key")

# Load a question from the CSV file
df = pd.read_csv("./data/ground-truth-retrieval.csv")
question = df.sample(n=1).iloc[0]['question']

print("Question:", question)

# Define the URL for the local server endpoint
url = "http://localhost:5000/question"
data = {"question": question}

try:
    # Send the POST request to the server
    response = requests.post(url, json=data)

    # Check the response status code and content
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    # Parse JSON if the response status code is 200 (OK)
    if response.status_code == 200:
        print("Response JSON:", response.json())
    else:
        print("Request failed with status code:", response.status_code)
        if response.headers.get("Content-Type") == "application/json":
            print("Error Details:", response.json())
        else:
            print("Server returned non-JSON response.")
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)

import pandas as pd

import requests

df = pd.read_csv("./data/ground-truth-retrieval.csv")
question = df.sample(n=1).iloc[0]['question']

print("question: ", question)

url = "http://localhost:5000/question"


data = {"question": question}

response = requests.post(url, json=data)
print(response.content)

