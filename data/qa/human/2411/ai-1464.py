import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument for the JSON file
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Get JSON file path from command line
json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = chart_data['categories']
series = chart_data['series']

# Create a new figure
fig = go.Figure()

# Add a bar trace for each data series
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s['values'],
        name=s['name'],
        marker_color=colors[i],
        text=s['values'],
        textposition='outside',
        cliponaxis=False,
        textfont=dict(family="Arial", size=12, color='#000000')
    ))

# Construct title and source strings from the JSON data
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}" if title_text else texts['subtitle']

source_text = ""
if texts.get('source'):
    source_text += texts['source']
if texts.get('note'):
    source_text += f"<br>{texts['note']}" if source_text else texts['note']

# Configure the chart layout
fig.update_layout(
    barmode='group',
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        font=dict(family="Arial")
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        ticks='outside',
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 800],
        dtick=200,
        tickfont=dict(family="Arial", size=12),
        title_font=dict(family="Arial")
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        font=dict(family="Arial")
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=60, r=40, t=50, b=150),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.3,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(family="Arial", size=10, color='grey')
        )
    ]
)

# Generate output image file name from the input JSON file name
output_filename = json_file_path.stem + '.png'

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")