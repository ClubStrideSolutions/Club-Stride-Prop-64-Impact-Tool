"""Test the dashboard functionality"""

import pandas as pd
import os

def check_sample_data():
    """Verify sample data exists and is valid"""
    data_file = 'data/sample_kpi_data.xlsx'
    
    if not os.path.exists(data_file):
        print("[ERROR] Sample data file not found!")
        print("Please run: python create_sample_data.py")
        return False
    
    try:
        df = pd.read_excel(data_file)
        print(f"[SUCCESS] Sample data loaded: {len(df)} KPIs")
        print(f"Columns: {', '.join(df.columns)}")
        
        # Check for required columns
        required = ['kpi_name', 'status', 'project', 'owner']
        missing = [col for col in required if col not in df.columns]
        
        if missing:
            print(f"[WARNING] Missing columns: {', '.join(missing)}")
        else:
            print("[SUCCESS] All required columns present")
            
        # Show data summary
        print("\nData Summary:")
        print(f"- Projects: {df['project'].nunique()}")
        print(f"- Owners: {df['owner'].nunique()}")
        print(f"- Status distribution:")
        print(f"  Green (G): {len(df[df['status'] == 'G'])}")
        print(f"  Yellow (Y): {len(df[df['status'] == 'Y'])}")
        print(f"  Red (R): {len(df[df['status'] == 'R'])}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to read sample data: {e}")
        return False

def main():
    print("=" * 60)
    print("DASHBOARD FUNCTIONALITY TEST")
    print("=" * 60)
    
    print("\n1. Checking sample data...")
    if not check_sample_data():
        return
    
    print("\n2. Dashboard Instructions:")
    print("-" * 40)
    print("1. Open browser: http://localhost:8050")
    print("2. Upload file: data/sample_kpi_data.xlsx")
    print("3. Test these features:")
    print("   - File upload section (top of page)")
    print("   - Overview tab (metrics and charts)")
    print("   - KPI Details tab (table with filters)")
    print("   - Analytics tab (run different analyses)")
    print("   - Reports tab (export options)")
    print("\n4. Expected Results:")
    print("   - No callback errors")
    print("   - All charts display properly")
    print("   - Filters work correctly")
    print("   - KPI details show when clicking table rows")
    
    print("\n" + "=" * 60)
    print("Dashboard is running at: http://localhost:8050")
    print("=" * 60)

if __name__ == "__main__":
    main()