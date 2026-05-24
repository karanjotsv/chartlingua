import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script.py> <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data_series = chart_info['chart_data']
categories = chart_info['categories']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=categories,
        y=series['y'],
        marker_color=colors[i]
    ))

source_text_parts = []
if texts.get('source'):
    source_text_parts.append(texts['source'])
if texts.get('note'):
    source_text_parts.append(texts['note'])
source_note_html = "<br>".join(source_text_parts)

annotations = []
if source_note_html:
    annotations.append(
        dict(
            text=source_note_html,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.50,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10)
        )
    )

fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="#000000"),
    margin=dict(l=80, r=40, t=40, b=160),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 600],
        tickmode='linear',
        dtick=100,
        gridcolor='#e5e7eb',
        showline=True,
        linewidth=1,
        linecolor='black',
        zeroline=False
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    width=800,
    height=600,
    annotations=annotations
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_name}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")