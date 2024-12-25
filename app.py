import datetime
import json
import re
from fuzzywuzzy import fuzz

# Function to extract company names, metrics, and dates from user query using regex
def extract_query_components(user_query, company_names, metrics):
    # Regex patterns to extract entity (company name), parameter (performance metric), and dates
    company_pattern = r"\b(?:{})\b".format("|".join(company_names))  # Dynamic company regex
    metric_pattern = r"\b(?:{})\b".format("|".join(metrics))  # Dynamic metric regex
    date_pattern = r"\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}|\d{4}-\d{1,2}-\d{1,2}|last year|this year|last quarter|previous month)\b"

    # Match company names and performance metrics
    company_match = re.search(company_pattern, user_query, re.IGNORECASE)
    metric_match = re.search(metric_pattern, user_query, re.IGNORECASE)
    date_matches = re.findall(date_pattern, user_query)

    # Use fuzzy matching if no exact match is found
    entity = None
    parameter = None
    for name in company_names:
        if fuzz.partial_ratio(name.lower(), user_query.lower()) > 80:  # Fuzzy match threshold
            entity = name
            break

    for metric in metrics:
        if fuzz.partial_ratio(metric.lower(), user_query.lower()) > 80:
            parameter = metric
            break

    # Extract dates
    start_date = None
    end_date = None
    if date_matches:
        start_date = date_matches[0] if len(date_matches) > 0 else None
        end_date = date_matches[1] if len(date_matches) > 1 else None

    return {"entity": entity, "parameter": parameter, "startDate": start_date, "endDate": end_date}

# Function to handle default dates and format dates into ISO 8601
def process_dates(start_date=None, end_date=None):
    today = datetime.date.today()
    one_year_ago = today - datetime.timedelta(days=365)

    # Handle relative date ranges like "last year", "this year", etc.
    if start_date == "last year":
        start_date = one_year_ago.replace(month=1, day=1).isoformat()
    elif start_date == "this year":
        start_date = today.replace(month=1, day=1).isoformat()

    if end_date == "last quarter":
        end_date = (today.replace(month=((today.month - 1) // 3 * 3) + 3, day=1) - datetime.timedelta(days=1)).isoformat()
    elif end_date == "previous month":
        end_date = (today.replace(day=1) - datetime.timedelta(days=1)).isoformat()
    elif end_date == "this year":
        end_date = today.replace(month=12, day=31).isoformat()

    # If no start or end date provided, use default values
    start_date = start_date or one_year_ago.isoformat()
    end_date = end_date or today.isoformat()

    return start_date, end_date

# Function to generate JSON output
def generate_json(user_query, company_names, metrics, previous_entities=[]):
    extracted_data = extract_query_components(user_query, company_names, metrics)

    # Handle missing data or defaults
    if extracted_data["entity"] and extracted_data["parameter"]:
        start_date, end_date = process_dates(extracted_data.get("startDate"), extracted_data.get("endDate"))
        entities = [{
            "entity": extracted_data.get("entity"),
            "parameter": extracted_data.get("parameter"),
            "startDate": start_date,
            "endDate": end_date
        }]
    else:
        raise Exception("Invalid or incomplete query. Please provide a valid company name and metric.")

    # Handle comparison queries (append previous entities)
    if "compare" in user_query.lower() and previous_entities:
        entities.extend(previous_entities)

    return entities

# Main function to run the application
def main():
    print("Welcome to the LLM-powered Performance Metrics Query System!")

    # Define the supported company names and performance metrics
    company_names = ["Flipkart", "Amazon", "Walmart", "Apple", "Microsoft"]
    metrics = ["GMV", "revenue", "profit", "sales", "loss"]

    previous_entities = []
    query_history = []

    while True:
        # Limit query history to 6
        if len(query_history) >= 6:
            query_history.pop(0)

        user_query = input("Enter your query (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            break

        # Append the current query to history
        query_history.append(user_query)

        try:
            result = generate_json(user_query, company_names, metrics, previous_entities)
            print("\nGenerated JSON Output:")
            print(json.dumps(result, indent=4))

            # Update previous entities for comparison queries
            previous_entities = result

        except Exception as e:
            print(f"Error: {str(e)}")

# Instructions to run the application
print("""
Instructions:
1. To run this application, ensure you have Python 3.6 or higher installed.
2. Install required dependencies using the following command:
   pip install fuzzywuzzy python-Levenshtein
3. You can enter queries about company performance metrics, e.g.:
   - "What was the GMV of Flipkart last year?"
   - "Provide the revenue for Amazon and Flipkart from Jan 2023 to Dec 2023."
4. You can compare results by asking about multiple companies, e.g.:
   - "Compare the GMV of Amazon and Flipkart."
5. To exit the application, type 'exit'.
""")

# Run the application
if __name__ == "__main__":
    main()
