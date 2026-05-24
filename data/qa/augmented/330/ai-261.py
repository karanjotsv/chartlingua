import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data series from JSON
x_values = [d['category'] for d in chart_data]
y_values = [d['value'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=[f'{v:.2f}' for v in y_values],
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

# Update layout
fig.update_layout(
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    margin=dict(l=80, r=40, b=100, t=50),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        title_standoff=15,
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        range=[0, max(y_values) * 1.2]
    ),
    annotations=[
        dict(
            text=texts['note'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            xanchor='left',
            yanchor='bottom'
        ),
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='bottom'
        )
    ]
)

# Generate output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

# Write the image file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved as {output_image_path}")