import pandas as pd
import os

print("EMPLOYEE SALARY INVESTIGATION TOOL")

if not os.path.exists("data.csv"):
    print("Error: data.csv not found!")
    exit()

df = pd.read_csv("data.csv")
print("\nDataset loaded!")
print(f"Total employees: {len(df)}")
print()

while True:
    print("Enter a job title keyword")
    print("(type 'quit' to exit)")
    keyword = input(" enter your choice : ")
    keyword = keyword.strip()
    
    if keyword.lower() == "quit":
        print("\nGoodbye User!")
        break
    
    if keyword == "":
        print("Please enter something.\n")
        continue
    
    print(f"\nSearching for '{keyword}'...\n")
    
    jobtitles = df['JobTitle']
    jobtitles_lower = jobtitles.str.lower()
    matches = jobtitles_lower.str.contains(keyword.lower())
    # .str.contains() checks if keyword is inside
    
    filtered = df[matches]
    # df[True/False list] keeps only True rows
    num_matches = len(filtered)
    
    if num_matches == 0:
        print(f"No matches found.\n")
        continue
    
    print(f"Number of matches: {num_matches}")
    
    basepay_column = filtered['BasePay']
    basepay_numbers = pd.to_numeric(basepay_column)
    average_basepay = basepay_numbers.mean()
    print(f"Average BasePay: ${average_basepay:,.2f}")
    totalpay_column = filtered['TotalPay']
    totalpay_numbers = pd.to_numeric(totalpay_column)
    highest_pay = totalpay_numbers.max()
    print(f"Highest TotalPay: ${highest_pay:,.2f}")
    print("\nTop Earner:")
    max_pay = 0
    top_name = ""
    top_job = ""
    top_year = ""
    
    for index, row in filtered.iterrows():
        current_pay = pd.to_numeric(row['TotalPay'])
        if current_pay > max_pay:
            max_pay = current_pay
            top_name = row['EmployeeName']
            top_job = row['JobTitle']
            top_year = row['Year']
    
    print(f"  Name: {top_name}")
    print(f"  Job: {top_job}")
    print(f"  Year: {top_year}")
    
    print("\nFirst 5 results:")
    first_five = filtered.head()
    print(first_five)
    
    print("\nSave results? (yes/no)")
    answer = input("Choice : ")
    answer = answer.strip().lower()
    
    if answer == "yes":
        filtered.to_csv('custom_search.csv', index=False)
        print("Saved to custom_search.csv\n")
    else:
        print()

print("Program ended.")