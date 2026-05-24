import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        mode='lines+markers+text',
        name=series.get("name", ""),
        line=dict(color=color, width=2.5),
        marker=dict(color=color, size=7),
        text=series.get("text"),
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color='#000000'
        ),
        hoverinfo='skip'
    ))

title_text = texts.get('title')
if texts.get('subtitle'):
    title_text = f"{title_text}<br><sub>{texts.get('subtitle')}</sub>" if title_text else f"<sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        tickvals=chart_data[0].get("x"),
        tickmode='array',
        showgrid=False,
        zeroline=False,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[18, 25],
        dtick=1,
        ticksuffix='%',
        gridcolor='#dddddd',
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(l=80, r=40, t=60, b=120),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get("source"),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")