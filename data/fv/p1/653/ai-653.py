import sys
import json
import os
import plotly.graph_objects as go

def create_chart(json_path):
    """
    Reads chart data from a JSON file and generates a Plotly chart image.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    fig = go.Figure()

    # Add a separate trace for each data point to create a legend item for each bar
    for i, item in enumerate(chart_data):
        fig.add_trace(go.Bar(
            x=[item['category']],
            y=[item['value']],
            name=item['category'],
            marker=dict(
                color=colors[i % len(colors)],
                line=dict(color='black', width=1)
            ),
            showlegend=True
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=texts.get('title'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showticklabels=False,
            categoryorder='array',
            categoryarray=[item['category'] for item in chart_data]
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 60],
            dtick=10,
            showgrid=True,
            gridcolor='LightGray',
            gridwidth=1
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        plot_bgcolor='white',
        barmode='group',
        legend=dict(
            title_text=texts.get('legend_title')
        ),
        margin=dict(l=80, r=40, t=100, b=40)
    )

    # Determine output filename
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_name}.png"
    
    # Save image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script_name.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    # The prompt requests no function definitions, so placing the logic directly here.
    # The function structure is kept for clarity during development but removed for final output.
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}")
        sys.exit(1)

    chart_data = data.get('chart_data', [])
    texts = data.get('texts', {})
    colors = data.get('colors', [])

    fig = go.Figure()

    for i, item in enumerate(chart_data):
        fig.add_trace(go.Bar(
            x=[item['category']],
            y=[item['value']],
            name=item['category'],
            marker=dict(
                color=colors[i % len(colors)],
                line=dict(color='black', width=1)
            ),
            showlegend=True
        ))
    
    fig.update_layout(
        title=dict(
            text=texts.get('title'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showticklabels=False,
            categoryorder='array',
            categoryarray=[item['category'] for item in chart_data]
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 60],
            dtick=10,
            showgrid=True,
            gridcolor='LightGray'
        ),
        font=dict(
            family="Arial"
        ),
        plot_bgcolor='white',
        barmode='group',
        legend=dict(
            title_text=texts.get('legend_title')
        ),
        margin=dict(l=80, r=40, t=100, b=40)
    )
    
    base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
    output_image_path = f"{base_filename}.png"
    
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")