import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series_data = chart_data['series']

fig = go.Figure()

for i, s in enumerate(series_data):
    fig.add_trace(go.Bar(
        y=categories,
        x=s['values'],
        name=s['name'],
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(color='white', width=1)
        ),
        text=[f'{v}' for v in s['values']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            color=s['text_color'],
            size=14
        ),
        hoverinfo='none'
    ))

title_text = f"<b>{texts['title']}</b><br><span style='color:#595959; font-size:18px'><i>{texts['subtitle']}</i></span>"
source_text = f"{texts['source']}<br><b>{texts['footer']}</b>"

annotations = []
for s in series_data:
    annotations.append(dict(
        xref='x', yref='paper',
        x=s['legend_x'], y=1.06,
        text=s['name'],
        font=dict(family='Arial', size=14, color=s['legend_color']),
        showarrow=False,
        xanchor='center'
    ))

annotations.append(dict(
    xref='paper', yref='paper',
    x=0, y=-0.22,
    text=source_text,
    align='left',
    showarrow=False,
    xanchor='left',
    yanchor='top',
    font=dict(family='Arial', size=12, color='#808080')
))

fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        y=0.98,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(size=24, family='Arial')
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        range=[0, 101]
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
        autorange='reversed',
        tickfont=dict(size=14, family='Arial')
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=80, r=20, t=140, b=120),
    annotations=annotations
)

base_filename = json_path[:-5] if json_path.endswith('.json') else json_path
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")