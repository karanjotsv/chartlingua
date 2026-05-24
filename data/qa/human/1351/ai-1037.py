import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    print("Usage: python script.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
base_name = pathlib.Path(json_path).stem
output_filename = f"{base_name}.png"

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Reverse data for horizontal bar chart in Plotly (top-to-bottom display)
chart_data.reverse()
colors.reverse()

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
annotations_text = [item['annotation'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors, line_width=0),
    text=annotations_text,
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='#333333'),
    cliponaxis=False,
    hoverinfo='none'
))

fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b><br><span style='font-size: 14px; color: #555555;'>{texts.get('subtitle', '')}</span>",
        font=dict(family='Arial', size=24, color='#333333'),
        x=0.01,
        xanchor='left',
        y=0.98,
        yanchor='top'
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        showticklabels=True
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        autorange="reversed" 
    ),
    font=dict(family='Arial', size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=40, t=120, b=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            font=dict(family='Arial', size=12, color='#666666')
        ),
        dict(
            text=texts.get('note', ''),
            showarrow=False,
            xref='paper', yref='paper',
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            font=dict(family='Arial', size=12, color='#666666')
        )
    ]
)

fig.write_image(output_filename, scale=2, width=900, height=600)

print(f"Chart saved to {output_filename}")