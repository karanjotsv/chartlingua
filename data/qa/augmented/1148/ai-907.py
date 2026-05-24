import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data and configuration from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Create the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=[f"<b>{val}</b>" for val in series['y']],
        textposition='outside',
        cliponaxis=False
    ))

# Build combined title string
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    if title_text:
        title_text += "<br>"
    title_text += f"<span style='font-size: smaller;'>{texts['subtitle']}</span>"

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 500],
        dtick=100,
        showgrid=True,
        gridcolor='#dddddd',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False
    ),
    margin=dict(l=50, r=50, t=50, b=100),
    annotations=[]
)

# Add source and note annotations
annotations = []
if texts.get("note"):
    annotations.append(dict(
        xref="paper", yref="paper",
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        text=texts["note"],
        showarrow=False,
        font=dict(size=12, color="#0073e5")
    ))
if texts.get("source"):
    annotations.append(dict(
        xref="paper", yref="paper",
        x=1, y=-0.15,
        xanchor='right', yanchor='top',
        text=texts["source"],
        showarrow=False,
        font=dict(size=12)
    ))

fig.update_layout(annotations=annotations)


# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")