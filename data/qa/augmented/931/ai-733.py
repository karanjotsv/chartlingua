import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='outside',
    texttemplate='%{y}',
    cliponaxis=False
))

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='lightgray',
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 4],
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        showline=False
    ),
    margin=dict(l=90, r=30, t=40, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12)
        )
    ]
)

fig.update_traces(
    textfont=dict(family="Arial", size=12, color='black')
)

fig.write_image(output_image_path, scale=2)