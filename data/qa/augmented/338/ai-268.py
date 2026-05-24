import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

if not os.path.isfile(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    text=values,
    texttemplate='%{y:,.0f}'.replace(',', ' '),
    textposition='outside',
    cliponaxis=False,
    textfont=dict(size=12, family="Arial")
))

title_text = texts.get('title')
if texts.get('subtitle'):
    title_text = f"{title_text}<br><sub>{texts.get('subtitle')}</sub>" if title_text else f"<sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title_text=title_text,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=14),
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12),
        showgrid=True,
        gridcolor='#F0F0F0'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 500000],
        tickvals=[0, 100000, 200000, 300000, 400000, 500000],
        ticktext=[f'{v:,}'.replace(',', '&nbsp;') for v in [0, 100000, 200000, 300000, 400000, 500000]],
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=90, r=40, b=100, t=50),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.20,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

base_filename, _ = os.path.splitext(json_file_path)
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")