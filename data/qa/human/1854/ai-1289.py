import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
json_filepath = pathlib.Path(json_path)

if not json_filepath.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_filepath, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in reversed(chart_data)]
values = [item['value'] for item in reversed(chart_data)]

bar_text_labels = [f'{v:,}'.replace(',', ' ') for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors[0]),
    text=bar_text_labels,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    hoverinfo='none',
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color='#000000'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        title_standoff=15,
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        ticks='outside',
        tickcolor='lightgrey',
        tickformat=' ',
        range=[0, 2300],
        dtick=250
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        showline=False,
        ticks='',
        automargin=True
    ),
    margin=dict(l=10, r=60, t=30, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=10, color='grey')
        )
    ]
)

output_filename = json_filepath.with_suffix(".png")
fig.write_image(str(output_filename), scale=2, width=800, height=500)

print(f"Chart saved to {output_filename}")