import pandas as pd

# Extract data from the table
data = pd.read_csv('standings_multiple_pages_20250930_023141.csv')

data = data[['Team Name', 'University', 'Solved']]

# Group by university and calculate the required statistics
university_stats = data.groupby('University').agg(
    total_teams_participated=('Team Name', 'count'),
    teams_solved_at_least_1=('Solved', lambda x: (x >= 1).sum())
).reset_index()

# Rename columns for clarity
university_stats.columns = ['University Name', 'Total Teams Participated', 'Teams Solved At Least 1 Problem']

# Sort by priority: 
# 1. Teams Solved At Least 1 Problem (higher to lower)
# 2. Total Teams Participated (higher to lower) 
# 3. University Name (lexicographical order)
university_stats = university_stats.sort_values(
    by=['Teams Solved At Least 1 Problem', 'Total Teams Participated', 'University Name'], 
    ascending=[False, False, True]
)

# Save to new CSV file
university_stats.to_csv('university_participation_stats.csv', index=False)

print("CSV file 'university_participation_stats.csv' has been created successfully!")
print(f"\nTotal universities: {len(university_stats)}")
print("\nGenerated Data:")
print(university_stats.to_string(index=False))