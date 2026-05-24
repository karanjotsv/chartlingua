import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

chart_data = chart_json['chart_data']
texts = chart_json['texts']
colors = chart_json['colors']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1.5)),
    sort=False,
    direction='clockwise',
    textinfo='label',
    textposition='outside',
    outsidetextfont=dict(color='#666666', size=12),
    hoverinfo='label+percent',
    automargin=True
))

fig.update_layout(
    title_text=f"<b>{texts['title']}</b>" if texts.get('title') else None,
    title_x=0.5,
    title_font=dict(size=22, family="Arial", color='black'),
    font=dict(family="Arial"),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=80, b=40, l=40, r=40)
)

output_filename = json_path.with_suffix(".png").name
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")