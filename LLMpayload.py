from authenticate import gmail

# Fetch emails from the last 2 days in the Primary inbox
def get_email_summaries():
    results = gmail.users().messages().list(
        userId='me', 
        q='newer_than:2d -in:trash'
    ).execute()

    messages = results.get('messages', [])

    email_summaries = []

    for msg in messages:
        # Fetching with format='metadata' is much faster than fetching the full body
        msg_data = gmail.users().messages().get(
            userId='me', id=msg['id'], format='metadata', 
            metadataHeaders=['Subject', 'From']
        ).execute()
        
        headers = {header['name']: header['value'] for header in msg_data['payload']['headers']}
        
        email_summaries.append({
            "id": msg['id'],
            "from": headers.get('From', 'Unknown'),
            "subject": headers.get('Subject', 'No Subject'),
            "snippet": msg_data.get('snippet', '')
        }) 

    return email_summaries