import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the provided file path exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Derive the base filename for the output PNG from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Read and parse the JSON file
# The script's logic for data, text, and colors is driven entirely by this file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Initialize the Plotly figure
fig = go.Figure()

# Iterate through the data series in the JSON and add them as traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=series.get('y'),
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='#000000'),
        cliponaxis=False  # Prevents text labels from being clipped at the top
    ))

# Configure the layout of the chart
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=80, r=40, t=50, b=100),  # Adjust margins to prevent element clipping
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 30],  # Set a fixed range to match the original chart
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=True,  # Display the x-axis baseline
        zerolinecolor='black',
        zerolinewidth=1
    )
)

# Add the source text as an annotation at the bottom right of the chart area
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=1, y=-0.18,  # Positioned relative to the plot area
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(
            family="Arial",
            size=11,
            color="#808080"
        )
    )

# Write the figure to a PNG image file with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")