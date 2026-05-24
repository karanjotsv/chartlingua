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
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create the figure
fig = go.Figure()

# Add the bar trace, assuming a single series for this chart type
series = chart_data['series'][0]
fig.add_trace(go.Bar(
    x=chart_data['categories'],
    y=series['values'],
    name=series['name'],
    marker_color=colors[0],
    text=series['values'],
    textposition='outside',
    texttemplate='<b>%{text}</b>',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    cliponaxis=False
))

# Update layout
fig.update_layout(
    font=dict(
        family="Arial",
        size=12
    ),
    title_text=texts['title'],
    yaxis_title_text=texts['y_axis_title'],
    xaxis_title_text=texts['x_axis_title'],
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=50, b=100),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False,
        range=[0, 700],
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.18,
            align='right',
            xanchor='right',
            yanchor='top',
            font=dict(
                size=12,
                color='#555555'
            )
        )
    ]
)

# Determine the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")