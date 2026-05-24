import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name'),
        line=dict(
            color=colors[i],
            dash=series.get('line_style')
        ),
        hoverinfo='none'
    ))

# --- Layout and Styling ---
fig.update_layout(
    # Chart Title
    title=dict(
        text=texts.get('title'),
        font=dict(family="Arial", size=32, color='black'),
        y=0.95,
        x=0.07,
        xanchor='left',
        yanchor='top'
    ),
    # General Font
    font=dict(family="Arial", color="black"),
    # Plot Area
    plot_bgcolor='white',
    # Margins (to prevent clipping of titles and annotations)
    margin=dict(t=100, b=120, l=120, r=220),
    # Disable default legend
    showlegend=False,
    # Axis Titles
    xaxis_title=dict(
        text=texts.get('x_axis_title'),
        font=dict(size=24)
    ),
    yaxis_title=dict(
        text=texts.get('y_axis_title'),
        font=dict(size=24)
    )
)

# --- Axis Styling ---
fig.update_xaxes(
    showline=True,
    linewidth=2,
    linecolor='black',
    mirror=True,
    showgrid=False,
    showticklabels=False,
    ticks=''
)
fig.update_yaxes(
    showline=True,
    linewidth=2,
    linecolor='black',
    mirror=True,
    showgrid=False,
    showticklabels=False,
    ticks='',
    zeroline=True,
    zerolinewidth=1,
    zerolinecolor='black'
)

# --- Custom Legend using Annotations and Shapes ---
# These coordinates are relative to the plot's paper area
legend_x_text = 0.88
legend_x_shape_start = 0.85
legend_x_shape_end = 0.92
legend_x_shape_2_start = 0.95
legend_x_shape_2_end = 1.01

fig.add_annotation(
    text=texts.get('legend_text_1'), xref="paper", yref="paper",
    x=legend_x_text, y=0.8, showarrow=False,
    xanchor='center', font=dict(family="Arial", size=20)
)
fig.add_shape(
    type="line", xref="paper", yref="paper",
    x0=legend_x_shape_start, y0=0.75, x1=legend_x_shape_end, y1=0.75,
    line=dict(color=colors[0], width=2)
)
fig.add_annotation(
    text=texts.get('legend_text_2'), xref="paper", yref="paper",
    x=legend_x_text, y=0.68, showarrow=False,
    xanchor='center', font=dict(family="Arial", size=20)
)
fig.add_shape(
    type="line", xref="paper", yref="paper",
    x0=legend_x_shape_2_start, y0=0.68, x1=legend_x_shape_2_end, y1=0.68,
    line=dict(color=colors[1], width=2, dash='dash')
)

# --- Source/Note Annotations ---
fig.add_annotation(
    text=texts.get('source_left'),
    xref="paper", yref="paper",
    x=0, y=-0.22,
    showarrow=False,
    xanchor='left',
    yanchor='top',
    align='left',
    font=dict(family="Arial", size=10)
)
fig.add_annotation(
    text=texts.get('source_right'),
    xref="paper", yref="paper",
    x=1, y=-0.22,
    showarrow=False,
    xanchor='right',
    yanchor='top',
    align='right',
    font=dict(family="Arial", size=10)
)

# --- Export Image ---
# Derive the base filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")