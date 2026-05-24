import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create the figure
fig = go.Figure()

# Add traces from the data
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=series['y'],
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False # Allows text to render outside the plot area
    ))

# Build title and source strings
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = texts.get('source') or ''

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=title_text,
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 60],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        ticks='outside',
        tickprefix=' '
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.25, # Adjusted for multiline x-axis labels
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")