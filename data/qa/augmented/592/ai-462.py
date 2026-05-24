import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = chart_data['categories']
series_values = chart_data['series'][0]['values']

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=series_values,
    marker_color=colors['bar_color'],
    text=series_values,
    textposition='outside',
    texttemplate='%{text:,}',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        color=colors['text_on_bar_color']
    )
))

annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            text=texts['note'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.18,
            xanchor='left',
            yanchor='top',
            font=dict(family="Arial", color=colors['axis_text_color'])
        )
    )

if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", color=colors['axis_text_color'])
        )
    )

fig.update_layout(
    font=dict(family="Arial", color=colors['axis_text_color']),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 3100],
        tickvals=[0, 500, 1000, 1500, 2000, 2500, 3000],
        showgrid=True,
        gridcolor=colors['grid_color'],
        zeroline=True,
        zerolinecolor=colors['grid_color'],
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=20, t=40, b=120),
    annotations=annotations,
    bargap=0.3
)

output_path = json_file_path.with_suffix('.png')
fig.write_image(str(output_path), scale=2)
print(f"Chart saved to {output_path}")