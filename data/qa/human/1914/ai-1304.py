import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
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
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#2573CF',
    text=values,
    texttemplate='%{y:.1f}%',
    textposition='outside',
    cliponaxis=False
))

title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    if title_text:
        title_text += "<br>"
    title_text += f'<sub>{texts["subtitle"]}</sub>'

annotations = []
if texts.get("source"):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0.99, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts["source"],
            showarrow=False,
            font=dict(family="Arial", size=12, color="grey")
        )
    )

fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_font=dict(family="Arial", size=18, color='black'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    xaxis=dict(
        showline=False,
        showgrid=False,
        ticks='outside',
        ticklen=5,
        tickcolor='black'
    ),
    yaxis=dict(
        range=[-10, 35],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='solid',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=2,
        ticksuffix='%'
    ),
    annotations=annotations
)

fig.update_traces(
    textfont=dict(family="Arial", size=12, color='black')
)

output_filename = json_path.rsplit('.', 1)[0] + '.png'
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")