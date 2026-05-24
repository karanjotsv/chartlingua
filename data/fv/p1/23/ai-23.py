import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Load data and configuration from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
labels = [item.get('label') for item in chart_data]
values = [item.get('value') for item in chart_data]
colors = chart_info.get('colors', [])
texts = chart_info.get('texts', {})

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    sort=False,
    direction='clockwise',
    rotation=90,  # Centers the first slice at the top
    textinfo='none' # Hides the default percentage labels on the slices
))

# Prepare annotations for source text
annotations = []
if texts.get('source_left'):
    annotations.append(dict(
        text=texts['source_left'],
        x=0,
        y=-0.1,
        xref='paper',
        yref='paper',
        showarrow=False,
        xanchor='left',
        yanchor='top',
        align='left'
    ))

if texts.get('source_right'):
    annotations.append(dict(
        text=texts['source_right'],
        x=0.6,
        y=-0.1,
        xref='paper',
        yref='paper',
        showarrow=False,
        xanchor='left',
        yanchor='top',
        align='left'
    ))

# Update the layout for a clean and accurate presentation
fig.update_layout(
    title_text=texts.get('title'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='white',
    legend=dict(
        x=1.02,
        y=0.9,
        xanchor='left',
        yanchor='top'
    ),
    margin=dict(l=40, r=40, t=80, b=250),
    annotations=annotations
)

# Generate the output image file
output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as '{output_filename}'")