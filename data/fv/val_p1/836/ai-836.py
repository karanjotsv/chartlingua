import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    sys.exit("Usage: python script.py <path_to_json_file>")

json_file_path = sys.argv[1]

# Load the chart data and configuration from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON object
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data structures for Plotly, preserving the original order
labels = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create a Plotly figure object
fig = go.Figure()

# Add the pie chart trace using the extracted data
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    textinfo='percent',
    texttemplate='%{value}%',
    hoverinfo='label+percent',
    sort=False  # This is crucial to maintain the order from the JSON file
))

# Format the title by combining title and subtitle if available
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Format the source text
source_text = texts.get('source', '')

# Configure the chart layout, font, title, legend, and margins
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial"
    ),
    showlegend=True,
    legend=dict(
        bgcolor='rgba(255,255,255,1)',
        bordercolor='Black',
        borderwidth=1
    ),
    margin=dict(l=40, r=150, t=100, b=40),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
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

# Derive the output PNG filename from the input JSON filename
base_filename, _ = os.path.splitext(json_file_path)
output_filename = f"{base_filename}.png"

# Save the generated chart as a high-resolution PNG file
fig.write_image(output_filename, scale=2)