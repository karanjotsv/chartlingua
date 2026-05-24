import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    cliponaxis=False,
    hoverinfo='none',
    textfont=dict(family='Arial', size=12, color='black')
))

fig.update_layout(
    font=dict(family="Arial", color="#555555"),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        range=[0, 7.5],
        ticks="outside",
        tickwidth=1,
        tickcolor='lightgrey',
        ticklen=5
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        zeroline=False,
        ticks="",
        title=dict(text=texts.get('y_axis_title') or '')
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=120, r=50, t=40, b=80),
    showlegend=False,
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.15,
            text=texts.get('source', ''),
            showarrow=False,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#808080')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")