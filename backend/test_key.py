# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# load_dotenv()
# api = os.getenv("GEMINI_API_KEY")
# print("Loaded key:", api)

# genai.configure(api_key=api)

# model = genai.GenerativeModel("models/gemini-1.0-pro")
# response = model.generate_content("Hello!")
# print(response.text)


import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api = os.getenv("GEMINI_API_KEY")
print("Loaded key:", api)

genai.configure(api_key=api)

# ⬅️ FIX: Try the raw, shortest, most common identifier for the fast model
model = genai.GenerativeModel("gemini-2.5-flash") 

response = model.generate_content("Hello!")
print(response.text)