import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data from the loaded JSON
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=values,
    texttemplate='%{y}',
    textposition='outside',
    textfont=dict(color='black', size=12)
))

# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note for annotations
annotations = []
if texts.get("source"):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1.0, y=-0.2,
            xanchor="right", yanchor="top",
            text=texts["source"],
            showarrow=False,
            font=dict(family="Arial", size=12, color="grey")
        )
    )

# Update layout
fig.update_layout(
    title_text=title_text,
    xaxis_title=texts.get("x_axis_title"),
    yaxis_title=texts.get("y_axis_title"),
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=40, b=100),
    yaxis=dict(
        range=[0, 1250],
        tickmode='linear',
        dtick=250,
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        showline=False,
        zeroline=False
    ),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    annotations=annotations
)

# Define output filename from the JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")