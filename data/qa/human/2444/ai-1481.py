import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series_data = chart_data['series']

fig = go.Figure()

for i, series in enumerate(series_data):
    bar_texts = [f"<b>{val:.0f}</b>" if val == int(val) else f"<b>{val:.1f}</b>" for val in series['data']]
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors[i],
        text=bar_texts,
        textposition='inside',
        textfont=dict(
            family="Arial",
            size=13,
            color="white"
        ),
        insidetextanchor='middle',
        hoverinfo='none'
    ))

fig.update_layout(
    barmode='stack',
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=50, b=120),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        title_standoff=15,
        gridcolor='lightgrey',
        griddash='dash',
        zeroline=False,
        range=[0, 100],
        tickvals=[0, 20, 40, 60, 80, 100],
        linecolor='black',
        ticks='outside',
        tickfont=dict(size=12)
    ),
    legend=dict(
        traceorder='normal',
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    )
)

if texts['source']:
    fig.add_annotation(
        showarrow=False,
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=1.0,
        y=-0.35,
        xanchor='right',
        yanchor='bottom',
        align="right",
        font=dict(family="Arial", size=10, color="#666666")
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)