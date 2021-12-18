var exampleModal = document.getElementById('deleteModal')
exampleModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  var button = event.relatedTarget
  // Extract info from data-bs-* attributes
  var entryId = button.getAttribute('entry-id')
  var userName = button.getAttribute('user-name')
  // If necessary, you could initiate an AJAX request here
  // and then do the updating in a callback.
  //
  // Update the modal's content.
  var modalBodyInput = exampleModal.querySelector('.modal-body input')
  var modalTextMessage = exampleModal.querySelector('.modal-body p')

  modalBodyInput.value = entryId
  modalTextMessage.textContent = "Are you sure you want to delete " + userName + "'s data"

})

var editModal = document.getElementById('editModal')
editModal.addEventListener('show.bs.modal', function (event) {
  var button = event.relatedTarget

  var entryId = button.getAttribute('entry-id')
  var userName = button.getAttribute('user-name')

  var modalBodyInput = editModal.querySelector('.modal-body input')
  var modalTextMessage = editModal.querySelector('.modal-body p')

  modalBodyInput.value = entryId
  modalTextMessage.textContent = "How would you like to edit " + userName + "'s data"

})

