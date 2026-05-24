import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Scatter(
        x=chart_data['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=colors[i], width=2)
    ))

title_parts = []
if texts.get('title'):
    title_parts.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle'):
    title_parts.append(f"<span style='font-size: smaller;'>{texts['subtitle']}</span>")
full_title = "<br>".join(title_parts)

annotations = []
footnote_parts = []
if texts.get('source'):
    footnote_parts.append(texts['source'])
if texts.get('note'):
    footnote_parts.append(texts['note'])

if footnote_parts:
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        text="<br>".join(footnote_parts),
        showarrow=False,
        align='left',
        font=dict(family="Arial", size=10)
    ))

fig.update_layout(
    title=dict(
        text=full_title,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        tickmode='array',
        tickvals=chart_data['x'],
        ticktext=[str(year) for year in chart_data['x']]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        range=[-14000, 2000]
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='#f0f0f0',
    legend=dict(
        x=1.02,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    margin=dict(l=80, r=120, t=80, b=80),
    annotations=annotations,
    hovermode='x unified'
)

output_filename = json_path.stem + '.png'
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")