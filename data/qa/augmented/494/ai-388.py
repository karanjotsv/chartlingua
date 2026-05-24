import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' contains invalid JSON.")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=[f'{v}%' for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickfont=dict(size=12),
        showline=True,
        linecolor='lightgrey',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        tickfont=dict(size=12),
        range=[0, 85],
        tickvals=[i for i in range(0, 81, 10)],
        ticksuffix='%'
    ),
    margin=dict(l=80, r=40, t=50, b=100)
)

if texts.get('title') or texts.get('subtitle'):
    title_text = f"<b>{texts.get('title', '')}</b>"
    if texts.get('subtitle'):
        title_text += f"<br><sup>{texts.get('subtitle')}</sup>"
    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.05,
            xanchor='left',
            font=dict(family="Arial", size=16)
        )
    )

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.98, y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(family="Arial", size=10, color='grey')
    )

base_filename = json_path.split('/')[-1].split('\\')[-1].replace('.json', '')
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")