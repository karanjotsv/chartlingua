import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data_config = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

labels = [item['category'] for item in data_config]
values = [item['value'] for item in data_config]
text_labels = [f"{item['category']}<br>{item['value']}%" for item in data_config]
text_colors = [item['text_color'] for item in data_config]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.5,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    text=text_labels,
    textposition='inside',
    textinfo='none',
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    textfont=dict(
        family="Arial",
        size=24,
        color=text_colors
    )
))

title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    showlegend=False,
    font=dict(
        family="Arial",
        size=16,
        color="black"
    ),
    margin=dict(t=80, b=80, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1,
            xanchor="left",
            yanchor="top",
            align="left",
            font=dict(
                family="Arial",
                size=12,
                color="grey"
            )
        )
    ]
)

output_filename_base = json_file_path.stem
output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")