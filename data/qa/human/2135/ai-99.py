import sys
import os
import json
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series = chart_data['series']

# --- 2. Create the Figure ---
fig = go.Figure()

# --- 3. Add Traces (Bars) ---
for i, s in enumerate(series):
    # Format text to show integers without decimals, and floats with one decimal place
    bar_texts = [f"<b>{int(v) if v == int(v) else f'{v:.1f}'}</b>" for v in s['data']]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=s['data'],
        name=s['name'],
        marker_color=colors[i],
        text=bar_texts,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', family='Arial', size=14)
    ))

# --- 4. Configure Layout ---
# Combine title and subtitle
title_parts = []
if texts.get('title'):
    title_parts.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle'):
    title_parts.append(texts['subtitle'])
full_title = "<br>".join(title_parts)

# Combine source and note
source_parts = []
if texts.get('source'):
    source_parts.append(texts['source'])
if texts.get('note'):
    source_parts.append(texts['note'])
full_source = "<br>".join(source_parts)

fig.update_layout(
    barmode='stack',
    title_text=full_title,
    title_x=0.05,
    title_xanchor='left',
    xaxis_title_text=texts.get('x_axis_title'),
    yaxis_title_text=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        linecolor='black',
        ticks='outside',
        tickcolor='black'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        range=[0, 501],
        tickvals=[0, 100, 200, 300, 400, 500]
    ),
    margin=dict(l=80, r=40, b=150, t=50)
)

# Add source annotation
if full_source:
    fig.add_annotation(
        text=full_source,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.4,
        xanchor='right',
        yanchor='bottom'
    )

# --- 5. Output Image ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`)")