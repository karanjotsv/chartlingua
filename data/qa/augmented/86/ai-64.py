import sys
import json
import plotly.graph_objects as go
import pathlib

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Derive the output PNG filename from the input JSON filename
output_filename_base = pathlib.Path(json_path).stem
output_filename = f"{output_filename_base}.png"

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
x_values = [item['category'] for item in chart_data]
y_values = [item['value'] for item in chart_data]
data_labels_suffix = texts.get('data_labels_suffix', '')
data_labels = [f"{v}{data_labels_suffix}" for v in y_values]
bar_color = colors[0] if colors else '#1f77b4'

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=data_labels,
    textposition='outside',
    marker_color=bar_color,
    cliponaxis=False
))

# Configure the layout, axes, and annotations
fig.update_layout(
    title_text=texts.get('title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='#f5f5f5',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 60],
        dtick=10,
        ticksuffix=data_labels_suffix,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            text=texts.get('source_left', ''),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.22,
            xanchor='left',
            yanchor='top'
        ),
        dict(
            text=texts.get('source_right', ''),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.22,
            xanchor='right',
            yanchor='top'
        )
    ]
)

# Set the font size for the text on bars
fig.update_traces(textfont_size=12)

# Write the output image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")