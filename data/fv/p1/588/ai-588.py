import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = chart_data.get('categories', [])
series_data = chart_data.get('series', [])

fig = go.Figure()

for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('y'),
        name=series.get('name'),
        marker_color=colors[i % len(colors)],
        marker_line_color='black',
        marker_line_width=1,
        error_y=series.get('error_y', {}),
        error_y_color='black',
        error_y_thickness=1.5
    ))

fig.update_layout(
    barmode='group',
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    legend_title_text=f"<b>{texts.get('legend_title')}</b>" if texts.get('legend_title') else None,
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='#EBEBEB',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        gridcolor='white',
        range=[0, 0.7],
        tickvals=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
        tickformat='.1f',
        zeroline=True,
        zerolinecolor='white',
        zerolinewidth=2,
        showline=True,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    margin=dict(l=80, r=40, t=50, b=80),
    legend=dict(
        x=0.98,
        y=0.9,
        xanchor='right',
        yanchor='top'
    )
)

output_base_name = pathlib.Path(json_path).stem
output_filename = f"{output_base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")