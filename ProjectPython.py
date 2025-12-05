import csv
import os





# 1/ Function to preview dataset
def preview_dataset(filename):
    data = []
    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")
        return data
    with open(filename, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader: 
            data.append(row)
    return headers, data

# Example usage
headers, data = preview_dataset("data.csv")
print("Headers:", headers)
print("Data:", data)






# 2/ Function to search for chief
def search_for_chief(headers, data):
    ress = []
    
    for i, row in enumerate(data, 1):
        for j, cell in enumerate(row):
            if "chief" in str(cell).lower():
                ress.append({
                    "row": i,
                    "column": headers[j] if j < len(headers) else f"Column {j}",
                    "value": cell
                })
    
    return ress

# Example usage of search_for_chief 
headers, data = preview_dataset("data.csv")
chiefres = search_for_chief(headers, data)

print(f"Search ress for 'chief':")
if chiefres:
    for res in chiefres:
        print(f"Row {res['row']}, Column '{res['column']}': {res['value']}")
else:
    print("No matches found for 'chief'")








# 3/ Function to read CSV file
def extract_two_columns(headers, data, x1, x2):
    extra = []
    for row in data:
        if x1 < len(row) and x2 < len(row):
            extra.append([row[x1], row[x2]])
    return extra

# Usage example
headers, data = preview_dataset("data.csv")
extracted_data = extract_two_columns(headers, data, 0, 1)

if len(headers) > 0:
    col1 = headers[0]
else:
    col1 = "Column 0"

if len(headers) > 1:
    col2 = headers[1]
else:
    col2 = "Column 1"

print(f"Extracted columns: '{col1}' and '{col2}'")
print(f"Number of rows extracted: {len(extracted_data)}")
print("\nExtracted data:")
for row in extracted_data:
    print(row)



# 4/ Data cleaning functions
import pandas as pd

headers, data = preview_dataset("data.csv")
# Convert to DataFrame
df = pd.DataFrame(data, columns=headers)
print("Before cleaning:")
print(df)

# Clean with pandas
df.fillna(0)
df.dropna()

print("\nAfter cleaning:")
print(df)

# Save manually
with open("data_cleaned.csv", "w") as f:
    headers = ",".join(df.columns)
    f.write(headers + "\n")
    for row in df.values:
        row_str = ",".join(str(x) for x in row)
        f.write(row_str + "\n")

print("Saved to data_cleaned.csv")
