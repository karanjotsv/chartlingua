import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
xaxis_labels = chart_info['xaxis_labels']

fig = go.Figure()

for i, series in enumerate(data_series):
    text_position = 'top center' if i == 0 else 'bottom center'
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers+text',
        name=series['name'],
        line=dict(color=colors[i], width=3),
        marker=dict(color=colors[i], size=7, symbol='circle', line=dict(color='white', width=1.5)),
        text=[str(val) for val in series['y']],
        textposition=text_position,
        textfont=dict(family="Arial", size=12, color='#333333'),
        hoverinfo='none'
    ))

fig.add_annotation(
    x=2.5,
    y=78,
    text=texts['series_1_label'],
    showarrow=False,
    font=dict(family="Arial", size=14, color=colors[0]),
    align="center",
    xanchor="center",
    yanchor="bottom"
)

fig.add_annotation(
    x=4.5,
    y=26,
    text=texts['series_2_label'],
    showarrow=False,
    font=dict(family="Arial", size=14, color=colors[1]),
    align="center",
    xanchor="center",
    yanchor="top"
)

fig.update_layout(
    title=dict(
        text=texts['title'],
        y=0.96,
        x=0.03,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=22)
    ),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        showticklabels=True,
        tickvals=xaxis_labels['tickvals'],
        ticktext=xaxis_labels['ticktext'],
        tickfont=dict(family="Arial", size=14, color='black'),
        zeroline=False,
        range=[-0.5, 8.5]
    ),
    yaxis=dict(
        visible=False,
        range=[20, 95]
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=20, r=20, t=110, b=80),
    font=dict(family="Arial")
)

fig.add_annotation(
    text=texts['source'],
    xref="paper", yref="paper",
    x=0.01, y=-0.12,
    showarrow=False,
    align="left",
    xanchor="left",
    yanchor="top",
    font=dict(family="Arial", size=12, color='grey')
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")