import base64
import io
import os
from collections import Counter

from flask import Flask, render_template, request
from PIL import Image
from ultralytics import YOLO

app = Flask(__name__)

#Load the trained YOLOv11 model once, when the app starts
MODEL_PATH = "best.pt"
model = YOLO(MODEL_PATH)

@app.route("/", methods=["GET", "POST"])
def index():
    #Main page that shows the upload form and runs detection
    if request.method=="POST":
        file = request.files.get("image")
        if file is None or file.filename == "":
            return render_template("index.html", error="Please choose an image first.")
        try:
            img= Image.open(file.stream).convert("RGB")
        except Exception:
            return render_template("index.html", error="That file does not look like a valid image.")

        #Run the model
        results=model.predict(img, conf=0.25, verbose=False)[0]
        #To show correct colors
        annotated = Image.fromarray(results.plot()[:, :, ::-1])

        #Encode the annotated image as base64 so we can show it in html
        buf = io.BytesIO()
        annotated.save(buf, format="JPEG")
        img_data = base64.b64encode(buf.getvalue()).decode("utf-8")

        #Build a list of detections and a per-class count summary
        detections = []
        counts = Counter()
        for box in results.boxes:
            name = results.names[int(box.cls)]
            counts[name]+=1
            detections.append(f"{name} - confidence {float(box.conf):.2f}")

        if counts:
            summary = "Detection: "+",".join(f"{n} {c}" for c, n in counts.items())
        else:
            summary = "No tractor or hay bales detected in this image."
        return render_template(
             "index.html", img_data=img_data, detections=detections, summary=summary
        )

    # GET request just show the empty form
    return render_template("index.html")

if __name__=="__main__":
    #Port 7860 is what huggingface space expects
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=False)