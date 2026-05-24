import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

texts = chart_info['texts']
chart_data = chart_info['chart_data']
colors = chart_info['colors']

fig = go.Figure()

chart_configs = [
    {  # Top Companies
        "domain": {'x': [0.52, 0.82], 'y': [0.55, 0.95]},
        "title_pos": {'x': 0.67, 'y': 0.98},
        "legend_pos": {'x': 0.85, 'y_start': 0.9, 'y_step': 0.06}
    },
    {  # Annual Salary
        "domain": {'x': [0.0, 0.3], 'y': [0.0, 0.4]},
        "title_pos": {'x': 0.15, 'y': 0.48},
        "legend_pos": {'x': 0.33, 'y_start': 0.4, 'y_step': 0.06}
    },
    {  # Titles
        "domain": {'x': [0.52, 0.82], 'y': [0.0, 0.4]},
        "title_pos": {'x': 0.67, 'y': 0.48},
        "legend_pos": {'x': 0.85, 'y_start': 0.4, 'y_step': 0.06}
    }
]

annotations = []

for i, chart in enumerate(chart_data):
    config = chart_configs[i]
    
    max_val = max(chart['values'])
    max_idx = chart['values'].index(max_val)
    pull_values = [0.1 if j == max_idx else 0 for j in range(len(chart['values']))]

    fig.add_trace(go.Pie(
        labels=chart['labels'],
        values=chart['values'],
        domain=config['domain'],
        marker_colors=colors,
        pull=pull_values,
        sort=False,
        showlegend=False,
        textinfo='none',
        hoverinfo='label+percent',
        name=''
    ))

    annotations.append(dict(
        text=f"<b>{chart['title']}</b>",
        x=config['title_pos']['x'],
        y=config['title_pos']['y'],
        xref='paper',
        yref='paper',
        showarrow=False,
        font=dict(size=16),
        xanchor='center',
        yanchor='bottom'
    ))

    for j, label in enumerate(chart['labels']):
        annotations.append(dict(
            text=f"<span style='color:{colors[j]};'>&#9632;</span> {label}",
            x=config['legend_pos']['x'],
            y=config['legend_pos']['y_start'] - j * config['legend_pos']['y_step'],
            xref='paper',
            yref='paper',
            showarrow=False,
            xanchor='left',
            yanchor='top',
            align='left'
        ))

main_title_text = (
    f"<span style='font-size: 24px;'><b>{texts['main_title']}</b></span>"
    f"<br><span style='font-size: 16px;'>{texts['subtitle']}</span>"
)
annotations.append(dict(
    text=main_title_text,
    x=0.03,
    y=0.75,
    xref='paper',
    yref='paper',
    showarrow=False,
    xanchor='left',
    yanchor='middle',
    align='left'
))

fig.update_layout(
    annotations=annotations,
    margin=dict(l=20, r=20, t=40, b=20),
    font=dict(family="Arial"),
    width=1100,
    height=700,
    plot_bgcolor='white',
    paper_bgcolor='white'
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")