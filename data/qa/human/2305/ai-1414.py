import sys
import json
import plotly.graph_objects as go
import pathlib

# This script requires a single command-line argument: the path to the JSON file.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get('chart_data', [])
chart_texts = chart_info.get('texts', {})
chart_colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series.get('name', ''),
        x=series.get('x', []),
        y=series.get('y', []),
        marker_color=chart_colors[i % len(chart_colors)],
        text=[f'{val}%' for val in series.get('y', [])],
        textposition='inside',
        textfont=dict(
            family='Arial',
            size=14,
            color='black'
        ),
        insidetextanchor='end',
        constraintext='inside'
    ))

# Combine title and subtitle if they exist
title_text = chart_texts.get('title') or ''
if chart_texts.get('subtitle'):
    title_text += f"<br><sub>{chart_texts.get('subtitle')}</sub>"

# Update layout for a professional and accurate look
fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12, color="black"),
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=chart_texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks=''
    ),
    yaxis=dict(
        title_text=chart_texts.get('y_axis_title'),
        range=[0, 60],
        tickvals=[0, 10, 20, 30, 40, 50, 60],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        font=dict(size=14)
    ),
    plot_bgcolor='white',
    margin=dict(l=80, r=40, t=50, b=150),
    annotations=[] # Initialize empty list for annotations
)

# Add source annotation
if chart_texts.get('source'):
    fig.add_annotation(
        text=chart_texts.get('source'),
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.35,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=12, color='grey')
    )

# Determine output filename from the input JSON filename
base_name = pathlib.Path(json_path).stem
output_file = f"{base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_file, scale=2)

print(f"Chart successfully generated and saved to '{output_file}'")