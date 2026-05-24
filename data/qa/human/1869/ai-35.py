import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <path_to_json_file>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}", file=sys.stderr)
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        mode='lines+markers+text',
        line=dict(color=colors['series'][i % len(colors['series'])], width=2.5),
        marker=dict(color=colors['series'][i % len(colors['series'])], size=7),
        text=[f"{y:.1f}%".replace('.0%', '%') for y in series['y']],
        textposition='top center',
        textfont=dict(family="Arial", size=12, color='black'),
        hoverinfo='none'
    ))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=True,
        gridcolor='#f0f0f0',
        zeroline=False,
        showline=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 3],
        dtick=0.5,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False
    ),
    margin=dict(l=60, r=40, t=40, b=120),
    showlegend=False
)

annotations = []
if texts.get('note_left'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.25,
            xanchor='left', yanchor='top',
            text=texts['note_left'],
            showarrow=False,
            font=dict(family="Arial", size=12, color=colors.get('link', '#000000'))
        )
    )
if texts.get('source'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.25,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color=colors.get('source', '#808080'))
        )
    )
if texts.get('note_right'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.32,
            xanchor='right', yanchor='top',
            text=texts['note_right'],
            showarrow=False,
            font=dict(family="Arial", size=12, color=colors.get('link', '#000000'))
        )
    )

fig.update_layout(annotations=annotations)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")