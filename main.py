import os
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
        # Safely extract the ID and subject depending on how your list is formatted
        email_id = email['id'] if isinstance(email, dict) else email
        email_subject = email.get('subject', f'Email ID: {email_id}') if isinstance(email, dict) else f"Email ID: {email}"
        
        # Fetch the full HTML payload
        raw_html = get_full_email(email_id)
        
        # 5. Extract data and evaluate the gatekeeper flag in ONE call
        extracted_data = extract_job_details(raw_html)

        if DRY_RUN:
            print("--- DRY RUN MODE ---")
            if not extracted_data.is_actionable_task:
                print(f"Skipped irrelevant email: {email_subject}")
            else:
                print(f"Actionable Task Found: {email_subject}")
                print(f"  Dynamic Title: {extracted_data.task_type} - {extracted_data.company_name}")
                print(f"  URL: {extracted_data.action_link}")
                print(f"  Deadline: {extracted_data.deadline}")
        else:
            # 6. Actually create the task using your dedicated function
            create_job_task(tasks, extracted_data, email_subject)

if __name__ == "__main__":
    run_pipeline()