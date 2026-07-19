# tractor-hay-detector
A Flask application serving a YOLOv11n object detection model that locates tractor & haybale in field and aerial imagery. Upload an image and getit back with bounding boxes and per-class counts. The model was trained on 100 self-collected images and labeled in Roboflow as a part of my machine learning coursework. The app is containerized with Docker and deployed publicly on Hugging Face Spaces.

**Deployed app:** https://huggingface.co/spaces/Malteneiji/tractor-hay-detector

**Direct link:** https://malteneiji-tractor-hay-detector.hf.space

## Preview
demo.png -> Shows the app detecting a tractor

## What the model does
- Detects two classes: `haybale` and `tractor`
- YOLOv11n (nano), fine-tuned from COCO-pretrained weights at 640px
- Use case: field-activity and harvest monitoring from drone/aerial imagery for example counting bales as a proxy for hay yield
- Dataset: 100 self-collected images labeled in Roboflow: [view it on Roboflow Universe](https://universe.roboflow.com/ms-workspace-sad6s/object-detection-tractor-hay)
  
## Project structure 
- app.py                : Flask application (upload → predict → annotated result)
- best.pt               : Trained YOLOv11n weights
- requirements.txt      : Python dependencies
- Dockerfile            : Container definition
- templates/index.html  : Web form + results page
- static/style.css      : Styling

## Run locally with Docker
Requires [Docker](https://www.docker.com/products/docker-desktop/) installed.

```bash
git clone https://github.com/YOUR_USERNAME/tractor-hay-detector.git
cd tractor-hay-detector
docker build -t tractor-hay-detector .
docker run -p 7860:7860 tractor-hay-detector
```
Then open **http://localhost:7860** in your browser.
The image installs CPU-only PyTorch, so no GPU is needed.

## How to use the interface
1. Open the app (locally or via the live direct link)
2. Click **Choose File** and select a field or aerial image (JPG/PNG)
3. Click **Detect objects**
4. The page returns the image with bounding boxes, confidence scores, and a count of detected objects per class

## Known issues & limitations
- Small and distant bales are often missed this is the main weakness
- Small training set (100 original images) with mild overfitting on localization
- Round and square bales share one label without adding intra-class variation
- Objects at frame edges are occasionally missed
