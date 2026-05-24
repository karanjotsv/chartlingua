import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['x']
series_data = chart_data['series']

fig = go.Figure()

for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=series['y'],
        textposition='inside',
        textfont=dict(family="Arial", size=12, color="white"),
        insidetextanchor='middle'
    ))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.28,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12, color='#666666')
        )
    )

fig.update_layout(
    barmode='stack',
    font=dict(family="Arial"),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 2500],
        gridcolor='#dddddd',
        zeroline=False
    ),
    xaxis=dict(
        type='category',
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.22,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(t=30, b=120, l=90, r=40),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")