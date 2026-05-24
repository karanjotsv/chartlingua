import sys
import json
import plotly.graph_objects as go
import os

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load the data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and texts from the loaded JSON
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
categories = data['categories']
series = data['series']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each series
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s['data'],
        name=s['name'],
        marker_color=colors[i],
        text=[f'{val}%' for val in s['data']],
        textposition='outside',
        cliponaxis=False
    ))

# Combine title and subtitle
title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

# Update layout for a professional look
fig.update_layout(
    barmode='group',
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickfont=dict(size=12),
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 85],
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.15,
        xanchor='center',
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=60, b=150),
    font=dict(family="Arial", size=12, color="black"),
    annotations=[]
)

# Add source annotations
if texts.get("source_left"):
    fig.add_annotation(
        text=texts["source_left"],
        xref="paper", yref="paper",
        x=0, y=-0.3,
        showarrow=False,
        align="left",
        xanchor="left",
        font=dict(size=12, color="#0073e5")
    )
if texts.get("source_right"):
    fig.add_annotation(
        text=texts["source_right"],
        xref="paper", yref="paper",
        x=1, y=-0.3,
        showarrow=False,
        align="right",
        xanchor="right"
    )

# Update text font for the bar labels
fig.update_traces(textfont_size=12, textfont_family="Arial", textfont_weight="bold")

# Generate the output image file path from the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")