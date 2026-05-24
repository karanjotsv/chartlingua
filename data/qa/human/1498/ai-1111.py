import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
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

# Plotly plots y-axis categories from bottom to top, so we reverse the lists
# to match the visual order (Vanuatu at the top).
chart_data.reverse()
colors.reverse()

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
labels = [item['label'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    text=labels,
    orientation='h',
    marker_color=colors,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12)
))

title_text = f"<b>{texts['title']}</b><br><span style='font-size: 14px; color: #555;'>{texts['subtitle']}</span>"

fig.update_layout(
    plot_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial", size=12),
    margin=dict(l=100, r=80, t=120, b=80),
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        showticklabels=True,
        tickfont=dict(size=12),
        range=[0, max(values) * 1.15]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        tickfont=dict(size=14)
    ),
    annotations=[
        dict(
            text=texts['source'],
            xref="paper", yref="paper",
            x=0, y=-0.12,
            xanchor='left', yanchor='top',
            showarrow=False,
            font=dict(size=12, color='#7f7f7f')
        ),
        dict(
            text=texts['note'],
            xref="paper", yref="paper",
            x=1, y=-0.12,
            xanchor='right', yanchor='top',
            showarrow=False,
            font=dict(size=12, color='#7f7f7f')
        )
    ]
)

base_filename, _ = os.path.splitext(json_path)
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")