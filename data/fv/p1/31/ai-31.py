import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data and text from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [d.get('category') for d in chart_data]
values = [d.get('value') for d in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace using data from the JSON
if chart_data:
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors[0] if colors else None,
        name=''  # Use an empty name to hide from legend
    ))

# Combine title and subtitle using HTML for rich text formatting
title_text = texts.get('title', '')
subtitle_text = texts.get('subtitle')
if subtitle_text:
    title_text = f"<b>{title_text}</b><br><sub>{subtitle_text}</sub>"

# Configure the layout of the chart
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=20)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True,
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 500],
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True,
        tickfont=dict(size=14)
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=30, t=80, b=80),
)

# Add source text as an annotation if it exists
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0, y=-0.2,
        showarrow=False,
        align="left",
        xanchor="left",
        yanchor="top",
        font=dict(size=12)
    )

# Determine the output filename and save the chart as a PNG image
output_path = json_path.with_suffix('.png')
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")