import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data and text from the loaded JSON
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
annotations = chart_data.get('annotations', [])

# Create a figure
fig = go.Figure()

# Add the main data trace
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        line=dict(color=colors[i % len(colors)], width=2.5),
        marker=dict(color=colors[i % len(colors)], size=6),
        name='',
        showlegend=False
    ))

# Add data point annotations
for ann in annotations:
    fig.add_annotation(
        x=ann['x'],
        y=ann['y'],
        text=ann['text'],
        showarrow=False,
        font=dict(family="Arial", size=11, color="#000000"),
        xanchor='center',
        yanchor='bottom',
        yshift=7
    )

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickvals=data_series[0]['x'][::2],
        ticktext=data_series[0]['x'][::2],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        linecolor='black',
        linewidth=1,
        ticks='outside',
        tickangle=0
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[-25, 125],
        tickvals=[-25, 0, 25, 50, 75, 100, 125],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black',
        linecolor='black',
        linewidth=1
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    height=600,
    width=900
)

# Add source annotation
fig.add_annotation(
    text=texts['source'],
    xref="paper",
    yref="paper",
    x=1.0,
    y=-0.2,
    showarrow=False,
    xanchor="right",
    yanchor="top",
    font=dict(family="Arial", size=12)
)

# Define output filename and save the image
output_filename = Path(json_path).stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")