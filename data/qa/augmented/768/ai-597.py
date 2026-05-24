import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    cliponaxis=False # Allows text to render outside the plot area
))

# Update layout for a clean, professional look
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        title_font=dict(size=14),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        range=[0, 25],
        tickvals=[0, 5, 10, 15, 20, 25]
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=80),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(size=12)
        )
    ]
)

# Ensure text on bars is not cut off
fig.update_traces(
    textfont_size=12,
    textangle=0
)

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")