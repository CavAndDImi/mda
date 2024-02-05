
function redir(int){
    
    if(int == 1) location.assign("/login")
    else location.assign("/register")
}
function check_wallet(){
    location.assign(location.pathname + "/wallet")
}
function info(){
    location.assign("/info")
}
function work(){
    location.assign(location.pathname + "/proof-of-work")
}
function friends(){
    location.assign(location.pathname + "/friends")
}

function shop(){
    location.assign(location.pathname + "/shop")
}

function tranz(){
    location.assign(location.pathname + "/transactions")
}

function addF(){
    if(document.getElementById('addF').value == 0){
        document.getElementById('addFr').style.display = '';
        document.getElementById('addFrSub').style.display = '';
        document.getElementById('msg').style.display = '';
        document.getElementById('addF').value = 1;}
    else{
        document.getElementById('addFr').style.display = 'none';
        document.getElementById('addFrSub').style.display = 'none';
        document.getElementById('msg').style.display = 'none';
        document.getElementById('addF').value = 0;
    }
}