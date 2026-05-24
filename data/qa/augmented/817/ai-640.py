import sys
import json
import os
import plotly.graph_objects as go

# Ensure the script receives a command-line argument for the JSON file path
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load the chart data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Reverse data order to display the highest value at the top in a Plotly horizontal bar chart
data.reverse()

# Prepare data for plotting
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure object
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{x}',
    cliponaxis=False,
    hoverinfo='none'
))

# Configure the layout of the chart to match the original image
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=60, t=30, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        range=[0, max(values) * 1.15],
        tickmode='linear',
        tick0=0,
        dtick=2
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        showline=False,
        zeroline=False
    )
)

# Add source annotation if it exists in the JSON
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.15,
        xanchor='right',
        yanchor='top'
    )

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the figure to a PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")