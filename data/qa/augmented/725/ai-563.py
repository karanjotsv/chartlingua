import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else '#2672CB',
    text=y_values,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False # Allows text to render outside plot area if needed
))

# Build title string
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br>{texts['subtitle']}"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(family="Arial")
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 25],
        gridcolor='#E0E0E0',
        griddash='dash',
        zeroline=False,
        showline=False,
        tickfont=dict(family="Arial")
    ),
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts.get("source", ""),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.15,
            xanchor="right",
            yanchor="top",
            font=dict(family="Arial", size=12)
        )
    ]
)

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")