import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
legend_labels = texts['legend_labels']
num_series = len(legend_labels)
series_data = [[item['values'][i] for item in chart_data] for i in range(num_series)]

fig = go.Figure()

for i in range(num_series):
    fig.add_trace(go.Bar(
        y=categories,
        x=series_data[i],
        name=legend_labels[i],
        orientation='h',
        marker_color=colors[i]
    ))

title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_y=0.95,
    font=dict(
        family="Arial",
        size=12
    ),
    barmode='group',
    bargap=0.3,
    bargroupgap=0.1,
    xaxis=dict(
        showgrid=True,
        gridcolor='LightGray',
        zeroline=False,
        title_text=texts['x_axis_title']
    ),
    yaxis=dict(
        showgrid=False,
        title_text=texts['y_axis_title']
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=200, r=20, t=100, b=100)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")