import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
if not Path(json_path).is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
formatted_text = [f"{v:,}".replace(',', ' ') for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker_color=colors[0],
    text=formatted_text,
    textposition='outside',
    textfont=dict(color='black', size=12),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=60, t=30, b=80),
    xaxis=dict(
        title=texts.get('xaxis_title'),
        title_font=dict(color='dimgrey', size=12),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, 17000],
        tickvals=[0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000],
        tickfont=dict(color='dimgrey')
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        tickfont=dict(color='dimgrey')
    )
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        font=dict(color='dimgrey')
    )

base_filename = Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")