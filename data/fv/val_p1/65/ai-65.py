import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', {})

# Initialize the figure
fig = go.Figure()

# Add traces to the figure by iterating through the chart_data
for series in chart_data:
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('series_name', ''),
        line=dict(
            color=colors.get(series.get('color_key')),
            dash=series.get('line_style')
        ),
        showlegend=False
    ))

# Construct the full title from title and subtitle
title_parts = []
if texts.get("title"):
    title_parts.append(f"<b>{texts['title']}</b>")
if texts.get("subtitle"):
    title_parts.append(texts['subtitle'])
full_title = "<br>".join(title_parts)

# Update layout for a professional and accurate appearance
fig.update_layout(
    font_family="Arial",
    title=dict(
        text=full_title,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=14)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[-2, 102],
        tickmode='linear',
        tick0=0,
        dtick=10,
        showgrid=True,
        gridcolor='#CCCCCC',
        gridwidth=1,
        zeroline=False,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[-2, 102],
        tickmode='linear',
        tick0=0,
        dtick=10,
        showgrid=True,
        gridcolor='#CCCCCC',
        gridwidth=1,
        zeroline=False,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=120, b=60),
    width=800,
    height=700
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")