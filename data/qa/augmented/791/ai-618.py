import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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

data = chart_info['chart_data']
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=chart_info['colors'][0]),
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        title=chart_info['texts']['x_axis_title'],
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dash',
        zeroline=False,
        ticks='outside',
        tickmode='linear',
        dtick=25,
        autorange=True
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        ticks=''
    ),
    showlegend=False,
    margin=dict(l=80, r=80, t=50, b=100),
    annotations=[
        dict(
            text=chart_info['texts']['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            align='right'
        )
    ]
)

output_filename = json_path.rsplit('.', 1)[0] + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")