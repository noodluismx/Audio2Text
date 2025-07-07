let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            document.getElementById("status").innerText = "Recording...";

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                const formData = new FormData();
                formData.append("audio_data", audioBlob, "recorded.wav");

                fetch("/transcribe", {
                    method: "POST",
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.transcription) {
                        document.getElementById("transcription").innerText = data.transcription;
                    } else {
                        document.getElementById("transcription").innerText = data.error;
                    }
                });

                audioChunks = [];
            };
        });
}

function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();
        document.getElementById("status").innerText = "Stopped recording.";
    }
}
