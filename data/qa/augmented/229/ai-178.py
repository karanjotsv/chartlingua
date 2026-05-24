import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

y_categories = [item['category'] for item in chart_data]
x_values = [item['value'] for item in chart_data]

formatted_texts = [f'{val:,}'.replace(',', ' ') for val in x_values]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=y_categories,
    x=x_values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=formatted_texts,
    textposition='outside',
    texttemplate='%{text}',
    hoverinfo='none',
    cliponaxis=False
))

shapes = []
for i in range(len(y_categories)):
    if i % 2 != 0:
        shapes.append(go.layout.Shape(
            type="rect",
            xref="paper",
            yref="y",
            x0=0,
            y0=i - 0.5,
            x1=1,
            y1=i + 0.5,
            fillcolor="#f5f5f5",
            layer="below",
            line_width=0,
        ))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, 16500],
        tickmode='linear',
        dtick=2000,
        tickformat=' '
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    margin=dict(l=100, r=60, t=30, b=80),
    shapes=shapes,
    annotations=[
        dict(
            text=texts.get('note', ''),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top'
        ),
        dict(
            text=texts.get('source', ''),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top'
        )
    ]
)

fig.update_traces(textfont_size=12)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")