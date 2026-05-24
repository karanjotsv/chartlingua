import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_vals = [d['x'] for d in chart_data]
y_vals = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_vals,
    y=y_vals,
    text=y_vals,
    textposition='outside',
    texttemplate='%{text:.2f}',
    marker_color=colors[0],
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    title=texts.get('title'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        tickmode='linear'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        gridcolor='#e9e9e9',
        zeroline=False,
        range=[0, 18],
        dtick=2.5
    ),
    margin=dict(l=80, r=40, t=50, b=100)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.98, y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=12)
    )

base_filename = json_file_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")