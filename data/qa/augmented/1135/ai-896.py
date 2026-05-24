import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

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
    texttemplate='%{x}',
    cliponaxis=False
))

title_text = texts.get('title')
subtitle_text = texts.get('subtitle')

full_title = ""
if title_text:
    full_title = title_text
if subtitle_text:
    full_title = f"{full_title}<br><sub>{subtitle_text}</sub>"

fig.update_layout(
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        range=[0, max(values) * 1.15]
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        autorange='reversed',
        showgrid=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=150, r=60, t=50, b=80),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='grey')
        )
    ]
)

base_name = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")