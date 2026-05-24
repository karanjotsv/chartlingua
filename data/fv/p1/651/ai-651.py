import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = Path(sys.argv[1])

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for plotting
labels = [item['label'] for item in chart_data['chart_data']]
values = [item['value'] for item in chart_data['chart_data']]
colors = chart_data['colors']
texts = chart_data['texts']

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,  # Preserve the original order from the JSON
    direction='clockwise'
))

# Update layout for styling, titles, and annotations
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = []
if texts.get('source'):
    source_text.append(texts['source'])
if texts.get('note'):
    source_text.append(texts['note'])
source_html = "<br>".join(source_text)

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="white"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=40, r=40, t=100, b=120),
    paper_bgcolor='black',
    plot_bgcolor='black',
    annotations=[
        dict(
            showarrow=False,
            text=source_html,
            x=1.0,
            y=-0.25,
            xref="paper",
            yref="paper",
            xanchor="right",
            yanchor="bottom",
            align="right"
        )
    ]
)

# Define output filename and save the image
output_filename = json_file_path.with_suffix(".png")
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")