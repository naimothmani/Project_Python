import csv
import pandas as pd

# Color definitions
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# PART 1: FILE HANDLING

def preview_dataset(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        data = []
        for row in reader:
            data.append(row)
    return headers, data

def search_chief(headers, data):
    results = []
    for i in range(len(data)):
        row = data[i]
        for j in range(len(row)):
            cell = row[j]
            if "chief" in cell.lower():
                results.append("Row " + str(i+1) + ", " + headers[j] + ": " + cell)
    return results

def search_keyword(headers, data, keyword):
    count = 0
    for row in data:
        for cell in row:
            if keyword.lower() in cell.lower():
                count += 1
                break
    return count

def extract_columns(headers, data, col1, col2):
    extracted = []
    for row in data:
        extracted.append([row[col1], row[col2]])
    return extracted

def save_extracted_columns(filename, headers, data, col1, col2):
    with open(filename, "w") as f:
        f.write(headers[col1] + "," + headers[col2] + "\n")
        for row in data:
            f.write(row[0] + "," + row[1] + "\n")

def run1(filename="data.csv"):
    print("\n" + Colors.BOLD + Colors.HEADER + "-"*60 + Colors.RESET)
    print(Colors.BOLD + Colors.HEADER + "PART 1: FILE HANDLING" + Colors.RESET)
    print(Colors.BOLD + Colors.HEADER + "-"*60 + Colors.RESET + "\n")
    headers, data = preview_dataset(filename)
    print(Colors.CYAN + "1. Dataset Preview" + Colors.RESET)
    total_rows = len(data)
    print("   Total rows: " + Colors.GREEN + str(total_rows) + Colors.RESET)
    headers_text = ", ".join(headers)
    print("   Headers: " + Colors.YELLOW + headers_text + Colors.RESET)
    chief_results = search_chief(headers, data)
    print("\n" + Colors.CYAN + "2. Search for 'chief'" + Colors.RESET)
    num_matches = len(chief_results)
    print("   Found: " + Colors.GREEN + str(num_matches) + Colors.RESET + " matches")
    counter = 1
    for result in chief_results[:3]:
        short_result = result[:50]
        print("   " + str(counter) + ". " + short_result + "...")
        counter = counter + 1
    manager_count = search_keyword(headers, data, "manager")
    police_count = search_keyword(headers, data, "police")
    print("   Manager: " + Colors.GREEN + str(manager_count) + Colors.RESET + " rows")
    print("   Police: " + Colors.GREEN + str(police_count) + Colors.RESET + " rows")
    extracted = extract_columns(headers, data, 0, 1)
    print("\n" + Colors.CYAN + "3. Column Extraction" + Colors.RESET)
    print("   Columns: " + Colors.YELLOW + headers[0] + ", " + headers[1] + Colors.RESET)
    num_extracted = len(extracted)
    print("   Extracted: " + Colors.GREEN + str(num_extracted) + Colors.RESET + " rows")
    save_extracted_columns("extracted_columns.csv", headers, extracted, 0, 1)
    print("   " + Colors.GREEN + "✓" + Colors.RESET + " Saved to extracted_columns.csv")
    return headers, data

# PART 2: DATA CLEANING

def load_and_convert_numeric(filename):
    df = pd.read_csv(filename, low_memory=False)
    numeric_cols = ['BasePay', 'OvertimePay', 'OtherPay', 'Benefits', 'TotalPay', 'TotalPayBenefits']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce') 
    return df
#converting to numeric to avoid errors.

def clean_dataset(df):
    print("\n" + Colors.BOLD + Colors.HEADER + "-"*60 + Colors.RESET)
    print(Colors.BOLD + Colors.HEADER + "PART 2: DATA CLEANING" + Colors.RESET)
    print(Colors.BOLD + Colors.HEADER + "-"*60 + Colors.RESET + "\n")
    
    print(Colors.CYAN + "Before Cleaning:" + Colors.RESET)
    print("   Rows: " + Colors.YELLOW + str(len(df)) + Colors.RESET)
    print("   Columns: " + Colors.YELLOW + str(len(df.columns)) + Colors.RESET)
    
    df = df.fillna(0)
    df = df.drop_duplicates()
    if 'TotalPay' in df.columns:
        before = len(df)
        df = df[df['TotalPay'] >= 0]
        removed = before - len(df)
        if removed > 0:
            print("   " + Colors.RED + "✗" + Colors.RESET + " Removed " + str(removed) + " rows (negative TotalPay)")
    
    if 'BasePay' in df.columns:
        before = len(df)
        df = df[df['BasePay'] >= 0]
        removed = before - len(df)
        if removed > 0:
            print("   " + Colors.RED + "✗" + Colors.RESET + " Removed " + str(removed) + " rows (negative BasePay)")
    
    print("\n" + Colors.CYAN + "After Cleaning:" + Colors.RESET)
    print("   Rows: " + Colors.GREEN + str(df.shape[0]) + Colors.RESET)
    print("   Columns: " + Colors.GREEN + str(df.shape[1]) + Colors.RESET)
    print("   Missing values: " + Colors.GREEN + str(df.isnull().sum().sum()) + Colors.RESET)
    print("   Duplicates: " + Colors.GREEN + str(df.duplicated().sum()) + Colors.RESET)
    return df

def save_cleaned_data(df, filename="data_cleaned.csv"):
    df.to_csv(filename, index=False)
    print("   " + Colors.GREEN + "✓" + Colors.RESET + " Saved to " + filename)

def run2(filename="data.csv"):
    df = load_and_convert_numeric(filename)
    df = clean_dataset(df)
    save_cleaned_data(df)
    return df

# PART 3: SUBSETTING & FILTERING

def create_high_earners(df, threshold=100000):
    high_earners = df[df['TotalPay'] > threshold]
    high_earners.to_csv("high_earners.csv", index=False)
    return high_earners

def create_year_subset(df, year=2013):
    year_subset = df[df['Year'] == year]
    year_subset.to_csv("year_" + str(year) + ".csv", index=False)
    return year_subset

def create_police_subset(df):
    police = df[df['JobTitle'].str.contains("POLICE")]
    police.to_csv("police_employees.csv", index=False)
    return police

def create_low_earners(df):
    low_earners = df[df['TotalPay'] < 5000]
    low_earners.to_csv("low_earners.csv", index=False)
    return low_earners

def create_fire_subset(df):
    fire = df[df['JobTitle'].str.contains("FIRE")]
    fire.to_csv("fire_employees.csv", index=False)
    return fire

def create_high_overtime(df):
    if 'OvertimePay' in df.columns:
        overtime = df[df['OvertimePay'] > 10000]
        overtime.to_csv("high_overtime.csv", index=False)
        return overtime
    return None

def create_top_1_percent(df):
    top_1_percent = df[df['TotalPay'] > df['TotalPay'].quantile(0.99)]
    top_1_percent.to_csv("top_1_percent.csv", index=False)
    return top_1_percent

def run3(df):
    print("\n" + Colors.BOLD + Colors.HEADER + "-"*60 + Colors.RESET)
    print(Colors.BOLD + Colors.HEADER + "PART 3: SUBSETTING & FILTERING" + Colors.RESET)
    print(Colors.BOLD + Colors.HEADER + "-"*60 + Colors.RESET + "\n")
    
    high_earners = create_high_earners(df)
    print("   " + Colors.CYAN + "a)" + Colors.RESET + " High earners (>$100k): " + Colors.GREEN + str(len(high_earners)) + Colors.RESET)
    
    year_2013 = create_year_subset(df, 2013)
    print("   " + Colors.CYAN + "b)" + Colors.RESET + " Year 2013: " + Colors.GREEN + str(len(year_2013)) + Colors.RESET)
    
    police = create_police_subset(df)
    print("   " + Colors.CYAN + "c)" + Colors.RESET + " Police employees: " + Colors.GREEN + str(len(police)) + Colors.RESET)
    
    low_earners = create_low_earners(df)
    print("   " + Colors.CYAN + "d)" + Colors.RESET + " Low earners (<$50k): " + Colors.GREEN + str(len(low_earners)) + Colors.RESET)
    
    fire = create_fire_subset(df)
    print("   " + Colors.CYAN + "e)" + Colors.RESET + " Fire department: " + Colors.GREEN + str(len(fire)) + Colors.RESET)
    
    overtime = create_high_overtime(df)
    if overtime is not None:
        print("   " + Colors.CYAN + "f)" + Colors.RESET + " High overtime (>$10k): " + Colors.GREEN + str(len(overtime)) + Colors.RESET)
    
    top_1_percent = create_top_1_percent(df)
    print("   " + Colors.CYAN + "g)" + Colors.RESET + " Top 1% earners: " + Colors.GREEN + str(len(top_1_percent)) + Colors.RESET)

# PART 4: NEW COLUMNS & SUMMARY STATISTICS

def create_is_manager_column(df):
    df['Is_Manager'] = df['JobTitle'].str.contains('MANAGER|CHIEF')
    manager_count = df['Is_Manager'].sum()
    non_manager_count = len(df) - manager_count
    print(Colors.CYAN + "Is_Manager Column:" + Colors.RESET)
    print("   Managers: " + Colors.GREEN + str(manager_count) + Colors.RESET)
    print("   Others: " + Colors.YELLOW + str(non_manager_count) + Colors.RESET)
    return df

def get_salary_grade(pay):
    if pay < 40000:
        return 'Low'
    elif pay < 100000:
        return 'Medium'
    elif pay < 150000:
        return 'High'
    else:
        return 'Very High'

def create_salary_grade_column(df):
    df['Salary_Grade'] = df['TotalPay'].apply(get_salary_grade)
    print("\n" + Colors.CYAN + "Salary_Grade Distribution:" + Colors.RESET)
    for grade, count in df['Salary_Grade'].value_counts().items():
        print("   " + grade + ": " + Colors.GREEN + str(count) + Colors.RESET)
    return df

def create_is_police_column(df):
    df['Is_Police'] = df['JobTitle'].str.contains('POLICE')
    print("\n" + Colors.CYAN + "Is_Police Column:" + Colors.RESET)
    print("   Police employees: " + Colors.GREEN + str(df['Is_Police'].sum()) + Colors.RESET)
    return df

def create_total_compensation_column(df):
    df['Total_Compensation'] = df['TotalPay'] + df['Benefits']
    print("\n" + Colors.CYAN + "Total_Compensation:" + Colors.RESET)
    print("   Average: " + Colors.GREEN + "$" + str(round(df['Total_Compensation'].mean(), 2)) + Colors.RESET)
    return df

def display_summary_statistics(df):
    print("\n" + Colors.CYAN + "Summary Statistics:" + Colors.RESET)
    print("   Total employees: " + Colors.GREEN + str(len(df)) + Colors.RESET)
    print("   Average BasePay: " + Colors.YELLOW + "$" + str(round(df['BasePay'].mean(), 2)) + Colors.RESET)
    print("   Average TotalPay: " + Colors.YELLOW + "$" + str(round(df['TotalPay'].mean(), 2)) + Colors.RESET)
    print("   Median TotalPay: " + Colors.YELLOW + "$" + str(round(df['TotalPay'].median(), 2)) + Colors.RESET)
    print("   Max TotalPay: " + Colors.GREEN + "$" + str(round(df['TotalPay'].max(), 2)) + Colors.RESET)
    print("   Min TotalPay: " + Colors.RED + "$" + str(round(df['TotalPay'].min(), 2)) + Colors.RESET)
    print("\n" + Colors.CYAN + "Top 5 Job Titles:" + Colors.RESET)
    rank = 1
    for job, count in df['JobTitle'].value_counts().head(5).items():
        print("   " + str(rank) + ". " + job + ": " + Colors.GREEN + str(count) + Colors.RESET)
        rank += 1

def run4(df):
    print("\n" + Colors.BOLD + Colors.HEADER + "="*60 + Colors.RESET)
    print(Colors.BOLD + Colors.HEADER + "PART 4: NEW COLUMNS & SUMMARY STATISTICS" + Colors.RESET)
    print(Colors.BOLD + Colors.HEADER + "-"*60 + Colors.RESET + "\n")
    df = create_is_manager_column(df)
    df = create_salary_grade_column(df)
    df = create_is_police_column(df)
    df = create_total_compensation_column(df)
    display_summary_statistics(df)
    return df

# PART 5: GROUPING & AGGREGATION

def average_totalpay_per_year(df):
    print("\n" + Colors.CYAN + "Average TotalPay per Year:" + Colors.RESET)
    for year, avg in df.groupby('Year')['TotalPay'].mean().items():
        print("   " + str(int(year)) + ": " + Colors.GREEN + "$" + str(round(avg, 2)) + Colors.RESET) # rounding to only 2 digits after ,

def top_5_highest_paying_jobs(df):
    print("\n" + Colors.CYAN + "Top 5 Highest Paying Jobs:" + Colors.RESET)
    top_jobs = df.groupby('JobTitle')['TotalPay'].mean().sort_values(ascending=False).head(5)
    for i, (job, avg) in enumerate(top_jobs.items(), 1):
        print("   " + str(i) + ". " + job + ": " + Colors.GREEN + "$" + str(round(avg, 2)) + Colors.RESET)

def count_by_salary_grade(df):
    print("\n" + Colors.CYAN + "Employees by Salary Grade:" + Colors.RESET)
    for grade, count in df.groupby('Salary_Grade').size().items():
        print("   " + grade + ": " + Colors.GREEN + str(count) + Colors.RESET)

def manager_vs_non_manager(df):
    print("\n" + Colors.CYAN + "Manager vs Non-Manager:" + Colors.RESET)
    for is_mgr, stats in df.groupby('Is_Manager')['TotalPay'].agg(['mean', 'count']).iterrows():
        role = "Manager" if is_mgr else "Non-Manager"
        print("   " + role + ": Avg=" + Colors.GREEN + "$" + str(round(stats['mean'], 2)) + Colors.RESET + ", Count=" + Colors.YELLOW + str(int(stats['count'])) + Colors.RESET)

def police_vs_fire_comparison(df):
    if 'Is_Police' in df.columns:
        police_avg = df[df['Is_Police']]['TotalPay'].mean()
        fire_avg = df[df['JobTitle'].str.contains('FIRE', na=False)]['TotalPay'].mean()
        print("\n" + Colors.CYAN + "Department Comparison:" + Colors.RESET)
        print("   Police avg: " + Colors.GREEN + "$" + str(round(police_avg, 2)) + Colors.RESET)
        print("   Fire avg: " + Colors.GREEN + "$" + str(round(fire_avg, 2)) + Colors.RESET)

def run5(df):
    print("\n" + Colors.BOLD + Colors.HEADER + "-"*60 + Colors.RESET)
    print(Colors.BOLD + Colors.HEADER + "PART 5: GROUPING & AGGREGATION" + Colors.RESET)
    print(Colors.BOLD + Colors.HEADER + "-"*60 + Colors.RESET)
    average_totalpay_per_year(df)
    top_5_highest_paying_jobs(df)
    count_by_salary_grade(df)
    manager_vs_non_manager(df)
    police_vs_fire_comparison(df)

# PART 6: JOINING

def create_agency_dataframe():
    agency_data = {
        'Agency': ['San Francisco'],
        'AgencyName': ['San Francisco City Government'],
        'Department': ['Municipal Services'],
        'Budget_Category': ['High']
    }
    return pd.DataFrame(agency_data)

def save_agency_codes(agency_df):
    agency_df.to_csv('agency_codes.csv', index=False)
    print("   " + Colors.GREEN + "✓" + Colors.RESET + " Created agency_codes.csv (" + str(len(agency_df)) + " agencies)")

def merge_with_agency(main_df, agency_df):
    if 'Agency' in main_df.columns:
        merged_df = pd.merge(main_df, agency_df, on='Agency', how='left')
        merged_df.to_csv('merged_data.csv', index=False)
        print("   " + Colors.GREEN + "✓" + Colors.RESET + " Merged " + str(len(merged_df)) + " rows")
        print("   " + Colors.CYAN + "New columns:" + Colors.RESET + " AgencyName, Department, Budget_Category")
        print("\n" + Colors.CYAN + "Sample Merged Data:" + Colors.RESET)
        if 'EmployeeName' in merged_df.columns:
            sample = merged_df[['EmployeeName', 'Agency', 'AgencyName', 'Department']].head(3)
            for _, row in sample.iterrows(): #_ means we dont care about the index we only need the rows
                print("   " + row['EmployeeName'] + " | " + row['AgencyName'])
        return merged_df
    else:
        print("   " + Colors.RED + "✗" + Colors.RESET + " No 'Agency' column found")
        return main_df

def run6(df):
    print("\n" + Colors.BOLD + Colors.HEADER + "-"*60 + Colors.RESET)
    print(Colors.BOLD + Colors.HEADER + "PART 6: JOINING" + Colors.RESET)
    print(Colors.BOLD + Colors.HEADER + "-"*60 + Colors.RESET + "\n")
    agency_df = create_agency_dataframe()
    save_agency_codes(agency_df)
    merged_df = merge_with_agency(df, agency_df)
    return merged_df

# MAIN EXECUTION

def main():
    print("\n" + Colors.BOLD + Colors.BLUE + "*"*60 + Colors.RESET)
    print(Colors.BOLD + Colors.BLUE + "  EMPLOYEE SALARY DATA ANALYSIS" + Colors.RESET)
    print(Colors.BOLD + Colors.BLUE + "*"*60 + Colors.RESET)
    
    run1()
    df = run2()
    run3(df)
    df = run4(df)
    run5(df)
    df = run6(df)
    
    print("\n" + Colors.BOLD + Colors.GREEN + "-"*60 + Colors.RESET)
    print(Colors.BOLD + Colors.GREEN + "  DONE !" + Colors.RESET)
    print(Colors.BOLD + Colors.GREEN + "-"*60 + Colors.RESET + "\n")

main()

