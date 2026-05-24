import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', ['#808080'])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    textfont=dict(
        family="Arial, bold",
        size=12,
        color='black'
    ),
    marker=dict(
        color=colors[0],
        line=dict(
            color='#4d4d4d',
            width=1
        )
    ),
    cliponaxis=False
))

# Combine title and subtitle using HTML for formatting
title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size: 12px;'>{texts.get('subtitle', '')}</span>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickfont=dict(size=11),
        showline=True,
        linewidth=1,
        linecolor='lightgrey',
        mirror=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 450],
        tick0=0,
        dtick=50,
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linewidth=1,
        linecolor='lightgrey',
        mirror=True
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=50, r=20, t=80, b=50)
)

# Determine output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")