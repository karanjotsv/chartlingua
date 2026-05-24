import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

# Add the density curve
curve = data['density_curve']
fig.add_trace(go.Scatter(
    x=curve['x'],
    y=curve['y'],
    mode='lines',
    line=dict(color=colors['line'], width=2),
    fill='tozeroy',
    fillcolor=colors['fill'],
    hoverinfo='none'
))

# Add the vertical mean line
mean_x = data['mean_line_x']
fig.add_shape(
    type="line",
    x0=mean_x, y0=0,
    x1=mean_x, y1=0.55,
    line=dict(
        color=colors['mean_line'],
        width=2,
        dash="dash"
    )
)

# Update layout to match the original image
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        font=dict(size=16)
    ),
    xaxis_title=texts['x_axis_label'],
    yaxis_title=texts['y_axis_label'],
    font=dict(family="Arial", size=12),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    showlegend=False,
    xaxis=dict(
        range=[0, 4.5],
        tickvals=[0, 1, 2, 3, 4],
        gridcolor=colors['grid'],
        zeroline=False,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        range=[0, 0.55],
        tickvals=[0.0, 0.2, 0.4],
        gridcolor=colors['grid'],
        zeroline=False,
        linecolor='black',
        ticks='outside'
    ),
    margin=dict(l=60, r=20, t=60, b=60)
)

# Determine output filename and save the image
base_filename = os.path.splitext(json_path)[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")