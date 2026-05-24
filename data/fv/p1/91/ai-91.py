import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])

# Read data and configuration from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_path} is not a valid JSON file.")
    sys.exit(1)

# Extract data from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(color=colors[i % len(colors)])
    ))

# Define y-axis ticks based on the original chart
y_tick_vals = [524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864]

# Update the layout of the figure
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        x=0.98,
        y=0.05,
        xanchor='right',
        yanchor='bottom',
        bgcolor='rgba(255,255,255,0.5)'
    ),
    xaxis=dict(
        range=[0, 250],
        dtick=50,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='lightgrey'
    ),
    yaxis=dict(
        type='log',
        tickvals=y_tick_vals,
        ticktext=[str(val) for val in y_tick_vals],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='lightgrey'
    ),
    margin=dict(l=90, r=40, t=80, b=80)
)

# Determine the output image filename from the input JSON filename
output_filename = json_path.stem + '.png'

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")