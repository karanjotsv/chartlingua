import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
num_series = len(colors)
series_values = [[item['values'][i] for item in chart_data] for i in range(num_series)]

fig = go.Figure()

# Add traces based on data
fig.add_trace(go.Scatter(
    x=categories,
    y=series_values[0],
    name=texts['legend_labels'][0],
    mode='lines+markers',
    line=dict(color=colors[0]),
    marker=dict(
        symbol='circle-open',
        color=colors[0],
        size=8,
        line=dict(width=1.5)
    )
))

fig.add_trace(go.Scatter(
    x=categories,
    y=series_values[1],
    name=texts['legend_labels'][1],
    mode='lines',
    line=dict(color=colors[1])
))


fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        tickmode='array',
        tickvals=categories[::2],
        ticktext=texts['x_axis_labels'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        type='log',
        tickvals=[10, 100, 1000, 2000, 3000],
        ticktext=['10.0', '100.0', '1000.0', '2000.0', '3000.0'],
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=80, r=40, t=80, b=150)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2, width=800, height=550)

print(f"Chart saved to {output_image_path}")