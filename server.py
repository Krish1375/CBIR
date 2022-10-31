import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from flask import Flask, request, render_template
from pathlib import Path
from api import Company

app = Flask(__name__)

# Read image features
fe = FeatureExtractor()
cs = Company()
features = []
img_paths = []
for feature_path in Path("./static/feature").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/img") / (feature_path.stem + ".png"))
features = np.array(features)
print("f1", features.shape)


@app.route('/')
def started():
    return render_template('started.html')


@app.route('/steps')
def steps():
    return render_template('steps.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + "_" + file.filename
        img.save(uploaded_img_path)
        print("f2", features.shape)
        # Run search
        query = fe.extract(img)

        # print(np.linalg.norm(features))
        # print(np.linalg.norm(query))
        dists = np.linalg.norm((query - features), axis=1)  # L2 distances to features
        # scaler = MinMaxScaler(feature_range=(0,1))
        # dists = scaler.fit_transform(dists.reshape(-1,1))
        dists = dists / (2 * np.linalg.norm(query))
        print(dists)
        # print(dists.size)
        # Lisn = (dists - np.min(dists))/np.ptp(dists)
        # print(Lisn)

        ids = np.argsort(dists)[:5]  # Top 30 result
        print("ids", ids)
        array2 = [None] * 20000
        for i in range(5):
            j = ids[i]
            print(img_paths[j])
            temp = str(img_paths[j])
            y = temp.split('img', 1)[1]
            res = y.split('.png')[0]
            only_alpha = ""
            for char in res:
                if char.isalpha():
                    only_alpha += char
            print(only_alpha)
            array2.pop(j)
            if only_alpha.isalpha():
                array2.insert(j, cs.CompanyInformation(only_alpha))
            else:
                array2.insert(j, "No information found")
            print(array2)
        print(array2)
        scores = [(dists[id], img_paths[id], array2[id]) for id in ids]

        print(scores)

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores)


    else:
        return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run("0.0.0.0")
