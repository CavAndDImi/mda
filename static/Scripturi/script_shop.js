
function redir(int){
    
    if(int == 1) location.assign("/login")
    else location.assign("/register")
}
function check_wallet(){
    location.assign(location.pathname + "/wallet")
}
