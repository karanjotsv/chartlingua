import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [item['x'] for item in data]
y_values = [item['y'] for item in data]
text_labels = [item['label'] for item in data]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers+text',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=7),
    text=text_labels,
    textposition='top center',
    textfont=dict(
        family='Arial',
        size=12,
        color='#000000'
    ),
    hoverinfo='none'
))

source_text = texts.get('source', '')
note_text = texts.get('note', '')

if note_text:
    note_text = f"<span style='color:{colors[0]};'>{note_text}</span>"

full_source_text = f"{source_text}<br>{note_text}" if source_text and note_text else source_text + note_text

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    width=900,
    height=600,
    margin=dict(l=80, r=40, t=40, b=120),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12, color='#666666')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[14, 16.5],
        dtick=0.5,
        showgrid=True,
        gridcolor='#E5E7EB',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        tickfont=dict(size=12, color='#666666')
    ),
    showlegend=False
)

if full_source_text:
    fig.add_annotation(
        text=full_source_text,
        showarrow=False,
        xref="paper",
        yref="paper",
        x=1.0,
        y=-0.22,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=12, color='#666666')
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart successfully generated and saved as '{output_filename}'")