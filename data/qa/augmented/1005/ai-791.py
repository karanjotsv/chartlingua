import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

x_vals = [d['x'] for d in data]
y_vals = [d['y'] for d in data]
text_labels = [d['label'] if d['label'] is not None else "" for d in data]
text_positions = [d['position'] if d['position'] is not None else "top center" for d in data]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_vals,
    y=y_vals,
    mode='lines+markers+text',
    line=dict(color=colors['line'], width=3),
    marker=dict(color=colors['line'], size=8),
    text=text_labels,
    textposition=text_positions,
    textfont=dict(
        family="Arial",
        size=11,
        color=colors['text']
    )
))

annotations = []
if texts['source']:
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1.0, y=-0.15,
            xanchor="right", yanchor="top",
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12)
        )
    )

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    showlegend=False,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickmode='array',
        tickvals=x_vals,
        ticktext=[str(x) for x in x_vals],
        tickformat='d',
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[39.5, 43],
        dtick=0.5,
        ticksuffix='%',
        gridcolor=colors['grid'],
        linecolor='black'
    ),
    margin=dict(l=80, r=40, t=40, b=80),
    annotations=annotations
)

output_filename = pathlib.Path(json_path).stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")