import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])

if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='#333333'
    )
))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            font=dict(family="Arial", size=11, color="#888888"),
            xanchor='right',
            yanchor='top'
        )
    )

fig.update_layout(
    font=dict(family="Arial", size=12, color="#333333"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(color="#333333")
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_font=dict(color="#888888", size=12),
        range=[0, 175],
        tickvals=[0, 25, 50, 75, 100, 125, 150, 175],
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dash',
        zeroline=False,
        showline=False,
        tickfont=dict(color="#333333")
    ),
    annotations=annotations
)

output_filename_base = json_file_path.stem
output_png_path = f"{output_filename_base}.png"

fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")