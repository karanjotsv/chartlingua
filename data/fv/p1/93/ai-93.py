import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
filename_base = os.path.splitext(os.path.basename(json_path))[0]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

texts = chart_data['texts']
charts = chart_data['charts']

fig = go.Figure()

# Define layout domains for each chart section
# [x_start, x_end, y_start, y_end]
domains = [
    [0.0, 0.32, 0.65, 0.95],      # 0: Population
    [0.34, 0.66, 0.65, 0.95],     # 1: Median Age
    [0.68, 1.0, 0.65, 0.95],      # 2: DDA Disabled
    [0.0, 0.32, 0.325, 0.625],    # 3: Economic Output
    [0.0, 0.32, 0.0, 0.3],        # 4: Unemployment
    [0.34, 0.66, 0.0, 0.3],        # 5: Weekly Earnings
    [0.68, 1.0, 0.0, 0.3]         # 6: House Prices
]

# --- Chart Titles ---
title_positions = [
    (0.16, 0.98), (0.5, 0.98), (0.84, 0.98),
    (0.16, 0.655),
    (0.16, 0.33), (0.5, 0.33), (0.84, 0.33)
]
chart_titles_data = [
    (charts[0]['title'], charts[0]['color']),
    (charts[1]['title'], charts[1]['color']),
    (charts[2]['title'], charts[2]['title_color']),
    (charts[3]['title'], charts[3]['color']),
    (charts[4]['title'], charts[4]['title_color']),
    (charts[5]['title'], charts[5]['color']),
    (charts[6]['title'], charts[6]['title_color'])
]

for i, (pos, (title, color)) in enumerate(zip(title_positions, chart_titles_data)):
    x, y = pos
    # Title Box
    fig.add_shape(type="rect", xref="paper", yref="paper",
                  x0=x - 0.15, y0=y, x1=x + 0.15, y1=y + 0.04,
                  fillcolor=color, line_width=0)
    # Title Pointer
    fig.add_shape(type="path", xref="paper", yref="paper",
                  path=f"M {x-0.015} {y} L {x} {y-0.02} L {x+0.015} {y} Z",
                  fillcolor=color, line_width=0)
    # Title Text
    fig.add_annotation(xref="paper", yref="paper", x=x, y=y + 0.02,
                       text=title, showarrow=False, font=dict(color="white", size=12, family="Arial"))

# --- Chart 0: Population (Donut) ---
c = charts[0]
d = domains[0]
fig.add_trace(go.Pie(
    values=c['data']['values'],
    hole=0.7,
    marker=dict(colors=[c['color'], '#e0e0e0']),
    domain=dict(x=[d[0], d[1]], y=[d[2], d[3]]),
    textinfo='none', hoverinfo='none', sort=False
))
fig.add_annotation(text=f"<b>{c['annotations']['center_value']}</b>",
                   xref="paper", yref="paper", x=(d[0]+d[1])/2, y=(d[2]+d[3])/2 + 0.01,
                   showarrow=False, font=dict(size=36, family="Arial"))
fig.add_annotation(text=c['annotations']['center_label'],
                   xref="paper", yref="paper", x=(d[0]+d[1])/2, y=(d[2]+d[3])/2 - 0.05,
                   showarrow=False, font=dict(size=12, family="Arial"))
fig.add_annotation(text=c['annotations']['bottom_label'],
                   xref="paper", yref="paper", x=(d[0]+d[1])/2, y=d[2] + 0.05,
                   showarrow=False, font=dict(size=14, family="Arial"))
fig.add_annotation(text=c['note'],
                   xref="paper", yref="paper", x=(d[0]+d[1])/2, y=d[2],
                   showarrow=False, font=dict(size=10, color="gray", family="Arial"))

# --- Chart 1: Median Age (Text) ---
c = charts[1]
d = domains[1]
y_pos = d[3] - 0.03
for item in c['data']:
    if item['label'] == "Wales":
        fig.add_annotation(text=f"<b>{item['label']}</b>",
                           xref="paper", yref="paper", x=d[0], y=y_pos,
                           xanchor='left', showarrow=False, font=dict(size=14, family="Arial"))
        fig.add_annotation(text=f"<b>{item['value']}</b><span style='font-size:14px;color:gray;'> {c['unit']}</span>",
                           xref="paper", yref="paper", x=d[1], y=y_pos,
                           xanchor='right', showarrow=False, font=dict(size=36, family="Arial", color=c['color']))
    else:
        fig.add_annotation(text=item['label'],
                           xref="paper", yref="paper", x=d[0], y=y_pos,
                           xanchor='left', showarrow=False, font=dict(size=14, family="Arial"))
        fig.add_annotation(text=f"{item['value']}<span style='font-size:12px;'> {c['unit']}</span>",
                           xref="paper", yref="paper", x=d[1], y=y_pos,
                           xanchor='right', showarrow=False, font=dict(size=24, family="Arial"))
    y_pos -= 0.05
fig.add_annotation(text=c['note'],
                   xref="paper", yref="paper", x=(d[0]+d[1])/2, y=d[2],
                   showarrow=False, font=dict(size=10, color="gray", family="Arial"))

# --- Chart 2: DDA Disabled (Bar) ---
c = charts[2]
d = domains[2]
categories = [item['category'] for item in c['data']]
values = [item['value'] for item in c['data']]
fig.add_trace(go.Bar(
    x=categories, y=values, marker_color=c['colors'],
    text=[f"{v}{c['unit']}" for v in values], textposition='outside',
    cliponaxis=False, hoverinfo='none',
    xaxis='x2', yaxis='y2'
))
fig.add_annotation(text=c['note'],
                   xref="paper", yref="paper", x=(d[0]+d[1])/2, y=d[2],
                   showarrow=False, font=dict(size=10, color="gray", family="Arial"))

# --- Chart 3: Economic Output (Donut) ---
c = charts[3]
d = domains[3]
fig.add_trace(go.Pie(
    values=c['data']['values'],
    hole=0.7,
    marker=dict(colors=[c['color'], '#e0e0e0']),
    domain=dict(x=[d[0], d[1]], y=[d[2], d[3]]),
    textinfo='none', hoverinfo='none', sort=False
))
fig.add_annotation(text=f"<b>{c['annotations']['center_value']}</b>",
                   xref="paper", yref="paper", x=(d[0]+d[1])/2, y=(d[2]+d[3])/2 + 0.01,
                   showarrow=False, font=dict(size=36, family="Arial"))
fig.add_annotation(text=c['annotations']['center_label'],
                   xref="paper", yref="paper", x=(d[0]+d[1])/2, y=(d[2]+d[3])/2 - 0.05,
                   showarrow=False, font=dict(size=12, family="Arial"))
fig.add_annotation(text=c['annotations']['bottom_label'],
                   xref="paper", yref="paper", x=(d[0]+d[1])/2, y=d[2] + 0.05,
                   showarrow=False, font=dict(size=14, family="Arial"))
fig.add_annotation(text=c['note'],
                   xref="paper", yref="paper", x=(d[0]+d[1])/2, y=d[2],
                   showarrow=False, font=dict(size=10, color="gray", family="Arial"))

# --- Chart 4: Unemployment (Bar) ---
c = charts[4]
d = domains[4]
categories = [item['category'] for item in c['data']]
values = [item['value'] for item in c['data']]
fig.add_trace(go.Bar(
    x=categories, y=values, marker_color=c['colors'],
    text=[f"{v}{c['unit']}" for v in values], textposition='outside',
    cliponaxis=False, hoverinfo='none',
    xaxis='x4', yaxis='y4'
))
fig.add_annotation(text=c['note'],
                   xref="paper", yref="paper", x=(d[0]+d[1])/2, y=d[2],
                   showarrow=False, font=dict(size=10, color="gray", family="Arial"))

# --- Chart 5: Weekly Earnings (Styled Text) ---
c = charts[5]
d = domains[5]
positions = [((d[0]+(d[1]-d[0])*0.25), (d[2]+(d[3]-d[2])*0.75)),
             ((d[0]+(d[1]-d[0])*0.75), (d[2]+(d[3]-d[2])*0.75)),
             ((d[0]+(d[1]-d[0])*0.25), (d[2]+(d[3]-d[2])*0.35)),
             ((d[0]+(d[1]-d[0])*0.75), (d[2]+(d[3]-d[2])*0.35))]
radius = 0.06
for i, item in enumerate(c['data']):
    x, y = positions[i]
    fig.add_shape(type="circle", xref="paper", yref="paper",
                  x0=x-radius, y0=y-radius, x1=x+radius, y1=y+radius,
                  fillcolor=c['color'], line_width=0, opacity=0.8)
    fig.add_annotation(text=item['label'], xref="paper", yref="paper", x=x, y=y+0.025,
                       showarrow=False, font=dict(color="white", size=10, family="Arial"))
    fig.add_annotation(text=f"<b>{item['value']}</b>", xref="paper", yref="paper", x=x, y=y-0.01,
                       showarrow=False, font=dict(color="white", size=20, family="Arial"))
fig.add_annotation(text=c['note'],
                   xref="paper", yref="paper", x=(d[0]+d[1])/2, y=d[2],
                   showarrow=False, font=dict(size=10, color="gray", family="Arial"))

# --- Chart 6: House Prices (Horizontal Bar) ---
c = charts[6]
d = domains[6]
categories = [item['category'] for item in c['data']]
values = [item['value'] for item in c['data']]
text_labels = [item['label'] for item in c['data']]
fig.add_trace(go.Bar(
    y=categories, x=values, orientation='h', marker_color=c['colors'],
    text=text_labels, textposition='outside', hoverinfo='none',
    xaxis='x6', yaxis='y6'
))
fig.add_annotation(text=c['note'],
                   xref="paper", yref="paper", x=(d[0]+d[1])/2, y=d[2],
                   showarrow=False, font=dict(size=10, color="gray", family="Arial"))

# --- Final Layout Updates ---
fig.update_layout(
    height=1100, width=800,
    title=dict(text=f"<b>{texts['title']}</b>", font=dict(size=28, color="#00537d", family="Arial"), x=0.5, y=0.99),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=20, r=20, t=40, b=100),
    font=dict(family="Arial"),
    # Subplot axes
    xaxis2=dict(domain=domains[2][:2], anchor='y2', showticklabels=False, showgrid=False, zeroline=False, showline=False),
    yaxis2=dict(domain=domains[2][2:], anchor='x2', range=[0, max(v['value'] for v in charts[2]['data']) * 1.2], autorange=False, showticklabels=False, showgrid=False, zeroline=False, showline=False),
    xaxis4=dict(domain=domains[4][:2], anchor='y4', showticklabels=False, showgrid=False, zeroline=False, showline=False),
    yaxis4=dict(domain=domains[4][2:], anchor='x4', range=[0, max(v['value'] for v in charts[4]['data']) * 1.2], autorange=False, showticklabels=False, showgrid=False, zeroline=False, showline=False),
    xaxis6=dict(domain=domains[6][:2], anchor='y6', range=[0, max(v['value'] for v in charts[6]['data']) * 1.2], autorange=False, showticklabels=False, showgrid=False, zeroline=False, showline=False),
    yaxis6=dict(domain=domains[6][2:], anchor='x6', autorange="reversed", showticklabels=False, showgrid=False, zeroline=False, showline=False)
)

# --- Footer ---
fig.add_annotation(
    text=f"<b>{texts['source']}</b>",
    xref="paper", yref="paper",
    x=0, y=-0.06,
    xanchor='left', yanchor='bottom',
    showarrow=False,
    font=dict(size=14, family="Arial")
)
fig.add_annotation(
    text=texts['footer'],
    xref="paper", yref="paper",
    x=0, y=-0.08,
    xanchor='left', yanchor='top',
    align='left',
    showarrow=False,
    font=dict(size=10, family="Arial", color="gray")
)

fig.write_image(f"{filename_base}.png", scale=2)