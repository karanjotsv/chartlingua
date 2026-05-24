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

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    hoverinfo='label+percent',
    textinfo='value',
    texttemplate='%{value}%',
    textposition='outside',
    sort=False,  # This is crucial to preserve the original order
    direction='clockwise',
    rotation=90 - (360 * values[0] / sum(values)) # Start with the first slice's right edge at 12 o'clock, approximately matching the original
))

# Update layout for a professional look
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_y=0.95,
    title_font_size=20,
    font_family="Arial",
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.85,
        xanchor='left',
        yanchor='top'
    ),
    margin=dict(t=100, b=80, l=40, r=40),
    plot_bgcolor='white'
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts.get('source'),
        xref="paper",
        yref="paper",
        x=0.98,
        y=0.02,
        xanchor='right',
        yanchor='bottom',
        showarrow=False,
        font=dict(
            family="Arial",
            size=12,
            color="grey"
        )
    )

# Determine output filename and save the image
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")