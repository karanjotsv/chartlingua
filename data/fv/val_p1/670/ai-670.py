import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name> <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    texttemplate='%{text}',
    textfont_size=8
))

title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"
yaxis_ticks = list(range(0, 1551, 50))

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.05,
        'xanchor': 'left',
        'yanchor': 'top'
    },
    font_family="Arial",
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'showgrid': False,
        'linecolor': 'black',
        'ticks': 'outside'
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'range': [0, 1600],
        'tickvals': yaxis_ticks,
        'gridcolor': '#e0e0e0',
        'gridwidth': 1,
        'griddash': 'dot',
        'zeroline': False,
        'linecolor': 'black',
        'ticks': 'outside'
    },
    yaxis2={
        'range': [0, 1600],
        'tickvals': yaxis_ticks,
        'overlaying': 'y',
        'side': 'right',
        'showgrid': False,
        'zeroline': False,
        'showticklabels': True,
        'linecolor': 'black',
        'ticks': 'outside'
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin={'l': 60, 'r': 60, 't': 80, 'b': 60},
    showlegend=False
)

base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")