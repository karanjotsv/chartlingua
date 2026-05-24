import sys
import json
import os
import plotly.graph_objects as go

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Ensure the JSON file exists before proceeding.
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Load all data and text from the specified JSON file.
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly's bottom-up plotting order to match the visual (top-down).
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
categories.reverse()
values.reverse()

# Create the figure object.
fig = go.Figure()

# Add the main bar trace.
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0] if colors else '#2F7ED8'),
    text=[str(v) for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=12),
    cliponaxis=False # Prevent text from being clipped by the plot area
))

# Configure the layout, fonts, titles, and annotations.
fig.update_layout(
    font=dict(family="Arial", size=12, color='#333333'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        range=[0, max(values) * 1.15] # Extend range to prevent text clipping
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        ticks='',
        showline=True,
        linecolor='#e0e0e0'
    ),
    margin=dict(l=150, r=40, t=40, b=80), # Adjust margins for labels
    annotations=[
        dict(
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.1,
            xanchor='right',
            yanchor='top',
            align='right',
            text=texts.get('source', ''),
            font=dict(family="Arial", size=12, color='grey')
        )
    ]
)

# Derive the output filename from the input JSON filename.
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Write the generated chart to a PNG file with a high resolution.
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")