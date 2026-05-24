import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Derive the output filename from the input JSON filename
output_filename = json_path.with_suffix(".png").name

# Load the chart data and configuration from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly
categories = [item.get('category') for item in chart_data]
values = [item.get('value') for item in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=values,
    texttemplate='%{text:.2f}',
    textposition='outside',
    cliponaxis=False  # Prevent text labels from being clipped by the plot area
))

# Combine title and subtitle using HTML for rich text formatting
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the figure layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 10.5],
        tickmode='linear',
        tick0=0,
        dtick=2,
        gridcolor='#e5e5e5',
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=50, b=120)
)

# Add annotations for source and note text
annotations = []
if texts.get("source"):
    annotations.append(
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            font=dict(size=11, color='grey')
        )
    )

if annotations:
    fig.update_layout(annotations=annotations)

# Save the generated chart to a PNG file with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")