import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[f'{v:,}'.replace(',', ' ') for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        tickformat=' ',
        range=[0, max(values) * 1.15] 
    ),
    yaxis=dict(
        autorange='reversed',
        showticklabels=True,
        automargin=True
    ),
    margin=dict(l=280, r=80, t=30, b=80),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.12,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#666')
        )
    ]
)

output_filename_base = json_file_path.stem
output_filename_png = f"{output_filename_base}.png"
fig.write_image(output_filename_png, scale=2)

print(f"Chart saved as {output_filename_png}")