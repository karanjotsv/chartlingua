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
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data to display from top to bottom in the correct order
labels.reverse()
values.reverse()
colors.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=labels,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=[f'{v:,}' for v in values],
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='#333333'
    )
))

title_text = f"<b>{texts['title']}</b><br><span style='font-size: 16px; color: #555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=24)
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dash',
        zeroline=False,
        showline=False,
        showticklabels=True
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        autorange='reversed' # Redundant with reversed data but ensures order
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=260, r=60, t=150, b=80),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            align='left',
            font=dict(size=12, color='#666666')
        ),
        dict(
            text='CC BY',
            showarrow=False,
            xref='paper', yref='paper',
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=12, color='#666666')
        )
    ]
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")