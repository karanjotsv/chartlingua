import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for the required command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Derive the output PNG filename from the JSON filename
output_path = json_path.with_suffix(".png")

# Load data and settings from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Add data series (traces) to the figure
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)] if colors else '#000000'
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=color, width=1.5),
        showlegend=False
    ))

# Update the layout of the figure
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridwidth=1,
        gridcolor='#BFBFBF',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        zeroline=False,
        tickvals=[-10, -8, -6, -5, -4, -2, 0, 2, 4],
        range=[-10.5, 4.5]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        type='log',
        showgrid=True,
        gridwidth=1,
        gridcolor='#D9D9D9',
        griddash='dot',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        zeroline=False,
        tickvals=[0.0005, 0.001, 0.01, 0.1],
        ticktext=['0.0005', '0.001', '0.010', '0.1'],
        range=[-3.3, -0.9] # log10(0.0005) to log10(0.12)
    ),
    font=dict(
        family="Arial",
        size=10
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=100, b=80),
    autosize=False,
    width=800,
    height=600
)

# Add annotations from the JSON data
if 'annotations' in texts and texts['annotations']:
    for ann in texts['annotations']:
        fig.add_annotation(
            text=ann.get('text'),
            x=ann.get('x'),
            y=ann.get('y'),
            xref=ann.get('xref', 'x'),
            yref=ann.get('yref', 'y'),
            showarrow=ann.get('showarrow', False),
            xanchor=ann.get('xanchor', 'left'),
            yanchor=ann.get('yanchor', 'middle'),
            font=ann.get('font', {})
        )

# Save the figure as a PNG image
try:
    fig.write_image(str(output_path), scale=2)
    print(f"Chart saved to {output_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)