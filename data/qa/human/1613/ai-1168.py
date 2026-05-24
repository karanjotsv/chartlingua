import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(data):
    mode = 'lines+markers' if len(series['x']) > 1 else 'markers'
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode=mode,
        line=dict(color=colors[i], width=2.5),
        marker=dict(color=colors[i], size=8 if mode == 'markers' else 6),
        hoverinfo='skip'
    ))

title_text = f"<span style='font-size: 24px;'><b>{texts['title']}</b></span><br><span style='font-size: 16px; color: #555555;'>{texts['subtitle']}</span>"
source_text = f"<span style='font-size: 12px; color: #7f7f7f;'>{texts['source']}</span>"
note_text = f"<span style='font-size: 12px; color: #7f7f7f;'>{texts['note']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showline=False,
        showgrid=False,
        tickvals=[2003, 2004, 2005, 2006, 2007],
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showline=False,
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dash',
        ticksuffix='%',
        range=[0, 3.5],
        dtick=0.5,
        tickfont=dict(size=14)
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=40, r=120, t=120, b=80)
)

annotations = [
    dict(
        text=source_text,
        showarrow=False,
        xref="paper", yref="paper",
        x=0, y=-0.16,
        xanchor='left', yanchor='top',
        align='left'
    ),
    dict(
        text=note_text,
        showarrow=False,
        xref="paper", yref="paper",
        x=1, y=-0.16,
        xanchor='right', yanchor='top',
        align='right'
    ),
    dict(
        x=data[0]['x'][-1],
        y=data[0]['y'][-1],
        text=data[0]['name'],
        font=dict(color=colors[0], size=16),
        showarrow=False,
        xanchor='left',
        xshift=10
    ),
    dict(
        x=data[1]['x'][-1],
        y=data[1]['y'][-1],
        text=data[1]['name'],
        font=dict(color=colors[1], size=16),
        showarrow=False,
        xanchor='left',
        xshift=15
    )
]

fig.update_layout(annotations=annotations)

output_filename_base = pathlib.Path(json_path).stem
fig.write_image(f"{output_filename_base}.png", scale=2)

print(f"Chart saved to {output_filename_base}.png")