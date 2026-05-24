import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=2)
    ),
    textinfo='percent',
    texttemplate='%{value}%',
    textfont=dict(size=16, color='black'),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    showlegend=True
)])

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(size=20)
    ),
    legend=dict(
        x=0.8,
        y=0.7,
        xanchor='left',
        yanchor='top',
        traceorder='normal',
        font=dict(size=14)
    ),
    font=dict(
        family="Arial"
    ),
    margin=dict(t=100, b=40, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

output_filename_base = json_file_path.stem
output_path = f"{output_filename_base}.png"

fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")