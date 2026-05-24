import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data['x_values'],
    y=data['y_values'],
    mode='lines',
    line=dict(color=colors[0], width=4),
    showlegend=False
))

title_parts = [texts['title'], texts['subtitle']]
full_title = '<br>'.join(filter(None, title_parts))

fig.update_layout(
    title=dict(
        text=full_title,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(size=18)
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showline=True,
        linecolor='black',
        showgrid=False,
        tickmode='array',
        tickvals=data['x_values'],
        ticktext=[str(x) for x in data['x_values']]
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        showline=False,
        linecolor='black',
        gridcolor='#E0E0E0',
        range=[3, 4],
        tickvals=[3, 3.25, 3.5, 3.75, 4]
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=90, r=40, t=100, b=80),
    showlegend=False
)

base_filename = Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")