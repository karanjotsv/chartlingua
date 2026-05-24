import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

filename_base = json_path.stem

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']

fig = make_subplots(
    rows=2,
    cols=1,
    specs=[[{'type': 'domain'}], [{'type': 'domain'}]],
    vertical_spacing=0.2
)

# Add first pie chart
fig.add_trace(go.Pie(
    labels=chart_data[0]['labels'],
    values=chart_data[0]['values'],
    marker_colors=chart_data[0]['colors'],
    name=chart_data[0]['title'],
    hole=0.0
), row=1, col=1)

# Add second pie chart
fig.add_trace(go.Pie(
    labels=chart_data[1]['labels'],
    values=chart_data[1]['values'],
    marker_colors=chart_data[1]['colors'],
    name=chart_data[1]['title'],
    hole=0.0
), row=2, col=1)

fig.update_traces(
    textposition='outside',
    texttemplate='%{label}<br>%{value}%',
    sort=False,
    pull=0.03,
    textfont_size=14,
    hoverinfo='none'
)

# With vertical_spacing=0.2, top pie domain y=[0.6, 1], bottom y=[0, 0.4]. Gap is [0.4, 0.6].
fig.update_layout(
    height=900,
    width=600,
    showlegend=False,
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(t=20, b=120, l=40, r=40),
    annotations=[
        dict(
            text=chart_data[0]['title'],
            x=0.5,
            y=0.55,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, family="Arial")
        ),
        dict(
            text=chart_data[1]['title'],
            x=0.5,
            y=-0.02, # Positioned below the second pie, requires bottom margin
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, family="Arial"),
            align="center"
        )
    ],
    shapes=[
        dict(
            type='line',
            x0=0.1,
            x1=0.9,
            y0=0.5,
            y1=0.5,
            xref='paper',
            yref='paper',
            line=dict(color='black', width=1)
        )
    ]
)

fig.write_image(f"{filename_base}.png", scale=2)
print(f"Chart saved to {filename_base}.png")