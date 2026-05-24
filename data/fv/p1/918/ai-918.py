import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Derive the base filename for the output image from the JSON file path
filename_base = os.path.splitext(os.path.basename(json_file_path))[0]

# Read and parse the JSON file
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
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for the Plotly pie chart
values = [item.get('value') for item in data]
categories = [item.get('category') for item in data]

# Create custom labels as seen on the original chart
custom_labels = []
for item in data:
    formatted_value = f"{item.get('value'):,}"
    label_text = f"<b>{item.get('category')}</b><br>{formatted_value}<br>{item.get('percentage')}%"
    custom_labels.append(label_text)

# Create the pie chart trace
pie_trace = go.Pie(
    labels=categories,
    values=values,
    text=custom_labels,
    textinfo='text',
    textposition='outside',
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    sort=False,  # Preserve the order from the JSON data
    direction='clockwise',
    automargin=True
)

# Combine title and subtitle for the chart title
title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

# Configure the chart layout
layout = go.Layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,  # The original chart does not have a separate legend
    margin=dict(l=80, r=80, t=100, b=80),
    width=800,
    height=650
)

# Create the figure object
fig = go.Figure(data=[pie_trace], layout=layout)

# Generate the output image file
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")