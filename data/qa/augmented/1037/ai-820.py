import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
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

# Extract data and text from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    text=y_values,
    textposition='outside',
    texttemplate='%{text}',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    # Clip text above bars that would go outside the plot area
    cliponaxis=False
))

# Combine title and subtitle if they exist
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<span style='font-size: 24px;'><b>{title_text}</b></span>"
if subtitle_text:
    full_title += f"<br><span style='font-size: 16px;'>{subtitle_text}</span>"

# Prepare annotations for the source text
annotations = []
source_text = texts.get('source')
if source_text:
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            text=source_text,
            showarrow=False,
            font=dict(family="Arial", size=12, color='grey')
        )
    )

# Update layout for a clean, professional look
fig.update_layout(
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    font=dict(family="Arial"),
    xaxis=dict(
        type='category',
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 40],
        showgrid=True,
        gridcolor='#E5E5E5',
        tickfont=dict(size=12),
        title_standoff=15
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=annotations
)

# Determine output filename from the input JSON path
output_path = pathlib.Path(json_path)
output_filename = output_path.with_suffix('.png').name

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")