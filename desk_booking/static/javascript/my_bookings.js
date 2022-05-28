

function delete_booking(booking_id) {
    booking_list = document.getElementById("booking_list")
    link = document.getElementById(booking_id)
    booking_list.removeChild(link)

    let xhr = new XMLHttpRequest();
    let url = window.location.href;
    
    xhr.open("POST", url, true)
    
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
        }
    };
    
    var data = booking_id;
    
    xhr.send(data);
}