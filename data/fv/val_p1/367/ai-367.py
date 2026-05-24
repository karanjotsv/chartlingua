import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

output_filename = json_file_path.with_suffix(".png").name

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- 2. Data Extraction ---
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])
categories = [d.get('category', '') for d in chart_data]

# --- 3. Chart Creation ---
fig = go.Figure()

for i, series in enumerate(chart_data):
    text_color = 'white' if series.get('value', 0) < 0 else 'black'
    
    fig.add_trace(go.Bar(
        x=[series.get('category', '')],
        y=[series.get('value')],
        name=series.get('category', ''),
        marker_color=colors[i] if i < len(colors) else None,
        error_y=dict(
            type='data',
            array=[series.get('error')],
            visible=True,
            color='dimgray',
            thickness=1.5
        ),
        text=[f"{series.get('value')}"],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=16,
            color=text_color
        ),
        width=0.6
    ))

# --- 4. Layout and Styling ---
title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.5,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=14,
        color="dimgray"
    ),
    plot_bgcolor='white',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0.0,
        font=dict(size=14),
        traceorder='normal'
    ),
    barmode='group',
    bargap=0.3,
    xaxis=dict(
        categoryorder='array',
        categoryarray=categories,
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        title_font=dict(size=14, color='black'),
        title_standoff=15
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        range=[-250, 650],
        dtick=200,
        title_font=dict(size=14, color='black'),
        title_standoff=10
    ),
    margin=dict(l=70, r=30, t=100, b=80),
)

# --- 5. Source/Note Annotation ---
annotation_text = []
if texts.get("source"):
    annotation_text.append(f"Source: {texts['source']}")
if texts.get("note"):
    annotation_text.append(f"Note: {texts['note']}")

if annotation_text:
    fig.add_annotation(
        text="<br>".join(annotation_text),
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.25,
        xanchor='left',
        yanchor='top',
        font=dict(size=12, color="dimgray")
    )

# --- 6. Output ---
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")