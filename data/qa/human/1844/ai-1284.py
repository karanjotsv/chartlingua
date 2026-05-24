import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=colors[i], width=2),
        marker=dict(color=colors[i], size=5),
        connectgaps=False
    ))

annotations = []

# Add series labels as annotations
for i, series in enumerate(chart_data):
    last_x, last_y = None, None
    for x, y in zip(reversed(series['x']), reversed(series['y'])):
        if y is not None:
            last_x, last_y = x, y
            break
    
    if last_x is not None and last_y is not None:
        annotations.append(
            dict(
                x=last_x,
                y=last_y,
                xref='x',
                yref='y',
                text=series['name'],
                showarrow=True,
                arrowhead=0,
                ax=30,
                ay=0,
                font=dict(family="Arial", size=12, color="black"),
                bgcolor="white",
                bordercolor="#cccccc",
                borderwidth=1,
                align="left"
            )
        )

# Add source annotation
annotations.append(
    dict(
        x=1,
        y=1.06,
        xref='paper',
        yref='paper',
        text=texts['source'],
        showarrow=False,
        align='right',
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=12)
    )
)

fig.update_layout(
    title_text=f"<b>{texts['title']}</b><br><span style='font-size: 14px; color: #555555;'>{texts['subtitle']}</span>",
    title_x=0.01,
    title_y=0.95,
    title_font=dict(family="Arial", size=20),
    
    plot_bgcolor='#E6F0F5',
    paper_bgcolor='white',
    
    font=dict(family="Arial", size=12),
    
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        ticks='outside',
        tickmode='array',
        tickvals=[1992, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014]
    ),
    
    yaxis=dict(
        showline=False,
        zeroline=False,
        gridcolor='white',
        gridwidth=1,
        tickformat=".1f",
        range=[0, 0.8]
    ),
    
    showlegend=False,
    
    margin=dict(l=40, r=100, t=100, b=40),
    
    annotations=annotations,
    
    shapes=[
        dict(
            type="line",
            xref="paper",
            yref="paper",
            x0=0,
            y0=1,
            x1=1,
            y1=1,
            line=dict(
                color=colors[1],
                width=2
            )
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")