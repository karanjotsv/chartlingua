import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_filename = json_path.stem + ".png"

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

x_values = [item['category'] for item in chart_data]
y_values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    text=y_values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    cliponaxis=False,
    showlegend=False
))

fig.update_traces(textfont=dict(family="Arial", size=12, color='black'))

title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_xanchor='left',
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        ticks='',
        automargin=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        showline=False,
        ticks='',
        zeroline=False,
        range=[0, 1.8],
        tickmode='array',
        tickvals=[0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75]
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=10, color='grey')
        )
    ]
)

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")