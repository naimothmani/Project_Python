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

df = pd.DataFrame(data, columns=headers)
print("Before cleaning:")
print(df)

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








# 5 / Create subsets

def create_subsets(df):
    subsets = {}
    
    if 'Salary' in df.columns:
        high = df[df.Salary > 50000]
        subsets["High earners"] = high
    
    if 'Year' in df.columns:
        year2013 = df[df.Year == 2013]
        subsets["Year 2013"] = year2013
    
    if 'JobTitle' in df.columns:
        police = df[df.JobTitle.str.upper().str.contains("POLICE")]
        subsets["Police"] = police
    
    return subsets

# Example
subsets = create_subsets(df)

for name, subset in subsets.items():
    print(f"{name}:")
    print(subset.head())
    
    with open(f"{name.lower().replace(' ', '_')}.csv", "w") as f:
        headers = ",".join(subset.columns)
        f.write(headers + "\n")
        for row in subset.values:
            row_str = ",".join(str(x) for x in row)
            f.write(row_str + "\n")
    print(f"Saved to {name.lower().replace(' ', '_')}.csv\n")









# 6/ Data visualization
def create_columns(df):
    if 'JobTitle' in df.columns:
        df['Is_Manager'] = df.JobTitle.str.upper().str.contains('MANAGER|CHIEF')
    return df
df = create_columns(df)
print("Data with new column 'Is_Manager':")
print(df[['JobTitle', 'Is_Manager']].head())



# 7/ Summary statistics
def summary_statistics(df):
    print("Summary Statistics:")
    
    if 'BasePay' in df.columns:
        avg = df.BasePay.mean()
        print(f"Average BasePay: {avg}")
    
    if 'JobTitle' in df.columns:
        job_counts = {}
        for job in df.JobTitle:
            if job in job_counts:
                job_counts[job] = job_counts[job] + 1
            else:
                job_counts[job] = 1
        
        items = list(job_counts.items())
        
        sorted_items = []
        for item in items:
            inserted = False
            for i in range(len(sorted_items)):
                if item[1] > sorted_items[i][1]:
                    sorted_items.insert(i, item)
                    inserted = True
                    break
            if not inserted:
                sorted_items.append(item)
        
        print("Top 5 most common titles:")
        for i in range(min(5, len(sorted_items))):
            job, count = sorted_items[i]
            print(f"  {i+1}. {job}: {count}")
    
    total = len(df)
    print(f"Total number of employees: {total}")
    
    print("\nBasic statistics:")
    print(df.describe())