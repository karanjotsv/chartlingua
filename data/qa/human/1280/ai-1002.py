import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

texts = chart_data['texts']
colors = chart_data['colors']
data_series = chart_data['chart_data']

fig = go.Figure()

for i, trace_info in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=trace_info['x'],
        y=trace_info['y'],
        mode=trace_info.get('mode', 'lines+markers'),
        name=trace_info['name'],
        line=dict(
            color=colors[i],
            dash=trace_info.get('line_style', 'solid')
        ),
        marker=dict(
            color=colors[i],
            size=6
        ),
        showlegend=False
    ))

title_text = f"<b>{texts['title']}</b><br><sup>{texts['subtitle']}</sup>"

fig.add_annotation(
    text=texts['source'],
    xref="paper", yref="paper",
    x=1.0, y=0.94,
    showarrow=False,
    xanchor='right',
    yanchor='bottom',
    align='right',
    font=dict(family="Arial", size=10)
)

for ann in texts.get('annotations', []):
    fig.add_annotation(
        x=ann['x'],
        y=ann['y'],
        text=ann['text'],
        showarrow=ann.get('showarrow', False),
        arrowhead=ann.get('arrowhead', 1),
        arrowcolor=ann.get('arrowcolor'),
        ax=ann.get('ax', 0),
        ay=ann.get('ay', 0),
        bgcolor=ann.get('bgcolor'),
        bordercolor=ann.get('bordercolor'),
        borderwidth=ann.get('borderwidth', 0),
        font=dict(family="Arial", size=12)
    )

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(family="Arial"),
    plot_bgcolor='#e9f2f8',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=140, b=80),
    xaxis=dict(
        tickvals=list(range(2007, 2020)),
        ticktext=[str(y) for y in range(2007, 2020)],
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        gridcolor='white',
        gridwidth=1,
        zeroline=False,
        range=[-10, 70]
    ),
    showlegend=False,
    shapes=[
        dict(
            type="line",
            xref="paper", yref="paper",
            x0=0, y0=0.88, x1=0.2, y1=0.88,
            line=dict(color="#3787c8", width=2)
        ),
        dict(
            type="line",
            xref="paper", yref="paper",
            x0=0, y0=-0.08, x1=1, y1=-0.08,
            line=dict(color="#3787c8", width=3)
        )
    ]
)

output_filename = json_path.with_suffix(".png")
fig.write_image(output_filename, scale=2, width=1000, height=600)
print(f"Chart saved to {output_filename}")