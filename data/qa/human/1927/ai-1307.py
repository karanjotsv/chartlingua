import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.name.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read the JSON data from the specified file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors[0] if colors else '#297ACC'),
    text=values,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

# Update layout
layout_options = {
    'font': dict(family="Arial", size=12),
    'plot_bgcolor': 'white',
    'paper_bgcolor': 'white',
    'xaxis': dict(
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        ticks='',
        title=texts.get('x_axis_title'),
        range=[0, max(values) * 1.2] # Proactively set range to avoid label clipping
    ),
    'yaxis': dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        autorange="reversed" # This is an alternative to reversing data, but reversed data is safer
    ),
    'margin': dict(l=200, r=40, b=80, t=40),
    'showlegend': False
}

# Add title if it exists
if texts.get('title'):
    title_text = texts['title']
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"
    layout_options['title'] = {'text': title_text, 'x': 0.05, 'xanchor': 'left'}

fig.update_layout(**layout_options)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=12, color='grey')
    )

# Determine the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")