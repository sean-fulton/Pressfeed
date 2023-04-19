function editComment(commentId) {
  var editBtn = document.getElementById("edit-comment-btn")
  var deleteBtn = document.getElementById("delete-comment-btn")
  var commentText = document.getElementById("comment-" + commentId + "-text");
  var editForm = document.getElementById("edit-comment-form-" + commentId);
  commentText.style.resize = "none";
  // commentText.style.width = "350px"
  editBtn.style.display = "none";
  deleteBtn.style.display = "none";
  editForm.style.display = "block";
}

function hideForm(commentId) {
  var editBtn = document.getElementById("edit-comment-btn")
  var deleteBtn = document.getElementById("delete-comment-btn")
  var form = document.getElementById("edit-comment-form-" + commentId);
  editBtn.style.display = "block";
  deleteBtn.style.display = "block";
  form.style.display = "none";
}