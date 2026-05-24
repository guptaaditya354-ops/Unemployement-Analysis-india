# UNEMPLOYMENT ANALYSIS - INDIA

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

print("Loading Data...")

df = pd.read_csv('Unemployment_Rate_upto_11_2020.csv')

# Strip column names
df.columns = df.columns.str.strip()

# Rename columns
df.rename(columns={
    'Estimated Unemployment Rate (%)': 'Unemployment',
    'Estimated Employed': 'Employed',
    'Estimated Labour Participation Rate (%)': 'Labour',
    'Region.1': 'Zone'
}, inplace=True)

# Date fix
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# Add Month and Year columns for filtering
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

print(f"Loaded! Shape: {df.shape}")
print(f"Date Range: {df['Date'].min()} to {df['Date'].max()}")

# ===== ANALYSIS =====

print("\n--- Statistics ---")
print(f"Average Unemployment: {df['Unemployment'].mean():.2f}%")

# COVID Impact
pre = df[df['Date'] < '2020-03-01']['Unemployment'].mean()
during = df[(df['Date'] >= '2020-03-01') & (df['Date'] <= '2020-06-01')]['Unemployment'].mean()

print(f"\nPre-COVID (Before Mar 2020): {pre:.2f}%")
print(f"During COVID (Mar-Jun 2020): {during:.2f}%")
print(f"Shock Increase: +{during-pre:.2f}%")

# Zone wise
print("\n--- Zone wise ---")
for zone in df['Zone'].unique():
    pre_z = df[(df['Zone']==zone) & (df['Date']<'2020-03-01')]['Unemployment'].mean()
    during_z = df[(df['Zone']==zone) & (df['Date']>='2020-03-01') & (df['Date']<='2020-06-01')]['Unemployment'].mean()
    print(f"{zone}: {pre_z:.2f}% -> {during_z:.2f}%")

# Top Affected States (April 2020)
print("\n--- Top Affected States (April 2020) ---")
# Filter for April 2020
april_2020 = df[(df['Month'] == 4) & (df['Year'] == 2020)]
print(f"April 2020 rows: {len(april_2020)}")

if len(april_2020) > 0:
    top = april_2020.nlargest(10, 'Unemployment')
    print(top[['Region', 'Zone', 'Unemployment']])
else:
    # Try May 2020 instead
    print("Checking May 2020...")
    may_2020 = df[(df['Month'] == 5) & (df['Year'] == 2020)]
    top = may_2020.nlargest(5, 'Unemployment')
    print(top[['Region', 'Zone', 'Unemployment']])

# ===== CHARTS =====

print("\nCreating Charts...")

# Chart 1: Overall Trend
plt.figure(figsize=(12, 5))
monthly = df.groupby('Date')['Unemployment'].mean()
plt.plot(monthly.index, monthly.values, linewidth=2, color='blue')
plt.axvline(pd.Timestamp('2020-03-25'), color='red', linestyle='--', label='Lockdown')
plt.title('Unemployment Rate in India')
plt.xlabel('Date')
plt.ylabel('Unemployment %')
plt.grid(True)
plt.legend()
plt.savefig('chart1_trend.png')
plt.close()

# Chart 2: Zone wise
plt.figure(figsize=(12, 5))
for zone in df['Zone'].unique():
    data = df[df['Zone'] == zone].groupby('Date')['Unemployment'].mean()
    plt.plot(data.index, data.values, label=zone)
plt.title('Unemployment by Zone')
plt.xlabel('Date')
plt.ylabel('Unemployment %')
plt.legend()
plt.grid(True)
plt.savefig('chart2_zone.png')
plt.close()

# Chart 3: Top States (April OR May 2020)
plt.figure(figsize=(10, 5))

# Use available data
if len(april_2020) > 0:
    peak_data = april_2020
else:
    peak_data = df[(df['Month'] == 5) & (df['Year'] == 2020)]

top = peak_data.nlargest(10, 'Unemployment')
plt.bar(top['Region'], top['Unemployment'], color='red')
plt.title('Most Affected States (Peak COVID Period)')
plt.xlabel('State')
plt.ylabel('Unemployment %')
plt.xticks(rotation=45)
plt.savefig('chart3_top_states.png')
plt.close()

# Chart 4: Labour Participation
plt.figure(figsize=(12, 5))
monthly_labour = df.groupby('Date')['Labour'].mean()
plt.plot(monthly_labour.index, monthly_labour.values, linewidth=2, color='green')
plt.title('Labour Participation Rate')
plt.xlabel('Date')
plt.ylabel('Labour %')
plt.grid(True)
plt.savefig('chart4_labour.png')
plt.close()

print("Charts Saved!")

# ===== INSIGHTS =====

print("\n" + "="*50)
print("INSIGHTS")
print("="*50)
print("""
📊 KEY FINDINGS:
1. Unemployment spiked by +9.48% during COVID lockdown
2. East Zone most affected (7.53% -> 26.05%)
3. South Zone also heavily impacted (4.21% -> 21.79%)
4. Labour participation dropped significantly

💡 POLICY RECOMMENDATIONS:
1. Focus on East zone (Bihar, Jharkhand, West Bengal)
2. Create emergency jobs in South states
3. Migrant worker welfare schemes
4. Skill development programs
""")

print("\n" + "="*50)
print("DONE!")
print("="*50)