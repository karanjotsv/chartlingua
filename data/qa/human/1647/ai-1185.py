import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script.py> <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
base_filename = Path(json_path).stem
output_filename = f"{base_filename}.png"

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

fig = go.Figure()

annotations = []

for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        name=series['name'],
        line=dict(color=color, width=2),
        marker=dict(color=color, size=6),
        showlegend=False
    ))

    annotations.append(dict(
        x=series['x'][-1],
        y=series['y'][-1],
        text=series['name'],
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=8,
        font=dict(family="Arial", size=12, color=color)
    ))

source_text = texts.get('source')
if source_text:
    annotations.append(dict(
        text=source_text,
        showarrow=False,
        xref="paper",
        yref="paper",
        x=0,
        y=-0.18,
        xanchor="left",
        yanchor="top",
        align="left",
        font=dict(family="Arial", size=10, color="#666666")
    ))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=24, color='#333333')
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=[1992, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010],
        showgrid=False,
        zeroline=False,
        range=[1991.5, 2012.5],
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        tickprefix='$',
        tickformat=',.0f',
        range=[6000, 27000],
        tickfont=dict(family="Arial", size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=100, t=80, b=120),
    annotations=annotations,
    width=900,
    height=600,
    font=dict(family="Arial")
)

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")