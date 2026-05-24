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

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = data['categories']
series = data['series']
series_colors = colors['series']
text_colors = colors['text']

fig = go.Figure()

for i, s in enumerate(series):
    # Prepare text labels, replacing None with empty strings
    text_labels = [v if v is not None else '' for v in s['data']]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=s['data'],
        name=s['name'],
        marker_color=series_colors[i],
        text=text_labels,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=12,
            color=text_colors[i]
        ),
        texttemplate='<b>%{text}</b>'
    ))

fig.update_layout(
    barmode='relative',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='#333333'),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 1050],
        tickvals=[0, 200, 400, 600, 800, 1000],
        ticktext=['0', '200', '400', '600', '800', '1 000'],
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    xaxis=dict(
        tickangle=-45,
        showgrid=False,
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.4,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=80, r=40, t=50, b=200),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.5,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(family="Arial", size=12, color='#666666')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")