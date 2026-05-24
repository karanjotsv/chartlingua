import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    texttemplate='%{value}%',
    textfont=dict(color='white', size=16),
    hoverinfo='label+percent',
    insidetextorientation='horizontal',
    sort=False,
    direction='clockwise'
))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sup>{texts.get('subtitle')}</sup>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=24)
    ),
    font=dict(family="Arial"),
    paper_bgcolor='#E9E9E9',
    plot_bgcolor='#E9E9E9',
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.55,
        traceorder='normal',
        font=dict(size=12)
    ),
    margin=dict(l=40, r=40, t=90, b=40)
)

output_path = f"{json_file_path.stem}.png"
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")