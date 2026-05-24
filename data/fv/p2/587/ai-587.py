import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

labels = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    texttemplate='%{label}: %{value}',
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,
    rotation=90
))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            x=0.99,
            y=-0.15,
            xref='paper',
            yref='paper',
            xanchor='right',
            yanchor='bottom',
            showarrow=False,
            font=dict(
                family="Arial",
                size=10,
                color="#cccccc"
            )
        )
    )

fig.update_layout(
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5,
        font=dict(
            family="Arial",
            color="white"
        )
    ),
    font=dict(
        family="Arial"
    ),
    paper_bgcolor='black',
    plot_bgcolor='white',
    margin=dict(l=60, r=60, t=40, b=80),
    annotations=annotations
)

fig.update_traces(
    textfont=dict(
        family="Arial",
        color='black'
    )
)

output_filename_base = json_file_path.stem
output_filename_png = f"{output_filename_base}.png"
fig.write_image(output_filename_png, scale=2)

print(f"Chart saved to {output_filename_png}")