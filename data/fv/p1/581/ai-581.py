import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
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

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    trace_color = colors[i % len(colors)] if colors else '#000000'
    
    marker_dict = None
    if series.get('mode') == 'markers':
        marker_dict = dict(
            symbol=series.get('marker_symbol', 'circle'),
            color=trace_color,
            size=6,
            line=dict(width=1.5)
        )

    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode=series.get('mode', 'lines'),
        line=dict(color=trace_color, width=2),
        marker=marker_dict
    ))

fig.update_layout(
    title_text=texts.get('title'),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.5)',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=80, r=40, t=80, b=80),
    xaxis=dict(
        title_font=dict(size=14),
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridwidth=1,
        gridcolor='#D3D3D3',
        griddash='dot',
        range=[0, 1],
        tickmode='linear',
        tick0=0,
        dtick=0.1,
        zeroline=False
    ),
    yaxis=dict(
        title_font=dict(size=14),
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridwidth=1,
        gridcolor='#D3D3D3',
        griddash='dot',
        range=[0, 5.1],
        tickmode='linear',
        tick0=0,
        dtick=0.5,
        zeroline=False
    )
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")