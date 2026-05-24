import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
output_image_path = json_file_path.rsplit('.', 1)[0] + '.png'

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors),
    sort=False,
    direction='clockwise',
    textposition='outside',
    textinfo='label+percent',
    hoverinfo='label+percent'
)])

title_text = ""
if texts.get('title'):
    title_text += f"<span style='font-size: 24px;'><b>{texts['title']}</b></span>"
if texts.get('subtitle'):
    title_text += f"<br><span style='font-size: 16px;'>{texts['subtitle']}</span>"

fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.5,
    font=dict(family="Arial", size=14),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=80, r=80, t=80, b=80)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=0,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=12, color="grey")
    )

fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")