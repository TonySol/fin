//universal modal
var uniModal = document.getElementById("uniModal");
var closeBtn = document.getElementsByClassName("close")[0];

var delBtn = document.getElementsByClassName("delBtn");
var editBtn = document.getElementsByClassName("editBtn");
var addBtn = document.getElementById("addBtn");

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

      const entryId = editBtn[i].getAttribute('entry-id');
      const userName = editBtn[i].getAttribute('user-name');

      const modalTitle = uniModal.querySelector('#modal-title');
      const contentEdit = uniModal.querySelector('.modal-content p');
      const hiddenIdInput = uniModal.querySelector('.modal-body input');
      const tableContent = uniModal.querySelector('.table');
      const modalStyle = uniModal.querySelector('#modal-styling');
      const actionForm = uniModal.querySelector('form');
      const btnSubmit = uniModal.querySelector('#btn-submit');
      const inputRow = uniModal.querySelectorAll('.main-input');

      modalTitle.textContent = "Edit entry";
      contentEdit.textContent = "What details about " + userName + " do you want to edit?";
      hiddenIdInput.value = entryId;
      tableContent.setAttribute('style', 'display: block');
      modalStyle.setAttribute('class', 'modal-dialog modal-xl');
      btnSubmit.setAttribute('class', 'btn btn-warning');
      actionForm.setAttribute('action', '/employees/edit');
      btnSubmit.textContent = "Apply Changes";

      inputRow.forEach(make);
      function make(inpt){
        inpt.removeAttribute('required')
      }
  }
}

addBtn.onclick = function() {
  uniModal.style.display = "block";

  const modalTitle = uniModal.querySelector('#modal-title');
  const contentEdit = uniModal.querySelector('.modal-content p');
  const hiddenIdInput = uniModal.querySelector('.modal-body input');
  const tableContent = uniModal.querySelector('.table');
  const modalStyle = uniModal.querySelector('#modal-styling');
  const actionForm = uniModal.querySelector('form');
  const btnSubmit = uniModal.querySelector('#btn-submit');
  const inputRow = uniModal.querySelectorAll('.main-input');

  modalTitle.textContent = "Add new entry";
  contentEdit.textContent = "Please fill in all fields carefully";
  hiddenIdInput.removeAttribute("name");
  tableContent.setAttribute('style', 'display: block');
  modalStyle.setAttribute('class', 'modal-dialog modal-xl');
  btnSubmit.setAttribute('class', 'btn btn-warning');
  actionForm.setAttribute('action', '/employees/add');
  btnSubmit.textContent = "Add new entry";

  inputRow.forEach(make);
  function make(inpt){
    inpt.setAttribute('required', '')
  }
}


let clsLen = delBtn.length;
for (let i = 0; i < clsLen; i++) {
    delBtn[i].onclick = function() {
      uniModal.style.display = "block";

      const entryId = delBtn[i].getAttribute('entry-id');
      const userName = delBtn[i].getAttribute('user-name');

      const modalTitle = uniModal.querySelector('#modal-title');
      const contentEdit = uniModal.querySelector('.modal-content p');
      const hiddenIdInput = uniModal.querySelector('.modal-body input');
      const tableContent = uniModal.querySelector('.table');
      const modalStyle = uniModal.querySelector('#modal-styling');
      const actionForm = uniModal.querySelector('form');
      const btnSubmit = uniModal.querySelector('#btn-submit');
      const inputRow = uniModal.querySelectorAll('.main-input');

      modalTitle.textContent = "Delete entry";
      contentEdit.textContent = "Are you sure you want delete " + userName + "'s data?";
      hiddenIdInput.value = entryId;
      tableContent.setAttribute('style', 'display: none');
      modalStyle.setAttribute('class', 'modal-dialog');
      btnSubmit.setAttribute('class', 'btn btn-danger');
      actionForm.setAttribute('action', '/employees/delete');
      btnSubmit.textContent = "Delete";

      inputRow.forEach(make);
      function make(inpt){
        inpt.removeAttribute('required')
      }
    }
}



