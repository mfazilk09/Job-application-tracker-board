from datetime import datetime, timedelta, timezone

def create_job_task(tasks_service, llm_data, email_subject):
    """
    Creates a task in Google Tasks using the data extracted by the LLM.
    
    Args:
        tasks_service: The authenticated Google Tasks API client.
        llm_data: The Pydantic object (or dictionary) returned by Gemini.
        email_subject: The subject of the original email (for context).
    """
    
    # 1. Format the Task Title
    action_name = llm_data.action_type.replace('_', ' ').title() if llm_data.action_type else "Action Required"
    task_title = f"{action_name}: {email_subject}"
    
    # 2. Format the Task Notes (adding the URL)
    task_notes = "Automatically tracked job application.\n\n"
    if llm_data.action_url:
        task_notes += f"Link: {llm_data.action_url}"
        
    # 3. Handle the Deadline
    due_date = llm_data.deadline_rfc3339
    
    # If the LLM didn't find a deadline, default to 3 days from now
    if not due_date:
        print("No deadline found by LLM. Defaulting to 3 days from now.")
        future_date = datetime.now(timezone.utc) + timedelta(days=3)
        # Google Tasks requires RFC 3339 format
        due_date = future_date.isoformat() 

    # 4. Construct the API Payload
    task_body = {
        'title': task_title,
        'notes': task_notes,
        'due': due_date
    }
    
    try:
        # 5. Insert into the default task list ('@default')
        result = tasks_service.tasklists().tasks().insert(
            tasklist='@Jobs', 
            body=task_body
        ).execute()
        
        print(f"Success! Task created: {result.get('title')} (ID: {result.get('id')})")
        return result
        
    except Exception as e:
        print(f"Failed to create Google Task: {e}")
        return None