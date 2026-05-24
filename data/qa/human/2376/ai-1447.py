import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit("Usage: python <script_name>.py <json_file_path>")

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [f"<b>{v}%</b>" for v in values]

fig = go.Figure(data=[
    go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=text_labels,
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False
    )
])

fig.update_layout(
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title=dict(
            text=texts.get('y_axis_title'),
            font=dict(family="Arial", size=14),
            standoff=10
        ),
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        range=[0, 105],
        tickvals=[0, 20, 40, 60, 80, 100],
        ticktext=[f"{i}%" for i in [0, 20, 40, 60, 80, 100]],
        tickfont=dict(family="Arial", size=12)
    ),
    plot_bgcolor='white',
    font=dict(family="Arial"),
    margin=dict(l=80, r=20, t=40, b=120),
    showlegend=False
)

if texts.get('source'):
    fig.add_annotation(
        x=1,
        y=-0.35,
        xref='paper',
        yref='paper',
        text=texts.get('source'),
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(family="Arial", size=12, color="#6c757d")
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)