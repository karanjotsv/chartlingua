import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

for i, series in enumerate(chart_data['chart_data']['series']):
    fig.add_trace(go.Bar(
        x=chart_data['chart_data']['categories'],
        y=series['data'],
        name=series['name'],
        marker_color=chart_data['colors'][i],
        text=series['data'],
        textposition='outside',
        texttemplate='%{y}',
        cliponaxis=False,
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

fig.update_layout(
    barmode='group',
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    yaxis=dict(
        title=chart_data['texts']['y_axis_title'],
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 65],
        zeroline=False
    ),
    xaxis=dict(
        title=chart_data['texts']['x_axis_title'],
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.3,
        xanchor='center',
        x=0.5
    ),
    margin=dict(t=50, b=150, l=80, r=40),
    annotations=[
        dict(
            text=chart_data['texts']['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.4,
            xanchor='right',
            yanchor='bottom',
            font=dict(
                family="Arial",
                size=12,
                color='#666'
            )
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")