import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}", file=sys.stderr)
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Reverse data for top-to-bottom display in a Plotly horizontal bar chart
categories = [item['category'] for item in data][::-1]
values = [item['value'] for item in data][::-1]
reversed_colors = colors[::-1]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=reversed_colors),
    text=[f"{v}%" for v in values],
    textposition='outside',
    textfont=dict(size=14),
    cliponaxis=False,
    hoverinfo='none'
))

title_text = f"<b style='font-size: 22px;'>{texts['title']}</b><br><span style='font-size: 15px; color: #505050;'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.97,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        ticksuffix='%',
        automargin=True,
        range=[0, max(values) * 1.15]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        autorange=True
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=150, r=40, t=140, b=80),
    showlegend=False,
    annotations=[
        dict(
            text=texts['source'],
            xref="paper", yref="paper",
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            align='left',
            showarrow=False,
            font=dict(size=12, color='#505050')
        )
    ]
)

base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)