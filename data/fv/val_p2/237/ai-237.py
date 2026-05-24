import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

fig = go.Figure()

marker_symbols = ['square', 'diamond', 'triangle-down']

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines+markers',
        line=dict(color=colors[i % len(colors)]),
        marker=dict(
            symbol=marker_symbols[i % len(marker_symbols)],
            color=colors[i % len(colors)],
            size=8
        )
    ))

fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False,
        tickmode='linear',
        dtick=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=True,
        range=[0, 250000000],
        tickprefix='$',
        tickformat=',.0f'
    ),
    legend=dict(
        x=0.98,
        y=0.8,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0)'
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    separators=".,",
    margin=dict(l=100, r=40, t=80, b=50)
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")