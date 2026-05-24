import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(chart_data):
    # Format text for bold appearance inside bars
    bar_texts = [f'<b>{val}</b>' for val in series['y']]
    
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i % len(colors)],
        text=bar_texts,
        textposition='inside',
        textfont=dict(
            family="Arial",
            size=12,
            color='white'
        ),
        insidetextanchor='middle'
    ))

# Combine title and subtitle if they exist
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += title_text
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

# Update layout
fig.update_layout(
    barmode='stack',
    title_text=full_title if full_title else None,
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 300],
        tick0=0,
        dtick=50,
        gridcolor='#e9e9e9'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=60, r=30, t=50, b=120)
)

# Add source annotation
fig.add_annotation(
    text=texts.get('source'),
    align='right',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=1.0,
    y=-0.32,
    xanchor='right',
    yanchor='bottom',
    font=dict(size=10)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")