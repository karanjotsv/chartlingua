import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit("Usage: python script.py <json_file_path>")

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

data_config = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

for i, series in enumerate(data_config['series']):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=data_config['categories'],
        y=series['data'],
        marker_color=colors[i],
        text=series['data'],
        textposition='outside',
        texttemplate='%{y}',
        cliponaxis=False,
        textfont=dict(family="Arial", size=12, color='black')
    ))

caption_parts = [texts.get('source', ''), texts.get('note', '')]
caption_text = "<br>".join(filter(None, caption_parts))

fig.update_layout(
    font=dict(family="Arial"),
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=40, b=150),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 25.1],
        tick0=0,
        dtick=5,
        showgrid=True,
        gridcolor='lightgray',
        griddash='dot'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        traceorder="normal"
    )
)

if caption_text:
    fig.add_annotation(
        text=caption_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.35,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=10, color="#555555")
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_file = f"{base_filename}.png"

fig.write_image(output_image_file, scale=2)

print(f"Chart saved to {output_image_file}")