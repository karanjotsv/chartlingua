import sys
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json>")
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

    fig = go.Figure()

    for i, series in enumerate(chart_data['series']):
        fig.add_trace(go.Scatter(
            x=chart_data['categories'],
            y=series['values'],
            name=series['name'],
            mode='lines+markers',
            line=dict(color=colors[i]),
            marker=dict(symbol=series['marker_symbol'], size=8)
        ))
        
    title_text = f"<b>{texts['title']}</b>" if texts.get('title') else ""

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            y=0.95,
            font=dict(size=18)
        ),
        xaxis=dict(
            title=texts.get('x_axis_title'),
            tickvals=[1, 3, 5, 7, 9],
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title=texts.get('y_axis_title'),
            range=[0.9, 1.6],
            showgrid=True,
            gridcolor='#A9A9A9',
            zeroline=False
        ),
        plot_bgcolor='#D3D3D3',
        paper_bgcolor='white',
        font=dict(
            family="Arial",
            size=12
        ),
        legend=dict(
            x=1.02,
            y=0.8,
            bgcolor='rgba(255,255,255,0.5)',
            bordercolor='Black',
            borderwidth=1
        ),
        margin=dict(l=80, r=40, t=80, b=80)
    )

    base_filename = json_path.rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()