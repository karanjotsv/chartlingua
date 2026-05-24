import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_filepath = sys.argv[1]

try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_filepath}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_filepath}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
annotation_texts = [d['annotation_text'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors,
    text=annotation_texts,
    textposition='none' # Annotations will be added separately
))

for i in range(len(chart_data)):
    fig.add_annotation(
        x=chart_data[i]['value'],
        y=chart_data[i]['category'],
        text=chart_data[i]['annotation_text'],
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=5,
        font=dict(family="Arial", size=12, color='#333333')
    )

title_text = f"<b>{texts['title']}</b><br><span style='font-size: 15px; color: #555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    title_text=title_text,
    title_x=0.01,
    title_y=0.98,
    title_font_family="Arial",
    title_font_size=24,
    font=dict(family="Arial", size=14, color='#333333'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        ticksuffix='%',
        range=[0, 40],
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        autorange='reversed',
        tickfont=dict(size=14)
    ),
    margin=dict(l=120, r=100, t=120, b=120),
    annotations=[
        dict(
            showarrow=False,
            text=texts['source_note'],
            xref="paper",
            yref="paper",
            x=0,
            y=-0.18,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(family="Arial", size=11, color='#7f7f7f')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_filepath))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")