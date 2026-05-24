import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json>")
    sys.exit(1)

# Get JSON file path from command-line argument
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

# Extract data for the chart
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    textinfo='percent',
    hoverinfo='label+percent',
    textfont=dict(size=18, family="Arial", color='black'),
    sort=False,
    direction='clockwise',
    pull=[0.01] * len(values) # Slight pull for better slice separation
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update the layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        font=dict(size=20, family="Arial"),
        x=0.5,
        xanchor='center'
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=True,
    legend=dict(
        x=0.85,
        y=0.8,
        xanchor='left',
        yanchor='top',
        font=dict(size=14),
        bgcolor='rgba(0,0,0,0)' # Transparent background
    ),
    margin=dict(l=40, r=150, t=80, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON path
p = pathlib.Path(json_path)
output_filename = f"{p.stem}.png"

# Write the image to a file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)