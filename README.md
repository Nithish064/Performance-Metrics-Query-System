# Performance Metrics Query System

This project allows users to query company performance metrics (e.g., GMV, revenue, profit) through a simple text-based interface. The system processes user input, extracts relevant company names, metrics, and dates, and generates structured JSON responses.

## Features:
- **Fuzzy Matching**: Handles minor typos and variations in company names and metrics.
- **Date Handling**: Supports both absolute and relative date queries (e.g., "last year," "this year").
- **Comparison Queries**: Allows users to compare performance metrics across multiple companies.
- **User Input**: Prompts users for queries and returns results in JSON format.

## Supported Companies:
- Flipkart
- Amazon
- Walmart
- Apple
- Microsoft

## Supported Metrics:
- GMV
- Revenue
- Profit
- Sales
- Loss

## Installation and Setup

### Prerequisites:
- Python 3.6 or higher.
- Required dependencies: `fuzzywuzzy` and `python-Levenshtein`.

### Steps to Run the Project:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/performance-metrics-query-system.git
   cd performance-metrics-query-system
Install Required Dependencies:

bash
Copy code
pip install fuzzywuzzy python-Levenshtein
Run the Script:

bash
Copy code
python app.py
Interact with the System: The application will prompt you to enter your queries. You can:

Query for performance metrics for a single company.
Compare performance metrics between companies.
Specify date ranges for the metrics (e.g., "last year" or "this year").
Example Queries:
"What was the GMV of Flipkart last year?"
"Provide the revenue for Amazon and Flipkart from Jan 2023 to Dec 2023."
"Compare the GMV of Amazon and Flipkart."
License:
This project is open-source and available under the MIT License.
