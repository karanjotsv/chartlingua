import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data for plotting
data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

# Initialize figure
fig = go.Figure()

# Add a trace for each series in the data
for i, series in enumerate(data['series']):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=data['categories'],
        y=series['values'],
        marker_color=colors[i],
        text=series['values'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='black', size=12)
    ))

# Update layout for styling and titles
fig.update_layout(
    barmode='stack',
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.98,
        xanchor='center',
        yanchor='top',
        font=dict(size=16)
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showticklabels=False,
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='center',
        x=0.5
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=40, r=40, t=100, b=40)
)

# Determine output filename from input JSON path
output_filename = os.path.splitext(json_path)[0] + '.png'

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")