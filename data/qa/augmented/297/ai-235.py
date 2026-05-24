import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = Path(json_path_str)
output_filename = f"{json_path.stem}.png"

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data for correct top-to-bottom display in Plotly
categories_reversed = categories[::-1]
values_reversed = values[::-1]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories_reversed,
    x=values_reversed,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values_reversed,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=40, t=40, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        title_font=dict(size=14),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        ticks='',
        range=[0, 55]
    ),
    yaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        ticks='outside',
        tickson='boundaries',
        categoryorder='array',
        categoryarray=categories_reversed
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            text=f"ⓘ {texts.get('note', '')}" if texts.get('note') else "",
            showarrow=False,
            font=dict(size=12, color="#0073e5")
        ),
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts.get('source', ''),
            showarrow=False,
            font=dict(size=12, color="#666666")
        )
    ]
)

fig.update_traces(textfont=dict(family="Arial", size=12, color='black'))

fig.write_image(output_filename, scale=2)