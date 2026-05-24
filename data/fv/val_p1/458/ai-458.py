import sys
import json
import plotly.graph_objects as go
import os

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_data_json['chart_data']
chart_texts = chart_data_json['texts']
chart_colors = chart_data_json['colors']

# Prepare data for Plotly
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
legend_labels = [f"{d['label']} {d['value']}%" for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie trace
fig.add_trace(go.Pie(
    labels=legend_labels,
    values=values,
    marker=dict(
        colors=chart_colors,
        line=dict(color='#A9A9A9', width=1)
    ),
    sort=False,
    direction='clockwise',
    rotation=90,
    textinfo='none',
    hoverinfo='label+percent',
    name='' # This can help avoid a trace name in the hover label
))

# Configure layout
title_text = ""
if chart_texts.get('title'):
    title_text = f"<b>{chart_texts['title']}</b>"
if chart_texts.get('subtitle'):
    title_text += f"<br>{chart_texts['subtitle']}"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(size=20)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.7,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.5)'
    ),
    margin=dict(t=90, b=50, l=50, r=50)
)

# Determine output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the image file
try:
    fig.write_image(output_filename, scale=2)
except ValueError as e:
    if "requires the kaleido package" in str(e):
        print("Error: The 'kaleido' package is required to write static images.")
        print("Please install it using: pip install kaleido")
        sys.exit(1)
    else:
        raise e

print(f"Chart saved to {output_filename}")