import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_filepath = sys.argv[1]

try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_filepath}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from the file '{json_filepath}'.")
    sys.exit(1)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=chart_data['categories'],
        y=series['data'],
        marker_color=colors[i % len(colors)]
    ))

title_text = texts['title']
if texts['subtitle']:
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    xaxis_title_text=texts['x_axis_title'],
    yaxis_title_text=texts['y_axis_title'],
    barmode='stack',
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        range=[0, 60],
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1
    ),
    xaxis=dict(
        showline=False,
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=60, r=40, t=80, b=200)
)

output_filename_base = json_filepath.rsplit('.', 1)[0]
output_filename_png = f"{output_filename_base}.png"

fig.write_image(output_filename_png, scale=2)
print(f"Chart saved to {output_filename_png}")