let video;
let canvas;
let nameInput;

function init(){
    video = document.getElementById("video")
    canvas = document.getElementById("canvas")
    nameInput = document.getElementById("name")

    navigator.mediaDevices.getUserMedia({video:true})
        .then(stream=>{
            video.srcObject = stream
        })
        .catch(error=>{
            console.log("error access webcam", error)
            alert("Can't Access Webcam")
        })
}

function capture(){
    const context = canvas.getContext("2d")
    context.drawImage(video,0,0,canvas.width,canvas.height)
    canvas.style.display = "block"
    video.style.display = "none"
}

function register(){
    const name = nameInput.value
    const photo = dataURItoBlob(canvas.toDataURL())

    if(!name || !photo){
        alert("Please provide your name and photo")
        return
    }
    const formData = new FormData()
    formData.append("name", name)
    formData.append("photo",photo, `${name}.jpg`)

    fetch("/register",{
        method:"POST",
        body:formData
    })

    .then(response=>response.json())
    .then(data=>{
        if(data.success){
            alert("Information Succesfully Registered")
            window.location.href = "/"
        }else{
            alert("Failed to Register")
        }

    })
    .catch(error=>{
        console.log("error", error)
    })
}

function login(){
    const context = canvas.getContext("2d")
    context.drawImage(video,0,0, canvas.width, canvas.height)
    const photo = dataURItoBlob(canvas.toDataURL())

    if(!photo){
        alert("Please provide a photo")
        return
    }
    const formData = new FormData()
    formData.append("photo",photo,"login.jpg")

    fetch("/login",{
        method:"POST",
        body:formData
    })

    .then(response=>response.json())
    .then(data=>{
        console.log(data)
        if(data.success){
            alert("Login Succesful! Welcome")
            window.location.href = "/success?user_name=" + nameInput.value
        }else{
            alert("Loin Failed :/ Please Try Again")
        }
    }).catch(error=>{
        console.log("error", error)
    })
}

function dataURItoBlob(dataURI){
    const byteString = atob(dataURI.split(",")[1])
    const mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0]

    const ab = new ArrayBuffer(byteString.length)
    const ia = new Uint8array(ab)
    for (let i = 0; i < byteString.length; i++){
        ia[i] = byteString.charCodeAt(i)
    }
    return new Blob([ab],{type:mimeString})
}
init()
