import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_json.get('chart_data', [])
texts = chart_json.get('texts', {})
colors = chart_json.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces by iterating through the chart_data
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines+markers',
        line=dict(color=colors[i], width=2),
        marker=dict(color=colors[i], size=5)
    ))

# Combine title and subtitle using HTML for styling
title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size:14px;color:#555555'>{texts.get('subtitle', '')}</span>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.97,
        xanchor='left',
        yanchor='top',
        font=dict(size=20)
    ),
    plot_bgcolor='#eef2f6',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='#333333'),
    showlegend=False,
    margin=dict(t=100, l=50, r=50, b=50),
    xaxis=dict(
        showgrid=False,
        tickmode='array',
        tickvals=[1990, 1995, 2000, 2005, 2010, 2015],
        zeroline=False,
        linecolor='#cccccc',
        ticks='outside'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='white',
        gridwidth=2,
        range=[25, 70],
        dtick=5,
        zeroline=False
    )
)

# Add source annotation
fig.add_annotation(
    text=texts.get('source'),
    xref="paper", yref="paper",
    x=0.99, y=0.98,
    showarrow=False,
    xanchor='right',
    yanchor='top',
    align='right',
    font=dict(size=11, color='#555555')
)

# Add data series annotations from JSON
for ann in texts.get('annotations', []):
    fig.add_annotation(
        x=ann.get('x'),
        y=ann.get('y'),
        text=ann.get('text'),
        showarrow=False,
        xanchor=ann.get('xanchor', 'center'),
        yanchor=ann.get('yanchor', 'middle'),
        xshift=ann.get('xshift', 0),
        yshift=ann.get('yshift', 0),
        font=dict(size=12, color='#333333'),
        bgcolor='white',
        bordercolor='#bbbbbb',
        borderwidth=0.5,
        opacity=0.9
    )

# Define output filename and save the image
output_filename = json_file_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2, width=1000, height=600)
print(f"Chart saved to {output_filename}")