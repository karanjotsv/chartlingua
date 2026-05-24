import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
num_series = len(chart_data[0]['values']) if chart_data else 0
data_series = [[item['values'][i] for item in chart_data] for i in range(num_series)]

fig = go.Figure()

for i in range(num_series):
    fig.add_trace(go.Bar(
        y=categories,
        x=data_series[i],
        name=texts.get('legend_labels', [])[i],
        orientation='h',
        marker_color=colors[i]
    ))

title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title = f"<b>{title_text}</b>"
    if subtitle_text:
        full_title += f"<br><sub>{subtitle_text}</sub>"

source_text = texts.get('source', '')
note_text = texts.get('note', '')

# In the original image, "Show source" is blue, resembling a hyperlink.
if note_text:
    note_text = f"<span style='color:{colors[0]}'>{note_text}</span>"

combined_source_note = f"{note_text}&nbsp;&nbsp;&nbsp;{source_text}" if note_text and source_text else source_text or note_text

fig.update_layout(
    barmode='group',
    bargap=0.25,
    bargroupgap=0.1,
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False,
        range=[0, 40]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', ''),
        showgrid=False,
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=200, r=40, t=60, b=120),
    annotations=[
        dict(
            text=combined_source_note,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10)
        )
    ]
)

output_filename = json_path.with_suffix(".png").name
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")