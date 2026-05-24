import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

text_labels = ['{:,}'.format(v).replace(',', ' ') for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        title=texts['x_axis_title'],
        title_font=dict(size=13),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        range=[0, 31500],
        dtick=2500,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        tickfont=dict(size=12)
    ),
    showlegend=False,
    margin=dict(l=150, r=60, t=40, b=80),
    height=800,
    width=950,
    separators='. '
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=0.99,
        y=-0.1,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(
            family="Arial",
            size=12,
            color="#888888"
        )
    )

output_filename_base = pathlib.Path(json_path).stem
fig.write_image(f"{output_filename_base}.png", scale=2)

print(f"Chart saved to {output_filename_base}.png")