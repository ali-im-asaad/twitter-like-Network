document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.edit').forEach(btn => {
        btn.onclick = () => {
            btn.style.display = 'none'
            const bodyDiv = document.querySelector(`#content${btn.dataset.postid}`)
            bodyDiv.innerHTML =
                `<form id="edit-form" class="card-text">
                    <div class="form-group">
                    <textarea class="form-control" id="edit-post-textarea" style="resize: vertical">${bodyDiv.innerHTML}</textarea>
                    </div>
                    <input type="submit" class="btn btn-primary post-submit" value="Save"/>
                </form>`
                
            document.querySelector('#edit-form').onsubmit = () => {
                const content = document.getElementById('edit-post-textarea').value;
                const postId = btn.dataset.postid;
                fetch('/postCollective', {
                    method: 'PUT',
                    body: JSON.stringify({ content, postId })
                }).then(response => response.json())
                    .then(() => {
                        bodyDiv.innerHTML = content
                        btn.style.display = 'block'
                    })

                return false;

            }      
        }
    })
      

    const likeButton = document.querySelectorAll('.like');
    likeButton.forEach(btn => {
        btn.onclick = () => {
            fetch('/postCollective', {
            method: 'PUT',
            body: JSON.stringify({ switchLike: true, postId: btn.dataset.postid })
            }).then(response => response.json())
            .then(result => {
                const likesNum = document.querySelector(`#likes${btn.dataset.postid}`)
                btn.innerHTML = Number(result.number_of_likes) < Number(likesNum.innerHTML) ? "Like" : "Unlike";
                likesNum.innerHTML = result.number_of_likes;
            })
        }
})

      
});

var follow = (user_id) => {
    
    fetch(`/profile/${user_id}/page/1`, {
    method: "POST"
    })
    .then(response => response.json())
    .then(result => {

    const followButton = document.getElementById('follow-btn');
    followButton.innerHTML = result.following_status;

    const followData = document.getElementById('follow-data');
    followData.innerHTML = `Followers: ${result.followers} | Following: ${result.following}`;
    })
    
    false
}


