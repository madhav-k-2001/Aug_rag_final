from langfuse import Langfuse
import csv

langfuse = Langfuse(
  secret_key="sk-lf-22b46cb9-5a7c-40fb-86a2-5ae3bf4eda37",
  public_key="pk-lf-2aeebf3b-35bf-448a-9605-eca1f8644d51",
  host="http://172.24.18.13:3000"  # 🇪🇺 EU region
  # host="https://us.cloud.langfuse.com" # 🇺🇸 US region
)
 
# Fetch list of traces, supports filters and pagination
traces = langfuse.fetch_traces()
csv_data = []
for trace in traces.data:
    # Ensure output is a dictionary and has "content"
    output_content = trace.output["content"] if isinstance(trace.output, dict) and "content" in trace.output else "No content or error"
    
    csv_data.append({
        "timestamp": trace.timestamp.isoformat(),
        "user_question": trace.input["user_question"],
        "output_content": output_content
    })

# Writing the extracted data to a CSV file
csv_columns = ['timestamp', 'user_question', 'output_content']
csv_file = "traces.csv"

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in csv_data:
            writer.writerow(data)
except IOError:
    print("I/O error")

print(f"CSV file '{csv_file}' has been created.")