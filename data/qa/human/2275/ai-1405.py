import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Read and load the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from the loaded JSON
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
categories = [item['category'] for item in data]
num_series = len(texts['legend_titles'])
y_values_by_series = [[] for _ in range(num_series)]
for item in data:
    for i in range(num_series):
        y_values_by_series[i].append(item['values'][i] if i < len(item['values']) else 0)

# Create the figure object
fig = go.Figure()

# Add a bar trace for each data series
for i in range(num_series):
    fig.add_trace(go.Bar(
        name=texts['legend_titles'][i],
        x=categories,
        y=y_values_by_series[i],
        marker_color=colors[i],
        text=[f'{val}%' if val > 0 else '' for val in y_values_by_series[i]],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', weight='bold', family='Arial')
    ))

# Update the layout of the chart
fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=60, r=30, t=50, b=180),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 21],
        tickvals=[0, 5, 10, 15, 20],
        ticktext=[f'{val}%' for val in [0, 5, 10, 15, 20]],
        gridcolor='#e0e0e0'
    ),
    xaxis=dict(
        tickangle=-45,
        title=texts['x_axis_title']
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.5,
        xanchor='center',
        x=0.5
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.6,
            xanchor='right', yanchor='bottom',
            text=texts['source'],
            showarrow=False,
            font=dict(size=12)
        )
    ]
)

# Define the output image filename based on the input JSON filename
output_filename = json_file_path.with_suffix('.png').name

# Write the figure to a PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")