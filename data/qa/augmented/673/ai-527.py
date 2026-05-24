import sys
import json
import plotly.graph_objects as go
import os

# Read the JSON file path from the first command-line argument
json_path = sys.argv[1]

# Load the chart configuration and data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, text, and color information
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize a new figure
fig = go.Figure()

# Iterate through the data series in the JSON and add them as bar traces
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker=dict(color=colors[i % len(colors)])
    ))

# Update the figure's layout with styles and text from the JSON
fig.update_layout(
    font=dict(family="Arial"),
    title=dict(text=texts.get('title')),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        griddash='dot',
        range=[0, 5000],
        tickvals=[0, 1000, 2000, 3000, 4000, 5000],
        ticktext=['0', '1 000', '2 000', '3 000', '4 000', '5 000'],
        zeroline=False,
        showline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=40, b=100),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='#666666')
        )
    ]
)

# Determine the output filename from the input JSON filename
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)