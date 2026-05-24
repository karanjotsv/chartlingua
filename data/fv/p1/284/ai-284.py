import sys
import json
import plotly.graph_objects as go
import os

# Check if the command-line argument for the JSON file is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from the loaded JSON
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly: separate categories and values
# The original image has the highest value at the top.
# Plotly's y-axis for horizontal bars starts from the bottom.
# To match the original visual, we need to reverse the order of the data.
categories = [item['category'] for item in data]
values = [item['value'] for item in data]
categories.reverse()
values.reverse()

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors[0]),
    showlegend=False
))

# Build the title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Build source and note string for annotations
source_note_parts = []
if texts.get('source'):
    source_note_parts.append(f"Source: {texts['source']}")
if texts.get('note'):
    source_note_parts.append(f"Note: {texts['note']}")
source_note_text = "<br>".join(source_note_parts)

# Update layout for a clean, accurate look
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(size=24)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False,
        showline=True,
        linecolor='grey',
        mirror=True,
        tickfont=dict(size=18)
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False,
        showline=True,
        linecolor='grey',
        mirror=True,
        tickfont=dict(size=18)
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='white',
    paper_bgcolor='#F4FBF4',
    margin=dict(l=150, r=40, t=100, b=80),
    annotations=[
        dict(
            showarrow=False,
            text=source_note_text,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.20,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ] if source_note_text else []
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")