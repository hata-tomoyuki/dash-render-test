(function () {
  let stream = null;

  async function startCamera() {
    const video = document.getElementById('camera-video');
    const canvas = document.getElementById('camera-canvas');
    const captureButton = document.getElementById('capture-button');
    const cancelButton = document.getElementById('cancel-camera-button');
    const cameraButton = document.getElementById('camera-trigger-button');

    if (!video || !canvas) {
      console.error('ビデオまたはキャンバス要素が見つかりません');
      return;
    }

    try {
      stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'environment',
          width: { ideal: 1920 },
          height: { ideal: 1080 },
        },
        audio: false,
      });

      video.srcObject = stream;
      video.muted = true;
      video.setAttribute('playsinline', 'true');
      video.setAttribute('webkit-playsinline', 'true');

      const playPromise = video.play();
      if (playPromise !== undefined) {
        playPromise.catch((err) => {
          console.warn('ビデオの自動再生に失敗しました:', err);
        });
      }

      if (cameraButton) cameraButton.style.display = 'none';
      video.style.display = 'block';
      if (captureButton) captureButton.style.display = 'block';
      if (cancelButton) cancelButton.style.display = 'block';
    } catch (err) {
      console.error('カメラアクセスエラー:', err);
      alert('カメラへのアクセスに失敗しました。ブラウザの設定でカメラの使用を許可してください。');
    }
  }

  function stopCamera() {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      stream = null;
    }

    const video = document.getElementById('camera-video');
    const captureButton = document.getElementById('capture-button');
    const cancelButton = document.getElementById('cancel-camera-button');
    const cameraButton = document.getElementById('camera-trigger-button');

    if (video) {
      video.srcObject = null;
      video.style.display = 'none';
      video.removeAttribute('playsinline');
      video.removeAttribute('webkit-playsinline');
    }
    if (captureButton) captureButton.style.display = 'none';
    if (cancelButton) cancelButton.style.display = 'none';
    if (cameraButton) cameraButton.style.display = 'block';
  }

  function capturePhoto() {
    const video = document.getElementById('camera-video');
    const canvas = document.getElementById('camera-canvas');

    if (!video || !canvas) {
      console.error('ビデオまたはキャンバス要素が見つかりません');
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(
      (blob) => {
        if (!blob) {
          console.error('Blobの生成に失敗しました');
          return;
        }

        const file = new File([blob], 'camera_capture.jpg', { type: 'image/jpeg' });
        const cameraUploadInput = document.querySelector('#camera-upload input[type="file"]');

        if (cameraUploadInput) {
          const dataTransfer = new DataTransfer();
          dataTransfer.items.add(file);
          cameraUploadInput.files = dataTransfer.files;

          const changeEvent = new Event('change', { bubbles: true });
          cameraUploadInput.dispatchEvent(changeEvent);
        }

        stopCamera();
      },
      'image/jpeg',
      0.95,
    );
  }

  function attachListeners() {
    const cameraButton = document.getElementById('camera-trigger-button');
    const captureButton = document.getElementById('capture-button');
    const cancelButton = document.getElementById('cancel-camera-button');

    if (cameraButton && !cameraButton.dataset.listenerAttached) {
      cameraButton.dataset.listenerAttached = 'true';
      cameraButton.addEventListener('click', (e) => {
        e.preventDefault();
        startCamera();
      });
    }

    if (captureButton && !captureButton.dataset.listenerAttached) {
      captureButton.dataset.listenerAttached = 'true';
      captureButton.addEventListener('click', (e) => {
        e.preventDefault();
        capturePhoto();
      });
    }

    if (cancelButton && !cancelButton.dataset.listenerAttached) {
      cancelButton.dataset.listenerAttached = 'true';
      cancelButton.addEventListener('click', (e) => {
        e.preventDefault();
        stopCamera();
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(attachListeners, 500);
    });
  } else {
    setTimeout(attachListeners, 500);
  }

  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.addedNodes.length > 0) {
        attachListeners();
      }
    });
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });

  window.addEventListener('beforeunload', () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
    }
  });
})();
