import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values_series1 = [item['values'][0] for item in chart_data]
values_series2 = [item['values'][1] for item in chart_data]
totals = [item['total'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values_series1,
    name=texts['legend_labels'][0],
    orientation='h',
    marker_color=colors[0]
))

fig.add_trace(go.Bar(
    y=categories,
    x=values_series2,
    name=texts['legend_labels'][1],
    orientation='h',
    marker_color=colors[1]
))

for i, total in enumerate(totals):
    fig.add_annotation(
        x=total,
        y=categories[i],
        text=f"{total}",
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=5,
        font=dict(family="Arial", size=12)
    )

fig.update_layout(
    barmode='stack',
    template='plotly_white',
    font=dict(family="Arial", size=12),
    margin=dict(l=250, r=60, t=30, b=100),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    yaxis=dict(
        showgrid=False,
        title_text=texts['y_axis_title'] if texts.get('y_axis_title') else ''
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    )
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.35,
        xanchor='right',
        yanchor='bottom',
        font=dict(family="Arial", size=10, color='grey')
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as {output_filename}")