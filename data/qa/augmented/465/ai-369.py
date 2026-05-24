import sys
import json
import plotly.graph_objects as go
import pathlib

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines+markers+text',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)], width=2.5),
        marker=dict(color=colors[i % len(colors)], size=8),
        text=series.get('text'),
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        hoverinfo='none'
    ))

# Build combined title and source strings
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = ""
if texts.get("source"):
    source_text += texts['source']
if texts.get("note"):
    source_text += f"<br>{texts['note']}"

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=60, b=100),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickmode='linear',
        dtick=1,
        tickangle=0,
        ticks="outside"
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        zeroline=False,
        range=[34.25, 36],
        dtick=0.25,
        ticks="outside"
    ),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

# Derive the output filename from the input JSON path
output_path = pathlib.Path(json_path).with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")