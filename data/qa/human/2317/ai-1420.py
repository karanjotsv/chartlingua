import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Read the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Load the chart data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each series in the data, preserving order
for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        y=chart_data['categories'],
        x=series['data'],
        name=series['name'],
        orientation='h',
        marker_color=colors[i],
        text=[f"{val}%" for val in series['data']],
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False
    ))

# Construct title and subtitle string from texts
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Construct annotations for source/note
annotations = []
if texts.get("source"):
    annotations.append(
        dict(
            xref="paper",
            yref="paper",
            x=1,
            y=-0.2,
            xanchor="right",
            yanchor="top",
            text=texts["source"],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#666666")
        )
    )

# Update the layout of the figure for a professional look and feel
fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.5,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        ticksuffix='%',
        range=[0, 40]
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#f0f0f0',
        zeroline=False,
        categoryorder='array',
        categoryarray=chart_data['categories']
    ),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=100, r=50, t=50, b=100),
    annotations=annotations
)

# Define the output image file path based on the input JSON filename
output_image_path = json_file_path.with_suffix(".png")

# Save the figure as a PNG image
fig.write_image(str(output_image_path), scale=2)