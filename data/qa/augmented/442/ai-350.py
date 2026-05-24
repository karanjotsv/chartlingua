import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
series_data = [list(t) for t in zip(*[item['values'] for item in chart_data])]

fig = go.Figure()

for i, series_name in enumerate(texts['series_names']):
    fig.add_trace(go.Bar(
        x=categories,
        y=series_data[i],
        name=series_name,
        marker_color=colors[i],
        text=series_data[i],
        textposition='outside',
        texttemplate='%{y}',
        cliponaxis=False
    ))

title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = ""
if texts.get("source"):
    source_text += texts["source"]
if texts.get("note"):
    source_text += f"<br>{texts['note']}"

fig.update_layout(
    barmode='group',
    title_text=title_text if title_text else None,
    yaxis_title_text=texts['y_axis_title'],
    xaxis_title_text=texts['x_axis_title'],
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=50, b=150),
    xaxis=dict(
        tickangle=-45,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        range=[0, 18000],
        dtick=2500,
        showgrid=True,
        gridwidth=1,
        gridcolor='#e0e0e0',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.5,
            xanchor="right",
            yanchor="bottom",
            align="right",
            font=dict(size=10)
        )
    ]
)

fig.update_traces(textfont=dict(family='Arial', size=11, color='black'))

output_filename = json_path.with_suffix(".png")
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")