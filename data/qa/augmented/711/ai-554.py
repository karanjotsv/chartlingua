import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
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

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the line trace
fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=8),
    name=''
))

# Update layout for a professional look
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    title=texts.get('title'),
    yaxis_title=texts.get('y_axis_title'),
    margin=dict(l=120, r=40, t=50, b=100),
    xaxis=dict(
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        showgrid=False,
        zeroline=False,
        linecolor='lightgray'
    ),
    yaxis=dict(
        range=[15000, 45000],
        tickmode='array',
        tickvals=[15000, 20000, 25000, 30000, 35000, 40000, 45000],
        ticktext=['15 000', '20 000', '25 000', '30 000', '35 000', '40 000', '45 000'],
        gridcolor='#EAEAEA',
        zeroline=False,
        linecolor='lightgray'
    )
)

# Add source annotation
fig.add_annotation(
    x=1,
    y=-0.22,
    xref="paper",
    yref="paper",
    text=texts.get('source'),
    showarrow=False,
    xanchor="right",
    yanchor="bottom",
    align="right",
    font=dict(size=12, color="#888888")
)

# Determine output filename and save the image
base_name = pathlib.Path(json_path).stem
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")