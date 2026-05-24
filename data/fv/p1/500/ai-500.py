import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit("Usage: python <script_name>.py <json_file_path>")

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        line=dict(color=colors[i % len(colors)], width=4),
        showlegend=False,
        connectgaps=False
    ))

for y_val in range(1, 11):
    fig.add_shape(
        type="rect",
        xref="paper",
        yref="y",
        x0=0,
        y0=y_val - 0.45,
        x1=1,
        y1=y_val + 0.45,
        fillcolor="#D3D3D3",
        layer="below",
        line_width=0
    )

title_text_parts = []
if texts.get('title'):
    title_text_parts.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle'):
    title_text_parts.append(f'<span style="font-size: 14px;">{texts["subtitle"]}</span>')
full_title = "<br>".join(title_text_parts)

source_text_parts = []
if texts.get('source'):
    source_text_parts.append(texts['source'])
if texts.get('note'):
    source_text_parts.append(texts['note'])
full_source = "<br>".join(source_text_parts)

fig.update_layout(
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
    font=dict(family="Arial"),
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(
        visible=False,
        range=[0, 100]
    ),
    yaxis=dict(
        visible=False,
        range=[0.5, 11]
    ),
    title=dict(
        text=full_title,
        x=0.05, xanchor='left', y=0.95, yanchor='top'
    ),
    showlegend=False
)

if full_source:
    fig.add_annotation(
        text=full_source,
        xref="paper", yref="paper",
        x=0, y=-0.05,
        xanchor='left', yanchor='top',
        showarrow=False,
        align='left'
    )

base_name = json_path.replace('\\', '/').split('/')[-1].rsplit('.', 1)[0]
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)