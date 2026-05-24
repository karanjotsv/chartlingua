import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

texts = chart_info['texts']
colors = chart_info['colors']
chart_data = chart_info['chart_data']

categories = [item['category'] for item in chart_data]
values_series1 = [item['values'][0] for item in chart_data]
values_series2 = [item['values'][1] for item in chart_data]
annotations_on_bars = [item['annotation'] for item in chart_data]

fig = go.Figure()

# Add traces for the bar chart
fig.add_trace(go.Bar(
    name=texts['legend_series'][0],
    x=categories,
    y=values_series1,
    marker_color=colors[0]
))

fig.add_trace(go.Bar(
    name=texts['legend_series'][1],
    x=categories,
    y=values_series2,
    marker_color=colors[1],
    text=annotations_on_bars,
    textposition='outside',
    textfont=dict(color='black', size=11),
    cliponaxis=False
))

# Update layout
fig.update_layout(
    font_family="Arial",
    title=dict(
        text=f"<b>{texts['title']}</b>",
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 35],
        tickprefix='$',
        gridcolor='#dddddd',
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    xaxis=dict(
        showgrid=False,
        showline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=0.9,
        xanchor='center',
        x=0.6,
        bgcolor='rgba(0,0,0,0)',
        borderwidth=0,
        font=dict(size=11)
    ),
    barmode='group',
    bargap=0.3,
    bargroupgap=0.05,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(t=80, b=100, l=60, r=20)
)

# Add dotted line under the title
fig.add_shape(
    type="line",
    xref="paper", yref="paper",
    x0=0, y0=0.92, x1=1, y1=0.92,
    line=dict(color="black", width=1, dash="dot")
)

# Add source text annotation
fig.add_annotation(
    text=texts['source'],
    xref="paper", yref="paper",
    x=0, y=-0.2,
    showarrow=False,
    xanchor='left',
    yanchor='top',
    align='left',
    font=dict(size=10)
)

# Add arrow annotation
fig.add_annotation(
    x=categories[0],
    y=values_series2[0],
    text=texts['annotation_text'],
    showarrow=True,
    arrowhead=6,
    arrowsize=0.7,
    arrowwidth=1,
    arrowcolor='#555555',
    ax=-70,
    ay=-60,
    align='left',
    font=dict(size=11)
)

# Generate and save the image
output_path = json_path.with_suffix(".png")
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")