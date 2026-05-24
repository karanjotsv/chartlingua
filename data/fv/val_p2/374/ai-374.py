import sys
import json
import plotly.graph_objects as go
import os

def create_chart(json_path):
    """
    Creates a chart from a JSON file and saves it as a PNG image.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_details = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}", file=sys.stderr)
        sys.exit(1)

    # Prepare data for Plotly
    chart_data = chart_details.get('chart_data', [])
    texts = chart_details.get('texts', {})
    colors = chart_details.get('colors', [])
    
    if not chart_data:
        print("Error: 'chart_data' is missing or empty in the JSON file.", file=sys.stderr)
        sys.exit(1)

    categories = [item['category'] for item in chart_data]
    values = [item['values'][0] for item in chart_data]

    # Create figure
    fig = go.Figure()

    # Add bar trace
    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker=dict(color=colors[0] if colors else '#4674b2'),
        hoverinfo='x'
    ))

    # Update layout
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            y=0.95,
            font=dict(size=18)
        ),
        xaxis=dict(
            title=texts.get('x_axis_title', ''),
            range=[0, 400000],
            tickmode='linear',
            tick0=0,
            dtick=100000,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title=texts.get('y_axis_title', ''),
            showgrid=False
        ),
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=180, r=40, t=80, b=60) # Increased left margin for long labels
    )

    # Ensure axes lines are visible
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black')

    # Determine output filename
    base_name = os.path.basename(json_path).rsplit('.', 1)[0]
    output_filename = f"{base_name}.png"
    
    # Save image
    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart saved to {output_filename}")
    except Exception as e:
        print(f"Error saving image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>", file=sys.stderr)
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    # Removed function definition for direct execution as requested
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            chart_details = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}", file=sys.stderr)
        sys.exit(1)

    chart_data = chart_details.get('chart_data', [])
    texts = chart_details.get('texts', {})
    colors = chart_details.get('colors', [])

    categories = [item['category'] for item in chart_data]
    values = [item['values'][0] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker=dict(color=colors[0]),
        hoverinfo='x'
    ))

    title_text = texts.get('title', '')

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            y=0.95,
            font=dict(size=18)
        ),
        xaxis=dict(
            title=texts.get('x_axis_title', ''),
            range=[0, 400000],
            tickmode='linear',
            tick0=0,
            dtick=100000,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title=texts.get('y_axis_title', None),
            showgrid=False,
            automargin=False # Allow manual margin setting
        ),
        font=dict(family="Arial", size=12, color="black"),
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=180, r=40, t=80, b=60)
    )

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', ticks='outside')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', ticks='outside')

    base_name = os.path.basename(json_file_path).rsplit('.', 1)[0]
    output_filename = f"{base_name}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")