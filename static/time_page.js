  function pingServer() {
    let xhr = new XMLHttpRequest();
    let url = 'ping/';
    
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    
    let csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        bool = xhr.status === 200
        if (!xhr.status === 200) {
          console.error('Error al enviar tiempo a Django');
        }
      }
    };
    let page_url = document.URL;
    let movieId = page_url.slice(28, page_url.length - 1)
    let data = {
      id: movieId
    };
    
    xhr.send(JSON.stringify(data));
    setTimeout(pingServer, 100);
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

  window.onload = pingServer;