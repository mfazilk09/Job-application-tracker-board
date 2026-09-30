from datetime import datetime, timedelta, timezone

def create_job_task(tasks_service, llm_data, email_subject):
    """
    Creates a task in Google Tasks using the data extracted by the LLM.
    
    Args:
        tasks_service: The authenticated Google Tasks API client.
        llm_data: The Pydantic object returned by Gemini.
        email_subject: The subject of the original email (for context).
    """
    
    # 1. Gatekeeper: Skip if the LLM flagged this as a general alert/schedule
    if not llm_data.is_actionable_task:
        print(f"Skipping non-actionable email: {email_subject}")
        return None

    # 2. Format the Task Title (e.g., "Online Assessment - PwC")
    company = llm_data.company_name if llm_data.company_name else "Unknown Company"
    task_type = llm_data.task_type if llm_data.task_type else "Task"
    task_title = f"{task_type} - {company}"
    
    # 3. Format the Task Notes (adding the URL and original subject)
    task_notes = f"Automatically tracked job application.\nOriginal Subject: {email_subject}\n\n"
    if llm_data.action_link:
        task_notes += f"Link: {llm_data.action_link}"
        
    # 4. Handle the Deadline
    due_date = llm_data.deadline
    
    # If the LLM didn't find a deadline, default to 3 days from now
    if not due_date or str(due_date).lower() == "none":
        print(f"No deadline found for {company}. Defaulting to 3 days from now.")
        future_date = datetime.now(timezone.utc) + timedelta(days=3)
        due_date = future_date.isoformat() 

    # 5. Construct the API Payload
    task_body = {
        'title': task_title,
        'notes': task_notes,
        'due': due_date
    }
    
    try:
        # 6. Insert the task
        # Fixed the resource hierarchy: tasks().insert() instead of tasklists().tasks().insert()
        result = tasks_service.tasks().insert(
            tasklist='@default', # Use '@default' or your specific Job list ID
            body=task_body
        ).execute()
        
        print(f"Success! Task created: {result.get('title')} (ID: {result.get('id')})")
        return result
        
    except Exception as e:
        print(f"Failed to create Google Task: {e}")
        return None