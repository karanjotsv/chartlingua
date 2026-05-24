import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Prepare data for Plotly
chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', [])

# Create labels that include the percentage, matching the original chart's legend and slice text
labels = [f"{item['category']} {item['value']}%" for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    sort=False,
    textinfo='label',
    textfont=dict(size=14, family="Arial", color='black'),
    hoverinfo='label',
    insidetextorientation='horizontal'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title', ''),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=24, family="Arial", color="black", weight="bold")
    ),
    legend=dict(
        orientation='v',
        yanchor="top",
        y=0.3,
        xanchor="left",
        x=0.2,
        font=dict(family="Arial", size=16, color="black"),
        bgcolor='rgba(0,0,0,0)' # Transparent background
    ),
    margin=dict(l=40, r=40, t=100, b=100),
    font=dict(family="Arial"),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Derive output filename from the input JSON filename
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")