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
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for the pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    hole=0,
    sort=False,
    direction='clockwise',
    rotation=90,
    textinfo='none', # Hide percentage labels on slices
    hoverinfo='label+percent',
    domain={'x': [0.0, 0.7], 'y': [0.1, 0.9]} # Confine pie to left part of the figure
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    legend=dict(
        x=0.75,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        traceorder='normal'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=40, r=40, t=80, b=40),
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='white',
    showlegend=True
)

# Determine the output filename
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)