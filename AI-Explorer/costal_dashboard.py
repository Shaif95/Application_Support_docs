from flask import Flask, render_template_string
import pandas as pd

# Optional: try to use a Hugging Face dataset if the 'datasets' library is installed
try:
    from datasets import load_dataset
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

app = Flask(__name__)

# -------------------------------------------------------------------
# Configuration: put your actual Gradio / Streamlit URLs here
# -------------------------------------------------------------------
GRADIO_DEMO_URL = "https://your-gradio-demo-url.example"      # TODO: replace with real link
STREAMLIT_DEMO_URL = "https://your-streamlit-dashboard.example"  # TODO: replace with real link

# -------------------------------------------------------------------
# Helper to load a small Hugging Face dataset slice
# -------------------------------------------------------------------
def get_example_hf_dataframe():
    """
    Returns a small pandas DataFrame from a Hugging Face dataset (if available).
    This is just an example that students can modify.
    """
    if not HF_AVAILABLE:
        return None, "The 'datasets' library is not installed. Run: pip install datasets"

    try:
        # Example dataset – students can replace with an environmental dataset they like.
        # For class use, pick a small, public dataset such as 'climate_fever'.
        ds = load_dataset("climate_fever", split="train").select(range(10))
        df = ds.to_pandas()
        return df, "Showing the first 10 rows of the Hugging Face 'climate_fever' dataset."
    except Exception as e:
        return None, f"Could not load Hugging Face dataset. Error: {e}"


# -------------------------------------------------------------------
# Single route with dashboard
# -------------------------------------------------------------------
@app.route("/")
def index():
    df, hf_message = get_example_hf_dataframe()

    template = r"""
    <!doctype html>
    <html lang="en">
    <head>
        <title>Coastal AI Explorer</title>
        <meta charset="utf-8" />
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5fafc;
            }
            header {
                background: #024873;
                color: white;
                padding: 1.5rem 2rem;
            }
            header h1 {
                margin: 0;
            }
            header p {
                margin: 0.3rem 0 0 0;
            }
            main {
                padding: 1.5rem 2rem;
            }
            .section {
                margin-bottom: 2rem;
                background: white;
                border-radius: 8px;
                padding: 1.5rem;
                box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            }
            .cards {
                display: flex;
                flex-wrap: wrap;
                gap: 1rem;
            }
            .card {
                flex: 1 1 260px;
                border-radius: 8px;
                padding: 1rem;
                border: 1px solid #dde7ee;
                background: #ffffff;
            }
            .card h3 {
                margin-top: 0;
            }
            .btn {
                display: inline-block;
                margin-top: 0.5rem;
                padding: 0.5rem 0.9rem;
                border-radius: 5px;
                text-decoration: none;
                color: white;
                background-color: #0277bd;
                font-size: 0.9rem;
            }
            .btn-secondary {
                background-color: #00897b;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                font-size: 0.85rem;
            }
            th, td {
                border: 1px solid #d0d7de;
                padding: 0.4rem 0.6rem;
            }
            th {
                background-color: #e3f2fd;
            }
            .note {
                font-size: 0.85rem;
                color: #555;
            }
            footer {
                margin-top: 1rem;
                padding: 1rem 2rem;
                font-size: 0.8rem;
                color: #666;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Coastal AI Explorer</h1>
            <p>
                An NRT Coastal Resilience learning hub where students explore environmental data
                and simple ML models using Hugging Face, Gradio, and Streamlit.
            </p>
        </header>

        <main>
            <!-- Overview section -->
            <section class="section">
                <h2>Overview</h2>
                <p>
                    This dashboard is a teaching example built with <strong>Flask</strong>.
                    In your NRT projects, you can plug in:
                </p>
                <ul>
                    <li>Environmental and coastal datasets from <strong>Hugging Face</strong></li>
                    <li>Interactive model demos hosted in <strong>Gradio</strong></li>
                    <li>Data dashboards built with <strong>Streamlit</strong></li>
                </ul>
                <p class="note">
                    Students: start by editing the dataset and links below to connect this page
                    to your own coastal AI experiments.
                </p>
            </section>

            <!-- Links to Gradio / Streamlit demos -->
            <section class="section">
                <h2>Interactive Model Demos</h2>
                <div class="cards">
                    <div class="card">
                        <h3>Gradio Model Demo</h3>
                        <p>
                            Link this card to a Gradio app that runs a simple ML model
                            on coastal or environmental data (classification, regression, etc.).
                        </p>
                        <a class="btn" href="{{ gradio_url }}" target="_blank">
                            Open Gradio Demo
                        </a>
                        <p class="note">
                            Replace <code>GRADIO_DEMO_URL</code> in <code>app.py</code> with your own Gradio link.
                        </p>
                    </div>

                    <div class="card">
                        <h3>Streamlit Data Explorer</h3>
                        <p>
                            Link this card to a Streamlit dashboard that visualizes
                            environmental time series, maps, or other coastal indicators.
                        </p>
                        <a class="btn btn-secondary" href="{{ streamlit_url }}" target="_blank">
                            Open Streamlit App
                        </a>
                        <p class="note">
                            Replace <code>STREAMLIT_DEMO_URL</code> in <code>app.py</code> with your own Streamlit link.
                        </p>
                    </div>
                </div>
            </section>

            <!-- Hugging Face dataset preview -->
            <section class="section">
                <h2>Hugging Face Dataset Preview</h2>
                <p>
                    Below is a small preview of a dataset loaded via the
                    <code>datasets</code> library. In your NRT coastal work,
                    you can swap this for an ocean / climate / ecology dataset.
                </p>

                {% if hf_message %}
                    <p class="note">{{ hf_message }}</p>
                {% endif %}

                {% if df is not none %}
                    <div style="max-height: 360px; overflow: auto; border: 1px solid #dde7ee; border-radius: 6px; margin-top: 0.5rem;">
                        <table>
                            <thead>
                                <tr>
                                    {% for col in df.columns %}
                                        <th>{{ col }}</th>
                                    {% endfor %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for _, row in df.iterrows() %}
                                    <tr>
                                        {% for col in df.columns %}
                                            <td>{{ row[col] }}</td>
                                        {% endfor %}
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                {% else %}
                    <p class="note">
                        No dataset loaded yet. Install the <code>datasets</code> library and
                        update <code>get_example_hf_dataframe()</code> to use your chosen Hugging Face dataset.
                    </p>
                {% endif %}
            </section>
        </main>

        <footer>
            Coastal AI Explorer · NRT Environmental Data &amp; ML Education · Built with Flask
        </footer>
    </body>
    </html>
    """

    return render_template_string(
        template,
        df=df,
        hf_message=hf_message,
        gradio_url=GRADIO_DEMO_URL,
        streamlit_url=STREAMLIT_DEMO_URL,
    )


if __name__ == "__main__":
    # For classroom/demo use only – in production use a proper WSGI server.
    app.run(debug=True)
