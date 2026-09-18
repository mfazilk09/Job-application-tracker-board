import os
from dotenv import load_dotenv

# 1. Load variables first
load_dotenv()

# 2. Import FUNCTIONS, not variables
from authenticate import tasks
from LLMpayload import get_email_summaries
from LLMclassification import get_target_email_ids
from fetch_emails import get_full_email
from decode_gmail_payload import extract_job_details

def run_pipeline():
    DRY_RUN = False 

    # 3. Call the functions in order, passing data to the next step
    
    # (Note: Added parentheses to actually call the function)
    emails = get_email_summaries() 
    
    if not emails:
        print("No recent emails found.")
        return

    # Pass the emails to Gemini to find the target IDs
    target_ids = get_target_email_ids(emails)
    
    for email_id in target_ids:
        # Fetch the full HTML payload for each relevant email
        raw_html = get_full_email(email_id)
        
        # Extract the specific URL and deadline
        extracted_data = extract_job_details(raw_html)
        
        task_body = {
            'title': 'Complete Assessment for Acme Corp',
            'notes': f'Assessment Link: {extracted_data.action_url}',
            'due': extracted_data.deadline_rfc3339 
        }

        if DRY_RUN:
            print("--- DRY RUN MODE ---")
            print(f"Target Email Found: {email_id}")
            print(f"  URL: {extracted_data.action_url}")
            print(f"  Deadline: {extracted_data.deadline_rfc3339}")
        else:
            # Actually insert the task using the tasks() collection
            tasks.tasks().insert(
            tasklist='@default', 
            body=task_body
            ).execute()
            print("Task created successfully!")

if __name__ == "__main__":
    run_pipeline()