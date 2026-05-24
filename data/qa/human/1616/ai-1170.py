import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except Exception as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines+markers',
        line=dict(color=color, width=2),
        marker=dict(color=color, size=5),
        hoverinfo='none'
    ))

    fig.add_annotation(
        x=series.get('x')[-1],
        y=series.get('y')[-1],
        text=series.get('name'),
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=8,
        font=dict(
            family="Arial",
            size=12,
            color=color
        )
    )

title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size: 14px; color: #555555;'>{texts.get('subtitle', '')}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickmode='array',
        tickvals=[1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012],
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        tickprefix='$',
        tickformat=',.0f',
        range=[0, 60000],
        tickfont=dict(size=12)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="#333333"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=70, r=150, t=120, b=80),
    width=900,
    height=600
)

fig.add_annotation(
    text=texts.get('source', ''),
    xref="paper", yref="paper",
    x=0, y=-0.15,
    showarrow=False,
    xanchor='left',
    yanchor='top',
    align='left',
    font=dict(size=10, color='#555555')
)

if texts.get('note'):
    fig.add_annotation(
        text=texts.get('note', ''),
        xref="paper", yref="paper",
        x=1, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=10, color='#555555')
    )

output_filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_path = f"{output_filename_base}.png"

try:
    fig.write_image(output_path, scale=2)
    print(f"Chart saved successfully to {output_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)