import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data from the loaded JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = texts['categories']

# Create the figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(chart_data):
    # Determine text color based on background color luminance for contrast
    hex_color = colors[i].lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    luminance = (0.299 * r + 0.587 * g + 0.114 * b)
    text_color = 'black' if luminance > 150 else 'white'

    # Create text labels, omitting for small values to avoid clutter
    text_labels = [f'{v}%' if v >= 1.5 else '' for v in series['values']]

    fig.add_trace(go.Bar(
        name=series['name'],
        x=categories,
        y=series['values'],
        marker_color=colors[i],
        text=text_labels,
        textposition='inside',
        textfont=dict(color=text_color, family="Arial", size=14, weight='bold'),
        insidetextanchor='middle'
    ))

# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Configure layout
fig.update_layout(
    barmode='stack',
    title_text=title_text,
    xaxis_title_text=texts['x_axis_title'],
    yaxis_title_text=texts['y_axis_title'],
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=50, b=150),
    yaxis=dict(
        range=[0, 125],
        tickvals=[0, 25, 50, 75, 100, 125],
        tickformat="g",
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        zeroline=False
    ),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=14)
    )
)

# Add source annotation
if texts.get("source"):
    fig.add_annotation(
        showarrow=False,
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=0.99,
        y=-0.28,
        xanchor='right',
        yanchor='top',
        font=dict(size=10)
    )

# Generate output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")