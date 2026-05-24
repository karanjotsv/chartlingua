import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        text=series.get('text'),
        textposition='inside',
        textfont=dict(color='white', family="Arial"),
        marker_color=colors[i],
        error_y=series.get('error_y')
    ))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

source_text_parts = []
if texts.get('source'):
    source_text_parts.append(texts.get('source'))
if texts.get('note'):
    source_text_parts.append(texts.get('note'))
source_note_text = "<br>".join(source_text_parts)

fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showticklabels=False,
        ticks='',
        showline=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='black',
        tickvals=[-200, 0, 200, 400, 600],
        range=[-250, 650]
    ),
    plot_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),
    barmode='group',
    bargap=0.6,
    annotations=[
        dict(
            text=source_note_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ] if source_note_text else [],
    margin=dict(l=60, r=30, t=100, b=100)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")