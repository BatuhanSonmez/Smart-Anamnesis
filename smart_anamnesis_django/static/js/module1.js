function startListening() {
    fetch("{% url 'start_listening' %}")
        .then(response => response.json())
        .then(data => {
            document.getElementById('transcription').value = data.transcription;
        });
}