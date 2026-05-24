import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(
    go.Bar(
        x=categories,
        y=values,
        marker_color=colors[0] if colors else '#2A7FDB',
        text=values,
        textposition='outside',
        textfont=dict(family="Arial", size=12),
        cliponaxis=False  # Prevents text labels from being clipped
    )
)

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=14),
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100) # Adjusted margins
)

# Update axes appearance to match the original
fig.update_yaxes(
    range=[0, 1200],
    dtick=200,
    gridcolor='#E5E5E5',
    gridwidth=1,
    zeroline=False
)

fig.update_xaxes(
    showgrid=False,
    tickangle=0
)

# Add source annotation
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper",
        yref="paper",
        x=0.99,
        y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(family="Arial", size=12, color="#666666")
    )

# Determine the output filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")