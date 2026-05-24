import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)] if colors else '#3876C4'
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers+text',
        name=series.get('name', ''),
        line=dict(color=color, width=2),
        marker=dict(color=color, size=6),
        text=[f'{val:.2f}%' for val in series['y']],
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color='#333333'
        ),
        hoverinfo='none'
    ))

# Combine title and subtitle if they exist
title_text = texts.get('title')
if title_text and texts.get('subtitle'):
    title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"
elif title_text:
    title_text = f"<b>{title_text}</b>"

# Combine source and note for the annotation
source_text_parts = []
if texts.get('source'):
    source_text_parts.append(texts['source'])
if texts.get('note'):
    source_text_parts.append(texts['note'])
source_text = "<br>".join(source_text_parts)

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=chart_data[0]['x'],
        ticktext=[str(year) for year in chart_data[0]['x']],
        showgrid=False,
        showline=True,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[5, 13.5],
        ticksuffix='%',
        gridcolor='#E5E5E5'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, b=100, t=50),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            x=1,
            y=-0.25,
            xref='paper',
            yref='paper',
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12, color='#555555')
        )
    ]
)

# Derive output filename from the input JSON path
output_filename_base = pathlib.Path(json_path).stem
output_png_path = f"{output_filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_png_path, scale=2)

print(f"Chart generated and saved to {output_png_path}")