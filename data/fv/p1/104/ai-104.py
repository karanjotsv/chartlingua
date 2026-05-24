import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly
labels = [d.get('label', '') for d in chart_data]
values = [d.get('value', 0) for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2)
    ),
    sort=False,
    direction='clockwise',
    textinfo='none',
    hoverinfo='skip'
))

# Combine title and subtitle, handling null values
title_parts = [texts.get('title'), texts.get('subtitle')]
title_text = "<br>".join(filter(None, title_parts))

# Combine source and note, handling null values
footnote_parts = [texts.get('source'), texts.get('note')]
footnote_text = "<br>".join(filter(None, footnote_parts))

# Update layout properties
fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_y=0.95,
    title_xanchor='left',
    title_yanchor='top',
    showlegend=False,
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(family="Arial", color='white'),
    margin=dict(l=20, r=20, t=50, b=50)
)

# Add footnote annotation if text exists
if footnote_text:
    fig.add_annotation(
        text=footnote_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.01,
        y=0.01,
        xanchor='left',
        yanchor='bottom',
        font=dict(size=12)
    )

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

# Write the image file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")