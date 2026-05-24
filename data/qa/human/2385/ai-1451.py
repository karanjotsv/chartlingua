import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get file paths
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

output_filename = json_path.stem + ".png"

# Load data from JSON
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
categories = chart_data['categories']
series_list = chart_data['series']

# Create figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors[i],
        text=series['data'],
        textposition='outside',
        texttemplate='%{text}',
        cliponaxis=False  # Prevents data labels from being clipped at the top
    ))

# Combine title and subtitle
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>" if title_text else f"<sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_label'),
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_label'),
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False,
        range=[0, 1050],
        dtick=200
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=50, b=150)
)

# Add source annotation
if texts.get("source"):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.3,
        xanchor='right',
        yanchor='bottom'
    )

# Update trace text styling
fig.update_traces(textfont=dict(size=12, family="Arial"))

# Save the figure
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")