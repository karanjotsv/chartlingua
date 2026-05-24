import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
annotations_data = chart_info.get('annotations', [])

# Prepare data for Plotly
labels = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the pie chart trace
# Note: The 3D effect from the original image is a stylistic choice often found in
# software like Excel and is not a standard, data-first representation.
# We are creating a 2D pie chart which is the standard Plotly equivalent.
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=2)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,
    direction='clockwise',
    rotation=60,
    pull=[0.02] * len(values) # Slight pull to mimic separation
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout with titles, fonts, and other styling
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=100, b=100, l=100, r=100),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Add annotations from the JSON data
for ann in annotations_data:
    fig.add_annotation(
        text=ann.get('text'),
        x=ann.get('x'),
        y=ann.get('y'),
        ax=ann.get('ax'),
        ay=ann.get('ay'),
        xref="paper",
        yref="paper",
        showarrow=True,
        arrowhead=1,
        arrowcolor="#636363",
        font=dict(
            family="Arial",
            size=12
        ),
        align=ann.get('align'),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#636363",
        borderwidth=1
    )


# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")