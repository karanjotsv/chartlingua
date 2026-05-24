import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

fig = go.Figure()

for i, series in enumerate(chart_info["chart_data"]):
    fig.add_trace(go.Bar(
        x=chart_info["categories"],
        y=series["y"],
        name=series["name"],
        marker_color=chart_info["colors"][i],
        text=series["text"],
        textposition='inside',
        textfont=dict(color='white', size=14, family='Arial'),
        insidetextanchor='middle'
    ))

fig.update_layout(
    barmode='stack',
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, b=150, t=50),
    xaxis=dict(
        title_text=chart_info["texts"]["x_axis_title"],
        categoryorder='array',
        categoryarray=chart_info["categories"],
        tickfont=dict(size=12),
        showgrid=False,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=chart_info["texts"]["y_axis_title"],
        range=[0, 60],
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.35,
        xanchor='center',
        x=0.5,
        font=dict(size=12)
    ),
    annotations=[
        dict(
            text=chart_info["texts"]["source"],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.45,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

output_filename = pathlib.Path(json_path).stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")