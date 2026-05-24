import sys
import json
import plotly.graph_objects as go
import pathlib

# Load data from JSON file provided as a command-line argument
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Create a new figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=[val / 100 for val in series['y']],  # Convert percentages to decimals for plotting
        marker_color=colors[i]
    ))

# Combine title and subtitle
title_text = texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the layout of the figure
fig.update_layout(
    barmode='group',
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 0.35],
        tickformat='.0%',
        showgrid=True,
        gridcolor='#E0E0E0'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(t=80, b=120, l=60, r=40)
)

# Derive output filename from the input JSON filename
output_filename = pathlib.Path(json_path).stem + '.png'

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")