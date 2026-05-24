import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[str(v) for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False 
))

fig.update_layout(
    template='plotly_white',
    title=texts.get('title'),
    font=dict(family="Arial", size=12),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E5E7EB',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        tickvals=[0, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000],
        ticktext=['0', '2 500', '5 000', '7 500', '10 000', '12 500', '15 000', '17 500', '20 ...'],
        range=[0, 21000]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed'
    ),
    margin=dict(l=150, r=60, t=40, b=100),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12)
        )
    ]
)

output_path = pathlib.Path(json_path).with_suffix('.png')
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")