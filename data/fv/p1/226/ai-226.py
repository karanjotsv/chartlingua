import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Derive base filename from the JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

# Extract data for plotting
chart_data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [f"{item['label']}<br>{item['value']}%" for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    text=text_labels,
    textinfo='text',
    textposition='outside',
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=90,
    textfont=dict(size=12, family="Arial")
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Build the title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Configure the layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=20)
    ),
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(t=100, b=120, l=40, r=40),
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
            align='left',
            font=dict(size=10)
        )
    ]
)

# Output the image
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")