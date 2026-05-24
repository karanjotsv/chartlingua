import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and configuration from the JSON object
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', {})

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [f"{v:.2f}%" for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker=dict(
        color=colors.get('bars'),
        line=dict(
            color=colors.get('border'),
            width=1.5
        )
    ),
    text=text_labels,
    textposition='outside',
    textfont=dict(
        family="Arial",
        color=colors.get('font')
    ),
    cliponaxis=False
))

# Build title string with potential subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor=colors.get('border'),
        mirror=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor=colors.get('border'),
        mirror=True,
        range=[0, max(values) * 1.25] if values else [0, 1]
    ),
    font=dict(
        family="Arial",
        color=colors.get('font')
    ),
    plot_bgcolor=colors.get('plot_bgcolor'),
    paper_bgcolor=colors.get('paper_bgcolor'),
    showlegend=False,
    margin=dict(t=80, b=50, l=50, r=50)
)

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")