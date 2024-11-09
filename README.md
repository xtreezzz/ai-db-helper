# AI Database Helper

## Overview

**AI Database Helper** is a Python-based tool designed to help junior developers understand and fix SQL errors in database queries using the Chinook database. It leverages OpenAI's GPT-4 model to generate detailed explanations, corrected queries, and relevant DDL statements based on error logs.

## Features

- **Automatic Error Analysis:** Parses error logs to identify SQL errors.
- **Contextual Explanations:** Incorporates organizational-specific context to provide tailored solutions.
- **JSON Output:** Generates structured JSON responses containing queries, explanations, and DDL statements.
- **Flexible Configuration:** Handles scenarios with or without additional contextual information.
- **Database Support:** Configurable to work with different databases (e.g., Greenplum, ClickHouse, Trino).

## Installation

### Prerequisites

- Python 3.7 or higher
- OpenAI API Key

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/xtreezzz/ai-db-helper.git
   cd ai-db-helper
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure OpenAI API Key and Settings**

   - Rename `config.py.example` to `config.py`.
   - Open `config.py` and replace `'YOUR_OPENAI_API_KEY'` with your actual OpenAI API key.
   - Set the `LANGUAGE` and `DATABASE` variables as needed.

   ```python
   # config.py

   OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'
   LANGUAGE = 'English'  # Default language for explanations
   DATABASE = 'Greenplum'  # Options: 'Greenplum', 'ClickHouse', 'Trino'
   ```

## Usage

1. **Prepare the Error Log**

   Modify the `error_log.py` file with the error details you want to analyze. Include or exclude the `errmsg_context` field based on your needs.

2. **Run the Script**

   ```bash
   python main.py
   ```

3. **View the Output**

   The output will be saved in `parsed_logs_success.json`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
