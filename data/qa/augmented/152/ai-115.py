import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the chart data and configuration from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
data_series = chart_info['chart_data'][0]
texts = chart_info['texts']
colors = chart_info['colors']
categories = data_series['categories']
values = data_series['values']

# Initialize a Plotly Figure
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    texttemplate='%{x}%',
    textposition='outside',
    textfont=dict(family="Arial", size=12)
))

# Configure the layout of the chart
fig.update_layout(
    font=dict(family="Arial", size=12, color='#333333'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=260, r=40, t=30, b=60),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#dddddd',
        griddash='dot',
        zeroline=False,
        ticksuffix='%',
        range=[0, 22.5]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange="reversed",
        showgrid=False
    ),
    showlegend=False,
    annotations=[]
)

# Add source annotation if present in the JSON
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=0.99,
        y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=10, color='#666666')
    )

# Determine the output filename from the input JSON filename
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Write the figure to a PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")