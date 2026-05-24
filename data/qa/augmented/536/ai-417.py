import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(family="Arial", size=12, color='black'),
    constraintext='none',
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=100),
    yaxis=dict(
        title=texts['y_title'],
        range=[0, 100],
        gridcolor='#e9e9e9',
        showline=False,
        zeroline=False
    ),
    xaxis=dict(
        title=texts['x_title'],
        showgrid=False,
        showline=True,
        linecolor='black',
        zeroline=False,
        ticks=''
    ),
    shapes=[
        dict(
            type="rect", xref="x", yref="paper",
            x0=0.5, y0=0, x1=1.5, y1=1,
            fillcolor="#f7f7f7", layer="below", line_width=0,
        ),
        dict(
            type="rect", xref="x", yref="paper",
            x0=2.5, y0=0, x1=3.5, y1=1,
            fillcolor="#f7f7f7", layer="below", line_width=0,
        )
    ],
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=12, color='#666666')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")