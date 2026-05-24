import sys
import json
import math
import os
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
        sys.exit(1)
    
    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_spec = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}", file=sys.stderr)
        sys.exit(1)

    chart_data = chart_spec['chart_data']
    texts = chart_spec['texts']
    colors = chart_spec['colors']

    labels = [d['label'] for d in chart_data]
    values = [d['value'] for d in chart_data]
    display_values = [d['display_value'] for d in chart_data]
    hover_labels = [d['category'] for d in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='white', width=1)),
        hoverinfo='label+percent',
        hovertemplate='%{customdata}: %{percent}<extra></extra>',
        customdata=hover_labels,
        textinfo='none',
        textposition='outside',
        sort=False,
        direction='clockwise',
        rotation=90
    ))

    annotations = []
    total_value = sum(values)
    if total_value > 0:
        cumulative_angle_deg = 90
        radius = 0.45
        
        for i, value in enumerate(values):
            slice_angle_deg = (value / total_value) * 360
            if display_values[i] is not None:
                mid_angle_deg = cumulative_angle_deg - (slice_angle_deg / 2)
                mid_angle_rad = math.radians(mid_angle_deg)
                
                # Center of pie is at (0.5, 0.5) in paper coordinates
                x_pos = 0.5 + radius * math.cos(mid_angle_rad)
                y_pos = 0.5 + radius * math.sin(mid_angle_rad)
                
                annotations.append(
                    go.layout.Annotation(
                        x=x_pos, y=y_pos,
                        text=str(display_values[i]),
                        showarrow=False,
                        font=dict(family="Arial", size=14, color="white"),
                        xref="paper", yref="paper"
                    )
                )
            cumulative_angle_deg -= slice_angle_deg

    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.05, xanchor='left',
            y=0.95, yanchor='top',
            font=dict(size=24)
        ),
        font=dict(family="Arial"),
        showlegend=False,
        margin=dict(t=100, b=40, l=40, r=40),
        paper_bgcolor='white',
        plot_bgcolor='white',
        annotations=annotations,
        uniformtext_minsize=12,
        uniformtext_mode='hide'
    )

    fig.update_traces(
        outsidetextfont=dict(size=14, color='#333333'),
        pull=[0.01 for _ in chart_data] # Small pull for separation
    )
    
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()