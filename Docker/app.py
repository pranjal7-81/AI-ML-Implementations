
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        number = int(request.form["number"])

        for i in range(1, 11):
            result += f"<p>{number} x {i} = {number * i}</p>"

    return f"""
    <html>
    <head>
        <title>Multiplication Table</title>
    </head>
    <body>
        <h1>Multiplication Table</h1>

        <form method="POST">
            <input type="number" name="number"
                   placeholder="Enter a number" required>
            <button type="submit">Generate Table</button>
        </form>

        {result}
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host = "0.0.0.0",debug=True)
