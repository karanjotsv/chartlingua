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

fig = go.Figure()

annotations = []

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        line=dict(color=colors[i], width=2.5),
        marker=dict(
            color='white',
            size=8,
            symbol='circle',
            line=dict(color=colors[i], width=2)
        ),
        showlegend=False,
        hoverinfo='none'
    ))

    for x_val, y_val in zip(series['x'], series['y']):
        y_shift = 0
        if series['name'] == 'Democrat':
            y_shift = 12 if y_val in [59, 78] else -12
        else:
            y_shift = -12
        
        annotations.append(dict(
            x=x_val,
            y=y_val,
            yshift=y_shift,
            text=str(y_val),
            showarrow=False,
            font=dict(color=colors[i], size=12, family="Arial")
        ))

annotations.append(dict(
    x=2012.8, y=65, text='Democrat', showarrow=False,
    font=dict(color=colors[0], family="Arial", size=14)
))
annotations.append(dict(
    x=2012.8, y=32, text='Republican', showarrow=False,
    font=dict(color=colors[1], family="Arial", size=14)
))

annotations.append(dict(
    xref="paper", yref="paper",
    x=0, y=-0.18,
    xanchor="left", yanchor="top",
    text=texts['source'],
    showarrow=False,
    align="left",
    font=dict(family="Arial", size=12)
))

fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b><br><span style='font-size:16px;color:#555555;'>{texts['subtitle']}</span>",
        y=0.96,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        tickvals=[2009, 2011, 2013, 2015, 2017],
        tickformat='%Y',
        range=[2008.5, 2017.5],
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False
    ),
    yaxis=dict(
        range=[0, 85],
        tickvals=[0, 80],
        ticktext=['0', '80%'],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
    ),
    annotations=annotations,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=40, r=40, t=100, b=100),
    showlegend=False
)

output_path = json_path.with_suffix(".png")
fig.write_image(output_path, scale=2)