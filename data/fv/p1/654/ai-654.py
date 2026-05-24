import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])

# Check if the provided JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load chart data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data and configuration from the JSON object
texts = chart_config['texts']
data_series = chart_config['data_series']
style_options = chart_config['style_options']

# Initialize a Plotly graph objects figure
fig = go.Figure()

# Add filled area traces with specified patterns, ensuring correct stacking order
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='none',
        fill='tozeroy' if i == 0 else 'tonexty',
        fillcolor=style_options['pattern_fill_color'],
        fillpattern=dict(
            shape=series['pattern_shape'],
            fgcolor=style_options['pattern_fg_color'],
            fillmode='replace'
        ),
        legendgroup=series['name'],
        showlegend=True,
        line=dict(width=0)
    ))

# Add dashed boundary lines on top of the filled areas
for series in data_series:
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        line=dict(
            color=series['line_color'],
            dash='dash',
            width=2
        ),
        legendgroup=series['name'],
        showlegend=False
    ))

# Add the fire icon as an annotation
fire_icon = style_options['fire_icon']
fig.add_annotation(
    x=fire_icon['x'],
    y=fire_icon['y'],
    text=fire_icon['text'],
    showarrow=False,
    font=dict(
        family="Arial",
        size=fire_icon['size'],
        color="#A52A2A"  # Brown-red color for the fire icon
    )
)

# Add the vertical axis line for the pre-fire state
fig.add_shape(
    type="line",
    x0=-15, y0=0,
    x1=-15, y1=85,
    line=dict(color="black", width=2)
)

# Configure the chart's layout, axes, title, and legend
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(size=18)
    ),
    xaxis=dict(
        title=dict(text=texts['xaxis_title'], standoff=15),
        range=[-20, 115],
        tickvals=[0, 20, 40, 60, 80, 100],
        showgrid=False,
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    ),
    yaxis=dict(
        range=[-5, 100],
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        title=None
    ),
    legend=dict(
        title=texts['legend_title'],
        x=0.6,
        y=0.98,
        yanchor='top',
        bgcolor='rgba(255,255,255,0.7)'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(l=40, r=40, t=100, b=60)
)

# Generate the output PNG filename from the input JSON filename
output_filename = json_path.with_suffix('.png')

# Save the figure to a PNG file with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")