import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

# Add the main step response trace
fig.add_trace(go.Scatter(
    x=data_series[0]['x'],
    y=data_series[0]['y'],
    mode='lines',
    line=dict(color=colors[0], width=1.5),
    name=data_series[0].get('name', '')
))

# Add the asymptote trace
fig.add_trace(go.Scatter(
    x=data_series[1]['x'],
    y=data_series[1]['y'],
    mode='lines',
    line=dict(color=colors[1], width=1, dash='dot'),
    name=data_series[1].get('name', '')
))

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center'
    ),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(family="Arial"),
    plot_bgcolor='white',
    width=560,
    height=420,
    xaxis=dict(
        range=[0, 8],
        tickmode='linear',
        tick0=0,
        dtick=1,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dot',
        zeroline=False
    ),
    yaxis=dict(
        range=[0, 2.5],
        tickmode='linear',
        tick0=0,
        dtick=0.5,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dot',
        zeroline=False
    ),
    showlegend=False,
    margin=dict(l=60, r=20, t=50, b=50)
)

output_filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{output_filename_base}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")