import sys
import json
import pathlib
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
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

# Add line trace
if len(chart_data) > 0:
    line_data = chart_data[0]
    fig.add_trace(go.Scatter(
        x=line_data['x'],
        y=line_data['y'],
        mode='lines',
        line=dict(color=colors[0], width=1.5),
        showlegend=False
    ))

# Add marker trace
if len(chart_data) > 1:
    marker_data = chart_data[1]
    fig.add_trace(go.Scatter(
        x=marker_data['x'],
        y=marker_data['y'],
        mode='markers',
        marker=dict(
            color='white',
            size=8,
            line=dict(
                color=colors[0],
                width=1.5
            )
        ),
        showlegend=False
    ))

fig.update_layout(
    title=dict(
        text=texts.get('title', ''),
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(
            family="Arial",
            size=18,
            color='black'
        )
    ),
    xaxis=dict(
        title=dict(
            text=texts.get('x_axis_title', ''),
            font=dict(family="Arial", size=14, color='black'),
            standoff=15
        ),
        tickfont=dict(family="Arial", size=12, color='black'),
        range=[0, 10.2],
        tickvals=[0, 2, 4, 6, 8, 10],
        showline=True,
        linewidth=1.2,
        linecolor='black',
        mirror=True,
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title=dict(
            text=texts.get('y_axis_title', ''),
            font=dict(family="Arial", size=14, color='black'),
            standoff=20
        ),
        tickfont=dict(family="Arial", size=12, color='black'),
        range=[-3.5, 2.5],
        tickvals=[-3, -2, -1, 0, 1, 2],
        showline=True,
        linewidth=1.2,
        linecolor='black',
        mirror=True,
        showgrid=False,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    width=600,
    height=600,
    margin=dict(l=90, r=40, t=80, b=80)
)

base_path = pathlib.Path(json_path)
output_filename = base_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")