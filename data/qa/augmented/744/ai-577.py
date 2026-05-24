import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Format data labels with a space as a thousands separator, matching the original chart
formatted_text_labels = [f'{v:,}'.replace(',', ' ') for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=formatted_text_labels,
    textposition='outside',
    texttemplate='%{text}',
    textfont=dict(size=12, color='black'),
    cliponaxis=False
))

title_text = ''
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f'<br><sup>{texts["subtitle"]}</sup>'

fig.update_layout(
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        linewidth=1,
        categoryorder='array',
        categoryarray=categories
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 125000],
        dtick=25000,
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        tickformat=' ',  # Use space as thousands separator for axis labels
        showline=False
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(t=40, b=100, l=80, r=40),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12, color='grey')
        )
    ]
)

output_filename = json_file_path.stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")