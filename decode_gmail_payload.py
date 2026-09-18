import os
from google import genai
from google.genai import types

# Import the JobAction schema from your new file
from define_data_schema import JobAction

def extract_job_details(raw_html):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Check your .env file.")
        
    client = genai.Client(api_key=api_key)

    prompt = f"""
    Analyze the following HTML email from a job application. 
    Find the main call-to-action link (like 'Start Assessment' or 'Schedule Interview') and any stated deadlines.
    
    Email HTML:
    {raw_html}
    """

    response = client.models.generate_content(
        model='gemini-3.5-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=JobAction, # This now references the imported class
            temperature=0.1
        ),
    )

    # Return the Pydantic object containing the structured data
    return response.parsed