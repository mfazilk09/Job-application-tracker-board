from authenticate import gmail
import base64

def get_full_email(email_id):
    # Fetch the full payload from the Gmail API
    full_email_data = gmail.users().messages().get(
        userId='me', 
        id=email_id, 
        format='full'
    ).execute()
    
    # We need to dig through the payload to find the HTML body
    payload = full_email_data['payload']
    
    def extract_html(part):
        if 'parts' in part:
            for nested_part in part['parts']:
                result = extract_html(nested_part)
                if result:
                    return result
        elif part.get('mimeType') == 'text/html':
            return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        return ""

    raw_html = extract_html(payload)
    
    # Optional: strip the heavy <style> blocks to save tokens before sending to LLM
    if raw_html:
        raw_html = raw_html.split('<style>')[0] 
        
    return raw_html