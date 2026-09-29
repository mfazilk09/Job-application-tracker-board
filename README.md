[![Job Tracker Automation](https://github.com/mfazilk09/Job-application-tracker-board/actions/workflows/job_tracker.yml/badge.svg)](https://github.com/mfazilk09/Job-application-tracker-board/actions/workflows/job_tracker.yml)

## 🛠 Technical Architecture & Features

* **Automated Data Pipeline:** Architected a modular Python backend integrating Google Cloud Platform APIs (Gmail and Google Tasks) to seamlessly route job application action items from inbox to task manager.
* **LLM Parsing Engine:** Engineered an extraction pipeline using the Google GenAI SDK (Gemini 3.5 Flash-Lite) to parse dynamic URLs and enforce strictly formatted RFC 3339 deadlines from nested HTML email payloads.
* **Schema Validation:** Enforced strict data structuring using Pydantic, ensuring LLM outputs are returned as predictable, strongly-typed JSON objects for reliable API ingestion.
* **Secure Credential Management:** Implemented stateless OAuth 2.0 authentication, keeping API keys and refresh tokens out of source control using `.env` files locally and GitHub Secrets in production.
* **Continuous Deployment (CI/CD):** Automated pipeline execution via GitHub Actions on a 4-hour cron schedule, utilizing `requirements.txt` to manage dependencies in a virtual container.
* **Decoupled System Design:** Built a scalable architecture with isolated modules for authentication, fetching, classification, and decoding, alongside a `dry-run` safety mode to validate outputs without mutating the live database.
