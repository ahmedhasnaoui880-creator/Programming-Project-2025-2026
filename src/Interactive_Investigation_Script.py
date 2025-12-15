import pandas as pd
import os
import sys

def load_data(filepath=None):
    """Load the employee dataset with error handling"""
    try:
        # If no filepath provided, use default relative path
        if filepath is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(script_dir, '..', 'Data', 'merged_data.csv')
        
        dtypes = {
            'Id': 'int32',
            'EmployeeName': 'string',
            'JobTitle': 'string',
            'BasePay': 'float32',
            'OvertimePay': 'float32',
            'OtherPay': 'float32',
            'Benefits': 'float32',
            'TotalPay': 'float32',
            'TotalPayBenefits': 'float32',
            'Year': 'int16',
            'Agency': 'string',
            'Status': 'string'
        }
        
        df = pd.read_csv(filepath, dtype=dtypes)
        print(f"✓ Successfully loaded {len(df):,} employee records\n")
        return df
    
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        print("Please make sure the file exists in the Data directory.")
        sys.exit(1)
    
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        sys.exit(1)
    
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        sys.exit(1)

def search_by_job_title(df, keyword):
    """Filter dataframe by job title keyword (case-insensitive)"""
    try:
        # Handle NaN values in JobTitle
        df_clean = df[df['JobTitle'].notna()].copy()
        
        # Case-insensitive search
        mask = df_clean['JobTitle'].str.contains(keyword, case=False, na=False)
        filtered_df = df_clean[mask]
        
        return filtered_df
    
    except Exception as e:
        print(f"Error during search: {str(e)}")
        return pd.DataFrame()

def display_results(filtered_df, keyword):
    """Display search results with statistics"""
    num_matches = len(filtered_df)
    
    print("=" * 60)
    print(f"SEARCH RESULTS FOR: '{keyword}'")
    print("=" * 60)
    
    if num_matches == 0:
        print("\n No matches found.")
        print("Tips:")
        print("  - Try a shorter keyword (e.g., 'manager' instead of 'senior manager')")
        print("  - Check for typos")
        print("  - Try a more general term")
        return False
    
    print(f"\n✓ Number of matches: {num_matches:,}")
    
    # Calculate statistics with error handling
    try:
        # Average BasePay (excluding NaN)
        avg_base_pay = filtered_df['BasePay'].mean()
        if pd.notna(avg_base_pay):
            print(f"✓ Average BasePay: ${avg_base_pay:,.2f}")
        else:
            print("✓ Average BasePay: N/A (no valid data)")
        
        # Highest TotalPay
        max_total_pay = filtered_df['TotalPay'].max()
        if pd.notna(max_total_pay):
            print(f"✓ Highest TotalPay: ${max_total_pay:,.2f}")
            
            # Find the employee with highest total pay
            top_earner = filtered_df[filtered_df['TotalPay'] == max_total_pay].iloc[0]
            print(f"  → {top_earner['EmployeeName']} ({top_earner['JobTitle']})")
        else:
            print("✓ Highest TotalPay: N/A (no valid data)")
        
        # Additional useful statistics
        print(f"\n Additional Statistics:")
        print(f"  • Median BasePay: ${filtered_df['BasePay'].median():,.2f}")
        print(f"  • Total Overtime Paid: ${filtered_df['OvertimePay'].sum():,.2f}")
        print(f"  • Agencies represented: {filtered_df['Agency'].nunique()}")
        
        # Show sample of results
        print(f"\n Sample Results (first 5):")
        print("-" * 60)
        sample_cols = ['EmployeeName', 'JobTitle', 'BasePay', 'TotalPay', 'Agency']
        available_cols = [col for col in sample_cols if col in filtered_df.columns]
        print(filtered_df[available_cols].head(5).to_string(index=False))
        
    except Exception as e:
        print(f"\n⚠ Warning: Error calculating some statistics: {str(e)}")
    
    return True

def save_results(filtered_df, filename='custom_search.csv'):
    """Save filtered results to CSV in the Data folder"""
    try:
        if len(filtered_df) == 0:
            print("\n⚠ No data to save.")
            return
        
        # Save to Data folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, '..', 'Data', filename)
        
        filtered_df.to_csv(output_path, index=False)
        print(f"\n Results saved to 'Data/{filename}'")
        print(f"   Total records saved: {len(filtered_df):,}")
    
    except PermissionError:
        print(f"\n Error: Permission denied. Please close '{filename}' if it's open.")
    
    except Exception as e:
        print(f"\n Error saving file: {str(e)}")

def main():
    """Main interactive loop"""
    print("\n" + "=" * 60)
    print("EMPLOYEE DATA INVESTIGATION TOOL")
    print("=" * 60)
    
    # Load data
    df = load_data()
    
    while True:
        print("\n" + "-" * 60)
        
        # Get user input
        try:
            keyword = input("\nEnter job title keyword to search (or 'quit' to exit): ").strip()
            
            if keyword.lower() in ['quit', 'exit', 'q']:
                print("\n Goodbye!")
                break
            
            if not keyword:
                print(" Please enter a valid keyword.")
                continue
            
            # Search
            print(f"\n Searching for '{keyword}'...")
            filtered_df = search_by_job_title(df, keyword)
            
            # Display results
            has_results = display_results(filtered_df, keyword)
            
            # Save if there are results
            if has_results:
                save_choice = input("\n Save these results? (y/n): ").strip().lower()
                if save_choice in ['y', 'yes']:
                    filename = input("Enter filename (or press Enter for 'custom_search.csv'): ").strip()
                    if not filename:
                        filename = 'custom_search.csv'
                    elif not filename.endswith('.csv'):
                        filename += '.csv'
                    
                    save_results(filtered_df, filename)
        
        except KeyboardInterrupt:
            print("\n Interrupted by user. Goodbye!")
            break
        
        except Exception as e:
            print(f"\n Unexpected error: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main()