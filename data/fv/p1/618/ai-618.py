import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Initialize the figure
fig = go.Figure()

# Add traces by iterating through the chart data
for i, series in enumerate(chart_config['chart_data']):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(
            color=chart_config['colors'][i],
            width=2.5
        ),
        hoverinfo='none'
    ))

# Update layout for styling and text
fig.update_layout(
    title=dict(
        text=chart_config['texts']['title'],
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis_title=chart_config['texts']['x_axis_title'],
    yaxis_title=chart_config['texts']['y_axis_title'],
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
    font=dict(
        family="Arial",
        color="#FFFFFF"
    ),
    xaxis=dict(
        range=[0, 1.0],
        tickmode='linear',
        tick0=0.0,
        dtick=0.1,
        gridcolor='#444444',
        linecolor='#FFFFFF',
        zeroline=False
    ),
    yaxis=dict(
        range=[0, 1.05],
        tickmode='linear',
        tick0=0.0,
        dtick=0.1,
        gridcolor='#444444',
        linecolor='#FFFFFF',
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0.15,
        traceorder="normal",
        itemsizing='constant'
    ),
    margin=dict(l=60, r=40, t=100, b=80),
    autosize=False,
    width=800,
    height=600
)

# Derive output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the image file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)