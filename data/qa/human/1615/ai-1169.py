import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

fig = go.Figure()

# Add the main trace without showing it in the legend
main_series = chart_data[0]
main_color = colors[0]
fig.add_trace(go.Scatter(
    x=main_series['x'],
    y=main_series['y'],
    name=main_series['name'],
    mode='lines+markers',
    line=dict(color=main_color),
    marker=dict(color=main_color, size=5),
    showlegend=False
))

# Add the rest of the traces to appear in the legend
for i in range(1, len(chart_data)):
    series = chart_data[i]
    color = colors[i]
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=color),
        marker=dict(color=color, size=5)
    ))

# Define y-axis ticks
y_tick_vals = [0, 2, 4, 6, 8, 10, 12, 14]
y_tick_text = ['0 ha'] + [f'{val} million ha' for val in y_tick_vals[1:]]

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.01,
        y=0.96,
        xanchor='left',
        yanchor='top',
        font=dict(size=24, color='#333333')
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickvals=[1997, 2000, 2005, 2010, 2015, 2017],
        showgrid=False,
        showline=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 15],
        tickvals=y_tick_vals,
        ticktext=y_tick_text,
        showgrid=True,
        gridcolor='#e5e5e5',
        griddash='dash',
        showline=False,
        zeroline=False
    ),
    font=dict(
        family="Arial",
        size=14,
        color="#333333"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=True,
    legend=dict(
        x=0.98,
        y=0.3,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255,255,255,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=80, r=200, t=100, b=80),
    annotations=[
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.1,
            xanchor='left', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(size=12, color='#666666')
        ),
        dict(
            x=main_series['x'][-1],
            y=main_series['y'][-1],
            text=main_series['name'],
            showarrow=False,
            xanchor='left',
            xshift=10,
            font=dict(color=main_color, size=14)
        )
    ]
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")