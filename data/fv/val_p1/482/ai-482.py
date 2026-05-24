import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for the required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Read the JSON file from the provided path
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

# Extract data and texts from the JSON structure
chart_data = chart_json['chart_data']
texts = chart_json['texts']
colors = chart_json['colors']
vertical_lines = chart_json.get('vertical_lines', [])

# Initialize the figure
fig = go.Figure()

# Add the line trace from the chart data
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)], width=3)
    ))

# Combine title and subtitle for the main chart title
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"

# Configure the layout of the chart
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[1989.5, 2016.5],
        tickmode='linear',
        tick0=1990,
        dtick=2,
        showgrid=False,
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 32],
        tickmode='linear',
        tick0=0,
        dtick=5,
        gridcolor='#e0e0e0'
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=50, r=20, t=80, b=80),
)

# Add vertical lines using shapes
for line in vertical_lines:
    fig.add_shape(
        type="line",
        x0=line['x'], y0=line['y_min'],
        x1=line['x'], y1=line['y_max'],
        line=dict(
            color=line.get('color', 'black'),
            width=line.get('width', 2),
        )
    )

# Add text annotations from the JSON
for ann in texts.get('annotations', []):
    fig.add_annotation(
        x=ann['x'],
        y=ann['y'],
        text=ann['text'],
        showarrow=False,
        xanchor='center',
        yanchor=ann.get('yanchor', 'bottom'),
        font=dict(family="Arial", size=12)
    )

# Add the source text as an annotation below the chart area
if texts.get('source'):
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0, y=-0.15,
        xanchor="left", yanchor="top",
        text=texts['source'],
        showarrow=False,
        align="left",
        font=dict(family="Arial", size=10)
    )

# Determine the output filename and save the chart as a PNG image
output_filename_base = json_path.stem
output_png_path = f"{output_filename_base}.png"
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")