import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False  # Allow text to be drawn outside the plot area
))

# Combine source and note for the annotation
source_text = ""
if texts.get("source"):
    source_text += texts["source"]
if texts.get("note"):
    # Adding spaces for visual separation, as in the original
    source_text += "      " + texts["note"]

# Update layout
fig.update_layout(
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e5e5e5',
        zeroline=False,
        range=[0, 18],
        dtick=2.5
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    margin=dict(l=80, r=40, t=40, b=100),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            x=1,
            y=-0.25,
            xref="paper",
            yref="paper",
            xanchor='right',
            yanchor='top',
            align='right'
        )
    ]
)

# Update traces for text styling
fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)

# Generate output filename from JSON path
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")