import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script.py> <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

series = chart_data[0]
fig.add_trace(go.Scatter(
    x=series['x'],
    y=series['y'],
    mode='lines+markers+text',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=8),
    text=series['text'],
    textposition='top center',
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    ),
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="#000000"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False,
        ticks='outside',
        range=[7, 28.5],
        tickvals=[7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5],
        ticktext=['7.5%', '10%', '12.5%', '15%', '17.5%', '20%', '22.5%', '25%', '27.5%']
    ),
    margin=dict(l=80, r=40, t=40, b=100)
)

annotations = []
if texts.get('additional_info'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.22,
            xanchor='left', yanchor='top',
            text=texts['additional_info'],
            showarrow=False,
            font=dict(family="Arial", size=12, color=colors[0])
        )
    )

source_text = texts.get('source', '')
note_text = texts.get('note', '')

if source_text or note_text:
    source_note_html = f"{source_text} &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:{colors[0]}'>{note_text}</span>"
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.22,
            xanchor='right', yanchor='top',
            text=source_note_html,
            showarrow=False,
            font=dict(family="Arial", size=12, color="#6c757d")
        )
    )

fig.update_layout(annotations=annotations)

base_filename = json_path.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")