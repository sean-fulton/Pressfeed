console.log("select_all_button.js loaded");

const selectAllButton = document.getElementById('select-all-button');
const checkboxes = document.querySelectorAll('#subscription-form input[type=checkbox]');

selectAllButton.addEventListener('click', () => {
    let numChecked = 0;
    // check if all boxes are currently checked
    checkboxes.forEach((checkbox) => {
        if(checkbox.checked) {
            numChecked = numChecked + 1;
        }
    });

    if (numChecked == checkboxes.length) {
        checkboxes.forEach((checkbox) => {
           checkbox.checked = false;
        });
    } else {
        checkboxes.forEach((checkbox) => {
           checkbox.checked = true;
        });
    }
});
