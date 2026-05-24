import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

fig = go.Figure()

for i, series in enumerate(chart_data["chart_data"]):
    fig.add_trace(go.Bar(
        x=chart_data["categories"],
        y=series["values"],
        name=series["name"],
        marker_color=chart_data["colors"][i],
        text=[f'{v}%' for v in series["values"]],
        textposition='outside',
        cliponaxis=False
    ))

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    xaxis=dict(
        title_text=chart_data["texts"]["x_axis_title"],
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=chart_data["texts"]["y_axis_title"],
        range=[0, 105],
        tickvals=[0, 20, 40, 60, 80, 100],
        ticktext=[f'{v}%' for v in [0, 20, 40, 60, 80, 100]],
        gridcolor='#E0E0E0'
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(t=30, b=150, l=60, r=30),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.35,
            text=chart_data["texts"]["source"],
            showarrow=False,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(
                family="Arial",
                size=10
            )
        )
    ]
)

output_filename = json_file_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart saved as {output_filename}")