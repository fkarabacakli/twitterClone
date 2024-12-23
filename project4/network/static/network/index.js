
function like(post_id){
    fetch(`like/${post_id}`, {
        method:"POST",
    })
    .then( response => response.json())
    .then( result => {
        if("error" in result){
            window.alert(result["error"])
        }
        else{
            button = document.getElementById(`like-button-${post_id}`)
            like_count = document.getElementById(`like-count-${post_id}`)
            count = parseInt(like_count.innerHTML)
            if ("like" in result){
                button.innerHTML = "&#128150;";
                like_count.innerHTML = count+1;
            }
            else{
                button.innerHTML = "&#129293;";
                like_count.innerHTML = count-1;
            }
            
        }
    })
}

function follow(user1){
    fetch(`follow/${user1}`, {
        method:"POST"
    })
    .then( response => response.json())
    .then(result => {
        if("error" in result){
            window.alert(result["error"])
        }
        else{
            button = document.getElementById(`follow-button-${user1}`)
            follower = document.getElementById(`follow-count-${user1}`)
            count = parseInt(follower.innerHTML)
            if ("follow" in result){
                button.innerHTML = "Unfollow";
                follower.innerHTML = count +1;
            }
            else{
                button.innerHTML = "Follow";
                follower.innerHTML= count -1 ;
            }
        }
    })
}

function edit(post_id){
    var edit_btn = document.getElementById(`edit-btn-${post_id}`)
    edit_btn.style.display = 'none';

    var data = document.getElementById(`post-text-${post_id}`);
    var data_copy = data.innerHTML;
    data.innerHTML = '';

    var txtArea = document.createElement('textarea');
    txtArea.value = data_copy;
    txtArea.style.width = '100%';
    txtArea.setAttribute('id', `edit-${post_id}`);
    data.appendChild(txtArea);

    var btn_sub = document.createElement('button');
    btn_sub.className = "btn btn-light";
    btn_sub.innerHTML = "Sumbit";
    data.appendChild(btn_sub);
    btn_sub.onclick = ()=> {
        fetch(`/network/${post_id}`, {
            method:'POST',
            body: JSON.stringify({
                text: txtArea.value,
            })
        })
        .then(response => response.json())
        .then(result => {
        if ('error' in result){
            window.alert(result["error"])
        }
        else{
            data.innerHTML = txtArea.value;
            btn_sub.remove;
            txtArea.remove;
            edit_btn.style.display = 'flex';
        }
        })
    }
}

function add_comment(post_id){
    var txtArea = document.getElementById(`txtArea-${post_id}`);
    fetch(`${post_id}/add`, {
        method:'POST',
        body: JSON.stringify({
            text: txtArea.value,
        })
    })
    .then(response => response.json())
    .then(result => {
        if ('error' in result){
            window.alert(result["error"])
        }
        else{
            user = result["user"];
            const new_div = document.createElement("div");
            new_div.classList.add('post');
            new_div.innerHTML = `
            <p>${txtArea.value}</p>
            <h6>${user}</h6>`
            document.querySelector('#comments').prepend(new_div);
            txtArea.value = "";
        }
    })
}
