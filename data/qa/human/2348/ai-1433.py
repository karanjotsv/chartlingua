import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['data'],
        name=series['name'],
        marker_color=colors['series_colors'][i],
        text=[f"{val}%" for val in series['data']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            color=colors['text_colors'][i],
            size=14
        )
    ))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

fig.update_layout(
    barmode='stack',
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        tickfont=dict(size=12),
        linecolor='lightgray'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 100],
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray',
        griddash='solid',
        tickfont=dict(size=12),
        linecolor='lightgray'
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5,
        font=dict(size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.3,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")