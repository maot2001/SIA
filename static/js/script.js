resultArray = {}
commented = {}
const save = JSON.parse(localStorage.getItem('resultArray'));
const save2 = JSON.parse(localStorage.getItem('commented'));

if (save != null) {
    resultArray = save
}
if (save2 != null) {
  commented = save2
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
    const user_comments = document.getElementById('comments');
    hiddenInput.value = JSON.stringify(resultArray);
    user_comments.value = JSON.stringify(commented);
    localStorage.removeItem('resultArray');
    localStorage.removeItem('commented');
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

function comment(itemId) {
  const commentInput = document.getElementById('commentInput' + itemId);
  const user_comment = commentInput.value;
  commented[itemId] = user_comment;
  localStorage.setItem('commented', JSON.stringify(commented));
  actComment(itemId);
}

function actComment(itemId) {
  const commentForm = document.getElementById('commentForm' + itemId);
  commentForm.classList.toggle('hidden');
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