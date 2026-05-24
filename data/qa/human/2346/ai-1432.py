import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = data['categories']
series_list = data['series']

fig = go.Figure()

for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors[i],
        texttemplate='<b>%{y}</b>',
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='#333333'),
        cliponaxis=False
    ))

fig.update_layout(
    barmode='group',
    yaxis_title=texts['yaxis_title'],
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=20, t=40, b=120),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    yaxis=dict(
        range=[0, 105],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        title_standoff=10
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    )
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.4,
        xanchor='right',
        yanchor='bottom',
        font=dict(family="Arial", size=10, color="grey")
    )

base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)