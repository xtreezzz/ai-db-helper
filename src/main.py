# main.py

import json
import re
from error_log import error_log
from prompt_builder import build_prompt
from openai_client import get_assistant_response

def main():
    # Retrieve 'errmsg_context' safely; default to empty string if not present
    errmsg_context = error_log.get('errmsg_context', '').strip()

    # Initialize the base structure of the output JSON with fields from error_log
    output_json = {
        "log": error_log.get("log", ""),
        "severity_level": error_log.get("severity_level", ""),
        "errmsg_template": error_log.get("errmsg_template", ""),
        "errmsg_variables": error_log.get("errmsg_variables", []),
        "errcode": error_log.get("errcode", ""),
        "errcode_numeric": error_log.get("errcode_numeric", ""),
        "errmsg_clean": error_log.get("errmsg_clean", ""),
        "script_parse_error": error_log.get("script_parse_error", None)
    }

    if errmsg_context:
        # If 'errmsg_context' exists and is not empty, transfer it without calling OpenAI API
        print("Found 'errmsg_context'. Transferring context without calling OpenAI API.")

        # Add 'context' to the output JSON
        output_json["context"] = errmsg_context

        # Save to file
        with open('parsed_logs_success.json', 'w', encoding='utf-8') as f:
            json.dump(output_json, f, ensure_ascii=False, indent=4)

        print("Context successfully transferred to 'parsed_logs_success.json'.")
    else:
        # If 'errmsg_context' is missing or empty, proceed with OpenAI API processing
        print("'errmsg_context' is missing or empty. Proceeding with OpenAI API processing.")
        prompt = build_prompt(error_log)
        assistant_reply = get_assistant_response(prompt)

        # Temporary print for debugging
        print("Full assistant reply:")
        print(assistant_reply)

        try:
            # Extract JSON content between ```json and ```
            json_pattern = r'```json\s*(\{.*?\})\s*```'
            match = re.search(json_pattern, assistant_reply, re.DOTALL)
            if not match:
                raise ValueError("JSON content not found in the assistant's reply.")

            json_content = match.group(1)

            # Parse the JSON
            result_json = json.loads(json_content)

            # Extract necessary fields from the assistant's response
            original_query = result_json.get('query', '')
            solution_explanation = result_json.get('solution', {}).get('explanation', '')
            correct_query = result_json.get('solution', {}).get('correct_query', '')
            ddl = result_json.get('ddl', '')
            context = result_json.get('context', '')

            # Update the output JSON with the extracted fields
            output_json.update({
                "original_query": original_query,
                "solution_explanation": solution_explanation,
                "correct_query": correct_query,
                "ddl": ddl,
                "context": context
            })

            # Save the updated JSON to file
            with open('parsed_logs_success.json', 'w', encoding='utf-8') as f:
                json.dump(output_json, f, ensure_ascii=False, indent=4)

            print("Original Query, explanation, corrected query, DDL, and Context added to 'parsed_logs_success.json'.")

        except json.JSONDecodeError as jde:
            print("JSON parsing error:")
            print(str(jde))
            print("Assistant's reply was:")
            print(assistant_reply)
        except Exception as e:
            print("An error occurred while processing the assistant's reply:")
            print(str(e))
            print("Assistant's reply was:")
            print(assistant_reply)

if __name__ == '__main__':
    main()
