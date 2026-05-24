import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not pathlib.Path(json_path).is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

# Extract data and texts from the JSON object
chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

# Create the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines+markers',
        line=dict(
            color=colors[i % len(colors)],
            dash=series.get('line_style', 'solid')
        ),
        marker=dict(
            symbol=series.get('marker_symbol'),
            color=colors[i % len(colors)],
            size=8,
            line=dict(width=1.5) # For open markers
        )
    ))

# Update the layout of the chart
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
    xaxis=dict(
        range=[7.5, 14.5],
        tickmode='array',
        tickvals=[8, 9, 10, 11, 12, 13, 14],
        showgrid=True,
        gridcolor='lightgray',
        linecolor='black',
        linewidth=1,
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        range=[0, 30],
        dtick=5,
        showgrid=True,
        gridcolor='lightgray',
        linecolor='black',
        linewidth=1,
        mirror=True,
        ticks='outside',
        zeroline=False
    ),
    legend=dict(
        x=0.95,
        y=0.65,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=80, r=40, t=80, b=80)
)

# Determine the output filename from the input JSON path
filename_base = pathlib.Path(json_path).stem
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")