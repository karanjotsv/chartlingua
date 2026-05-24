import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading JSON file: {e}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=[f'{v:.1f}' for v in values],
    textposition='outside',
    marker_color=colors[0],
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br><i>{texts["subtitle"]}</i>' if title_text else f'<i>{texts["subtitle"]}</i>'

source_text = ""
if texts.get("source"):
    source_text += texts["source"]
if texts.get("note"):
    source_text += f'<br>{texts["note"]}' if source_text else texts["note"]

fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.05,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    xaxis=dict(
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(family="Arial")
    ),
    yaxis=dict(
        range=[0, 100],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False
    )
)

if source_text:
    fig.add_annotation(
        text=source_text,
        showarrow=False,
        xref="paper", yref="paper",
        x=1.0, y=-0.25,
        xanchor='right', yanchor='top',
        align='right',
        font=dict(family="Arial", size=10, color='grey')
    )

output_path = pathlib.Path(json_path)
output_filename = output_path.with_suffix(".png")

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")