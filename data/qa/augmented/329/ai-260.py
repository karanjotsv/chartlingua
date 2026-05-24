import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Load data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0] if colors else None,
    text=[f"{v}%" for v in values],
    textposition='outside',
    cliponaxis=False,
    insidetextanchor='start' # Not strictly needed but can help with alignment
))

# Update layout for a professional look, matching the source image
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=250, r=40, t=40, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        range=[0, 71], # Extend range slightly to fit text
        zeroline=False,
        ticksuffix='%'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # To display categories from top to bottom
        showgrid=False
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.12,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Determine the output filename from the input JSON path
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(str(output_filename), scale=2)

print(f"Chart saved to {output_filename}")