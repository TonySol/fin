




//universal modal
var uniModal = document.getElementById("uniModal");
var closeBtn = document.getElementsByClassName("close")[0];

var delBtn = document.getElementsByClassName("delBtn");
var editBtn = document.getElementsByClassName("editBtn");


// When the user clicks on <span> (x), close the modal
closeBtn.onclick = function() {
  uniModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == uniModal) {
    uniModal.style.display = "none";
  }
}
let clsEditLen = editBtn.length;
for (let i = 0; i < clsEditLen; i++) {
editBtn[i].onclick = function() {
  uniModal.style.display = "block";

  var entryId = editBtn[i].getAttribute('entry-id');
  var userName = editBtn[i].getAttribute('user-name');

  var modalTitle = uniModal.querySelector('#modal-title');
  var contentEdit = uniModal.querySelector('.modal-content p');
  var tableContent = uniModal.querySelector('.table');
  var modalStyle = uniModal.querySelector('#modal-styling');
  var btnSubmit = uniModal.querySelector('#btn-submit');

  modalTitle.textContent = "Edit entry";
  contentEdit.textContent = "What data of " + userName + "'s you want to change?";
  tableContent.setAttribute('style', 'display: block');
  modalStyle.setAttribute('class', 'modal-dialog modal-xl');
  btnSubmit.setAttribute('class', 'btn btn-warning');
  btnSubmit.textContent = "Apply Changes"
}}

let clsLen = delBtn.length;
for (let i = 0; i < clsLen; i++) {
    delBtn[i].onclick = function() {
      uniModal.style.display = "block";

      var entryId = delBtn[i].getAttribute('entry-id');
      var userName = delBtn[i].getAttribute('user-name');

      var modalTitle = uniModal.querySelector('#modal-title');
      var contentEdit = uniModal.querySelector('.modal-content p');
      var hiddenIdInput = uniModal.querySelector('.modal-body input');
      var tableContent = uniModal.querySelector('.table');
      var modalStyle = uniModal.querySelector('#modal-styling');
      var btnSubmit = uniModal.querySelector('#btn-submit');

      modalTitle.textContent = "Delete entry";
      contentEdit.textContent = "Are you sure you want to delete " + userName + "'s data?";
      hiddenIdInput.value = entryId;
      tableContent.setAttribute('style', 'display: none');
      modalStyle.setAttribute('class', 'modal-dialog');
      btnSubmit.setAttribute('class', 'btn btn-danger');
      btnSubmit.textContent = "Delete"

}}



