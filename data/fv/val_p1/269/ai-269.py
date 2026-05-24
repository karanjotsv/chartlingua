import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from JSON
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the donut chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.4,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    texttemplate="%{label}<br>%{value}%",
    textposition='inside',
    textfont=dict(family="Arial", size=20, color='black'),
    hoverinfo='skip',
    sort=False,
    direction='clockwise',
    rotation=90
)])

# Combine title and source using HTML for styling
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('source'):
    title_text += f"<br><span style='font-size: 14px; color: #555;'>{texts['source']}</span>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    showlegend=False,
    font=dict(
        family="Arial"
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=100, b=20, l=20, r=20),
    autosize=False,
    width=800,
    height=800
)

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")