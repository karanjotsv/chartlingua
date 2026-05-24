import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]
json_file_path = Path(json_path)

if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

chart_data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

fig = make_subplots(
    rows=2, cols=1,
    specs=[[{'type': 'domain'}], [{'type': 'domain'}]],
    vertical_spacing=0.15
)

series1 = chart_data['series'][0]
fig.add_trace(go.Pie(
    labels=chart_data['labels'],
    values=series1['values'],
    textinfo='percent',
    insidetextfont=dict(color='white', size=14, family='Arial'),
    marker=dict(colors=colors, line=dict(color='#A69B87', width=2)),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    showlegend=True,
    name=''
), row=1, col=1)

series2 = chart_data['series'][1]
fig.add_trace(go.Pie(
    labels=chart_data['labels'],
    values=series2['values'],
    textinfo='percent',
    insidetextfont=dict(color='white', size=14, family='Arial'),
    marker=dict(colors=colors, line=dict(color='#A69B87', width=2)),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    showlegend=False
), row=2, col=1)

fig.add_annotation(
    text=series1['name'],
    align='left',
    showarrow=False,
    xref='paper', yref='paper',
    x=0.05, y=0.9,
    font=dict(family='Arial', size=14, color='#000000')
)

fig.add_annotation(
    text=series2['name'],
    align='left',
    showarrow=False,
    xref='paper', yref='paper',
    x=0.05, y=0.38,
    font=dict(family='Arial', size=14, color='#000000')
)

fig.update_layout(
    title_text=f"<b>{texts['title']}</b>",
    title_font=dict(family='Arial', size=18, color='white'),
    title_x=0.05,
    title_y=0.96,
    font=dict(family='Arial'),
    plot_bgcolor='#A69B87',
    paper_bgcolor='#A69B87',
    legend=dict(
        title=dict(text=f"<b>{texts['legend_title']}</b>", font=dict(family='Arial', size=14, color='#000000')),
        x=0.05,
        y=0.18,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)',
        font=dict(family='Arial', size=12, color='#000000'),
        traceorder='normal'
    ),
    width=600,
    height=800,
    margin=dict(l=40, r=40, t=120, b=40),
    shapes=[
        dict(
            type="rect",
            xref="paper",
            yref="paper",
            x0=0,
            y0=0.90,
            x1=1,
            y1=1,
            fillcolor="#5A412B",
            line_width=0,
            layer="below"
        )
    ]
)

fig.update_traces(texttemplate='%{value}%')

output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")