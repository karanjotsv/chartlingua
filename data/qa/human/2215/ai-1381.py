import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
text_colors = chart_data['text_colors']

fig = go.Figure()

for i, series in enumerate(data['series']):
    fig.add_trace(go.Bar(
        x=data['categories'],
        y=series['values'],
        name=series['name'],
        marker_color=colors[i],
        text=[f"{v}%" for v in series['values']],
        textposition='inside',
        textfont=dict(
            family="Arial",
            color=text_colors[i]
        ),
        hoverinfo='skip'
    ))

title_text = ""
if texts['title']:
    title_text += texts['title']
if texts['subtitle']:
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Calculate dynamic y-axis range
totals = [sum(series['values'][i] for series in data['series']) for i in range(len(data['categories']))]
max_y = max(totals)
y_range_max = (max_y // 20 + 1) * 20 if max_y > 0 else 20

fig.update_layout(
    barmode='stack',
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=texts['xaxis_title'],
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['yaxis_title'],
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        ticksuffix='%',
        range=[0, y_range_max],
        dtick=20,
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=80, r=40, t=50, b=150),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=10, color='#888888')
        )
    ]
)

output_filename = json_file_path.with_suffix(".png")
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")