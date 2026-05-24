import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', {})

fig = go.Figure()

if chart_data:
    series = chart_data[0]
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines+markers',
        line=dict(color=colors.get('series_colors', ['#FF0000'])[0], width=2),
        marker=dict(
            symbol='cross',
            color=colors.get('series_colors', ['#FF0000'])[0],
            size=12,
            line=dict(width=2.5)
        )
    ))

x_axis_range = [0, 6.5]
y_axis_range = [0, 360]

fig.update_layout(
    font_family="Arial",
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor=colors.get('background_color', '#FFFFFF'),
    showlegend=False,
    margin=dict(l=60, r=20, t=20, b=50),
    xaxis=dict(
        range=x_axis_range,
        tickvals=[0, 1, 2, 3, 4, 5, 6],
        showline=True,
        linecolor=colors.get('axis_color', 'black'),
        linewidth=1,
        showgrid=True,
        gridcolor=colors.get('grid_color', '#A9A9A9'),
        gridwidth=1,
        zeroline=False,
        minor=dict(
            dtick=0.2,
            showgrid=True,
            gridcolor=colors.get('grid_color', '#A9A9A9'),
            gridwidth=1
        )
    ),
    yaxis=dict(
        range=y_axis_range,
        tickvals=[0, 100, 200, 300],
        showline=True,
        linecolor=colors.get('axis_color', 'black'),
        linewidth=1,
        showgrid=True,
        gridcolor=colors.get('grid_color', '#A9A9A9'),
        gridwidth=1,
        zeroline=False,
        minor=dict(
            dtick=20,
            showgrid=True,
            gridcolor=colors.get('grid_color', '#A9A9A9'),
            gridwidth=1
        )
    )
)

fig.add_trace(go.Scatter(
    x=[x_axis_range[1]], y=[0],
    mode='markers',
    marker=dict(
        symbol='arrow-wide',
        color=colors.get('axis_color', 'black'),
        size=10,
        angle=0
    ),
    showlegend=False,
    hoverinfo='none',
    cliponaxis=False
))

fig.add_trace(go.Scatter(
    x=[0], y=[y_axis_range[1]],
    mode='markers',
    marker=dict(
        symbol='arrow-wide',
        color=colors.get('axis_color', 'black'),
        size=10,
        angle=90
    ),
    showlegend=False,
    hoverinfo='none',
    cliponaxis=False
))

output_filename_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{output_filename_base}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")