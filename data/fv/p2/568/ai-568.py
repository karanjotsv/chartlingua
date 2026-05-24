import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08)

fig.add_trace(go.Scatter(
    x=data[0]['x_values'],
    y=data[0]['y_values'],
    mode='lines',
    line=dict(color=colors['line_color']),
    name=data[0]['name']
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=data[1]['x_values'],
    y=data[1]['y_values'],
    mode='lines',
    line=dict(color=colors['line_color']),
    name=data[1]['name']
), row=1, col=2)

fig.update_xaxes(
    title_text=texts['subplots'][0]['x_axis_title'],
    row=1, col=1,
    range=[1000, 12200],
    tickmode='linear',
    tick0=2000,
    dtick=2000,
    showline=True, linewidth=1, linecolor='black', mirror=True,
    gridcolor='white'
)
fig.update_yaxes(
    title_text=texts['subplots'][0]['y_axis_title'],
    row=1, col=1,
    range=[0, 5000],
    showline=True, linewidth=1, linecolor='black', mirror=True,
    gridcolor='white'
)

fig.update_xaxes(
    title_text=texts['subplots'][1]['x_axis_title'],
    row=1, col=2,
    range=[1000, 12200],
    tickmode='linear',
    tick0=2000,
    dtick=2000,
    showline=True, linewidth=1, linecolor='black', mirror=True,
    gridcolor='white'
)
fig.update_yaxes(
    title_text=texts['subplots'][1]['y_axis_title'],
    row=1, col=2,
    range=[0, 15],
    tickmode='linear',
    tick0=0,
    dtick=5,
    showline=True, linewidth=1, linecolor='black', mirror=True,
    gridcolor='white'
)

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts.get('main_title'),
    title_x=0.5,
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, b=120, t=80),
    height=450,
    width=1000
)

fig.add_annotation(
    text=f"<b>{texts['subplots'][0]['title']}</b>",
    xref="paper", yref="paper",
    x=0.23, y=-0.3,
    showarrow=False,
    font=dict(family="Arial", size=14, color="black")
)

fig.add_annotation(
    text=f"<b>{texts['subplots'][1]['title']}</b>",
    xref="paper", yref="paper",
    x=0.77, y=-0.3,
    showarrow=False,
    font=dict(family="Arial", size=14, color="black")
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")