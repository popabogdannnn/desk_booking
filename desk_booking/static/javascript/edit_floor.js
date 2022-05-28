
var array_of_desks = []
var temp = []
var width;
var height;
var map;
var draw;
var background = new Image();
var mouse = [];

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
                draw.strokeStyle = 'red';
            }
            else {
                draw.strokeStyle = 'black';
            }
        }
        else {
            draw.strokeStyle = 'black';
        }
        draw.rect(desk[0], desk[1], desk[2] - desk[0], desk[3] - desk[1]);

        draw.stroke();
    }
}

function init() {
    if(document.getElementById('floor_map') != null) {
        map = document.getElementById('floor_map');
        
        console.log(image_url);

        draw = map.getContext('2d');
        
        background.src = image_url;
        

        width = map.width;
        height = map.height;
        

        setInterval(draw_desks, 30);
        
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
                if(!mouse_inside_desk(mouse, array_of_desks[i])) {
                    new_array_of_desks.push(array_of_desks[i]);
                }
                else {
                    ok = true;
                }
            }
            array_of_desks = new_array_of_desks;

            console.log("Left? : " + x + " ; Top? : " + y + ".");
            
            if(ok) {
                temp = [];
                return;
            }

            temp.push(x, y);
            if(temp.length == 4) {
                
                if(temp[0] > temp[2]) {
                    [temp[0], temp[2]] = [temp[2], temp[0]]; 
                }
                if(temp[1] > temp[3]) {
                    [temp[1], temp[3]] = [temp[3], temp[1]];
                }

                array_of_desks.push(temp)
                console.log(array_of_desks)
                temp = []
            }
        }
    }


    if(document.getElementById('update_desks_button') != null) {
        button = document.getElementById('update_desks_button');

        button.addEventListener("click", (e) => {
            let xhr = new XMLHttpRequest();
            let url = window.location.href;
            
            xhr.open("POST", url, true);

            
            xhr.setRequestHeader("Content-Type", "application/json")
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
            
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    console.log(xhr.responseText);
                }
            };
            
            var data = JSON.stringify({"email": "hey@mail.com", "password": "101010"});
            
            xhr.send(data);
        })
    }

}



window.onload = init;
