import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0])
))

fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#dddddd',
        zeroline=False,
        range=[0, 60],
        tickmode='linear',
        tick0=0,
        dtick=10
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        autorange='reversed',
        showgrid=False
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=320, r=40, t=80, b=40)
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")