// Adapted from https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Taking_still_photos

window.addEventListener('load', () => {
    let video = document.querySelector('video');
    let photo = document.querySelector('#photo');
    let canvas = document.querySelector('canvas');
    let context = canvas.getContext('2d');

    let width = 320;    // We will scale the photo width to this
    let height = 0;     // This will be computed based on the input stream
    let streaming = false;

    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then(stream => {
            video.srcObject = stream;
            video.play();
        })
        .catch(err => {
            console.log(`An error occurred: ${err}`);
        });

    video.addEventListener('canplay', (_) => {
        if (streaming) { return; }

        height = video.videoHeight / (video.videoWidth / width);

        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;

        setTimeout(() => {
            takepicture();
            setInterval(takepicture, 60000);
        }, 1000);
    }, false);

    function takepicture() {
        if (!height) {
            console.log('Failed to take picture');
            return;
        }

        context.drawImage(video, 0, 0, width, height);

        let data = canvas.toDataURL('image/png');
        photo.setAttribute('src', data);

        // POST the base64 string to the webserver
        fetch(window.location.pathname, {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data })
        });
    }
}, false);
