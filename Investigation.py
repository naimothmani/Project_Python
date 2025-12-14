import pandas as pd
import os

# color definitions
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

print(Colors.HEADER + Colors.BOLD + "EMPLOYEE SALARY INVESTIGATION TOOL" + Colors.RESET)
if not os.path.exists("data.csv"):
    print(Colors.RED + "Error: data.csv not found!" + Colors.RESET)
    exit()
# since status and notes show NaN , we put them as empty strings
df = pd.read_csv("data.csv", low_memory=False)
df['Notes'] = df['Notes'].fillna('')
df['Status'] = df['Status'].fillna('')

print(Colors.CYAN + "Total employees: " + str(len(df)) + Colors.RESET + "\n")
while True:
    print(Colors.YELLOW + "Enter a job title keyword (type 'exit' to exit)" + Colors.RESET)
    keyword = input(Colors.BLUE + "Your choice: " + Colors.RESET).strip()
    
    if keyword.lower() == "exit":
        print("\n" + Colors.GREEN + "Goodbye , till next time!" + Colors.RESET)
        break
    
    if keyword == "":
        print(Colors.RED + "Please enter something.\n" + Colors.RESET)
        continue
    
    print("\n" + Colors.CYAN + "Searching for '" + keyword + "'..." + Colors.RESET + "\n")
    
    jobtitles = df['JobTitle']
    jobtitles_lower = jobtitles.str.lower()
    matches = jobtitles_lower.str.contains(keyword.lower())
    
    filtered = df[matches]
    num_matches = len(filtered)
    
    if num_matches == 0:
        print(Colors.RED + "No matches found.\n" + Colors.RESET)
        continue
    
    print(Colors.GREEN + "Number of matches: " + str(num_matches) + Colors.RESET)
    
    basepay_numbers = pd.to_numeric(filtered['BasePay'], errors='coerce')  #if it finds something it cant convert it puts it as NaN
    average_basepay = basepay_numbers.mean()
    print(Colors.CYAN + "Average BasePay: " + Colors.BOLD + "$" + str(average_basepay) + Colors.RESET)
    totalpay_numbers = pd.to_numeric(filtered['TotalPay'], errors='coerce')
    highest_pay = totalpay_numbers.max()
    print(Colors.CYAN + "Highest TotalPay: " + Colors.BOLD + "$" + str(highest_pay) + Colors.RESET)
    
    print("\n" + Colors.YELLOW + "Top Earner:" + Colors.RESET)
    max_pay = 0
    top_name = ""
    top_job = ""
    top_year = ""
    
    for index, row in filtered.iterrows():
        current_pay = pd.to_numeric(row['TotalPay'], errors='coerce')
        if current_pay > max_pay:
            max_pay = current_pay
            top_name = row['EmployeeName']
            top_job = row['JobTitle']
            top_year = row['Year']
    
    print("  " + Colors.BOLD + "Name:" + Colors.RESET + " " + top_name)
    print("  " + Colors.BOLD + "Job:" + Colors.RESET + " " + top_job)
    print("  " + Colors.BOLD + "Year:" + Colors.RESET + " " + str(top_year))
    
    print("\n" + Colors.BLUE + "-" * 150 + Colors.RESET)
    print(Colors.BLUE + Colors.BOLD + "First 5 Results:" + Colors.RESET)
    print(Colors.BLUE + "-" * 150 + Colors.RESET)
    
    # Set pandas display options for better formatting
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 30)
    
    print(filtered.head().to_string(index=False))
    print(Colors.BLUE + "-" * 150 + Colors.RESET + "\n")
    
    print(Colors.YELLOW + "Save results? (type yes/no)" + Colors.RESET)
    answer = input(Colors.BLUE + "Choice: " + Colors.RESET).strip().lower()
    
    if answer == "yes":
        filtered.to_csv('custom_search.csv', index=False)
        print(Colors.GREEN + "Saved to custom_search.csv\n" + Colors.RESET)
    else:
        print()

print(Colors.GREEN + "Program ended." + Colors.RESET)
