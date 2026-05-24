import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

chart_data = chart_json['chart_data']
texts = chart_json['texts']
colors = chart_json['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=colors[i], width=3)
    ))

title_text = texts.get('title')
if texts.get('subtitle'):
    title_text = f"{title_text}<br><sub>{texts['subtitle']}</sub>" if title_text else f"<sub>{texts['subtitle']}</sub>"

source_text = ""
if texts.get('source'):
    source_text += texts['source']
if texts.get('note'):
    source_text = f"{source_text}<br>{texts['note']}" if source_text else texts['note']

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left',
        y=0.98,
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_label'),
        showgrid=False,
        linecolor='black',
        linewidth=1,
        ticks='outside',
        mirror=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_label'),
        range=[0, 1600],
        tickmode='linear',
        tick0=0,
        dtick=200,
        showgrid=True,
        gridcolor='#e5e5e5',
        linecolor='black',
        linewidth=1,
        ticks='outside',
        mirror=True,
        zeroline=False,
        tickformat=',.0f'
    ),
    margin=dict(l=60, r=40, t=40, b=80),
)

if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0, y=-0.15,
        showarrow=False,
        xanchor='left',
        yanchor='top',
        align='left'
    )

base_name = json_path.split('/')[-1].split('\\')[-1]
filename_base = base_name.rsplit('.', 1)[0]
output_filename = f"{filename_base}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")