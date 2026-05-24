import sys
import json
import os
import plotly.graph_objects as go

# Ensure the script is called with a JSON file path
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces (bars) to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x', []),
        y=series.get('y', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None,
        showlegend=False
    ))

# Construct title and subtitle from JSON texts
title_text = ""
if texts.get('title'):
    title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

# Update the layout of the figure
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font_family="Arial",
    xaxis_title_text=texts.get('x_axis_title'),
    yaxis_title_text=texts.get('y_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    bargap=0.15,
    margin=dict(t=60, b=80, l=60, r=40),
    xaxis=dict(
        type='category',
        showgrid=False,
        linecolor='black',
        ticks='outside',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 50],
        showgrid=True,
        gridcolor='lightgrey',
        linecolor='black',
        ticks='outside',
        tickfont=dict(size=12)
    )
)

# Add source annotation if present
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top',
        font=dict(size=10)
    )

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)