import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from JSON
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart trace
# Explode all slices except the first one to match the visual style
pull_values = [0.03 if i > 0 else 0 for i in range(len(data))]

pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    pull=pull_values,
    textinfo='label+percent',
    textposition='outside',
    outsidetextfont=dict(family="Arial", size=12, color='black'),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    showlegend=False
)

# Create the layout
layout = go.Layout(
    title=None, # No title in the original chart
    font=dict(family="Arial"),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=80, r=80, t=80, b=80),  # Generous margins for outside labels
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            x=1,
            y=0,
            xref="paper",
            yref="paper",
            xanchor="right",
            yanchor="bottom",
            font=dict(family="Arial", size=10, color="grey")
        )
    ]
)

# Create the figure
fig = go.Figure(data=[pie_trace], layout=layout)

# Generate and save the output image
output_filename = json_file_path.stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")