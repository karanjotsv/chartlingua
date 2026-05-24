import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

chart_data = chart_config['chart_data']
x_categories = chart_config['x_categories']
texts = chart_config['texts']
colors = chart_config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=x_categories,
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=[f'{val:.2f}'.rstrip('0').rstrip('.') if isinstance(val, (int, float)) else val for val in series['text']],
        textposition='inside',
        textfont=dict(
            family='Arial, bold',
            size=12,
            color=series['textfont_color']
        ),
        insidetextanchor='middle',
        hovertemplate='%{y}<extra></extra>'
    ))

fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Arial', size=12, color='black'),
    margin=dict(l=80, r=40, t=50, b=120),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        categoryorder='array',
        categoryarray=x_categories,
        showgrid=False,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='black'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 12.5],
        tickvals=[0, 2.5, 5, 7.5, 10, 12.5],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='left',
        x=0,
        traceorder='normal'
    ),
    showlegend=True
)

fig.add_annotation(
    text=texts['source'],
    align='right',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=1,
    y=-0.32,
    xanchor='right',
    yanchor='bottom',
    font=dict(family='Arial', size=12, color='#666666')
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")