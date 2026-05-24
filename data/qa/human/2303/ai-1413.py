import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['values'],
        name=series['name'],
        marker_color=colors[i],
        text=[f'{v}%' for v in series['values']],
        textposition='inside',
        textfont=dict(
            family='Arial',
            size=16,
            color='white' if i < 2 else 'black', # White for dark bars, black for light one
            weight='bold'
        ),
        insidetextanchor='middle'
    ))

fig.add_vline(x=0.5, line_width=20, line_color="white", layer="below")

fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12),
        domain=[0, 1]
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 125],
        tickvals=[0, 25, 50, 75, 100, 125],
        ticktext=[f'{v}%' for v in [0, 25, 50, 75, 100, 125]],
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dot',
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=40, b=150),
    annotations=[
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.35,
            xanchor='right',
            yanchor='bottom'
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")