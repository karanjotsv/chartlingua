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

# Extract data from the JSON object
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = chart_data.get('categories', [])
series_data = chart_data.get('series', [])

# Create the figure object
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(series_data):
    # Format text for inside the bars, using HTML for bolding
    bar_texts = [f"<b>{val:.2f}%</b>" if val > 5 else f"<b>{val:.2f}%</b>" for val in series['data']]
    
    # Custom text color logic: light text for dark backgrounds, dark for light
    text_font_color = 'white' if i < 2 else 'black'
    
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=bar_texts,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            color=text_font_color
        ),
        hoverinfo='skip'
    ))

# Combine title and subtitle if they exist
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if title_text and subtitle_text:
    title_text = f"<b>{title_text}</b><br><sub>{subtitle_text}</sub>"
elif title_text:
    title_text = f"<b>{title_text}</b>"

# Update layout
fig.update_layout(
    barmode='stack',
    title_text=title_text,
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5
    ),
    yaxis=dict(
        range=[0, 125],
        tickvals=[0, 25, 50, 75, 100, 125],
        ticktext=['0%', '25%', '50%', '75%', '100%', '125%'],
        gridcolor='#dddddd',
        zeroline=False
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=60, b=120)
)

# Add source annotation
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0.99, y=-0.25,
        showarrow=False,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=12, color="#7f7f7f")
    )

# Determine output filename from the input JSON path
output_filename = pathlib.Path(json_path).stem + '.png'

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")