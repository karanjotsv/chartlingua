import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = pathlib.Path(json_path_str)

if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_data = [item['year'] for item in data]
y_data = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_data,
    y=y_data,
    marker_color=colors[0],
    showlegend=False
))

title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
full_title = f"<b>{title_text}</b><br><sub>{subtitle_text}</sub>" if title_text else ""

fig.update_layout(
    title=dict(
        text=full_title,
        x=0.01,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        tickangle=0,
        showline=True,
        linewidth=1,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 12500000],
        tickformat=' ',
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=90, r=40, t=50, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")