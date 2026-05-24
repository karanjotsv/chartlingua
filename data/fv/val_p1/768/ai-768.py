import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and settings from the loaded JSON
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])
shapes = chart_data.get('shapes', [])

# Create figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(data_series):
    color = colors[i] if i < len(colors) else '#000000'
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines+markers',
        line=dict(color=color, width=1.5),
        marker=dict(symbol='square', size=4, color=color),
        name='', # No name for legend entry
        hoverinfo='none'
    ))

# Build combined title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Configure layout
fig.update_layout(
    title_text=title_text if title_text else None,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=60, b=60),
    xaxis=dict(
        range=[-60, 60],
        tickmode='linear',
        tick0=-60,
        dtick=20,
        ticksuffix=' V',
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor='lightgrey',
        griddash='dot',
        zeroline=False
    ),
    yaxis=dict(
        range=[0.970, 1.001],
        tickmode='linear',
        tick0=0.970,
        dtick=0.005,
        tickformat='.3f',
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor='lightgrey',
        griddash='dot',
        zeroline=False
    ),
    annotations=texts.get('annotations', []),
    shapes=shapes
)


# Generate output filename from input JSON path
if '.' in json_path:
    base_filename = json_path.rsplit('.', 1)[0]
else:
    base_filename = json_path

output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")