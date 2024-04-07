resultArray = {}
const save = JSON.parse(localStorage.getItem('resultArray'));

if (save != null) {
    resultArray = save
}
desblock()

function desblock() {
    if (Object.keys(resultArray).length > 0) {
        document.getElementById("submitBtn").style.display = "block";
    } else {
        document.getElementById("submitBtn").style.display = "none";
    }
}

document.getElementById('submitBtn').addEventListener('click', function() {
    const hiddenInput = document.getElementById('resultArray');
    hiddenInput.value = JSON.stringify(resultArray);
    localStorage.removeItem('resultArray');
});


const images = document.querySelectorAll('.image');
images.forEach(image => {
    let startTime;

    image.addEventListener('mouseover', function() {
        startTime = new Date();
    });

    image.addEventListener('mouseout', function() {
        if (startTime) {
            const duration = new Date() - startTime;
            const imageId = image.id;
            sendTime(imageId, duration);
        }
    });

    image.addEventListener('click', function() {
      const imageId = image.id;
      console.log(imageId);
      sendId(imageId);
  });

    const movie_name = image.dataset.name;
    const description = image.dataset.description;
    let tooltip;
    if (description != "None") {
      tooltip = "Name: " + movie_name + "\nDescription: " + description
    }
    else {
      tooltip = "Name: " + movie_name
    }
    if (image.hasAttribute("title")) {
      image.removeAttribute("title")
    }
    image.setAttribute("title", tooltip)
});

function good(itemId) {
    resultArray[itemId] = 1;
    localStorage.setItem('resultArray', JSON.stringify(resultArray));
    desblock()
}

function bad(itemId) {
    resultArray[itemId] = 0;
    localStorage.setItem('resultArray', JSON.stringify(resultArray));
    desblock()
}

function sendTime(imageId, elapsedTime) {
    let xhr = new XMLHttpRequest();
    let url = 'save_duration/';
    
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    
    let csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (!xhr.status === 200) {
          console.error('Error al enviar tiempo a Django');
        }
      }
    };
    let data = {
        id: imageId,
      time: elapsedTime
    };
    
    xhr.send(JSON.stringify(data));
  }

  function sendId(imageId) {
    let xhr = new XMLHttpRequest();
    let url = 'movie/';
    
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    
    let csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (!xhr.status === 200) {
          console.error('Error al enviar Id a Django');
        }
        else {
          data = JSON.parse(xhr.response)
          window.location = data.new_url;
        }
      }
    };
    let data = {
        id: imageId
    };
    
    xhr.send(JSON.stringify(data));
  }
  
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }