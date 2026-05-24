import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from command-line argument ---
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- 2. Extract data and texts ---
data = config.get('chart_data', {})
texts = config.get('texts', {})
colors = config.get('colors', [])
x_values = data.get('x', [])
series_data = data.get('series', [])

# --- 3. Create the figure ---
fig = go.Figure()

# --- 4. Add data traces and line labels ---
for i, series in enumerate(series_data):
    color = colors[i % len(colors)]
    fig.add_trace(go.Scatter(
        x=x_values,
        y=series.get('y', []),
        mode='lines+markers',
        name=series.get('name', ''),
        line=dict(color=color, width=2),
        marker=dict(color=color, size=5),
        showlegend=False
    ))
    
    # Add annotation for the series name at the end of the line
    fig.add_annotation(
        x=x_values[-1],
        y=series.get('y', [])[-1],
        text=f"<b>{series.get('name', '')}</b>",
        showarrow=False,
        xanchor='left',
        xshift=8,
        font=dict(
            family="Arial",
            size=12,
            color=color
        )
    )

# --- 5. Configure layout ---
title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size:14px; color: #555555;'>{texts.get('subtitle', '')}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=20, color='black')
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickmode='array',
        tickvals=[1995, 1996, 1998, 2000, 2002, 2004, 2006],
        linecolor='lightgrey',
        ticks='outside',
        tickfont=dict(size=14),
        domain=[0, 0.9] # Leave space on the right for labels
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='#e0e0e0',
        zeroline=False,
        range=[0, 1600000],
        tickvals=[0, 200000, 400000, 600000, 800000, 1000000, 1200000, 1400000],
        ticktext=["0", "200,000", "400,000", "600,000", "800,000", "1 million", "1.2 million", "1.4 million"],
        tickfont=dict(size=14)
    ),
    margin=dict(l=60, r=10, t=110, b=80),
    showlegend=False
)

# --- 6. Add source and note annotations ---
fig.add_annotation(
    text=texts.get('source', ''),
    showarrow=False,
    xref='paper', yref='paper',
    x=0.0, y=-0.1,
    xanchor='left', yanchor='top',
    font=dict(family="Arial", size=11, color='grey')
)

fig.add_annotation(
    text=texts.get('note', ''),
    showarrow=False,
    xref='paper', yref='paper',
    x=1.0, y=-0.1,
    xanchor='right', yanchor='top',
    font=dict(family="Arial", size=11, color='grey')
)

# --- 7. Save the output image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")