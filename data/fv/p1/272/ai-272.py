import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- Script Execution ---

# Validate and get the input JSON file path from command-line arguments
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data components from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly traces
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
annotations_text = [item['annotation'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the main bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    width=0.6,
    hoverinfo='none' # Disable default hover labels
))

# Add annotations with background boxes above each bar
for i in range(len(chart_data)):
    fig.add_annotation(
        x=categories[i],
        y=values[i],
        text=annotations_text[i],
        showarrow=False,
        yshift=15,
        font=dict(
            family="Arial",
            size=11,
            color="black"
        ),
        bgcolor="#EAEAEA",
        borderpad=4
    )

# Configure the chart layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(size=16)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickfont=dict(size=10),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickangle=0
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 5.2],
        dtick=1,
        showgrid=True,
        gridcolor='#CCCCCC',
        showline=True,
        linewidth=1,
        linecolor='black',
        zeroline=False
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=80, b=160, l=40, r=40)
)

# Generate the output image file
base_filename = json_file_path.stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")