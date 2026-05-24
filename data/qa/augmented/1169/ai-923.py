import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and decode the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace with data values as text labels
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=[f'{val:.1f}' for val in y_values],
    textposition='outside',
    marker_color=colors['bar_color'],
    cliponaxis=False,  # Allow text to be drawn outside the plot area
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Build combined title string from JSON data
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Build annotations for source text
annotations = []
if texts.get('source'):
    annotations.append(dict(
        text=texts['source'],
        xref='paper', yref='paper',
        x=0.98, y=-0.15,
        xanchor='right', yanchor='top',
        showarrow=False,
        font=dict(family="Arial", size=12, color='#666666')
    ))

# Update layout for a professional and accurate appearance
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 500],
        showgrid=True,
        gridcolor='#e5e5e5',
        showline=False,
        tickfont=dict(family="Arial", size=12)
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=50, b=120),
    annotations=annotations
)

# Determine the output filename from the input JSON path
output_filename_base = Path(json_path).stem
output_png_path = f"{output_filename_base}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_png_path, scale=2)

print(f"Chart successfully generated and saved to '{output_png_path}'")