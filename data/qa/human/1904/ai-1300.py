import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=categories,
    y=values,
    mode='lines+markers',
    marker=dict(
        color=colors[0],
        size=8
    ),
    line=dict(
        color=colors[0],
        width=3
    ),
    showlegend=False
))

annotations = []
for i, item in enumerate(data):
    annotations.append(dict(
        x=item['category'],
        y=item['value'],
        text=str(item['value']),
        showarrow=False,
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        xanchor='center',
        yanchor='bottom',
        yshift=5
    ))

if texts.get('source'):
    annotations.append(dict(
        xref="paper",
        yref="paper",
        x=0.99,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(
            family="Arial",
            size=12,
            color="grey"
        )
    ))

fig.update_layout(
    font=dict(family="Arial"),
    paper_bgcolor='#F8F9FA',
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='#F0F0F0',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[100, 130],
        tickvals=[100, 105, 110, 115, 120, 125, 130],
        showgrid=True,
        gridwidth=1,
        gridcolor='#EAEAEA',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=40, b=80),
    annotations=annotations
)

output_filename = json_file_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")