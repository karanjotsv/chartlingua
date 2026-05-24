import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
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

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
textfont_colors = config.get('textfont_colors', ['black'] * len(chart_data))

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        marker_color=colors[i],
        text=series['y'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=12,
            color=textfont_colors[i]
        ),
        texttemplate='%{y}',
        hoverinfo='none'
    ))

full_title = ""
if texts.get("title"):
    full_title += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    full_title += f'<br><sub>{texts["subtitle"]}</sub>'

fig.update_layout(
    barmode='stack',
    title_text=full_title if full_title else None,
    title_x=0.05,
    title_font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        linewidth=1,
        tickvals=chart_data[0]['x'],
        ticktext=[str(x) for x in chart_data[0]['x']],
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        range=[0, 10.5],
        dtick=2
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(l=80, r=40, t=50, b=150)
)

if texts.get("source"):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.32,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=10)
    )

base_filename = json_path.split('/')[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")