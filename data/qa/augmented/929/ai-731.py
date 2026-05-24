import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: Failed to decode JSON.")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

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
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False  # Prevents text on top of bars from being clipped
))

# Update layout
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='lightgray'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 125],
        tickmode='linear',
        dtick=25,
        gridcolor='lightgray',
        zeroline=False
    ),
    margin=dict(l=90, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.15, # Positioned below the x-axis
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color="#7f7f7f")
        )
    ]
)

# Set title if it exists
if texts.get('title'):
    fig.update_layout(title_text=texts.get('title'), title_x=0.5)

# Generate output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")