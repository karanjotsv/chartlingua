import sys
import json
import plotly.graph_objects as go
import os

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data from the JSON object
chart_data = chart_info.get("chart_data", {})
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
categories = chart_data.get("categories", [])
series_data = chart_data.get("series", [])

# Create a figure
fig = go.Figure()

# Define font colors for the text inside the bars to ensure readability
text_font_colors = ["white", "white", "black"]

# Add a trace for each data series
for i, series in enumerate(series_data):
    # Use bold HTML tags for text inside bars
    bar_texts = [f'<b>{val}%</b>' for val in series.get("data", [])]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get("data", []),
        name=series.get("name", ""),
        marker_color=colors[i % len(colors)],
        text=bar_texts,
        textposition='inside',
        insidetextanchor='middle',
        insidetextfont=dict(
            family="Arial",
            size=14,
            color=text_font_colors[i % len(text_font_colors)]
        ),
        hoverinfo='none'
    ))

# Build title and subtitle string
title_text = texts.get("title", "")
subtitle_text = texts.get("subtitle", "")
if title_text and subtitle_text:
    full_title = f"<b>{title_text}</b><br>{subtitle_text}"
elif title_text:
    full_title = f"<b>{title_text}</b>"
else:
    full_title = subtitle_text or ""


# Update the layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        tickfont=dict(size=12),
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 100],
        tickvals=[0, 25, 50, 75, 100],
        ticksuffix='%',
        gridcolor='#e0e0e0'
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=70, r=30, t=50, b=120),
    annotations=[
        dict(
            text=texts.get("source", ""),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.25,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename, _ = os.path.splitext(os.path.basename(json_path))
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")