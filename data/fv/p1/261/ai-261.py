import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load the data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    categories = [item['category'] for item in series['data']]
    values = [item['value'] for item in series['data']]
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        name=series['series_name'],
        marker_color=colors[i % len(colors)]
    ))

# Build the title string
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(family="Arial")
    ),
    plot_bgcolor='#E5E5E5',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    xaxis=dict(
        tickangle=-60,
        automargin=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[50, 100],
        dtick=5,
        gridcolor='#C0C0C0'
    ),
    legend=dict(
        x=1.02,
        y=0.75,
        xanchor='left',
        yanchor='middle'
    ),
    margin=dict(l=60, r=120, t=80, b=150)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")