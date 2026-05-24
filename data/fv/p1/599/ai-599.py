import sys
import json
import plotly.graph_objects as go

def main():
    """
    Main function to generate a pie chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file at {json_path} was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file at {json_path} is not a valid JSON file.")
        sys.exit(1)

    chart_data = data.get('chart_data', [])
    colors = data.get('colors', [])

    labels = [item['label'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        textinfo='value',
        textfont=dict(
            family="Arial, bold",
            size=14,
            color='white'
        ),
        pull=[0.08] * len(values),
        sort=False,
        direction='clockwise',
        hoverinfo='label+percent+value'
    ))

    fig.update_layout(
        showlegend=True,
        font=dict(
            family="Arial",
            size=12
        ),
        legend=dict(
            x=0.8,
            y=0.5,
            xanchor='left',
            yanchor='middle',
            font=dict(
                size=11
            ),
            bgcolor='rgba(255,255,255,0)' # Transparent background
        ),
        margin=dict(l=20, r=320, t=20, b=20),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    if json_path.endswith('.json'):
        base_name = json_path[:-5]
    else:
        base_name = json_path
    
    output_filename = f"{base_name}.png"

    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart saved to {output_filename}")
    except Exception as e:
        print(f"Error writing image file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()