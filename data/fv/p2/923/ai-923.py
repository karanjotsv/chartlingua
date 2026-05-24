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
    chart_data = json.load(f)

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['values'],
        name=series['name'],
        marker_color=chart_data['colors'][i],
        marker_line_color='black',
        marker_line_width=1.5,
        error_y=dict(
            type='data',
            array=series['errors'],
            visible=True,
            color='black',
            thickness=1.5,
            width=4
        )
    ))

texts = chart_data['texts']

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=18, color='black'),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        title_font=dict(size=22),
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=False,
        tickfont=dict(size=16)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        title_font=dict(size=22),
        range=[0, 80],
        tickmode='linear',
        tick0=0,
        dtick=20,
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=False,
        gridcolor='#cccccc',
        gridwidth=1,
        griddash='dot',
        tickfont=dict(size=16)
    ),
    legend=dict(
        x=0.05,
        y=0.98,
        xanchor='left',
        yanchor='top',
        bgcolor='white',
        borderwidth=0,
        font=dict(size=18)
    ),
    margin=dict(l=100, r=40, t=40, b=80)
)

output_filename_base = json_path.stem
output_png_path = f"{output_filename_base}.png"
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")