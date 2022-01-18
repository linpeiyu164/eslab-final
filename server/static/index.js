var eventSource = new EventSource("/listen")

data_source = document.querySelector("false_control")

async function controlSend(){
    const data = { camera : 'left', direction : 'forward' }
    try{
        const res = await fetch('/control', {
            body : JSON.stringify(data),
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, same-origin, *omit
            headers: {
            'user-agent': 'Mozilla/4.0 MDN Example',
            'content-type': 'application/json'
            },
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, cors, *same-origin
            redirect: 'follow', // manual, *follow, error
            referrer: 'no-referrer', // *client, no-referrer
        })
        console.log(res)
    }catch(err){
        console.log(err)
    }
}

async function infoSend(){
    const data = { name : "Exhibit2" }
    try{
        const res = await fetch('/info', {
            body : JSON.stringify(data),
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, same-origin, *omit
            headers: {
            'user-agent': 'Mozilla/4.0 MDN Example',
            'content-type': 'application/json'
            },
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, cors, *same-origin
            redirect: 'follow', // manual, *follow, error
            referrer: 'no-referrer', // *client, no-referrer
        })
        console.log(res)
    }catch(err){
        console.log(err)
    }
}

eventSource.addEventListener("message", e => {
    console.log(e.data)
}, false)

eventSource.addEventListener("online", e => {
    data = JSON.parse(e.data)
    console.log(data)
    if(data.name != '' &&  data.info != ''){
        document.querySelector("#information_div").style.display = 'block'
        document.querySelector("#information_title").innerHTML = data.name
        document.querySelector("#information_body").innerHTML = data.info
        if(data.img != "No nearby"){
            document.querySelector("#image").src = "/static/"+data.img
        }
        
    }
    document.querySelector("#direction").innerHTML = data.direction
    // document.querySelector("#camera").innerHTML = data.camera
})

