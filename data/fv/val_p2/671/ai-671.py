import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

chart_data = chart_json['chart_data']
texts = chart_json['texts']
series_colors = chart_json['colors']
style_options = chart_json.get('style_options', {})

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['data'],
        name=series.get('name', ''),
        marker_color=series_colors[i % len(series_colors)],
        marker_line_color=style_options.get('bar_border_color', '#000000'),
        marker_line_width=1
    ))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color=style_options.get('text_color', '#000000')
    ),
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    plot_bgcolor=style_options.get('background_color', '#FFFFFF'),
    paper_bgcolor=style_options.get('background_color', '#FFFFFF'),
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        mirror=True,
        tickmode='linear',
        tickfont=dict(size=10)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 5],
        dtick=0.5,
        tickformat=",.2f",
        gridcolor=style_options.get('grid_color', '#CCCCCC'),
        showgrid=True,
        showline=True,
        linecolor='black',
        linewidth=1,
        mirror=True,
        zeroline=False
    ),
    margin=dict(l=50, r=20, t=60, b=40)
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")