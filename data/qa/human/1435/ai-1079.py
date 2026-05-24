import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])

if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

labels = [d["label"] for d in chart_data]
values = [d["value"] for d in chart_data]
slice_text = [f"<b>{d['label']}</b><br>{d['value']}%" for d in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors["series"],
    text=slice_text,
    textinfo='text',
    textposition='inside',
    textfont=dict(
        family="Arial",
        size=18,
        color='black' # Default color, will be overridden
    ),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
)])

fig.data[0].textfont.color = colors.get("text_on_slice", "black")

title_text = texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text_parts = [texts.get('source', ''), texts.get('note', '')]
source_text = '<br>'.join(filter(None, source_text_parts))

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.9,
        x=0.05,
        xanchor='left',
        yanchor='top',
        font=dict(
            family="Arial",
            size=26,
            color=colors['title']
        )
    ),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0.01,
            xanchor='left',
            yanchor='bottom',
            align='left',
            font=dict(
                family="Arial",
                size=12,
                color='black'
            )
        )
    ],
    font=dict(family="Arial"),
    showlegend=False,
    margin=dict(t=150, b=60, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

output_filename = json_file_path.with_suffix(".png").name
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")