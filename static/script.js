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