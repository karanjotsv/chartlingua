import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data_list = config['chart_data']
categories = [d['category'] for d in chart_data_list]
values = [d['value'] for d in chart_data_list]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=categories,
    y=values,
    mode='lines+markers+text',
    line=dict(color=config['colors'][0], width=2.5),
    marker=dict(color=config['colors'][0], size=7),
    text=[f'{v}%' for v in values],
    textposition='top center',
    textfont=dict(family='Arial', size=12, color='black'),
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=40, b=100),
    xaxis=dict(
        showgrid=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=dict(text=config['texts']['y_axis_title'], standoff=10),
        range=[3, 5.6],
        dtick=0.5,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dash',
        zeroline=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    showlegend=False,
    annotations=[
        dict(
            text=config['texts']['source_note'],
            showarrow=False,
            xref="paper", yref="paper",
            x=0.99, y=-0.22,
            xanchor='right', yanchor='bottom',
            font=dict(size=12, color='#6c757d')
        )
    ]
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)