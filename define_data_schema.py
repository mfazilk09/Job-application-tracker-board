from pydantic import BaseModel, Field
from typing import Optional

class JobAction(BaseModel):
    action_url: Optional[str] = Field(
        description="The exact URL for the main call-to-action (e.g., taking an assessment, booking an interview). Ignore privacy policies, social media, or generic company homepage links."
    )
    action_type: Optional[str] = Field(
        description="Categorize the link: 'assessment', 'interview_booking', 'portal_login', or 'other'."
    )
    deadline_rfc3339: Optional[str] = Field(
        description="The deadline or scheduled time mentioned in the email, strictly formatted as an RFC 3339 timestamp (e.g., '2026-09-15T12:00:00.000Z')."
    )