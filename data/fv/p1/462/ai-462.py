import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

labels = [d['category'] for d in data]
values = [d['value'] for d in data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    textinfo='value',
    textposition='outside',
    sort=False,
    hoverinfo='label+percent',
    textfont=dict(family="Arial", size=12, color='black')
))

if chart_data.get('legend_total'):
    total_info = chart_data['legend_total']
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        name=total_info['text'],
        marker=dict(symbol='square', size=12, color=total_info['color'])
    ))

title_text = texts['title']
if texts.get('subtitle'):
    title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=True,
    legend=dict(
        x=0.98,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(255,255,255,0.5)'
    ),
    margin=dict(l=50, r=250, t=80, b=50),
    width=800,
    height=500
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")