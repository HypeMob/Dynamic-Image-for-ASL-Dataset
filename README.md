<h1>Dynamic Image for Sign Language Recognition</h1>

<h2>Project Overview</h2>
<br>
American Sign Language (ASL) recognition from video typically relies on one of two approaches: <strong>static image processing</strong>, where a single key frame is extracted from a video, or <strong>video processing</strong>, where multiple frames are analyzed to capture motion. Static image processing is fast and lightweight but loses temporal information, resulting in lower accuracy. Video processing captures motion more precisely but at a much higher computational cost.
<br>
<br>
This project explores <strong>Dynamic Image</strong> as a middle ground between the two. A Dynamic Image compresses information from multiple frames into a single image without discarding the temporal motion cues, letting a model learn motion patterns while keeping the computational footprint of image-based processing.
<br>
<br>
This repository accompanies the paper <em>"Dynamic Images For Sign Language Recognition: A Middle Ground Between Static Image And Video-Based Models"</em>, accepted for oral presentation at the 9th International Conference on Informatics and Computational Sciences (ICICoS 2026), technically endorsed by the IEEE Indonesia Section.
<br>
<br>
<strong>Note:</strong> the paper has been accepted but is not yet publicly published. Some assets (e.g. the manuscript, final dataset files) are therefore not included here yet.

<h2>Project Framework</h2>
<img width="800" height="560" alt="Screenshot 2026-09-26 125815" src="https://github.com/user-attachments/assets/ff202a8e-211f-4329-95e6-69d7e92521b2" />


<h2>What is a Dynamic Image?</h2>
<img width="800" height="560" alt="Screenshot 2026-09-26 130229" src="https://github.com/user-attachments/assets/3324d9e5-3eb3-49ba-91a0-df0df96b3ed7" />
<br>
A Dynamic Image is a single-image representation that encodes the temporal ordering of frames in a video using a ranking-based pooling function, rather than a single snapshot in time. It summarizes how motion evolves across a clip into one still image, which can then be processed with standard image-based deep learning models instead of video-based ones.



<h2>Methods Compared</h2>
<ul>
  <li><h4>Static Image Processing</h4>A single representative frame is extracted per video and classified directly. Lowest computational cost, lowest accuracy.</li>
  <li><h4>Dynamic Image Processing</h4>Frames from the full video are compressed into one Dynamic Image, preserving temporal motion cues. Balances cost and accuracy.</li>
  <li><h4>Video Processing</h4>Multiple frames (or the full clip) are processed to explicitly model motion over time. Highest accuracy, highest computational cost.</li>
</ul>

<h2>Dataset</h2>
<img width="800" height="445" alt="Screenshot 2026-09-26 130501" src="https://github.com/user-attachments/assets/7e61fe89-7de4-4b53-9d64-ba48f3914510" />
<br>
We combined two publicly available ASL datasets, keeping only the sign classes common to both:
<ul>
  <li><strong>DSP Dataset</strong> — 13 classes, 20 videos per class, ~0.5s duration per video</li>
  <li><strong>WLASL Dataset</strong> — 12 of the same classes, 6 videos per class, ~4s duration per video</li>
</ul>
The common classes across both datasets were selected and merged to build the final dataset used for training and evaluation.

<h2>Preprocessing</h2>
<img width="800" height="556" alt="Screenshot 2026-09-26 130552" src="https://github.com/user-attachments/assets/8b960a05-bd73-4502-9998-92034851e294" />
<ul>
  <li>Trimming and preparing raw video clips</li>
  <li>Frame normalization</li>
  <li>Hand detection and landmark labeling using Google MediaPipe Hand Landmarker</li>
  <li>Dynamic Image generation from the processed frame sequences</li>
</ul>

<h2>Models Used</h2>
<img width="800" height="547" alt="Screenshot 2026-09-26 130637" src="https://github.com/user-attachments/assets/8f51b758-ba5a-4024-b6b0-e24356ab4445" />
<ul>
  <li><h4>Static Image Processing</h4>ResNet, MobileNet, EfficientNet</li>
  <li><h4>Dynamic Image Processing</h4>ResNet, MobileNet, EfficientNet</li>
  <li><h4>Video Processing</h4>MobileNet, X3D, EfficientNet + LSTM</li>
</ul>

<h2>Results Summary</h2>
<img width="800" height="361" alt="image" src="https://github.com/user-attachments/assets/46455796-7684-481e-8e96-de5a046546ac" />
<br>
<strong>Performance (Accuracy, avg.)</strong>
<ol>
  <li>Video Processing — 0.7477</li>
  <li>Dynamic Image Processing — 0.5825</li>
  <li>Static Image Processing — 0.4554</li>
</ol>
<strong>Computational Cost (avg.)</strong>
<table>
  <tr><th>Rank</th><th>Method</th><th>Memory Usage (Mb)</th><th>Time Consumption (s)</th></tr>
  <tr><td>1</td><td>Dynamic Image Processing</td><td>10.61</td><td>0.309</td></tr>
  <tr><td>2</td><td>Video Processing</td><td>68.21</td><td>0.5806</td></tr>
  <tr><td>3</td><td>Static Image Processing</td><td>78.6367</td><td>0.714</td></tr>
</table>
<br>
Dynamic Image Processing lands closest to Video Processing on accuracy while using the least memory and the least processing time of all three methods — confirming it as an effective middle ground.

<h2>Directory Explanatory</h2>
<h3>Folder Definitions</h3>

<li>
  <h4><a href="Preprocessing">Preprocessing</a></h4>
  <p>Contains the shared preprocessing scripts applied to raw video before any of the three methods are run.</p>
  <ul>
    <li>
      <strong><a href="Preprocessing/crop_trim.py">crop_trim.py</a></strong>
      <br>
      Trims each raw video clip and crops frames to isolate the relevant region.
    </li>
    <li>
      <strong><a href="Preprocessing/HandLandmarker.py">HandLandmarker.py</a></strong>
      <br>
      Applies Google's MediaPipe Hand Landmarker to detect and label hand landmarks on each frame.
    </li>
  </ul>
</li>

<li>
  <h4><a href="Static Image Processing">Static Image Processing</a></h4>
  <p>Contains the pipeline for single-frame (static image) classification, used as the baseline comparison.</p>
  <ul>
    <li>
      <strong><a href="Static Image Processing/Source Code">Source Code</a></strong>
      <ul>
        <li>
          <strong><a href="Static Image Processing/Source Code/model_code.py">model_code.py</a></strong>
          <br>
          Trains and evaluates the static image classification models (ResNet, MobileNet, EfficientNet).
        </li>
      </ul>
    </li>
    <li>
      <strong><a href="Static Image Processing/Static Image Results.docx">Static Image Results.docx</a></strong>
      <br>
      Experiment results (accuracy, memory usage, processing time) for the static image pipeline.
    </li>
  </ul>
</li>

<li>
  <h4><a href="Dynamic Image Processing">Dynamic Image Processing</a></h4>
  <p>Contains the pipeline for generating and classifying Dynamic Images.</p>
  <ul>
    <li>
      <strong><a href="Dynamic Image Processing/Source Code">Source Code</a></strong>
      <ul>
        <li>
          <strong><a href="Dynamic Image Processing/Source Code/dynamic_image_convertion.ipynb">dynamic_image_convertion.ipynb</a></strong>
          <br>
          Generates Dynamic Images from raw video input. Implementation based on <a href="https://github.com/hbilen/dynamic-image-nets">hbilen/dynamic-image-nets</a>.
        </li>
        <li>
          <strong><a href="Dynamic Image Processing/Source Code/model_code.ipynb">model_code.ipynb</a></strong>
          <br>
          Trains and evaluates the classification models (ResNet, MobileNet, EfficientNet) on the generated Dynamic Images.
        </li>
      </ul>
    </li>
    <li>
      <strong><a href="Dynamic Image Processing/Dynamic Image Results.docx">Dynamic Image Results.docx</a></strong>
      <br>
      Experiment results (accuracy, memory usage, processing time) for the Dynamic Image pipeline.
    </li>
  </ul>
</li>

<li>
  <h4><a href="Video Processing">Video Processing</a></h4>
  <p>Contains the pipeline for direct video-based classification.</p>
  <ul>
    <li>
      <strong><a href="Video Processing/Source Code">Source Code</a></strong>
      <ul>
        <li>
          <strong><a href="Video Processing/Source Code/Final Code(3models).ipynb">Final Code(3models).ipynb</a></strong>
          <br>
          Trains and evaluates the video-based classification models: MobileNet, X3D, and EfficientNet + LSTM.
        </li>
      </ul>
    </li>
    <li>
      <strong><a href="Video Processing/Video Classification Result.docx">Video Classification Result.docx</a></strong>
      <br>
      Experiment results (accuracy, memory usage, processing time) for the video-based pipeline.
    </li>
  </ul>
</li>

<li>
  <h4><a href="Testing Memory and Time Usage">Testing Memory and Time Usage</a></h4>
  <p>Contains the scripts/notebooks used to benchmark memory consumption and processing time across all three methods, producing the Computational Cost comparison above.</p>
</li>
