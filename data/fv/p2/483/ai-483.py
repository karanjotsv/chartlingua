import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    texttemplate='%{label}<br>%{value}%',
    textposition='inside',
    textfont=dict(size=16, color='black'),
    sort=False,
    direction='clockwise',
    rotation=90
)])

# Update layout
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=18)
    ),
    showlegend=False,
    font=dict(family="Arial", color='black'),
    margin=dict(t=120, b=80, l=40, r=40),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ]
)

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")