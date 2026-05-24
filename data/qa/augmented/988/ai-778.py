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

# Extract categories and values, and reverse them for correct Plotly ordering
categories = [item['category'] for item in chart_data][::-1]
values = [item['value'] for item in chart_data][::-1]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0], line=dict(width=0)),
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

# Build title and source text
title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>' if title_text else f'<sub>{texts["subtitle"]}</sub>'

fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        title_font=dict(size=12),
        range=[0, 115],
        tickmode='linear',
        dtick=10,
        showgrid=True,
        gridcolor='#F0F0F0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticks='outside',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=150, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=0,
            yanchor='top',
            xanchor='right',
            font=dict(size=10, color='#888888'),
            yshift=-25
        )
    ]
)

base_filename = os.path.splitext(json_path)[0]
output_filename = base_filename + '.png'

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")