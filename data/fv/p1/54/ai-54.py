import sys
import json
import os
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker=dict(color=colors),
    text=values,
    texttemplate='%{y}%',
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    ),
    hoverinfo='none',
    cliponaxis=False
))

# Update layout for a professional look and feel
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.95,
        font=dict(
            family="Arial",
            size=18
        )
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        titlefont=dict(family="Arial", size=14),
        range=[0, 105],
        tickmode='linear',
        tick0=0,
        dtick=10,
        ticksuffix='%',
        tickfont=dict(family="Arial", size=12),
        gridcolor='#D3D3D3',
        zeroline=False
    ),
    xaxis=dict(
        tickfont=dict(family="Arial", size=12)
    ),
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=40, t=100, b=120)
)

# Set position for the text on top of the bars
fig.update_traces(
    textfont_size=14,
    textangle=0,
    insidetextanchor='end'
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")