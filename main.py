import os
import time
from dotenv import load_dotenv

# 1. Load variables first
load_dotenv()

# 2. Import FUNCTIONS
from authenticate import tasks
from LLMpayload import get_email_summaries
from fetch_emails import get_full_email
from decode_gmail_payload import extract_job_details
from task_creation import create_job_task # <-- Import your updated function!

def run_pipeline():
    DRY_RUN = False

    # 3. Get recent emails
    emails = get_email_summaries() 
    
    if not emails:
        print("No recent emails found.")
        return

    # 4. Loop directly through the emails (bypassing the obsolete classification step)
    for email in emails:
        email_id = email['id'] if isinstance(email, dict) else email
        email_subject = email.get('subject', f'ID: {email_id}') if isinstance(email, dict) else "Email"
        
        raw_html = get_full_email(email_id)
        
        # 1. Extract the dynamic data using Gemini
        extracted_data = extract_job_details(raw_html)

        # --- ADD THIS SAFETY CHECK ---
        if not extracted_data:
            print(f"⚠️ Gemini failed to extract data for: {email_subject}. Skipping...")
            continue 
        # -----------------------------

        if DRY_RUN:
            print(f"DRY RUN: Would create '{extracted_data.task_type} - {extracted_data.company_name}'")
        else:
            # 2. Use the dynamic creation function (NO hardcoded task_body here)
            task_result = create_job_task(tasks, extracted_data, email_subject)
            
            # 3. Prevent duplicates: mark as read if the task was created
            if task_result:
                # Make sure to pass your initialized Gmail service object here
                from authenticate import gmail
                from fetch_emails import mark_as_read
                
                mark_as_read(email_id, gmail)

        print("Pausing for 5 seconds to respect Gemini API limits...")
        time.sleep(5)

if __name__ == "__main__":
    run_pipeline()