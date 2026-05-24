import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

chart_data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    cliponaxis=False,
    hoverinfo='none',
    textfont=dict(
        family='Arial',
        size=12,
        color='black'
    )
))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            x=1,
            y=-0.2,
            xref='paper',
            yref='paper',
            text=texts['source'],
            showarrow=False,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=12, color='#555555')
        )
    )

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 42],
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=annotations
)

output_filename_base = pathlib.Path(json_path).stem
output_path = f"{output_filename_base}.png"
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")