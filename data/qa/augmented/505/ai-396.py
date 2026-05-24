import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
categories = chart_info.get('categories', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series.get('name'),
        x=categories,
        y=series.get('values'),
        marker_color=colors[i % len(colors)]
    ))

fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=80, r=40, t=50, b=150),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 75],
        gridcolor='#e0e0e0',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    xaxis=dict(
        tickfont=dict(size=12),
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    )
)

annotations = []
if texts.get('source_note'):
    annotations.append(
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            text=texts.get('source_note'),
            showarrow=False,
            align='right',
            font=dict(size=10, color='#555555')
        )
    )

fig.update_layout(annotations=annotations)

output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart saved to {output_filename}")