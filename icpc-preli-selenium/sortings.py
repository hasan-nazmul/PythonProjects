import pandas as pd

def count_teams_by_university(input_file, output_file):
    """
    Read CSV file, count teams per university, sort in descending order, and save to new CSV
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Count teams per university
    team_counts = df['University'].value_counts().reset_index()
    
    # Rename columns for clarity
    team_counts.columns = ['University', 'Number_of_Teams']
    
    # Sort in descending order by team count
    team_counts = team_counts.sort_values('Number_of_Teams', ascending=False)
    
    # Save to new CSV file
    team_counts.to_csv(output_file, index=False)
    
    print(f"Team counts saved to {output_file}")
    print("\nTop 10 universities by team count:")
    print(team_counts.head(10).to_string(index=False))
    
    return team_counts

# Usage
input_csv = 'icpc_teams_all_complete.csv'
output_csv = 'university_team_counts.csv'
result = count_teams_by_university(input_csv, output_csv)