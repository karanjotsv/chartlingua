import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

output_path = json_path.with_suffix('.png')

with open(json_path, 'r', encoding='utf-8') as f:
    chart_details = json.load(f)

data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

fig = go.Figure()

for i, series in enumerate(data['series']):
    fig.add_trace(go.Bar(
        x=data['categories'],
        y=series['data'],
        name=series['name'],
        marker_color=colors[i]
    ))

title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}" if texts.get('title') and texts.get('subtitle') else texts.get('title', '')
source_parts = [texts.get('source'), texts.get('note')]
source_text = "<br>".join(filter(None, source_parts))

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='#000000'),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_font_size=14,
        tickfont_size=12,
        range=[0, 101],
        tickvals=[0, 20, 40, 60, 80, 100],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickfont_size=12,
        showgrid=False,
        zeroline=True,
        zerolinecolor='#e0e0e0',
        zerolinewidth=1
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        traceorder='normal',
        font_size=12
    ),
    margin=dict(l=70, r=40, t=50, b=150)
)

if source_text:
    fig.add_annotation(
        text=source_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.98,
        y=-0.45,
        xanchor='right',
        yanchor='bottom',
        font_size=10
    )

fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")