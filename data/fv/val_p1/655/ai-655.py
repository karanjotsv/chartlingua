import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Check if the file exists
if not pathlib.Path(json_path).is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data for the chart
data_points = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Prepare data for Plotly pie chart
labels_for_hover = [item['label'].replace('<br>', ' ') for item in data_points]
values = [item['value'] for item in data_points]
text_for_display = [f"{item['label']}<br>{item['display_value']}" for item in data_points]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels_for_hover,
    values=values,
    text=text_for_display,
    textinfo='text',
    textposition='outside',
    hoverinfo='label+percent',
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    sort=False,
    direction='clockwise'
)

# Create the figure layout
layout = go.Layout(
    title=dict(
        text=texts.get('title', ''),
        y=0.08,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=24)
    ),
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    showlegend=False,
    margin=dict(l=60, r=60, t=60, b=120),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Create the figure object
fig = go.Figure(data=[pie_trace], layout=layout)

# Determine the output filename from the input JSON path
output_filename = pathlib.Path(json_path).stem + ".png"

# Write the image file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)