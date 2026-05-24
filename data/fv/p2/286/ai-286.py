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

labels_for_hover = [item['category'].replace('<br>', ' ') for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [f"{item['category']}<br>{item['value']}%" for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels_for_hover,
    values=values,
    text=text_labels,
    textinfo='text',
    textposition='outside',
    marker=dict(
        colors=colors,
        line=dict(color='black', width=2)
    ),
    sort=False,
    direction='clockwise',
    pull=[0.05, 0, 0, 0, 0, 0]
))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = ""
if texts.get('source'):
    source_text = f"<i>{texts['source']}</i>"

fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.5,
    font=dict(family="Arial", size=14, color="black"),
    showlegend=False,
    paper_bgcolor='#F9C984',
    plot_bgcolor='#F9C984',
    margin=dict(l=100, r=100, t=80, b=80),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.15,
            xanchor='center',
            yanchor='top',
            font=dict(family="Arial", size=12, color="black")
        )
    ] if source_text else []
)

output_base_name = json_path.stem
output_filename = f"{output_base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")