import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error: Could not read or parse the JSON file at '{json_path}'.\n{e}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#000000',
    marker_line_color='black',
    marker_line_width=1,
    showlegend=False
))

fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.02,
    title_xanchor='left',
    title_y=0.95,
    title_yanchor='top',
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=None,
    font_family="Arial",
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        showgrid=False
    ),
    yaxis=dict(
        range=[0, 12.5],
        tickvals=[0, 2.5, 5.0, 7.5, 10.0, 12.5],
        tickformat='.1f',
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        gridcolor='#CCCCCC',
        showgrid=True
    ),
    margin=dict(l=60, r=20, t=80, b=120),
    height=550,
    width=800
)

fig.add_annotation(
    text=texts.get('y_axis_title'),
    xref="paper", yref="paper",
    x=-0.01, y=1.04,
    showarrow=False,
    font=dict(
        family="Arial",
        size=14
    ),
    xanchor='right',
    yanchor='middle'
)

output_path = pathlib.Path(json_path).with_suffix('.png')
fig.write_image(str(output_path), scale=2)

print(f"Chart successfully generated and saved to {output_path}")