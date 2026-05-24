import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=[str(y) for y in y_values],
    textposition='outside',
    textfont=dict(color='black', size=12),
    cliponaxis=False
))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0.99, y=-0.15,
            xanchor="right", yanchor="top",
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="grey")
        )
    )
if texts.get('note'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0.01, y=-0.15,
            xanchor="left", yanchor="top",
            text=texts['note'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#0073e5")
        )
    )

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='rgb(248, 248, 252)',
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 1500],
        dtick=250,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        tickvals=x_values,
        tickfont=dict(size=12),
        showgrid=False
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=annotations
)

base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")