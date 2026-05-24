import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', {})

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors.get('bar_color'),
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial", color=colors.get('text_color')),
    plot_bgcolor=colors.get('background_color'),
    paper_bgcolor=colors.get('background_color'),
    showlegend=False,
    margin=dict(l=60, r=20, t=20, b=40),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor=colors.get('grid_color'),
        gridwidth=1,
        tickvals=[0, 100000, 200000, 300000],
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor=colors.get('axis_line_color'),
        ticks="outside",
        tickcolor=colors.get('axis_line_color')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        autorange="reversed",
        showgrid=False,
        tickfont=dict(weight='bold'),
        showline=True,
        linewidth=1,
        linecolor=colors.get('axis_line_color'),
        ticks="outside",
        tickcolor=colors.get('axis_line_color')
    )
)

base_name = json_path.rsplit('.', 1)[0]
output_file = f"{base_name}.png"
fig.write_image(output_file, scale=2)

print(f"Chart saved to {output_file}")