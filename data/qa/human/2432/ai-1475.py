import sys
import json
import plotly.graph_objects as go

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
categories = chart_info.get('categories', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['values'],
        name=series['name'],
        marker_color=colors[i % len(colors)],
        text=[f'{v}%' for v in series['values']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', family='Arial', size=12, weight='bold'),
        hovertemplate='%{y}%<extra></extra>'
    ))

# Combine title and subtitle if they exist
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

# Update layout
fig.update_layout(
    barmode='stack',
    title_text=full_title if full_title else None,
    font=dict(family="Arial"),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 100],
        tickvals=[0, 25, 50, 75, 100],
        ticksuffix='%',
        gridcolor='#e0e0e0'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=60, b=120),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.25,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Determine the output filename from the input JSON path
output_filename = json_path.rsplit('.', 1)[0] + '.png'

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")