import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}", file=sys.stderr)
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series_list = chart_data['series']

fig = go.Figure()

for i, series in enumerate(series_list):
    fig.add_trace(go.Scatter(
        x=categories,
        y=series['values'],
        name=series['name'],
        mode='lines',
        line=dict(color=colors[i], width=2)
    ))

title_text = texts['title']
if texts.get('subtitle'):
    title_text = f"<b>{texts['title']}</b><br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text,
    yaxis_title_text=texts['y_axis_title'],
    xaxis_title_text=texts['x_axis_title'],
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        tickmode='array',
        tickvals=categories,
        ticktext=[str(c) for c in categories]
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        range=[0, 250]
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="left",
        x=0
    ),
    margin=dict(l=70, r=30, t=80, b=100)
)

output_filename_base = json_file_path.stem
output_png_path = f"{output_filename_base}.png"
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")