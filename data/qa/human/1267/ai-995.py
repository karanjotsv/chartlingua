import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Get the file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Create the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        name=series['name'],
        line=dict(color=colors[i]),
        marker=dict(color=colors[i], size=6),
        showlegend=False
    ))

# Add annotation for the series name at the end of the line
last_x = data[0]['x'][-1]
last_y = data[0]['y'][-1]
fig.add_annotation(
    x=last_x,
    y=last_y,
    text=data[0]['name'],
    showarrow=False,
    xanchor='left',
    yanchor='middle',
    xshift=10,
    font=dict(family="Arial", size=12, color=colors[0])
)

# Combine title and subtitle using HTML tags for formatting
title_text = f"<b>{texts['title']}</b><br><span style='font-size:14px;'>{texts['subtitle']}</span>"

# Combine source and note for the footer annotation
source_text = f"{texts['source']}  {texts['note']}"

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=False,
        tickvals=[2010, 2011, 2012, 2013, 2014],
        tickmode='array',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='lightgrey',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        range=[0, 3000]
    ),
    plot_bgcolor='white',
    margin=dict(l=50, r=50, t=120, b=80),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=10, color='#7f7f7f')
        )
    ]
)

# Define output filename from the input JSON filename
output_filename = json_file_path.stem + '.png'

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")