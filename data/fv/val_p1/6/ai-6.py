import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.6,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=3)),
    pull=[0.03, 0.03, 0.03, 0.03],
    textinfo='value',
    texttemplate='%{value}%',
    textfont=dict(color='white', size=16),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=155
)])

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title', ''),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    showlegend=True,
    legend=dict(
        x=0.5,
        y=-0.1,
        xanchor='center',
        yanchor='top',
        orientation='v'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=40, r=40, b=150, t=150),
    paper_bgcolor='white',
    plot_bgcolor='white',
    autosize=False,
    width=600,
    height=700
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
except ValueError as e:
     if "requires the kaleido package" in str(e):
        print("Please install kaleido: pip install kaleido")
        sys.exit(1)
     raise

print(f"Chart saved to {output_filename}")