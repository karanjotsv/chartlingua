import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    hoverinfo='none'
))

for category, value in zip(categories, values):
    text_label = f"{value}%"
    x_anchor = 'left' if value >= 0 else 'right'
    x_shift = 6 if value >= 0 else -6
    
    fig.add_annotation(
        x=value,
        y=category,
        text=text_label,
        showarrow=False,
        xanchor=x_anchor,
        xshift=x_shift,
        font=dict(family="Arial", size=12, color="black"),
        align="center"
    )

shapes = []
for i in range(len(categories)):
    if i % 2 != 0:
        shape = go.layout.Shape(
            type="rect",
            xref="paper",
            yref="y",
            x0=0,
            y0=i - 0.5,
            x1=1,
            y1=i + 0.5,
            fillcolor="#f0f0f0",
            layer="below",
            line_width=0,
        )
        shapes.append(shape)

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    shapes=shapes,
    xaxis=dict(
        title=texts['x_axis_title'],
        range=[-50, 35],
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=230, r=45, t=30, b=80),
    showlegend=False,
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.98, y=-0.14,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=10, color='grey')
    )

base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")