import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    texttemplate='%{y}',
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False
))

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        gridcolor='#e0e0e0',
        range=[0, 35000],
        tickmode='linear',
        tick0=0,
        dtick=5000,
        zeroline=False,
        title_standoff=10
    ),
    margin=dict(t=40, b=80, l=90, r=20)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=1, y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=12, color='#666666')
    )

base_filename = pathlib.Path(json_path).stem
output_file = f"{base_filename}.png"
fig.write_image(output_file, scale=2)
print(f"Chart saved to {output_file}")