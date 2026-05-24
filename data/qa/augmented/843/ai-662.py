import sys
import json
import os
import plotly.graph_objects as go

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_path}'.")
    sys.exit(1)

# Extract data from the JSON object
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
x_values = chart_data['x']
y_values = chart_data['y']
annotations_data = chart_data.get('annotations', [])

# Initialize the figure
fig = go.Figure()

# Add alternating background rectangles for the banded effect
for i, x_val in enumerate(x_values):
    if i % 2 == 0:
        fig.add_shape(
            type="rect",
            xref="x",
            yref="paper",
            x0=i - 0.5,
            y0=0,
            x1=i + 0.5,
            y1=1,
            fillcolor="#F5F5F5",
            layer="below",
            line_width=0,
        )

# Add the main line trace
fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers',
    line=dict(color=colors[0], width=3),
    marker=dict(color=colors[0], size=7),
    showlegend=False
))

# Create a mapping of x to y values for easy annotation placement
y_map = {x: y for x, y in zip(x_values, y_values)}

# Add data point labels as annotations
for ann in annotations_data:
    if ann['x'] in y_map:
        fig.add_annotation(
            x=ann['x'],
            y=y_map[ann['x']],
            text=f"<b>{ann['text']}</b>",
            showarrow=False,
            font=dict(family="Arial", size=11, color="black"),
            yshift=15,
            xanchor='center'
        )

# Update the layout of the chart
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        tickangle=0,
        categoryorder='array',
        categoryarray=x_values,
        ticks="outside",
        tickcolor='lightgrey'
    ),
    yaxis=dict(
        title=dict(text=texts['y_axis_title'], standoff=10),
        range=[-1, 40],
        dtick=5,
        ticksuffix='%',
        gridcolor='#EAEAEA',
        showline=False,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='darkgrey'
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=12, color="grey")
        )
    ]
)

# Derive output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")