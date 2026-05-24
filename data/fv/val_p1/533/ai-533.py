import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Create subplots for the two pie charts
fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

# Define the domains for each pie chart
domains = [
    {'x': [0, 0.48], 'y': [0.1, 1.0]},
    {'x': [0.52, 1.0], 'y': [0.1, 1.0]}
]

# Add pie chart traces
fig.add_trace(go.Pie(
    labels=data[0]['labels'],
    values=data[0]['values'],
    name=data[0]['title'],
    domain=domains[0],
    marker_colors=colors,
    texttemplate='<b>%{value}%</b>',
    textposition='inside',
    textfont=dict(color='white', size=24),
    hoverinfo='label+percent',
    sort=False,
    showlegend=True # Show legend for the first pie
), 1, 1)

fig.add_trace(go.Pie(
    labels=data[1]['labels'],
    values=data[1]['values'],
    name=data[1]['title'],
    domain=domains[1],
    marker_colors=colors,
    texttemplate='<b>%{value}%</b>',
    textposition='inside',
    textfont=dict(color='white', size=24),
    hoverinfo='label+percent',
    sort=False,
    showlegend=False # Hide for the second to avoid duplicates
), 1, 2)

# Update layout
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    title_font=dict(family='Arial', size=26, color='black'),
    font=dict(family="Arial", size=12, color="black"),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=100, b=150, l=40, r=40),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    annotations=[
        dict(
            text=data[0]['title'],
            x=0.24, y=0.85, xref="paper", yref="paper",
            font=dict(size=16),
            showarrow=False
        ),
        dict(
            text=data[1]['title'],
            x=0.76, y=0.85, xref="paper", yref="paper",
            font=dict(size=16),
            showarrow=False
        ),
        dict(
            text=texts['source'],
            x=0, y=-0.2, xref="paper", yref="paper",
            xanchor='left', yanchor='bottom',
            align='left',
            showarrow=False,
            font=dict(size=10)
        )
    ]
)

# Derive base filename from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")