import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
output_filename_base = Path(json_path).stem

# Read and decode the JSON configuration file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for the Plotly trace
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace with data and styling from JSON
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#1f77b4',
    text=values,
    texttemplate='%{y:.2f}',
    textposition='outside',
    textfont=dict(family="Arial", size=12, color="black"),
    hoverinfo='none',
    cliponaxis=False  # Prevents text labels from being clipped
))

# Combine title and subtitle using HTML tags for rich text formatting
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

# Apply layout settings to match the original chart's appearance
fig.update_layout(
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_family="Arial",
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_standoff=10,
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, 6.2],
        tickvals=[0, 1, 2, 3, 4, 5, 6],
        tickfont=dict(size=12)
    ),
    margin=dict(l=90, r=40, t=50, b=120)
)

# Add annotations for footer text (source, notes, etc.)
annotations = []
if texts.get('source'):
    annotations.append(dict(
        text=texts.get('source'),
        align='right',
        showarrow=False,
        xref='paper', yref='paper',
        x=1.0, y=-0.28,
        xanchor='right', yanchor='top',
        font=dict(size=11, color='#666666')
    ))
if texts.get('footer_info'):
    annotations.append(dict(
        text=texts.get('footer_info'),
        align='left',
        showarrow=False,
        xref='paper', yref='paper',
        x=0, y=-0.28,
        xanchor='left', yanchor='top',
        font=dict(size=11, color='#0073C0')
    ))

fig.update_layout(annotations=annotations)

# Define the output image file path
output_image_path = f"{output_filename_base}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")