import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

text_labels = [str(int(v)) if isinstance(v, (int, float)) and v == int(v) else str(v) for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0],
    text=text_labels,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        range=[0, 8.5]
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        title=texts.get('y_axis_title')
    ),
    margin=dict(l=250, r=40, t=40, b=100),
    showlegend=False,
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=-0.01, y=-0.18,
            xanchor='left', yanchor='top',
            text=texts.get('source_left'),
            showarrow=False,
            font=dict(size=12, color='#0073e5')
        ),
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.18,
            xanchor='right', yanchor='top',
            text=texts.get('source_right'),
            showarrow=False,
            align='right',
            font=dict(size=12, color='#666666')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_directory = os.path.dirname(json_path)
output_filepath = os.path.join(output_directory, f"{base_filename}.png") if output_directory else f"{base_filename}.png"


fig.write_image(output_filepath, scale=2)

print(f"Chart saved to {output_filepath}")