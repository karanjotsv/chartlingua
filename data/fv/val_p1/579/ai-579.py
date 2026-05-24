import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit("Usage: python <script_name>.py <json_file_path>")

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
legend_map = chart_info['legend_map']

fig = go.Figure()

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
bar_colors = [colors[d['type']] for d in chart_data]

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(
        color=bar_colors,
        line=dict(color='black', width=1)
    ),
    showlegend=False
))

for key, name in legend_map.items():
    fig.add_trace(go.Bar(
        x=[None],
        y=[None],
        name=name,
        marker=dict(
            color=colors[key],
            line=dict(color='black', width=1)
        )
    ))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(text=title_text, x=0.05, y=0.98, xanchor='left'),
    xaxis=dict(
        type='log',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    yaxis=dict(
        autorange="reversed",
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=250, r=20, t=80, b=40),
    legend=dict(
        x=0.95,
        y=0.05,
        xanchor='right',
        yanchor='bottom',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    )
)

base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)