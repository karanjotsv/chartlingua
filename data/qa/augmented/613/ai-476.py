import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

chart_data = data['chart_data']
texts = data['texts']
colors = data['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    texttemplate='%{text:.2f}',
    textposition='outside',
    hoverinfo='none',
    cliponaxis=False
))

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        ticks='',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, 1800],
        tickvals=[0, 250, 500, 750, 1000, 1250, 1500, 1750],
        ticktext=['0', '250', '500', '750', '1 000', '1 250', '1 500', '1 750'],
        tickfont=dict(size=12)
    ),
    margin=dict(l=100, r=20, t=30, b=80),
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.99, y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=11)
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)