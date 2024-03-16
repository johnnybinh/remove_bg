from flask import Flask, send_file, redirect, flash, request, render_template
from rembg import remove
from PIL import Image
from io import BytesIO
import os

ALLOWED_EXTENSIONS = {"png"}

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def upload_image():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]
        if file.name == "":
            flash("no selected file")
            return "no file", 400
        if file:
            input_image = Image.open(file.stream)
            print(input_image)
            output = remove(input_image)
            output_convert = output.convert("RGBA")
            print(output)

            img_io = BytesIO()
            output_convert.save(img_io, "PNG")
            img_io.seek(0)
            print("sending")
            # output.save((os.path.join("./save") + file.filename))
            return send_file(
                img_io,
                mimetype="image/png",
                as_attachment=True,
                download_name="output.png",
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)
