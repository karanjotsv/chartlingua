import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", ["#1f77b4"])

# Prepare data for Plotly; reverse order to match visual top-to-bottom
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
categories.reverse()
values.reverse()

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{x}',
    cliponaxis=False
))

# Combine title and subtitle if they exist
title_text = texts.get("title", "")
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout for a clean, professional look
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get("x_axis_title"),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, max(values) * 1.15],
        dtick=5
    ),
    yaxis=dict(
        title=texts.get("y_axis_title"),
        showgrid=False,
        showline=True,
        linecolor='black'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=120, r=40, t=50, b=80),
    showlegend=False
)

# Add source annotation
if texts.get("source"):
    fig.add_annotation(
        text=texts.get("source"),
        xref="paper", yref="paper",
        x=0.98, y=-0.15,
        showarrow=False,
        xanchor='right', yanchor='top',
        align='right',
        font=dict(size=10, color="#555555")
    )


# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"


# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")