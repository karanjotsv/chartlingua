import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#3078D1',
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False 
))

title_text = ""
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0.99, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            align='right',
            font=dict(family="Arial", size=12)
        )
    )

if texts.get('note'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0.01, y=-0.15,
            xanchor='left', yanchor='top',
            text=texts['note'],
            showarrow=False,
            align='left',
            font=dict(family="Arial", size=12, color="#0073C0")
        )
    )

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 700],
        dtick=100,
        gridcolor='#EAEAEA',
        gridwidth=1,
        showline=False,
        tickfont=dict(size=12)
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=annotations,
    bargap=0.35
)

fig.update_traces(
    textfont=dict(family="Arial", size=12, color='black')
)

output_filename_base = json_path.rsplit('.', 1)[0]
output_filename_png = f"{output_filename_base}.png"

fig.write_image(output_filename_png, scale=2)
print(f"Chart saved to {output_filename_png}")