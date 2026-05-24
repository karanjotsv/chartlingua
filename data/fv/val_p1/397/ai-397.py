import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

labels = [f"{item['category']} {item['value']}%" for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#808080', width=1)
    ),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,
    direction='clockwise',
    rotation=90
))

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center',
        font=dict(size=24, weight='bold')
    ),
    font=dict(
        family="Arial"
    ),
    showlegend=True,
    legend=dict(
        x=0.85,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        traceorder='normal'
    ),
    paper_bgcolor='rgba(255,255,255,1)',
    plot_bgcolor='rgba(255,255,255,1)',
    width=700,
    height=600,
    margin=dict(l=50, r=50, t=100, b=50)
)

base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")