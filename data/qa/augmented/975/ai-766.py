import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from the JSON structure
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Prepare data for Plotly
x_values = [d['x'] for d in data]
y_values = [d['y'] for d in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    texttemplate='%{text}',
    marker_color=colors[0] if colors else None,
    textfont=dict(family='Arial', size=12, color='black'),
    cliponaxis=False # Prevents text from being clipped at the top
))

# Combine title and subtitle
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    if full_title:
        full_title += "<br>"
    full_title += f"<i>{subtitle_text}</i>"

# Update layout
fig.update_layout(
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='#CCCCCC',
        tickfont=dict(family='Arial')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 850],
        tickmode='linear',
        tick0=0,
        dtick=100,
        gridcolor='#E0E0E0',
        showline=False,
        tickfont=dict(family='Arial')
    ),
    plot_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=80, r=40, t=80, b=100)
)

# Add source annotation
fig.add_annotation(
    text=texts.get('source'),
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0.99,
    y=-0.2,
    xanchor='right',
    yanchor='top',
    font=dict(family='Arial', size=12)
)


# Generate output filename from JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)