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
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
series_data = [list(series) for series in zip(*[item['values'] for item in chart_data])]

fig = go.Figure()

for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series,
        name=texts.get('legend_labels', [])[i],
        marker_color=colors[i],
        text=series,
        textposition='outside',
        texttemplate='%{text:,}',
        showlegend=False 
    ))
    # Add dummy scatter trace for circular legend markers
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(symbol='circle', color=colors[i], size=10),
        name=texts.get('legend_labels', [])[i],
        showlegend=True
    ))

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(color='#666666'),
        title_text=texts.get('x_axis_title')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        range=[0, 40000],
        tickformat=' ',
        tickfont=dict(color='#666666')
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5,
        itemsizing='constant'
    ),
    margin=dict(l=80, r=40, b=120, t=40),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.3,
            xanchor='right', yanchor='bottom',
            text=texts.get('source'),
            showarrow=False,
            font=dict(size=12, color='#666666')
        )
    ]
)

fig.update_traces(
    textfont=dict(
        family='Arial',
        size=12,
        color='black'
    ),
    cliponaxis=False
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")