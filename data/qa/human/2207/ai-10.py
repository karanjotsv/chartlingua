import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
series_names = chart_config['series_names']

fig = go.Figure()

categories = [item['category'] for item in data]

for i, series_name in enumerate(series_names):
    values = [item['values'][i] for item in data]
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        name=series_name,
        marker_color=colors[i],
        text=values,
        textposition='outside',
        texttemplate='%{text:.1f}',
        cliponaxis=False
    ))

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=40, t=40, b=150),
    yaxis=dict(
        title=texts['yaxis_title'],
        range=[0, 5],
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        zeroline=False,
        tickvals=[0, 1, 2, 3, 4, 5]
    ),
    xaxis=dict(
        title=texts['xaxis_title'],
        showgrid=False,
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.4,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10, color="#666666")
        )
    ]
)

if texts.get('title') and texts['title']:
    fig.update_layout(
        title_text=f"<b>{texts['title']}</b>" + (f"<br><sub>{texts['subtitle']}</sub>" if texts.get('subtitle') else ""),
        title_x=0.5,
        title_y=0.95,
        title_xanchor='center',
        title_yanchor='top'
    )


base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")