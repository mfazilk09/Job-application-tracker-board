import os
from google import genai
from google.genai import types
from LLMpayload import get_email_summaries
import json

def get_target_email_ids(email_summaries):
# Configure your Gemini API key (get this from Google AI Studio)
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Check your .env file and main.py load_dotenv() order.")

    # initialise the client
    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an AI assistant tracking job applications. 
    Review the following list of recent emails. Identify ANY email that looks like a job application confirmation, an invitation to interview, an online assessment, or a rejection.

    Return a JSON array of strings containing ONLY the 'id' of the relevant emails. If none are relevant, return an empty array [].

    Emails:
    {json.dumps(email_summaries, indent=2)}
    """

    # 4. Call the model
    response = client.models.generate_content(
        model='gemini-3.5-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1 # Keeps the AI focused and factual
        )
    )

    # Parse the LLM's response back into a Python list
    target_email_ids = json.loads(response.text)

    return target_email_ids

    print(f"Found {len(target_email_ids)} relevant job emails.")