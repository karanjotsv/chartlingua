import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python <script_name> <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data for Plotly's top-to-bottom rendering of horizontal bars
categories.reverse()
values.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,
    hoverinfo='none'
))

title_text = ""
if texts.get("title"):
    title_text = f"<b>{texts['title']}</b>"
    if texts.get("subtitle"):
        title_text += f"<br><sup>{texts['subtitle']}</sup>"

annotations = []
if texts.get("note"):
    annotations.append(
        dict(
            showarrow=False,
            text=texts['note'],
            xref="paper",
            yref="paper",
            x=0,
            y=-0.18,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    )
if texts.get("source"):
    annotations.append(
        dict(
            showarrow=False,
            text=texts['source'],
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            align='right'
        )
    )

fig.update_layout(
    title=dict(text=title_text, x=0.01, xanchor='left'),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dot',
        zeroline=False,
        showline=False,
        ticks='outside',
        tickcolor='lightgrey'
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=100, r=50, t=50, b=100),
    showlegend=False,
    annotations=annotations
)

output_filename_base = json_path.stem
fig.write_image(f"{output_filename_base}.png", scale=2)

print(f"Chart saved to {output_filename_base}.png")