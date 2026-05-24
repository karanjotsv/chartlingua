import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', {})

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [f"{v}%" for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=text_labels,
    textposition='outside',
    marker_color=colors.get('series1', '#2672C9'),
    cliponaxis=False,
    hoverinfo='none'
))

title_text = texts.get('title')
full_title = f"<b>{title_text}</b>" if title_text else ""
if texts.get('subtitle'):
    full_title += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', ''),
        range=[0, 120],
        tickformat=',.0f',
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        tickmode='array',
        tickvals=categories,
        ticktext=categories,
        showgrid=False,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=80),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            x=1,
            y=-0.15,
            xref='paper',
            yref='paper',
            xanchor='right',
            yanchor='top',
            font=dict(size=10)
        )
    ]
)

output_filename = pathlib.Path(json_path).stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")