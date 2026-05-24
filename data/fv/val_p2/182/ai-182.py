import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts from the JSON structure
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
chart_type = chart_info.get("chart_type")

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
bar_colors = [item['color'] for item in chart_data]
data_labels = [item.get('label') for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=bar_colors,
    text=data_labels,
    textposition='outside',
    texttemplate='%{text}',
    hoverinfo='none',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=80, b=100, l=60, r=40),
    yaxis=dict(
        range=[0, 70],
        showgrid=True,
        gridcolor='#D3D3D3',
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickangle=0
    )
)

# Style data labels
fig.update_traces(textfont_size=12)

# Define output path and save the image
output_path = json_file_path.with_suffix('.png')
fig.write_image(output_path, scale=2, width=800, height=600)

print(f"Chart saved to {output_path}")