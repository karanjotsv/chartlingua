import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if a file path is provided
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_filepath = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_filepath}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_filepath}'")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0] if colors else '#1f77b4',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

# Create vertical separator lines
shapes = []
for i in range(len(categories) - 1):
    shapes.append(
        go.layout.Shape(
            type="line",
            x0=i + 0.5,
            y0=0,
            x1=i + 0.5,
            y1=1,
            xref="x",
            yref="paper",
            line=dict(color="rgba(230, 230, 230, 1)", width=1)
        )
    )

# Build title and source strings
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout for a clean, professional look
fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.5,
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 25],
        tickmode='linear',
        tick0=0,
        dtick=5,
        gridcolor='lightgray',
        griddash='dot',
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    shapes=shapes,
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.28, # Position below x-axis labels
            xanchor='right',
            yanchor='top',
            align='right'
        )
    ]
)

# Generate output filename from the input JSON path
output_path = pathlib.Path(json_filepath)
output_filename = output_path.with_suffix('.png').name

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")