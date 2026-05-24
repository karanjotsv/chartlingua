import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts
data = chart_data['chart_data'][0]
texts = chart_data['texts']
colors = chart_data['colors']

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=data['x'],
    y=data['y'],
    name=data.get('name', ''),
    marker_color=colors[0],
    text=data['y'],
    textposition='outside',
    texttemplate='%{y}',
    textfont=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    cliponaxis=False # Allow text labels to go beyond the axis range
))

# Update layout for a professional look
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    title_text=texts['title'],
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        zeroline=True,
        zerolinecolor='#444444',
        zerolinewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        range=[0, 85],
        tickvals=[0, 10, 20, 30, 40, 50, 60, 70, 80],
        zeroline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            text=texts['source'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.18,
            xanchor='left',
            yanchor='top',
            font=dict(
                size=12,
                color='#888888'
            )
        )
    ]
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")