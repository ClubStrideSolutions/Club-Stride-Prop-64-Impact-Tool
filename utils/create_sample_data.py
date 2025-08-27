"""Create sample KPI data Excel file for testing"""

import pandas as pd
from datetime import datetime, timedelta
import random
import os

# Create sample KPI data
def create_sample_kpi_data():
    """Generate sample KPI data for testing"""
    
    # Sample projects and owners
    projects = ['Digital Transformation', 'Youth Health Program', 'Sustainability Initiative', 
                'Customer Experience', 'Innovation Lab']
    owners = ['John Smith', 'Sarah Johnson', 'Mike Davis', 'Emily Brown', 'David Wilson']
    
    # Sample KPIs
    kpi_templates = [
        {'name': 'User Adoption Rate', 'goal': 'Increase platform adoption', 'target': 85},
        {'name': 'System Uptime', 'goal': 'Maintain system reliability', 'target': 99.5},
        {'name': 'Customer Satisfaction Score', 'goal': 'Improve customer experience', 'target': 90},
        {'name': 'Training Completion Rate', 'goal': 'Ensure staff readiness', 'target': 95},
        {'name': 'Cost Reduction', 'goal': 'Optimize operational costs', 'target': 20},
        {'name': 'Time to Market', 'goal': 'Accelerate product delivery', 'target': 30},
        {'name': 'Quality Score', 'goal': 'Maintain quality standards', 'target': 95},
        {'name': 'Engagement Rate', 'goal': 'Increase stakeholder engagement', 'target': 75},
        {'name': 'Process Efficiency', 'goal': 'Streamline operations', 'target': 80},
        {'name': 'Risk Mitigation', 'goal': 'Reduce operational risks', 'target': 90}
    ]
    
    data = []
    
    for i in range(30):  # Create 30 KPI records
        kpi = random.choice(kpi_templates)
        project = random.choice(projects)
        owner = random.choice(owners)
        
        # Generate realistic values
        target_value = kpi['target']
        actual_value = round(target_value * random.uniform(0.7, 1.15), 2)
        
        # Determine status based on performance
        performance = (actual_value / target_value) * 100
        if performance >= 90:
            status = 'G'  # Green
            progress = random.choice([4, 5])
        elif performance >= 70:
            status = 'Y'  # Yellow
            progress = random.choice([2, 3, 4])
        else:
            status = 'R'  # Red
            progress = random.choice([1, 2, 3])
        
        # Generate dates
        days_ago = random.randint(0, 30)
        last_updated = datetime.now() - timedelta(days=days_ago)
        
        # Calculate health and risk scores
        health_score = min(100, max(0, performance + random.uniform(-10, 10)))
        risk_score = 100 - health_score
        
        # Add description
        description = f"{kpi['name']} for {project} - Tracking {kpi['goal'].lower()}"
        
        data.append({
            'kpi_name': f"{kpi['name']} - {project[:15]}",
            'project': project,
            'goal': kpi['goal'],
            'description': description,
            'owner': owner,
            'status': status,
            'progress': progress,
            'target_value': target_value,
            'actual_value': actual_value,
            'last_updated': last_updated.strftime('%Y-%m-%d'),
            'health_score': round(health_score, 2),
            'risk_score': round(risk_score, 2),
            'notes': f"Last review: {random.choice(['On track', 'Needs attention', 'Under review', 'Action required'])}"
        })
    
    return pd.DataFrame(data)

def main():
    """Create and save sample Excel file"""
    
    # Create data directory if it doesn't exist
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Generate sample data
    df = create_sample_kpi_data()
    
    # Save to Excel with formatting
    output_file = os.path.join(data_dir, 'sample_kpi_data.xlsx')
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='KPI Data', index=False)
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['KPI Data']
        
        # Auto-adjust column widths
        for column in df.columns:
            column_width = max(df[column].astype(str).map(len).max(), len(column)) + 2
            col_idx = df.columns.get_loc(column)
            worksheet.column_dimensions[chr(65 + col_idx)].width = min(column_width, 50)
    
    print(f"[SUCCESS] Sample KPI data created successfully!")
    print(f"[FILE] File saved to: {output_file}")
    print(f"[INFO] Total KPIs: {len(df)}")
    print(f"[GREEN] Green status: {len(df[df['status'] == 'G'])}")
    print(f"[YELLOW] Yellow status: {len(df[df['status'] == 'Y'])}")
    print(f"[RED] Red status: {len(df[df['status'] == 'R'])}")
    print("\nYou can now upload this file to the dashboard!")
    
    # Display first few rows
    print("\nSample data preview:")
    print(df.head())
    
    return output_file

if __name__ == "__main__":
    main()