import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=[d['category'] for d in chart_info['chart_data']],
    y=[d['value'] for d in chart_info['chart_data']],
    marker=dict(color=chart_info['colors'][0]),
    width=0.6
))

fig.update_layout(
    title=dict(
        text=chart_info['texts']['title'],
        x=0.5,
        y=0.95,
        font=dict(size=28)
    ),
    xaxis=dict(
        title_text=chart_info['texts']['x_axis_title'],
        tickfont=dict(size=14),
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=chart_info['texts']['y_axis_title'],
        range=[0, 60],
        dtick=10,
        tickfont=dict(size=14),
        showgrid=True,
        gridcolor='#cccccc',
        showline=False,
        zeroline=False
    ),
    font=dict(
        family="Arial",
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=100, b=80, l=60, r=40)
)

if '\\' in json_path:
    base_name = json_path.split('\\')[-1]
else:
    base_name = json_path.split('/')[-1]
    
output_filename = base_name.rsplit('.', 1)[0] + '.png'

fig.write_image(output_filename, scale=2)