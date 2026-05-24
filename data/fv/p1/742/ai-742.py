import sys
import json
import os
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
series_data = chart_data.get('series', [])
x_axis_labels = texts.get('x_axis_labels', chart_data.get('categories', []))

# Create the figure object
fig = go.Figure()

# Add a bar trace for each series in the data, in order
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        name=series.get('name'),
        x=x_axis_labels,
        y=series.get('values'),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Update the layout of the chart
fig.update_layout(
    barmode='stack',
    title={
        'text': texts.get('title'),
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis={
        'title': texts.get('x_axis_title'),
        'tickangle': 0,
        'automargin': True
    },
    yaxis={
        'title': texts.get('y_axis_title'),
        'range': [0, 60],
        'gridcolor': '#E5E5E5'
    },
    legend={
        'orientation': 'h',
        'yanchor': 'top',
        'y': -0.3, # Adjust to position below x-axis labels
        'xanchor': 'center',
        'x': 0.5
    },
    font={
        'family': "Arial",
        'size': 12
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=50, r=50, t=80, b=180) # Increased bottom margin for labels/legend
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")