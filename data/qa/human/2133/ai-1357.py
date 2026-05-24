import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]
output_filename = json_path.rsplit('.', 1)[0] + '.png'

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['data'],
        name=series['name'],
        marker_color=colors[i],
        text=[f'{val}%' for val in series['data']],
        textposition='outside',
        textfont=dict(family='Arial', size=12, color='black'),
        cliponaxis=False 
    ))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 85],
        tickformat='%g%%',
        showgrid=True,
        gridcolor='#E0E0E0'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=60, r=40, b=150, t=60),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper",
            yref="paper",
            x=1,
            y=-0.4,
            xanchor="right",
            yanchor="bottom",
            align="right"
        )
    ]
)

fig.add_vline(x=0.5, line_width=1, line_color='#EAEAEA')
fig.add_vline(x=1.5, line_width=1, line_color='#EAEAEA')

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")