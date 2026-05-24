import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script.py> <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Scatter(
        x=chart_data['categories'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=colors[i], width=1.5)
    ))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='#F5F5F5',
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    legend_title_text=texts.get('legend_title'),
    margin=dict(l=80, r=60, t=40, b=60),
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99
    )
)

fig.update_xaxes(
    showline=False,
    showgrid=True,
    gridwidth=1,
    gridcolor='#E5E5E5'
)

fig.update_yaxes(
    range=[0, 480000],
    dtick=20000,
    showline=False,
    showgrid=True,
    gridwidth=1,
    gridcolor='#E5E5E5'
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")