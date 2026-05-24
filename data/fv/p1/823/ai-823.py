import sys
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    fig = go.Figure()

    for i, series in enumerate(chart_info['chart_data']):
        color = chart_info['colors'][i]
        # The second series in the original chart is dotted
        line_style = 'solid' if i == 0 else 'dot'
        
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            name=series.get('name', f'Series {i+1}'),
            line=dict(color=color, dash=line_style)
        ))

    texts = chart_info['texts']
    
    # Although title and subtitle are null, this handles them if they exist
    title_text = ""
    if texts.get("title"):
        title_text += f'<b>{texts["title"]}</b>'
    if texts.get("subtitle"):
        title_text += f'<br><sub>{texts["subtitle"]}</sub>'
        
    fig.update_layout(
        font=dict(family="Arial", size=12),
        title_text=title_text if title_text else None,
        title_x=0.5,
        xaxis_title=texts.get('x_axis_title'),
        yaxis_title=texts.get('y_axis_title'),
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=60, r=40, t=40, b=60),
        xaxis=dict(
            range=[0, 4500],
            tickmode='array',
            tickvals=[0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500],
            showgrid=True,
            gridcolor='#D3D3D3',
            gridwidth=1,
            griddash='dot'
        ),
        yaxis=dict(
            range=[-0.3, 0.7],
            tickmode='array',
            tickvals=[-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
            showgrid=True,
            gridcolor='#D3D3D3',
            gridwidth=1,
            griddash='dot'
        )
    )
    
    output_filename_base = json_path.rsplit('.', 1)[0]
    output_png_path = f"{output_filename_base}.png"
    
    fig.write_image(output_png_path, scale=2)
    print(f"Chart saved to {output_png_path}")

if __name__ == "__main__":
    main()