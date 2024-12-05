from flask import Flask, render_template

app = Flask(__name__)

# Define the route for the home page, by home page launch index.html from templace folder
@app.route("/")
def home():
    """for home page"""
    return render_template("index.html")

# Run the Flask development server; line below needed in order not to run app.py when imporing to other scripts
if __name__ == "__main__":
    app.run(debug=True)
