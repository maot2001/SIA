const imagenes = document.querySelectorAll('.imagen'); // Selecciona todas las imágenes por su clase CSS
console.log('pp')
imagenes.forEach(imagen => {
    let startTime;

    imagen.addEventListener('mouseover', function() {
        startTime = new Date();
        console.log('on image')
    });

    imagen.addEventListener('mouseout', function() {
        if (startTime) {
            const duration = new Date() - startTime; // Calcula la duración en milisegundos
            const imagenId = imagen.id; // Obtiene el ID de la imagen actual
            console.log(duration)
            console.log(imagenId)
            enviarDuracionAlServidor(imagenId, duration);
            console.log('out image')
        }
    });
});

function enviarDuracionAlServidor(imagenId, duration) {
    // Envía la duración al servidor Django con el ID de la imagen
    fetch('/guardar-duracion/', {
        method: 'POST',
        body: JSON.stringify({ imagenId: imagenId, duration: duration }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            console.log('Duración enviada al servidor con éxito');
        } else {
            console.error('Error al enviar la duración al servidor');
        }
    })
    .catch(error => {
        console.error('Error de red:', error);
    });
}