import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

# Load the error rate report
with open('error_rate_report.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Prepare data for Panel 1: Overall Performance Comparison
chatbots_data = data['summary']['chatbots']
df_performance = pd.DataFrame(chatbots_data)

# Sort by error_rate_percent in ascending order
df_performance = df_performance.sort_values('error_rate_percent', ascending=True)

# Prepare data for Panel 2: Error Type Distribution
error_dist = data['error_type_distribution']
error_types = [
    "Fiscal vs Calendar Period Confusion",
    "Period Shift",
    "Rounding / Formatting",
    "Ambiguous Interpretation",
    "Non-Answer / Refusal"
]

# Create DataFrame for error type distribution
error_data = []
for chatbot in df_performance['chatbot']:
    row = {'chatbot': chatbot}
    for error_type in error_types:
        row[error_type] = error_dist[chatbot].get(error_type, 0)
    error_data.append(row)

df_errors = pd.DataFrame(error_data)

# Create the figure with 1 row, 2 columns
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Panel 1: Horizontal Bar Chart - Overall Performance Comparison
ax1 = axes[0]
bars = ax1.barh(df_performance['chatbot'], df_performance['error_rate_percent'], 
                color=sns.color_palette("viridis", len(df_performance)))

# Add data labels on each bar
for i, (idx, row) in enumerate(df_performance.iterrows()):
    ax1.text(row['error_rate_percent'] + 1, i, f"{row['error_rate_percent']:.1f}%",
             va='center', fontsize=10, fontweight='bold')

ax1.set_xlabel('Error Rate (%)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Chatbot', fontsize=12, fontweight='bold')
ax1.set_title('Overall Performance Comparison', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlim(0, max(df_performance['error_rate_percent']) * 1.15)
ax1.grid(axis='x', alpha=0.3, linestyle='--')

# Panel 2: Stacked Bar Chart - Error Type Distribution
ax2 = axes[1]

# Prepare data for stacking (bottom-up order for better visualization)
stack_order = error_types[::-1]  # Reverse order for bottom-up stacking
colors = sns.color_palette("Set2", len(error_types))

# Create stacked bars
bottom = None
for i, error_type in enumerate(stack_order):
    values = df_errors[error_type].values
    ax2.barh(df_errors['chatbot'], values, left=bottom, 
             label=error_type, color=colors[i], alpha=0.8)
    if bottom is None:
        bottom = values
    else:
        bottom = bottom + values

ax2.set_xlabel('Number of Errors', fontsize=12, fontweight='bold')
ax2.set_ylabel('Chatbot', fontsize=12, fontweight='bold')
ax2.set_title('Error Type Distribution', fontsize=14, fontweight='bold', pad=15)
ax2.legend(loc='lower right', fontsize=9, framealpha=0.9)
ax2.grid(axis='x', alpha=0.3, linestyle='--')

# Add super title
fig.suptitle('Comprehensive Chatbot Error Analysis', 
             fontsize=16, fontweight='bold', y=0.98)

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save the figure
output_path = 'error_rate_visualization.png'
plt.savefig(output_path, bbox_inches='tight', facecolor='white')
print(f"Visualization saved to: {output_path}")

# Display the plot
plt.show()

