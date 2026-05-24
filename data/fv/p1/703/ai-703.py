import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item.get('category') for item in chart_data]
values = [item.get('value') for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker=dict(
        color=colors[0] if colors else '#9999FF',
        line=dict(
            color='black',
            width=1.5
        )
    ),
    name=''
))

# Combine title and subtitle if available
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        tickangle=-90,
        showgrid=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', ''),
        range=[0, 350],
        dtick=50,
        showgrid=True,
        gridcolor='darkgrey',
        gridwidth=1
    ),
    plot_bgcolor='#E5E5E5',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    margin=dict(l=60, r=40, t=80, b=280) # Increased bottom margin for long labels
)


# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)