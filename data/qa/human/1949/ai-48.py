import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# The original chart displays "Label Value%" for each slice.
# We create this custom text for the pie chart trace.
custom_text = [f"{item['label']} {item['value']}%" for item in data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=custom_text,
    textinfo='text',
    textposition='outside',
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    hole=0,
    sort=False,
    direction='clockwise'
))

# Build title string if it exists
title_text = texts.get('title')
if title_text and texts.get('subtitle'):
    title_text = f"{texts['title']}<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text,
    showlegend=False,
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(l=100, r=100, t=50, b=50),
    paper_bgcolor='white',
    plot_bgcolor='white',
    uniformtext_minsize=10,
    uniformtext_mode='hide'
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=0,
        xanchor='right',
        yanchor='bottom',
        font=dict(family="Arial", size=10, color="grey")
    )

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_filename = f"{base_filename}.png"

fig.write_image(output_image_filename, scale=2)

print(f"Chart saved to {output_image_filename}")