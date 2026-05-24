import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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

fig = go.Figure()

chart_data = config['chart_data']
y_labels = config['texts']['y_axis_labels']
colors = config['colors']
text_colors = config['text_colors']

for i, series in enumerate(chart_data):
    bar_texts = []
    for j, value in enumerate(series['values']):
        if "Total" in y_labels[j]:
            bar_texts.append(f"{value}%" if value > 0 else "")
        else:
            bar_texts.append(str(value) if value > 0 else "")

    fig.add_trace(go.Bar(
        y=y_labels,
        x=series['values'],
        name=series['name'],
        orientation='h',
        marker=dict(color=colors[i], line=dict(width=0)),
        text=bar_texts,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=12,
            color=text_colors[i]
        )
    ))

annotations = []

# Column Headers
y_pos = len(y_labels) - 0.6
total_bar_data = [s['values'][-1] for s in config['chart_data']]
x_positions = [
    total_bar_data[0] / 2,
    total_bar_data[0] + total_bar_data[1] / 2,
    total_bar_data[0] + total_bar_data[1] + total_bar_data[2] / 2
]

for i, label in enumerate(config['texts']['x_axis_labels']):
    annotations.append(
        go.layout.Annotation(
            text=label,
            x=x_positions[i],
            y=y_pos,
            xref='x',
            yref='y',
            showarrow=False,
            font=dict(family="Arial", size=12, color="#555555")
        )
    )

# Source and Footer Annotations
annotations.append(go.layout.Annotation(
    text=config['texts']['source_note'],
    xref="paper", yref="paper",
    x=0, y=-0.22,
    xanchor='left', yanchor='top',
    align='left',
    showarrow=False,
    font=dict(family="Arial", size=11, color="#555555")
))

annotations.append(go.layout.Annotation(
    text=f"<b>{config['texts']['footer']}</b>",
    xref="paper", yref="paper",
    x=0, y=-0.35,
    xanchor='left', yanchor='top',
    align='left',
    showarrow=False,
    font=dict(family="Arial", size=12, color="black")
))

fig.update_layout(
    barmode='stack',
    title=dict(
        text=f"<b>{config['texts']['title']}</b><br><span style='font-size: 14px; color: #555555;'>{config['texts']['subtitle']}</span>",
        x=0.01,
        xanchor='left',
        yanchor='top',
        y=0.96
    ),
    xaxis=dict(
        visible=False,
        range=[0, 101]
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        tickfont=dict(family="Arial", size=12)
    ),
    font=dict(family="Arial"),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=220, r=20, t=120, b=180),
    annotations=annotations
)

output_filename = json_path.rsplit('.', 1)[0] + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")