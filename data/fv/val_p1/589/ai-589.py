import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_filepath = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_filepath):
    print(f"Error: File not found at {json_filepath}")
    sys.exit(1)

# Read data from JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_filepath}")
    sys.exit(1)


# Extract data and texts
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series.get('name'),
        x=series.get('x'),
        y=series.get('y'),
        marker_color=colors[i % len(colors)],
        marker_line=dict(color='black', width=1),
        error_y=dict(
            type='data',
            array=series.get('error_y'),
            visible=True,
            thickness=1.5,
            width=4,
            color='black'
        )
    ))

# Update layout
fig.update_layout(
    barmode='group',
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    legend_title_text=texts.get('legend_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='#E5E5E5',
    paper_bgcolor='white',
    yaxis=dict(
        gridcolor='white',
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticks='outside',
        range=[0, 0.7]
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        ticks='outside'
    ),
    margin=dict(l=80, r=40, t=40, b=80),
    legend=dict(
        traceorder='normal'
    )
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_filepath))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")