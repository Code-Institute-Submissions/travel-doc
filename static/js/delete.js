document.addEventListener("DOMContentLoaded", function() {
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    const deleteConfirm = document.getElementById("deleteConfirm");
  
    // For comment deletion
    document.querySelectorAll(".btn-delete[comment_id]").forEach(button => {
      button.addEventListener("click", (e) => {
        e.preventDefault();
        const commentId = e.target.getAttribute("comment_id");
        deleteConfirm.href = `delete_comment/${commentId}`;
        deleteModal.show();
      });
    });
  
    // For job deletion
    document.querySelectorAll(".btn-delete[job_id]").forEach(button => {
      button.addEventListener("click", (e) => {
        e.preventDefault();
        const jobId = e.target.getAttribute("job_id");
        deleteConfirm.href = `/job/${jobId}/delete/`;
        deleteModal.show();
      });
    });
  
    // For job application deletion
    document.querySelectorAll(".btn-delete[data-id]").forEach(button => {
      button.addEventListener("click", (e) => {
        e.preventDefault();
        const appId = e.target.getAttribute("data-id");
        deleteConfirm.href = `/job_application/${appId}/delete/`;
        deleteModal.show();
      });
    });
  
    // For post deletion
    document.querySelectorAll(".btn-delete[post_id]").forEach(button => {
      button.addEventListener("click", (e) => {
        e.preventDefault();
        const postId = e.target.getAttribute("post_id");
        deleteConfirm.href = `/post/${postId}/delete/`;
        deleteModal.show();
      });
    });
  });
  