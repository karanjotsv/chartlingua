import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the provided file exists
if not pathlib.Path(json_path).is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read the chart data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)


# Extract data and text from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False
))

# Update layout
title_text = texts.get('title')
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br>{texts.get('subtitle')}" if title_text else texts.get('subtitle')

fig.update_layout(
    title_text=title_text,
    yaxis_title=texts.get('y_axis_label'),
    xaxis_title=texts.get('x_axis_label'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    bargap=0.3,
    margin=dict(l=80, r=40, t=60, b=120),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 70],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        tickfont=dict(size=12)
    )
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts.get('source'),
        xref="paper", yref="paper",
        x=1.0, y=-0.2,
        xanchor='right', yanchor='top',
        showarrow=False,
        font=dict(size=10, color="#888888")
    )


# Generate the output PNG filename from the input JSON filename
base_name = pathlib.Path(json_path).stem
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")