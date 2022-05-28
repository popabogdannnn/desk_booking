
var available_desks;
var array_of_desks = [];
var keys;
var index;

var width;
var height;
var draw;
var mouse = [];
var background;
var map;
var interval;

function mouse_inside_desk(mouse, desk) {
    if(mouse[0] >= desk[0] && desk[2] >= mouse[0] && desk[1] <= mouse[1] && mouse[1] <= desk[3]) {
        return true;
    }
    else {
        return false;
    }
}

function draw_desks() {
    draw.clearRect(0, 0, width, height);
    draw.drawImage(background, 0, 0);
    
    for(let i = 0; i < array_of_desks.length; i++) {
        desk = array_of_desks[i];
        draw.beginPath();
        if(mouse.length == 2) {
            if(mouse_inside_desk(mouse, desk)) {
                draw.strokeStyle = 'green';
            }
            else {
                draw.strokeStyle = 'blue';
            }
        }
        else {
            draw.strokeStyle = 'blue';
        }
        draw.rect(desk[0], desk[1], desk[2] - desk[0], desk[3] - desk[1]);

        draw.stroke();
    }
}


function update_page() {
    let content = document.getElementById('page_content')
    
    if(content == null) {
        return;
    }
    
    if(keys.length == 0) {
        
        content.innerHTML = "Nothing was found";
        return;
    }

    content.innerHTML = "";
    map = document.createElement("canvas")
    map.onmousemove = function mouse_move_over_map(e) {
        var rect = e.target.getBoundingClientRect();
        var x = parseInt(e.clientX - rect.left);
        var y = parseInt(e.clientY - rect.top);
        mouse = [x, y];
    }

    map.onclick = function image_click(e) {
            
        var rect = e.target.getBoundingClientRect();
        var x = parseInt(e.clientX - rect.left); //x position within the element.
        var y = parseInt(e.clientY - rect.top);  //y position within the element.
        
        let new_array_of_desks = []
        let ok = false;
        for(let i = 0; i < array_of_desks.length; i++) {
            if(mouse_inside_desk(mouse, array_of_desks[i])) {
                
            }
        }
    }

    increment_button = document.createElement("button");
    increment_button.addEventListener("click", (e) => {
        index = Math.min(index + 1, keys.length - 1);
        update_page();
    })
    increment_button.innerHTML = ">"

    decrement_button = document.createElement("button");
    decrement_button.addEventListener("click", (e) => {
        index = Math.max(index - 1, 0);
        update_page();
    })
    decrement_button.innerHTML = "<";

    title = document.createElement("h5")
    title.innerHTML = available_desks[keys[index]]["name"]
    content.appendChild(title)
    content.appendChild(document.createElement("br"))
    content.appendChild(map)
    content.appendChild(document.createElement("br"))
    content.appendChild(decrement_button)
    
    content.appendChild(increment_button)

    background = new Image();
    draw = map.getContext('2d');
    background.src = available_desks[keys[index]]["image_url"]
    array_of_desks = available_desks[keys[index]]["available_desks"]
    
    
    background.onload = function() {
        width = this.width;
        height = this.height;
        map.width = width;
        map.height = height;
    }

    clearInterval(interval);
    setInterval(draw_desks, 30);
}


function get_available_desks(first_day, last_day) {
    let xhr = new XMLHttpRequest();
    let url = window.location.href;
    xhr.open("FETCH", url, true);

    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            available_desks = JSON.parse(JSON.parse(xhr.responseText));
            keys = Object.keys(available_desks);
            if(available_desks == '{}') {
                keys = [];
            }
            index = 0;
            update_page();
        }
    };
    
    var data = JSON.stringify({
        'first_day': first_day,
        'last_day': last_day,
    });
    
    xhr.send(data);
}


window.onload = function init() {
    if(document.getElementById('search_desks') != null) {
        button = document.getElementById('search_desks')
        button.addEventListener("click", (e) => {
            first_day = document.getElementById('first_day').value
            last_day = document.getElementById('last_day').value
            
            if(first_day <= last_day) {
                get_available_desks(first_day, last_day);
            }
        })
    }
}