import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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

# Prepare data for Plotly, reversing the order for correct horizontal bar chart display
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
categories.reverse()
values.reverse()

# Initialize the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0] if colors else '#008B27',
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,
    insidetextanchor='end',
    showlegend=False
))

# Build the title string from JSON data
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout for a professional appearance
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(size=18)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        range=[0, max(values) * 1.15],
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='black',
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        categoryorder='array',
        categoryarray=categories
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=160, r=40, t=80, b=80),
    bargap=0.4
)

# Update text font for the data labels on the bars
fig.update_traces(textfont=dict(family='Arial', size=14, color='black'))

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")