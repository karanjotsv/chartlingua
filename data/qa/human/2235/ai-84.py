import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
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

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = data['categories']
series_data = data['series']

fig = go.Figure()

for i, series in enumerate(series_data):
    # Format text labels to show integers without decimal points and make them bold
    text_labels = [f'<b>{v:.1f}</b>' if v % 1 != 0 and v != 0 else f'<b>{int(v)}</b>' for v in series['values']]
    
    # Handle the 0.1 case which should be formatted as 0.1
    for j, val in enumerate(series['values']):
        if val == 0.1:
            text_labels[j] = '<b>0.1</b>'
        elif val == 0:
            text_labels[j] = '<b>0</b>'
            
    fig.add_trace(go.Bar(
        x=categories,
        y=series['values'],
        name=series['name'],
        marker_color=colors[i],
        text=text_labels,
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False
    ))

fig.update_layout(
    barmode='group',
    bargap=0.2,
    bargroupgap=0.1,
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=40, b=120),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        categoryorder='array',
        categoryarray=categories,
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 60],
        showgrid=True,
        gridcolor='#e0e0e0'
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            align='right'
        )
    ]
)

filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")