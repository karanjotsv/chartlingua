import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for Plotly (reverse order for horizontal bar chart)
# Plotly plots the first item in the y-axis list at the bottom.
# To match the visual order (highest on top), we reverse the data lists.
reversed_data = chart_data[::-1]
categories = [item['category'] for item in reversed_data]
values = [item['value'] for item in reversed_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='black'),
    cliponaxis=False  # Allow text to be drawn outside the axis range
))

# Build title string
title_text = texts.get("title") or ""
subtitle_text = texts.get("subtitle") or ""
if title_text and subtitle_text:
    full_title = f"<b>{title_text}</b><br>{subtitle_text}"
elif title_text:
    full_title = f"<b>{title_text}</b>"
else:
    full_title = subtitle_text

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(text=full_title, x=0.05, y=0.95, xanchor='left', yanchor='top'),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        range=[0, 250],
        dtick=25
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    bargap=0.4,
    margin=dict(l=150, r=40, t=40, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.12,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

# Generate output filename from the input JSON filename
output_filename = json_file_path.stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")