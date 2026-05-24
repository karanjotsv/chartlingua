import sys
import os
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
num_series = len(texts['legend_labels'])
series_data = [[item['values'][i] for item in chart_data] for i in range(num_series)]

fig = go.Figure()

for i in range(num_series):
    fig.add_trace(go.Bar(
        x=categories,
        y=series_data[i],
        name=texts['legend_labels'][i],
        marker_color=colors[i],
        text=[str(v) for v in series_data[i]],
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False
    ))

fig.update_layout(
    barmode='group',
    title_text=texts['title'] if texts.get('title') else None,
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 125],
        tickvals=[0, 25, 50, 75, 100, 125],
        gridcolor='#E5E5E5',
        showline=False,
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        font=dict(size=12)
    ),
    margin=dict(l=80, r=40, b=120, t=50),
    annotations=[
        dict(
            text=texts['source'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.3,
            xanchor='right',
            yanchor='bottom',
            font=dict(family="Arial", size=12, color='grey')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")