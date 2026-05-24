import sys
import json
import plotly.graph_objects as go
import pathlib

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data and texts from the loaded JSON
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
    marker_color=colors,
    text=values,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    cliponaxis=False # Allows text to be drawn outside the plotting area
))

# Build title and source strings, handling null values gracefully
title_text_parts = [texts.get('title'), texts.get('subtitle')]
title_text = '<br>'.join(filter(None, title_text_parts))

source_text = texts.get('source')

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 200],
        dtick=25,
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        showline=False,
        tickfont=dict(size=12)
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100)
)

# Add source annotation
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper",
        yref="paper",
        x=1,
        y=-0.2, # Position below the x-axis labels
        xanchor='right',
        yanchor='top',
        showarrow=False,
        font=dict(
            family="Arial",
            size=12,
            color='black'
        )
    )

# Determine output filename and save the image
output_path = pathlib.Path(json_file_path)
output_filename = output_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")