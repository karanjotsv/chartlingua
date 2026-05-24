import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        name=series.get("name"),
        mode='lines',
        line=dict(
            color=color,
            dash=series.get("line_style", "solid")
        )
    ))

# Build title and subtitle string
title_text = texts.get("title", "")
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts.get("subtitle")}</sub>'

# Update layout
fig.update_layout(
    title_text=title_text,
    xaxis_title=texts.get("x_axis_title"),
    yaxis_title=texts.get("y_axis_title"),
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        range=[20, 75],
        tickmode='linear',
        dtick=5,
        gridcolor='lightgray'
    ),
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        range=[140, 200],
        tickmode='linear',
        dtick=10,
        gridcolor='lightgray',
        griddash='dash'
    ),
    legend=dict(
        x=0.25,
        y=0.45,
        xanchor='left',
        yanchor='top',
        bgcolor='white',
        borderwidth=0
    ),
    margin=dict(l=80, r=40, t=80, b=80)
)

# Derive output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")