import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if len(sys.argv) != 2:
    print("Usage: python <script.py> <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

charts_config = config['charts']
colors_config = config['colors']
desc_box_width = 0.45
plot_start_x = desc_box_width + 0.03

fig = make_subplots(
    rows=2, cols=1,
    vertical_spacing=0.15
)

y_domains = [fig.layout.yaxis.domain, fig.layout.yaxis2.domain]
max_vals = [max(c['chart_data']['values']) for c in charts_config]

for i, chart_spec in enumerate(charts_config):
    chart_data = chart_spec['chart_data']
    texts = chart_spec['texts']
    
    y_start, y_end = y_domains[i]
    title_bar_height = 0.08

    # Add background shape for the title
    fig.add_shape(type="rect", xref="paper", yref="paper",
                  x0=0, y0=y_end, x1=1, y1=y_end + title_bar_height,
                  fillcolor=colors_config['title_background'],
                  line_width=0, layer='below')

    # Add title text
    fig.add_annotation(text=f"<b>{texts['title']}</b>", xref="paper", yref="paper",
                       x=0.5, y=y_end + title_bar_height / 2,
                       showarrow=False, font=dict(color=colors_config['title_font'], size=16, family="Arial"),
                       xanchor='center', yanchor='middle')

    # Add background shape for the description
    fig.add_shape(type="rect", xref="paper", yref="paper",
                  x0=0.01, y0=y_start, x1=desc_box_width, y1=y_end,
                  fillcolor=colors_config['description_background'],
                  line_width=0, layer='below')

    # Add description text
    fig.add_annotation(text=texts['description'], xref="paper", yref="paper",
                       x=0.01 + (desc_box_width - 0.01) / 2, y=(y_start + y_end) / 2,
                       showarrow=False, font=dict(color=colors_config['description_font'], size=11, family="Arial"),
                       align="left", xanchor='center', yanchor='middle')

    # Add the bar chart
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=chart_data['values'],
        marker=dict(color=colors_config['bar'], line=dict(color=colors_config['bar_border'], width=1)),
        text=chart_data['values'],
        textposition='outside',
        textfont=dict(color=colors_config['data_label'], family="Arial", size=12),
        cliponaxis=False
    ), row=i + 1, col=1)


fig.update_xaxes(
    domain=[plot_start_x, 0.98],
    tickfont=dict(family="Arial", size=12),
    showline=True, linewidth=1, linecolor=colors_config['grid'], mirror=True,
    showgrid=False
)

fig.update_yaxes(
    row=1, col=1,
    showticklabels=False,
    showgrid=True, gridcolor=colors_config['grid'],
    zeroline=False,
    range=[0, max_vals[0] * 1.15],
    showline=True, linewidth=1, linecolor=colors_config['grid'], mirror=True
)
fig.update_yaxes(
    row=2, col=1,
    showticklabels=False,
    showgrid=True, gridcolor=colors_config['grid'],
    zeroline=False,
    range=[0, max_vals[1] * 1.15],
    showline=True, linewidth=1, linecolor=colors_config['grid'], mirror=True
)


fig.update_layout(
    height=800,
    width=900,
    showlegend=False,
    paper_bgcolor=colors_config['paper_background'],
    plot_bgcolor=colors_config['plot_background'],
    margin=dict(t=80, b=40, l=20, r=20),
    font=dict(family="Arial")
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")