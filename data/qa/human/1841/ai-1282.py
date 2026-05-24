import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

output_filename_base = json_file_path.stem

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=colors[i], width=2),
        marker=dict(
            symbol=series.get('marker_symbol', 'circle'),
            color=colors[i],
            size=6,
            line=dict(color='white', width=1)
        ),
        showlegend=False
    ))

annotations = []
annotations.append(
    dict(
        xref="paper", yref="paper",
        x=0.99, y=0.98,
        xanchor='right', yanchor='bottom',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12, color="#555555")
    )
)

for i, series in enumerate(chart_data):
    annotations.append(
        dict(
            x=series['x'][-2],
            y=series['y'][-2],
            xref="x", yref="y",
            text=series['name'],
            showarrow=True,
            font=dict(family="Arial", size=12, color="#000000"),
            align="left",
            arrowhead=0,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor=colors[i],
            ax=50,
            ay=0,
            xanchor='left',
            bgcolor="white",
            borderpad=4
        )
    )

fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=f"<b>{texts['title']}</b><br><span style='font-size:16px;color:#555555;'>{texts['subtitle']}</span>",
        y=0.95, x=0.01,
        xanchor='left', yanchor='top',
        font=dict(size=22)
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='grey',
        linewidth=1,
        tickmode='array',
        tickvals=chart_data[0]['x'],
        ticktext=[str(year) for year in chart_data[0]['x']],
        range=[2009.5, 2020.5]
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='white',
        gridwidth=2,
        zeroline=False,
        range=[3.5, 18],
        dtick=2
    ),
    plot_bgcolor='#EBF4F8',
    paper_bgcolor='white',
    margin=dict(l=40, r=40, t=100, b=40),
    showlegend=False,
    annotations=annotations
)

output_path = f"{output_filename_base}.png"
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")