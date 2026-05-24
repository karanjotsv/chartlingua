import sys
import json
import os
import plotly.graph_objects as go

# Ensure a static image export backend like 'kaleido' is installed.
# e.g., pip install kaleido

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (json.JSONDecodeError, UnicodeDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0],
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12)
))

title_text = ""
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

annotations = []
if texts.get('source'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0.99, y=-0.12,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        align='right',
        font=dict(size=10, color='grey')
    ))

if texts.get('additional_info'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0.01, y=-0.12,
        xanchor='left', yanchor='top',
        text=f'<span style="color:#0073e5; font-weight:bold;">ⓘ</span> {texts["additional_info"]}',
        showarrow=False,
        align='left',
        font=dict(size=12, color='#0073e5')
    ))

fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.05,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12),
    showlegend=False,
    plot_bgcolor='white',
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        zeroline=False
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        range=[0, 14500]
    ),
    margin=dict(l=120, r=80, t=50, b=100),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2, width=800, height=800)
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)

print(f"Chart successfully saved to {output_filename}")