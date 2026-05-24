import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', [])

categories = [item.get('category') for item in chart_data]
values = [item.get('value') for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    texttemplate='%{text:d}',
    marker_color=colors[0] if colors else '#2A75D0',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(family="Arial"),
    xaxis_title=texts.get('xaxis_title'),
    yaxis_title=texts.get('yaxis_title'),
    yaxis=dict(
        range=[0, 6000],
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        tickvals=[0, 1000, 2000, 3000, 4000, 5000, 6000],
        ticktext=['0', '1 000', '2 000', '3 000', '4 000', '5 000', '6 000']
    ),
    xaxis=dict(
        showgrid=False,
        categoryorder='array',
        categoryarray=categories
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=40, b=120)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=1, y=-0.2,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=12)
    )

output_filename = json_path.rsplit('.', 1)[0] + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")