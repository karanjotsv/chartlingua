import sys
import json
import os
import plotly.graph_objects as go

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load the chart configuration from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and configuration from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series specified in the JSON
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i % len(colors)],
        text=[f"<b>{val}%</b>" for val in series['y']],
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False
    ))

# Configure the chart layout
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 105],
        tickvals=[0, 20, 40, 60, 80, 100],
        ticktext=[f"{v}%" for v in [0, 20, 40, 60, 80, 100]],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.28,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(l=80, r=40, b=150, t=40)
)

# Add source annotation if it exists in the JSON
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.32,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=10)
    )

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file and print a confirmation message
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")