import sys
import json
import plotly.graph_objects as go
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)

    chart_data = chart_data_json['chart_data']
    texts = chart_data_json['texts']
    colors = chart_data_json['colors']

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            name=series['name'],
            line=dict(color=colors[i], width=2.5)
        ))

    fig.update_layout(
        plot_bgcolor='white',
        showlegend=False,
        font=dict(family="Arial", size=12, color='#000000'),
        width=800,
        height=450,
        margin=dict(l=80, r=40, t=40, b=80),
        xaxis=dict(
            range=[55, 95],
            tickvals=[55, 95],
            ticktext=['55°C', '95°C'],
            tickfont=dict(size=14),
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#003366',
            linewidth=2,
            mirror=True
        ),
        yaxis=dict(
            title_text=texts['y_axis_title'],
            title_font=dict(size=16),
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#003366',
            linewidth=2,
            mirror=True,
            range=[0, 1]
        )
    )

    if texts.get('annotations'):
        for annotation in texts['annotations']:
            fig.add_annotation(
                text=annotation['text'],
                x=annotation['x'],
                y=annotation['y'],
                xref=annotation['xref'],
                yref=annotation['yref'],
                showarrow=annotation['showarrow'],
                arrowhead=annotation['arrowhead'],
                arrowcolor=annotation['arrowcolor'],
                ax=annotation['ax'],
                ay=annotation['ay'],
                font=annotation['font'],
                align=annotation['align']
            )

    filename_base = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{filename_base}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()