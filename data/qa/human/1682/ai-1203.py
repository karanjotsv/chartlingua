import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Derive the base filename for the output PNG from the JSON filename
output_filename_base = json_file_path.stem

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the loaded configuration
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Initialize the Plotly figure
fig = go.Figure()

# Add traces (lines) to the figure based on the chart data
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)] if colors else '#000000'
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines+markers',
        name=series.get('name', ''),
        line=dict(color=color, width=2),
        marker=dict(color=color, size=5)
    ))

# Construct the title string with HTML for styling
title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size: 14px; color: #555;'>{texts.get('subtitle', '')}</span>"

# Update layout, axes, and annotations
fig.update_layout(
    font_family="Arial",
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=20)
    ),
    xaxis=dict(
        tickvals=[1990, 1992, 1994, 1996, 1998, 2000, 2002, 2004],
        showgrid=False,
        zeroline=True,
        zerolinecolor='#cccccc',
        zerolinewidth=1
    ),
    yaxis=dict(
        range=[0, 6],
        tickvals=[0, 1, 2, 3, 4, 5],
        ticksuffix='%',
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot'
    ),
    showlegend=False,
    plot_bgcolor='white',
    margin=dict(l=50, r=50, t=120, b=80),
)

# Add annotations for the series label and source notes
annotations = []

# Series label annotation
if chart_data:
    last_series = chart_data[0]
    annotations.append(dict(
        x=last_series['x'][-1],
        y=last_series['y'][-1],
        text=last_series['name'],
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=8,
        font=dict(size=12, color=colors[0])
    ))

# Source note annotation
if texts.get('source_note'):
    annotations.append(dict(
        x=0,
        y=-0.15,
        xref='paper',
        yref='paper',
        text=texts['source_note'],
        showarrow=False,
        xanchor='left',
        yanchor='top',
        font=dict(size=12, color='#666')
    ))

# Watermark/credit annotation
if texts.get('w_mark'):
    annotations.append(dict(
        x=1,
        y=-0.15,
        xref='paper',
        yref='paper',
        text=texts['w_mark'],
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(size=12, color='#666')
    ))

fig.update_layout(annotations=annotations)

# Generate the output image file
output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")