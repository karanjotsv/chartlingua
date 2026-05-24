import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

output_file_path = json_file_path.with_suffix(".png")

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    texttemplate='%{label} %{value}%',
    textposition='outside',
    hoverinfo='label+percent',
    direction='clockwise',
    sort=False,
    pull=[0.01] * len(values) # Small pull for visual separation
))

fig.update_layout(
    font=dict(family="Arial", size=14, color="black"),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=80, t=50, b=80),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('note'),
            xref="paper",
            yref="paper",
            x=0,
            y=0,
            xanchor='left',
            yanchor='bottom',
            font=dict(size=12, color="#3366cc")
        ),
        dict(
            showarrow=False,
            text=texts.get('source'),
            xref="paper",
            yref="paper",
            x=1,
            y=0,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

fig.update_traces(textfont_size=16)

fig.write_image(output_file_path, scale=2)

print(f"Chart saved to {output_file_path}")