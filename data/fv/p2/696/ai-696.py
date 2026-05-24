import sys
import json
import os
import math
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

chart_data = chart_spec['chart_data'][0]
texts = chart_spec['texts']
colors = chart_spec['colors']

num_bins = len(chart_data['x'])
log_x = [math.log10(v) for v in chart_data['x']]
log_step = (log_x[-1] - log_x[0]) / (num_bins - 1)

widths = []
for x_center in chart_data['x']:
    log_center = math.log10(x_center)
    log_lower = log_center - log_step / 2.0
    log_upper = log_center + log_step / 2.0
    width = (10**log_upper) - (10**log_lower)
    widths.append(width)

fig.add_trace(go.Bar(
    x=chart_data['x'],
    y=chart_data['y'],
    width=widths,
    marker=dict(
        color=colors['fill_colors'],
        line=dict(
            color=colors['outline_color'],
            width=1
        )
    ),
    showlegend=False
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        type='log',
        tickvals=[0.01, 1, 100, 10000],
        ticktext=['0.01', '1', '100', '10000'],
        showgrid=False,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 1600],
        tickvals=[0, 200, 400, 600, 800, 1000, 1200, 1400],
        showgrid=False,
        linecolor='black',
        ticks='outside',
        zeroline=False
    ),
    bargap=0,
    margin=dict(l=60, r=20, t=30, b=80),
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_path = f"{base_filename}.png"

fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")