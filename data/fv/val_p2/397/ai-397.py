import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', {})

# Initialize the figure
fig = go.Figure()

# Add traces (lines) for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=colors.get('line_colors', [])[i], width=2),
        showlegend=False
    ))

# Prepare layout elements
# Add horizontal bands for background styling
shapes = []
for y_start in range(100, 800, 200):
    shapes.append(
        go.layout.Shape(
            type="rect",
            xref="paper",
            yref="y",
            x0=0,
            y0=y_start,
            x1=1,
            y1=y_start + 100,
            fillcolor=colors.get('band_color'),
            layer="below",
            line_width=0
        )
    )

# Prepare annotations for line labels
annotations = []
for ann in texts.get('annotations', []):
    annotations.append(
        dict(
            x=ann.get('x'),
            y=ann.get('y'),
            text=ann.get('text', ''),
            showarrow=False,
            font=dict(
                family="Arial",
                size=12,
                color=colors.get('text_color')
            ),
            textangle=-ann.get('angle', 0), # Plotly textangle is clockwise
            xanchor='center',
            yanchor='middle'
        )
    )

# Combine title and subtitle if they exist
title_text = texts.get('title_text', '')
if texts.get('subtitle_text'):
    title_text += f"<br><sub>{texts.get('subtitle_text')}</sub>"

# Update layout
fig.update_layout(
    title_text=title_text if title_text else None,
    paper_bgcolor=colors.get('paper_bgcolor'),
    plot_bgcolor=colors.get('plot_bgcolor'),
    font=dict(family="Arial", size=12, color=colors.get('text_color')),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[1500, 5000],
        tickmode='linear',
        tick0=1500,
        dtick=500,
        showgrid=True,
        gridcolor=colors.get('grid_color'),
        gridwidth=1,
        zeroline=False,
        mirror=True,
        ticks='outside',
        showline=True,
        linewidth=2,
        linecolor='black'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 800],
        tickmode='linear',
        tick0=100,
        dtick=100,
        showgrid=True,
        gridcolor=colors.get('grid_color'),
        gridwidth=1,
        zeroline=False,
        mirror=True,
        ticks='outside',
        showline=True,
        linewidth=2,
        linecolor='black'
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=80),
    shapes=shapes,
    annotations=annotations
)

# Define output filename and save the chart
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")