import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

categories = [item['category'] for item in chart_data['chart_data']]
values = [item['value'] for item in chart_data['chart_data']]
texts = chart_data['texts']
colors = chart_data['colors']

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    hoverinfo='none'
))

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#F0F0F0',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1250],
        dtick=250,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        tickfont=dict(size=12),
        automargin=True
    ),
    margin=dict(l=90, r=40, t=40, b=120)
)

if texts.get('source'):
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.99, y=-0.28,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(size=12, color="#555555")
    )

output_filename = json_path.with_suffix(".png")
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")