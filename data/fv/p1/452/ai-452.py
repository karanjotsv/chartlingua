import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# This script requires a single command-line argument: the path to the JSON file.
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])

# Ensure the provided JSON file exists.
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load all chart data and text from the specified JSON file.
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON.
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data structures for Plotly.
labels = [d.get('label', '') for d in chart_data]
values = [d.get('value', 0) for d in chart_data]

# Initialize the Plotly figure.
fig = go.Figure()

# Add the pie chart trace using the data from the JSON file.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    sort=False,  # Preserve the original data order.
    direction='clockwise',
    rotation=80,  # Adjust to match the visual starting point of the first slice.
    textinfo='none',
    hoverinfo='label+percent'
))

# Configure the chart layout.
fig.update_layout(
    showlegend=True,
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='white',
    margin=dict(l=20, r=20, t=20, b=170), # Increase bottom margin for source text.
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    )
)

# Add the source and note text as a single annotation at the bottom.
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=0,
        yanchor='top',
        xanchor='left',
        yshift=-25  # Position below the chart area.
    )

# Determine the output image filename from the input JSON filename.
output_filename = f"{json_path.stem}.png"

# Save the generated chart to a PNG file with high resolution.
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")