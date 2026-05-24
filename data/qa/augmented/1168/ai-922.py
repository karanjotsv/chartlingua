import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for Plotly
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    text=y_values,
    textposition='auto',
    hoverinfo='none'
))

# Update layout to match the original image
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showgrid=False,
        showline=False,
        tickangle=-45
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 700],
        gridcolor='#e9e9e9',
        zeroline=False
    ),
    margin=dict(l=60, r=40, t=40, b=100)
)

# Add source annotation
if texts.get("source"):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=-0.18, 
        xanchor='right',
        yanchor='top'
    )

# Determine the output filename from the input JSON path
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")