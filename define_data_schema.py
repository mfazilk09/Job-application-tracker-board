from pydantic import BaseModel, Field
from typing import Optional

class JobActionItem(BaseModel):
    is_actionable_task: bool = Field(description="True ONLY if this is a direct invitation for a job interview, test, or assessment. False for job alerts, newsletters, or non-job schedules.")
    company_name: str = Field(description="The name of the company, e.g., 'PwC'")
    task_type: str = Field(description="A short summary of the task, e.g., 'Online Assessment' or 'Video Interview'")
    action_link: str = Field(description="The URL to start the assessment or join the interview")
    deadline: str = Field(description="RFC 3339 formatted date. If relative (e.g. '7 days'), calculate it based on today's date.")