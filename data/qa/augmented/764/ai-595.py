import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

fig = go.Figure()

for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers+text',
        name=series.get('name', ''),
        line=dict(color=colors['series_colors'][i], width=2),
        marker=dict(color=colors['series_colors'][i], size=7),
        text=[f"{val:.2f}" if isinstance(val, float) and val % 1 != 0 else str(int(val)) for val in series['y']],
        textposition=series['text_positions'],
        textfont=dict(
            family="Arial",
            size=11,
            color=colors['font_color']
        ),
        hoverinfo='none'
    ))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color=colors['font_color'])
        )
    )

fig.update_layout(
    font=dict(family="Arial", size=12, color=colors['font_color']),
    plot_bgcolor=colors['background_color'],
    paper_bgcolor=colors['background_color'],
    showlegend=False,
    margin=dict(l=80, r=40, b=100, t=40),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickmode='array',
        tickvals=texts['x_tick_values'],
        ticktext=texts['x_tick_labels'],
        showgrid=False,
        zeroline=False,
        showline=False,
        range=[min(texts['x_tick_values']) - 1, max(texts['x_tick_values']) + 1]
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 620],
        dtick=100,
        gridcolor=colors['grid_color'],
        zeroline=False,
        showline=False
    ),
    annotations=annotations
)

output_path = json_path.with_suffix('.png')
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")