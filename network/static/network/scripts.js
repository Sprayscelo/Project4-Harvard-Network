document.addEventListener("DOMContentLoaded", function () {
    
        let editPosts = document.querySelectorAll(`#editPost`)
        editPosts.forEach(i => {
            i.addEventListener(`click`, e => {
                let content = e.target.previousElementSibling
                if (e.target.innerHTML === `Edit`) {                    e.target.innerHTML = `Save`
                    content.innerHTML = `<textarea id="textAreaSet"> ${content.innerText}</textarea>`
                    console.log(e.target.parentElement.dataset.id)
                }
                else {
                    let newContent = document.querySelector("#textAreaSet").value
                    console.log(newContent)
                    fetch(`editPost/${e.target.parentElement.dataset.id}`, {
                        method: "PUT",
                        headers: {
                            "Content-Type": `application/json`
                        },
                        body: JSON.stringify({
                            content: newContent
                        })
                    })
                    e.target.innerHTML = `Edit`
                    content.innerHTML = `${newContent}`
                }
                
            }) 
        })
            let likeicon = document.querySelectorAll(".likeIcon")
            likeicon.forEach( i => { 
                i.addEventListener("click", e => {
                let icone = e.target.parentElement
                console.log(e.target.dataset)
                like(e.target.dataset.id, e.target.dataset.user, icone)
            })
        })
    })

function followUsuario(newFollowUser) {
            fetch(`${newFollowUser}`, {
                method: "PUT",
                body: JSON.stringify({
                    following: newFollowUser
                })
            })
        }

function like(postID, user, icon) {
    if (icon.attributes.fill.value == "red") {
        icon.attributes.fill.value = "black"
    }
    else {
        icon.attributes.fill.value = "red"
    }
    console.log(postID)
    fetch(`/following`, {
        method: "PUT",
        body: JSON.stringify({
            id: postID,
            likes: user
        })
    }).then(response => {
        location.reload()
    })
}