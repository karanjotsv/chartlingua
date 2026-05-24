import sys
import json
import plotly.graph_objects as go
import pathlib

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the sole command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_info.get("chart_data", [])
categories = chart_info.get("categories", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
y_axis_title = texts.get("y_axis_title")
source_text = texts.get("source")

# --- 2. Create the Plotly Figure ---
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get("values", []),
        name=series.get("name", ""),
        marker_color=colors[i % len(colors)],
        text=series.get("values", []),
        textposition='outside',
        texttemplate='%{text}',
        textfont=dict(family="Arial", color='black'),
        cliponaxis=False
    ))

# --- 3. Configure Layout and Styling ---
# Build title string
title_text = texts.get("title", "")
subtitle_text = texts.get("subtitle")
if subtitle_text:
    title_text = f"<b>{title_text}</b><br><sub>{subtitle_text}</sub>"

# Build annotations for source/note
annotations = []
if source_text:
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.3,  # Positioned at the bottom-right
            xanchor='right', yanchor='bottom',
            text=source_text,
            showarrow=False,
            font=dict(family="Arial", size=12)
        )
    )

fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        tickfont=dict(size=12),
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=y_axis_title,
        range=[0, 25],
        tickfont=dict(size=12),
        gridcolor='#e0e0e0',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=70, r=40, b=150, t=50),
    annotations=annotations
)

# --- 4. Output the Image ---
# Derive the output filename from the input JSON path
p = pathlib.Path(json_path)
output_path = p.with_suffix('.png')

# Save the figure as a high-resolution PNG file
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")