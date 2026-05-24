import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

texts = chart_info['texts']
colors = chart_info['colors']
data_series = chart_info['chart_data'][0]

fig.add_trace(go.Scatter(
    x=data_series['x'],
    y=data_series['y'],
    mode='lines+markers',
    line=dict(color=colors[0]),
    marker=dict(
        symbol='circle',
        color='white',
        line=dict(
            color='#FF0000',
            width=1.5
        ),
        size=7
    ),
    showlegend=False
))

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        font=dict(size=16)
    ),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgrey',
        griddash='dot',
        zeroline=False,
        ticks='outside'
    ),
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgrey',
        griddash='dot',
        zeroline=False,
        ticks='outside',
        range=[0, 0.20]
    ),
    margin=dict(l=80, r=40, t=80, b=80),
    showlegend=False
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")