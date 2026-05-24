import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Prepare data for Plotly
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

values = [d['value'] for d in data]

# Create the pie chart trace
pie_trace = go.Pie(
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    hole=0,
    sort=False,
    direction='clockwise',
    rotation=90,
    textinfo='none',
    hoverinfo='none'
)

# Define the layout
fig = go.Figure(data=[pie_trace])

# Create annotations for each slice
annotations = []
annotation_positions = [
    {'x': 0.88, 'y': 0.85, 'ax': -65, 'ay': -45, 'align': 'left'},  # 40%
    {'x': 0.82, 'y': 0.22, 'ax': -50, 'ay': 30, 'align': 'left'},   # 13%
    {'x': 0.22, 'y': 0.18, 'ax': 45, 'ay': 25, 'align': 'left'},    # 11%
    {'x': 0.15, 'y': 0.85, 'ax': 60, 'ay': -45, 'align': 'left'}    # 35%
]

for i, d in enumerate(data):
    pos = annotation_positions[i]
    annotations.append(
        go.layout.Annotation(
            x=pos['x'],
            y=pos['y'],
            xref="paper",
            yref="paper",
            text=d['label'],
            showarrow=True,
            arrowhead=0,
            ax=pos['ax'],
            ay=pos['ay'],
            font=dict(family="Arial", size=12, color="black"),
            align=pos['align'],
            arrowcolor="#555555",
            arrowwidth=1
        )
    )

# Add title and subtitle
title_text = f"<b>{texts['title']}</b><br><span style='font-size: 15px; color:#555555;'>{texts['subtitle']}</span>"

# Add source annotation
source_text = texts['source']
annotations.append(
    go.layout.Annotation(
        x=0,
        y=-0.1,
        xref="paper",
        yref="paper",
        text=source_text,
        showarrow=False,
        xanchor='left',
        yanchor='top',
        align='left',
        font=dict(family="Arial", size=11, color="#555555")
    )
)

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.02,
        xanchor='left',
        y=0.95,
        yanchor='top',
        font=dict(family="Arial", size=22, color="black")
    ),
    showlegend=False,
    margin=dict(l=20, r=20, t=130, b=120),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=annotations,
    font=dict(family="Arial")
)

# Generate the output image file
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")