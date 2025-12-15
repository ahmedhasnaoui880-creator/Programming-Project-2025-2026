import pandas as pd
import os

def get_data_path(filename):
    """Get the correct path to data files"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '..', 'Data', filename)
    return data_path

def New_Columns():
    """Create new calculated columns - PART IV"""
    data_file = get_data_path('cleaned_data.csv')
    df = pd.read_csv(data_file, low_memory=False)
    
    print("=" * 60)
    print("PART IV - CREATING NEW COLUMNS")
    print("=" * 60)
    print(f"\nLoaded {len(df):,} records from cleaned dataset")
    
    # Convert numeric columns to proper types
    numeric_columns = ['BasePay', 'OvertimePay', 'OtherPay', 'Benefits', 'TotalPay', 'TotalPayBenefits']
    print("\nConverting columns to numeric types...")
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    if 'Year' in df.columns:
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')
    
    if 'Id' in df.columns:
        df['Id'] = pd.to_numeric(df['Id'], errors='coerce').astype('Int64')
    
    print("✓ All numeric conversions complete\n")
    
    # ============ REQUIRED COLUMNS ============
    
    # 1. Is_Manager column
    print("Creating computed columns...")
    df['Is_Manager'] = df['JobTitle'].str.contains('MANAGER|CHIEF', case=False, na=False)
    print(f"  ✓ Is_Manager: {df['Is_Manager'].sum():,} managers/chiefs identified")
    
    # ============ ADDITIONAL USEFUL COLUMNS ============
    
    # 2. Total compensation without benefits
    df['TotalCompensation'] = df['BasePay'].fillna(0) + df['OvertimePay'].fillna(0) + df['OtherPay'].fillna(0)
    
    # 3. Overtime percentage of base pay
    df['OvertimePercent'] = None
    mask = (df['BasePay'] > 0) & (df['BasePay'].notna())
    df.loc[mask, 'OvertimePercent'] = (df.loc[mask, 'OvertimePay'] / df.loc[mask, 'BasePay']) * 100
    
    # 4. Benefits to total pay ratio
    df['BenefitsRatio'] = None
    mask = (df['TotalPay'] > 0) & (df['TotalPay'].notna())
    df.loc[mask, 'BenefitsRatio'] = df.loc[mask, 'Benefits'] / df.loc[mask, 'TotalPay']
    
    # 5. Salary categories
    df['SalaryCategory'] = pd.cut(
        df['TotalPayBenefits'], 
        bins=[0, 50000, 100000, 150000, float('inf')],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # 6. High overtime flag
    df['HighOvertimeFlag'] = df['OvertimePercent'] > 20
    
    # 7. Name length
    if 'EmployeeName' in df.columns:
        df['NameLength'] = df['EmployeeName'].str.len()
    
    # Save the modified dataframe
    output_file = get_data_path('data_with_new_columns.csv')
    df.to_csv(output_file, index=False)
    print(f"\n✓ All columns created and saved to {output_file}")
    
    # Show summary
    print("\n" + "="*60)
    print("NEW COLUMNS SUMMARY")
    print("="*60)
    print(f"Total records: {len(df):,}")
    print(f"\nKey Statistics:")
    print(f"  • Managers/Chiefs: {df['Is_Manager'].sum():,} ({df['Is_Manager'].sum()/len(df)*100:.1f}%)")
    print(f"  • High Overtime Employees: {df['HighOvertimeFlag'].sum():,}")
    print(f"  • Salary Categories:")
    print(df['SalaryCategory'].value_counts().sort_index().to_string())
    
    return df

def Summary_Statistics(df):
    """Generate summary statistics - PART IV"""
    print("\n" + "="*60)
    print("PART IV - SUMMARY STATISTICS")
    print("="*60)
    
    # ============ STATISTICS ============
    
    # 1. Total number of employees
    print(f"\n1. Total Number of Employees: {len(df):,}")
    
    # 2. Average BasePay
    avg_base_pay = df['BasePay'].mean()
    print(f"\n2. Average BasePay: ${avg_base_pay:,.2f}")
    
    # 3. Top 5 most common job titles (REQUIRED - exactly 5)
    print(f"\n3. Top 5 Most Common Job Titles:")
    top_5_titles = df['JobTitle'].value_counts().head(5)
    for i, (title, count) in enumerate(top_5_titles.items(), 1):
        print(f"   {i}. {title}: {count:,} employees")
    
    # ============ ADDITIONAL STATISTICS ============
    
    # Basic statistics
    print("\n4. Basic Statistics for Key Columns:")
    print(df[['BasePay', 'OvertimePay', 'TotalPay', 'Benefits']].describe())
    
    # Top 10 Job Titles by Average Pay
    print("\n5. Top 10 Job Titles by Average Pay:")
    job_summary = df.groupby('JobTitle').agg({
        'BasePay': 'mean',
        'TotalPayBenefits': ['mean', 'count']
    }).round(2)
    job_summary.columns = ['AvgBasePay', 'AvgTotalPayBenefits', 'Count']
    job_summary = job_summary.sort_values('AvgTotalPayBenefits', ascending=False).head(10)
    print(job_summary.to_string())
    
    # Manager vs Non-Manager comparison
    if 'Is_Manager' in df.columns:
        print("\n6. Manager vs Non-Manager Comparison:")
        manager_stats = df.groupby('Is_Manager').agg({
            'BasePay': 'mean',
            'TotalPay': 'mean',
            'TotalPayBenefits': 'mean'
        }).round(2)
        manager_stats.index = ['Non-Manager', 'Manager']
        print(manager_stats.to_string())
    
    # Correlation between numerical columns
    print("\n7. Correlation Matrix:")
    correlation = df[['BasePay', 'OvertimePay', 'OtherPay', 'Benefits']].corr()
    print(correlation.round(3))
    
    # Percentiles
    print("\n8. TotalPayBenefits Percentiles:")
    percentiles = df['TotalPayBenefits'].quantile([0.25, 0.5, 0.75, 0.9, 0.95])
    for pct, val in percentiles.items():
        print(f"   {int(pct*100)}th percentile: ${val:,.2f}")
    
    # Status distribution
    print("\n9. Employment Status Distribution:")
    if 'Status' in df.columns:
        print(df['Status'].value_counts().to_string())

def Joining():
    """Merge employee data with agency codes - PART VI"""
    print("\n" + "="*60)
    print("PART VI - JOINING DATASETS")
    print("="*60)
    
    # ===== STEP 1: Load Main Dataset =====
    data_file = get_data_path('cleaned_data.csv')
    
    dtypes_main = {
        'EmployeeName': 'string',
        'JobTitle': 'string',
        'Agency': 'string',
        'Status': 'string',
        'Notes': 'string'
    }
    
    print("\nLoading main dataset...")
    df_employees = pd.read_csv(data_file, dtype=dtypes_main, low_memory=False)
    
    # Convert numeric columns
    numeric_columns = ['Id', 'BasePay', 'OvertimePay', 'OtherPay', 'Benefits', 'TotalPay', 'TotalPayBenefits', 'Year']
    for col in numeric_columns:
        if col in df_employees.columns:
            df_employees[col] = pd.to_numeric(df_employees[col], errors='coerce')
    
    print(f"✓ Loaded {len(df_employees):,} employee records")
    
    # Get unique agencies
    unique_agencies = df_employees['Agency'].dropna().unique()
    print(f"✓ Found {len(unique_agencies)} unique agencies")
    
    # ===== STEP 2: Create Agency Mapping =====
    print("\nCreating agency code mapping file...")
    
    # Create agency codes manually
    agency_codes = []
    for i in range(len(unique_agencies)):
        agency_codes.append(f'AG-{str(i).zfill(4)}')
    
    # Create mapping DataFrame
    agency_mapping = pd.DataFrame({
        'Agency': unique_agencies,
        'AgencyCode': agency_codes,
        'Department': ['General' for _ in range(len(unique_agencies))]
    })
    
    # Save agency mapping
    mapping_file = get_data_path('agency_code.csv')
    agency_mapping.to_csv(mapping_file, index=False)
    print(f"✓ Agency mapping saved to {mapping_file}")
    print(f"✓ Created {len(agency_mapping)} agency codes")
    
    # ===== STEP 3: Load Agency Codes =====
    print("\nLoading agency codes...")
    df_agency_codes = pd.read_csv(mapping_file)
    print(f"✓ Loaded {len(df_agency_codes)} agency codes")
    
    # ===== STEP 4: Merge Datasets =====
    print("\nMerging datasets on 'Agency' column...")
    merged_df = pd.merge(
        df_employees,
        df_agency_codes,
        on='Agency',
        how='left'
    )
    print("✓ Merge completed")
    
    # ===== STEP 5: Validate Merge =====
    print("\n" + "="*60)
    print("MERGE VALIDATION")
    print("="*60)
    print(f"  • Original employee records: {len(df_employees):,}")
    print(f"  • Merged records: {len(merged_df):,}")
    print(f"  • Agencies in main data: {df_employees['Agency'].nunique()}")
    print(f"  • Agencies in mapping: {len(df_agency_codes)}")
    
    # Check for unmatched agencies
    unmatched_count = merged_df['AgencyCode'].isna().sum()
    if unmatched_count > 0:
        print(f"\n⚠ Warning: {unmatched_count:,} records with unmatched agencies")
        unmatched_agencies = merged_df[merged_df['AgencyCode'].isna()]['Agency'].unique()
        print(f"  Unmatched agencies: {len(unmatched_agencies)}")
        if len(unmatched_agencies) > 0 and len(unmatched_agencies) <= 10:
            for agency in unmatched_agencies:
                print(f"    - {agency}")
    else:
        print("\n✓ All agencies matched successfully!")
    
    # Show sample of merged data
    print("\n" + "="*60)
    print("SAMPLE OF MERGED DATA (First 5 rows)")
    print("="*60)
    display_cols = ['EmployeeName', 'JobTitle', 'Agency', 'AgencyCode', 'TotalPay']
    available_cols = [col for col in display_cols if col in merged_df.columns]
    print(merged_df[available_cols].head(5).to_string(index=False))
    
    # ===== STEP 6: Save Merged Dataset =====
    merged_file = get_data_path('merged_data.csv')
    merged_df.to_csv(merged_file, index=False)
    print(f"\n✓ Merged data saved to {merged_file}")
    
    return merged_df

# Main execution
if __name__ == "__main__":
    try:
        print("="*60)
        print("DATA MANAGEMENT PIPELINE")
        print("Parts IV (New Columns & Stats) + VI (Joining)")
        print("="*60)
        
        # Part IV - Step 1: Create new columns
        print("\n[PART IV - STEP 1/2] Creating new columns...")
        df = New_Columns()
        
        # Part IV - Step 2: Generate summary statistics
        print("\n[PART IV - STEP 2/2] Generating summary statistics...")
        Summary_Statistics(df)
        
        # Part VI - Join with agency codes
        print("\n[PART VI] Joining with agency codes...")
        merged_df = Joining()
        
        print("\n" + "="*60)
        print("✓ ALL OPERATIONS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nOutput files created:")
        print("  1. data_with_new_columns.csv (Part IV)")
        print("  2. agency_code.csv (Part VI)")
        print("  3. merged_data.csv (Part VI)")
        
    except FileNotFoundError as e:
        print(f"\n Error: Could not find file - {e}")
        print("Make sure you've run Part II (Data_cleaning.py) first!")
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        import traceback
        traceback.print_exc()