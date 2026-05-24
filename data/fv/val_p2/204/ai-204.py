import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_config.get("chart_data", [])
texts = chart_config.get("texts", {})
colors = chart_config.get("colors", [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker=dict(
        color=colors[0] if colors else '#9b9bff',
        line=dict(
            color='black',
            width=1.5
        )
    ),
    showlegend=False
))

# Add annotations inside the bars
for item in chart_data:
    fig.add_annotation(
        x=item['category'],
        y=item.get('annotation_y', item['value'] / 2),
        text=str(item['value']),
        showarrow=False,
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        align="center",
        bordercolor="#ff00ff",  # Magenta
        borderwidth=1.5,
        borderpad=4,
        bgcolor=colors[0] if colors else '#9b9bff',
        opacity=1.0
    )

# Combine title and subtitle
full_title = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    full_title += f"<br>{texts.get('subtitle')}"

# Update layout to match the original chart
fig.update_layout(
    title=dict(
        text=full_title,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=11)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 6000],
        tickvals=[0, 1000, 2000, 3000, 4000, 5000, 6000],
        gridcolor='#a9a9a9',
        zeroline=False
    ),
    font=dict(
        family="Arial",
        color="black"
    ),
    plot_bgcolor='#d3d3d3',
    paper_bgcolor='white',
    bargap=0.2,
    showlegend=False,
    margin=dict(l=60, r=40, t=100, b=150) # Increased bottom margin for long labels
)

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")