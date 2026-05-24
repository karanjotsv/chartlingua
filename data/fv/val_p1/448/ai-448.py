import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series_list = chart_data['series']

fig = go.Figure()

for i, series in enumerate(series_list):
    bar_texts = [f'{val:,}' for val in series['data']]
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors[i],
        text=bar_texts,
        textposition='outside',
        textfont=dict(family="Arial", size=11, color='black'),
        cliponaxis=False
    ))

title_text = texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=18, color='black')
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        tickformat=',.0f',
        range=[0, 9800000],
        tickfont=dict(family="Arial", size=12)
    ),
    legend=dict(
        x=0.1,
        y=0.7,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.5)',
        bordercolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12)
    ),
    plot_bgcolor='#EBF2F8',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=80, r=40, t=100, b=140),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.25,
            align='left',
            xanchor='left',
            yanchor='bottom',
            font=dict(family="Arial", size=11, color='black')
        )
    ]
)

output_path = json_path.with_suffix('.png')
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")