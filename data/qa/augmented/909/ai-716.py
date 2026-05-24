import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Determine the base filename for the output PNG from the JSON path
output_filename_base = pathlib.Path(json_path).stem

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly by extracting categories and values
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    cliponaxis=False  # Prevents text from being clipped if it extends beyond axis range
))

# Configure the layout of the chart
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    # Set generous margins to prevent labels from being cut off
    margin=dict(l=250, r=50, t=50, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False,
        # Set a slightly larger range to accommodate the text on the longest bar
        range=[0, max(values) * 1.12]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        # This displays the categories in the same top-to-bottom order as the source image
        autorange="reversed"
    )
)

# Add source text as an annotation at the bottom-right of the chart area
source_text = texts.get('source', '')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0.98, y=-0.12,  # Position below the x-axis, to the right
        xanchor="right", yanchor="top",
        showarrow=False,
        font=dict(size=10, color="grey"),
        align="right"
    )

# Define the output image path and save the figure as a PNG
output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")