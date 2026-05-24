import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Read JSON file from command-line argument
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)] if colors else '#0000FF'
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=color, width=1.5)
    ))

# Build the title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=20)
    ),
    font=dict(
        family="Arial",
        color="white"
    ),
    plot_bgcolor='black',
    paper_bgcolor='black',
    showlegend=False,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    margin=dict(l=40, r=20, t=80, b=40)
)

# Update axes styling to match the original
fig.update_xaxes(
    showgrid=True,
    gridcolor='dimgray',
    griddash='dot',
    showline=True,
    linecolor='white',
    zeroline=False,
    tickformat='%Y',
    dtick='M12' # Tick every 12 months (1 year)
)

fig.update_yaxes(
    range=[0, 100],
    showgrid=True,
    gridcolor='white',
    griddash='solid',
    showline=True,
    linecolor='white',
    zeroline=False,
    dtick=10
)

# Generate and save the output image
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")