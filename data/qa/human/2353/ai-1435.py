import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
num_series = len(texts['legend_labels'])
series_values = [[] for _ in range(num_series)]

for item in chart_data:
    for i in range(num_series):
        series_values[i].append(item['values'][i])

# Create the figure
fig = go.Figure()

# Add traces for each series
for i in range(num_series):
    fig.add_trace(go.Bar(
        x=categories,
        y=series_values[i],
        name=texts['legend_labels'][i],
        marker_color=colors[i],
        text=series_values[i],
        textposition='outside',
        texttemplate='%{text}',
        textfont=dict(family="Arial", size=12)
    ))

# Update layout
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=texts['title'] if texts.get('title') else '',
        font=dict(size=24)
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 70],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, b=120, t=50)
)

# Add source annotation if it exists
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.28,
        font=dict(family="Arial", size=10)
    )

# Determine output filename and save the image
base_filename, _ = os.path.splitext(json_path)
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")