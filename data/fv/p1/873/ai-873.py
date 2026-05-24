import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly
labels = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    texttemplate='%{label} %{value}%',
    textposition='outside',
    sort=False,  # Preserve the original order from the JSON
    direction='clockwise',
    showlegend=False
))

# Combine title and subtitle
title_text = f"<b>{texts['title']}</b><br><span style='font-size: 18px;'>{texts['subtitle']}</span>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(size=30)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(t=120, b=80, l=80, r=80),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.05,
        xanchor='center',
        yanchor='top',
        showarrow=False,
        font=dict(size=14)
    )

# Define output filename and save the image
output_filename = json_file_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")