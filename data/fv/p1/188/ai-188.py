import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
filename_base = json_path.rsplit('.', 1)[0]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

years = [d['year'] for d in chart_data]
values = [d['value'] for d in chart_data]
bar_colors = [colors[d['category']] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=years,
    y=values,
    marker_color=bar_colors,
    marker_line_color=colors['bar_outline'],
    marker_line_width=1.5,
    showlegend=False
))

# Custom legend: shapes for color swatches
legend_x0, legend_x1 = 1952, 1956
el_nino_swatches = [
    {'y0': 0.96, 'y1': 1.0, 'color': colors['very_strong_el_nino']},
    {'y0': 0.92, 'y1': 0.96, 'color': colors['strong_el_nino']},
    {'y0': 0.88, 'y1': 0.92, 'color': colors['moderate_el_nino']},
    {'y0': 0.84, 'y1': 0.88, 'color': colors['weak_el_nino']}
]
for swatch in el_nino_swatches:
    fig.add_shape(type="rect", xref="x", yref="y", x0=legend_x0, y0=swatch['y0'], x1=legend_x1, y1=swatch['y1'], fillcolor=swatch['color'], line_width=0)

fig.add_shape(type="rect", xref="x", yref="y", x0=legend_x0, y0=0.64, x1=legend_x1, y1=0.68, fillcolor=colors['neutral'], line_width=0)

la_nina_swatches = [
    {'y0': 0.50, 'y1': 0.54, 'color': colors['weak_la_nina']},
    {'y0': 0.46, 'y1': 0.50, 'color': colors['moderate_la_nina']},
    {'y0': 0.42, 'y1': 0.46, 'color': colors['strong_la_nina']}
]
for swatch in la_nina_swatches:
    fig.add_shape(type="rect", xref="x", yref="y", x0=legend_x0, y0=swatch['y0'], x1=legend_x1, y1=swatch['y1'], fillcolor=swatch['color'], line_width=0)

# Custom legend: text annotations
legend_text_x = 1957.5
fig.add_annotation(xref="x", yref="y", x=legend_text_x, y=0.92, text=texts['legend_el_nino'], showarrow=False, align='left', xanchor='left', yanchor='middle', font=dict(color=colors['text_secondary'], size=18, family="Arial"))
fig.add_annotation(xref="x", yref="y", x=legend_text_x, y=0.66, text=texts['legend_neutral'], showarrow=False, align='left', xanchor='left', yanchor='middle', font=dict(color=colors['text_secondary'], size=18, family="Arial"))
fig.add_annotation(xref="x", yref="y", x=legend_text_x, y=0.48, text=texts['legend_la_nina'], showarrow=False, align='left', xanchor='left', yanchor='middle', font=dict(color=colors['text_secondary'], size=18, family="Arial"))

# Source annotation
fig.add_annotation(
    xref="paper", yref="paper",
    x=0.5, y=-0.15,
    text=texts['source'],
    showarrow=False,
    xanchor='center', yanchor='top',
    font=dict(size=9, color=colors['text_primary'], family="Arial")
)

fig.update_layout(
    title_text=texts['title'],
    title_x=0.05,
    title_y=0.95,
    title_font=dict(size=26, color=colors['text_primary'], family="Arial"),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font=dict(family="Arial", color=colors['text_primary']),
    margin=dict(l=60, r=20, t=100, b=80),
    bargap=0.1
)

fig.update_xaxes(
    tickvals=list(range(1950, 2021, 10)),
    tickfont=dict(size=18),
    showgrid=True,
    gridcolor=colors['grid'],
    gridwidth=1,
    zeroline=True,
    zerolinecolor=colors['text_primary'],
    zerolinewidth=2,
    range=[1949, 2023]
)

fig.update_yaxes(
    tickvals=[0, 0.25, 0.50, 0.75, 1.0],
    ticktext=['0 °C', '0.25', '0.50', '0.75', '1 °C'],
    tickfont=dict(size=18),
    showgrid=True,
    gridcolor=colors['grid'],
    gridwidth=1,
    zeroline=False,
    range=[-0.5, 1.05]
)

fig.write_image(f"{filename_base}.png", scale=2, width=900, height=600)