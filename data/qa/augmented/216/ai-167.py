import sys
import os
import json
import plotly.graph_objects as go

# Check if a file path is provided
if len(sys.argv) < 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
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

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data from the list of dictionaries
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
    marker_color=colors[0] if colors else '#3172c4',
    textfont=dict(family="Arial", size=14, color='black'),
    cliponaxis=False  # Prevent text labels from being clipped
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='lightgray',
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_standoff=20,
        range=[0, 85],
        tickvals=[0, 10, 20, 30, 40, 50, 60, 70, 80],
        gridcolor='#f0f0f0',
        zeroline=False,
        showline=False,
        tickfont=dict(size=14)
    ),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=12)
        )
    ]
)

# Determine the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")