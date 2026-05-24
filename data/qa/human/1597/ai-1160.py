import sys
import json
import plotly.graph_objects as go
import os

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data from the loaded JSON
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
x_values = chart_data['x']
series_data = chart_data['series']

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(series_data):
    color = colors[i % len(colors)]
    fig.add_trace(go.Scatter(
        x=x_values,
        y=series['y'],
        mode='lines+markers',
        name=series['name'],
        line=dict(color=color, width=2),
        marker=dict(color=color, size=5),
        hoverinfo='none'
    ))

# Add annotations for series labels to the right of the lines
annotations = []
for i, series in enumerate(series_data):
    color = colors[i % len(colors)]
    annotations.append(dict(
        xref='x',
        yref='y',
        x=x_values[-1],
        y=series['y'][-1],
        xanchor='left',
        yanchor='middle',
        text=series['name'],
        font=dict(family='Arial', size=12, color=color),
        showarrow=False,
        xshift=8
    ))

# Combine title and subtitle
title_text = f"<span style='font-size: 24px;'><b>{texts['title']}</b></span><br><span style='font-size: 16px;'>{texts['subtitle']}</span>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.98,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        tickvals=x_values,
        tickformat='%Y',
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        griddash='dash',
        range=[0, 60],
        tickvals=[0, 10, 20, 30, 40, 50],
        zeroline=False,
        showline=False,
        showticklabels=True
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=50, r=220, t=100, b=80),
    annotations=annotations
)

# Add source and note annotations at the bottom
fig.add_annotation(
    showarrow=False,
    text=texts['source'],
    xref="paper",
    yref="paper",
    x=0,
    y=-0.15,
    xanchor='left',
    yanchor='top',
    font=dict(size=12)
)
fig.add_annotation(
    showarrow=False,
    text=texts['note'],
    xref="paper",
    yref="paper",
    x=1,
    y=-0.15,
    xanchor='right',
    yanchor='top',
    font=dict(size=12)
)

# Define output filename based on the input JSON file
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")