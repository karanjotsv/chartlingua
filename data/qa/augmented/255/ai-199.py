import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors),
    textposition='none'
))

for category, value in zip(categories, values):
    x_anchor = 'left' if value >= 0 else 'right'
    x_shift = 5 if value >= 0 else -5
    fig.add_annotation(
        x=value,
        y=category,
        text=f"{value}%",
        showarrow=False,
        font=dict(family="Arial", size=12, color="black"),
        xanchor=x_anchor,
        xshift=x_shift,
        yanchor='middle'
    )

title_text = texts.get('title')
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br>{texts.get('subtitle')}" if title_text else texts.get('subtitle')

source_text = texts.get('source', '')

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        font=dict(family="Arial")
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1.2,
        ticksuffix='%'
    ),
    yaxis=dict(
        autorange="reversed",
        showgrid=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    margin=dict(l=100, r=60, t=60, b=80),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10, family="Arial")
        )
    ]
)

path_parts = json_path.replace('\\', '/').split('/')
filename_with_ext = path_parts[-1]
base_filename = filename_with_ext.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")