import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)


chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
facet_titles = [d['group'] for d in chart_data]

fig = make_subplots(
    rows=1,
    cols=len(chart_data),
    subplot_titles=facet_titles,
    shared_yaxes=True,
    horizontal_spacing=0.02
)

legend_series_names = texts['legend_series_names']
for col_idx, facet in enumerate(chart_data, 1):
    for series_idx, series in enumerate(facet['series']):
        fig.add_trace(
            go.Bar(
                x=facet['categories'],
                y=series['values'],
                name=legend_series_names[series_idx],
                marker_color=colors[series_idx],
                showlegend=(col_idx == 1)
            ),
            row=1,
            col=col_idx
        )

fig.update_layout(
    barmode='stack',
    font_family="Arial",
    plot_bgcolor='white',
    legend_title_text=None,
    legend=dict(traceorder='normal'),
    margin=dict(l=80, r=20, t=80, b=120),
    height=500,
    width=900
)

fig.update_annotations(
    font=dict(family="Arial", size=14, color='black'),
    bgcolor='#e0e0e0',
    borderpad=4
)

fig.update_xaxes(
    tickangle=-45,
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    zeroline=False
)

fig.update_yaxes(
    title_text=texts['y_axis_title'] if texts.get('y_axis_title') else None,
    showgrid=True,
    gridcolor='lightgray',
    range=[0, 0.5],
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    zeroline=False,
    col=1
)

if texts.get('x_axis_title'):
    fig.add_annotation(
        text=texts['x_axis_title'],
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.28,
        showarrow=False,
        font=dict(size=14, family="Arial")
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")