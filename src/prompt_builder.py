# prompt_builder.py

from config import LANGUAGE, DATABASE

def build_prompt(error_log):
    # Safely retrieve 'errmsg_context'; default to empty string if not present
    errmsg_context = error_log.get('errmsg_context', '')

    prompt = (
        f"""
You are to assist a junior developer in understanding and fixing SQL errors in {DATABASE} database queries. Given an error message from {DATABASE} and an optional context specific to the organization, generate:

- An example query that could produce this error using the Chinook database.
- An explanation of why the error occurs (in {LANGUAGE}).
- A corrected query with an explanation.
- Relevant DDL statements from the Chinook database schema.

**Important:** Provide your answer in **valid JSON format**, ensuring all strings are properly escaped (e.g., backslashes as `\\n` and quotes as `\\"`). Do not include any additional text or explanations outside of the JSON block.

Provide your answer in the following JSON format:

```json
{{
  "query": "<original_query>",
  "error": {{
    "message": "<error_message>",
    "type": "<error_type>",
    "code": "<error_code>"
  }},
  "solution": {{
    "correct_query": "<corrected_query>",
    "explanation": "<detailed_explanation>"
  }},
  "ddl": {{
    // Include relevant DDL statements here
  }},
  "context": "<context_information>"
}}
```

**Few-Shot Example**

```json
{{
    "query": "SELECT artists.name, COUNT(albums.albumid) FROM artists JOIN albums ON artists.artistid = albums.artistid;",
    "error": {{
      "message": "ERROR: column \"artists.name\" must appear in the GROUP BY clause or be used in an aggregate function",
      "type": "Group By Error",
      "code": "42803"
    }},
    "solution": {{
      "correct_query": "SELECT artists.name, COUNT(albums.albumid) FROM artists JOIN albums ON artists.artistid = albums.artistid GROUP BY artists.name;",
      "explanation": "The error occurs because the column 'artists.name' is not included in the GROUP BY clause when using an aggregate function (COUNT). To fix the error, add 'artists.name' to the GROUP BY clause."
    }},
    "ddl": {{
      "artists": "CREATE TABLE artists (\\n  artistid INTEGER PRIMARY KEY,\\n  name VARCHAR(120)\\n);",
      "albums": "CREATE TABLE albums (\\n  albumid INTEGER PRIMARY KEY,\\n  title VARCHAR(160),\\n  artistid INTEGER REFERENCES artists(artistid)\\n);"
    }},
    "context": ""
}}
```

**Your Task**

Given the following error message and optional context:

- **Error Message:**

  "ERROR: {error_log['errmsg_clean']}"

- **Context:**

  "{errmsg_context}"

Generate an example as shown above, using the Chinook database, to help a junior developer understand and fix the error. The explanation should be in {LANGUAGE}. If the `context` field is not empty, incorporate it into the explanation to align with the organization's specific rules and policies.
""")
    return prompt
