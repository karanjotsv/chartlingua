import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = config['chart_data']
texts = config['texts']
colors = config['colors']
series_names = texts['legend_items']

categories = [item['category'] for item in data]
fig = go.Figure()

for i, series_name in enumerate(series_names):
    values = [item.get(series_name, 0) for item in data]
    text_labels = [f'{v}%' for v in values]

    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        name=series_name,
        orientation='h',
        marker_color=colors[i],
        text=text_labels,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', family='Arial', size=12),
        hovertemplate='%{y}: ' + series_name + ' %{x}%<extra></extra>'
    ))

title_text = f"<b>{texts['title']}</b>" if texts.get('title') else ""
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    barmode='stack',
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(text=title_text, x=0.05, y=0.95, xanchor='left'),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=150, r=40, t=40, b=120),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        title_font=dict(size=12),
        ticksuffix='%',
        range=[0, 100.1],
        showgrid=True,
        gridcolor='#dddddd',
        zeroline=False
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        zeroline=False,
        ticks='outside',
        ticklen=5
    )
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=1, y=-0.28,
        showarrow=False,
        align='right',
        xanchor='right',
        font=dict(size=10, color="grey")
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2, width=900, height=800)

print(f"Chart saved to {output_filename}")