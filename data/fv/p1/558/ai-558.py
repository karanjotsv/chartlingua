import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data components from the loaded JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Initialize a Plotly Figure
fig = go.Figure()

# Add the 'true' line trace
fig.add_trace(go.Scatter(
    x=chart_data[0]['x'],
    y=chart_data[0]['y'],
    name=chart_data[0]['name'],
    mode='lines',
    line=dict(color=colors[0], width=1.5)
))

# Add the 'approx. n=4' scatter trace with open square markers
fig.add_trace(go.Scatter(
    x=chart_data[1]['x'],
    y=chart_data[1]['y'],
    name=chart_data[1]['name'],
    mode='markers',
    marker=dict(
        symbol='square-open',
        color=colors[1],
        size=5,
        line=dict(width=1)
    )
))

# Configure the layout of the chart
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.95,
        xanchor='center'
    ),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    xaxis=dict(
        range=[-0.02, 1.02],
        showgrid=True,
        gridcolor='#d3d3d3',
        griddash='dot',
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        range=[-0.25, 5.25],
        showgrid=True,
        gridcolor='#d3d3d3',
        griddash='dot',
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        mirror=True,
        ticks='outside'
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.9)',
        bordercolor='black',
        borderwidth=0.5
    ),
    margin=dict(l=60, r=30, t=80, b=60)
)

# Determine the output filename from the input JSON path
output_filename = f"{json_path.stem}.png"

# Save the figure to a PNG file with a high resolution
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")