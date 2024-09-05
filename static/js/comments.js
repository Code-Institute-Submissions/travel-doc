const commentText = document.getElementById("id_body");
const commentForm = document.getElementById("commentForm");
const submitButton = document.getElementById("submitButton");

const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteConfirm = document.getElementById("deleteConfirm");

/**
* Initializes edit functionality for the provided edit buttons.
* 
* For each button in the `editButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Fetches the content of the corresponding comment.
* - Populates the `commentText` input/textarea with the comment's content for editing.
* - Updates the submit button's text to "Update".
* - Sets the form's action attribute to the `edit_comment/{commentId}` endpoint.
*/
for (let button of document.querySelectorAll(".btn-edit[comment_id]")){
  button.addEventListener("click", (e) => {
    let commentId = e.target.getAttribute("comment_id");
    let commentContent = document.getElementById(`comment${commentId}`).innerText;
    commentText.value = commentContent;
    submitButton.innerText = "Update";
    commentForm.setAttribute("action", `edit_comment/${commentId}`);
  });
}

/**
* Initializes deletion functionality for the provided delete buttons.
* 
* For each button in the `deleteButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Updates the `deleteConfirm` link's href to point to the 
* deletion endpoint for the specific comment.
* - Displays a confirmation modal (`deleteModal`) to prompt 
* the user for confirmation before deletion.
*/
for (let button of document.querySelectorAll(".btn-delete[comment_id]")) {
  button.addEventListener("click", (e) => {
    let commentId = e.target.getAttribute("comment_id");
    deleteConfirm.href = `delete_comment/${commentId}`;
    deleteModal.show();
  });
}


// For job deletion
for (let button of document.querySelectorAll(".btn-delete[job_id]")) {
  button.addEventListener("click", (e) => {
    const jobId = e.target.getAttribute("job_id");
    console.log('Deleting job with ID: ${jobId');
    if(jobId){
      deleteConfirm.href = `/job/${jobId}/delete/`;
      deleteModal.show();
    } else {
        console.log("Job ID is missing or invalid.")
    }
  });
};


//For deletion of Job Applications
for (let button of document.querySelectorAll(".btn-delete[data-id]")) {
  button.addEventListener("click", (e) => {
    const appId= e.target.getAttribute("data-id");
    if (appId) {
      // Generate the correct URL for deletion
      deleteConfirm.href = `/job_application/${appId}/delete/`;
      deleteModal.show();
    } else {
      console.error("Application ID is missing or invalid.");
    }
  });
}


//For deletion of Posts
for (let button of document.querySelectorAll(".btn-delete[post_id]")) {
  button.addEventListener("click", (e) => {
    let postId = e.target.getAttribute("post_id");
    deleteConfirm.href = `/post/${postId}/delete/`;
    deleteModal.show();
  });
}