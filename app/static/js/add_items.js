document.addEventListener('DOMContentLoaded', function() {
    var addTagButton = document.getElementById('addTagBtn');
    var addIngredientButton = document.getElementById('addIngredientBtn');

    addTagButton.addEventListener('click', function() {
        toggleTextField('newTag', 'Legg til ny kategori', addTagButton);
    });

    addIngredientButton.addEventListener('click', function() {
        toggleTextField('newIngredient', 'Legg til ny ingrediens', addIngredientButton);
    });

    function toggleTextField(name, placeholder, button) {
        var existingFormGroup = document.getElementById(name + 'FormGroup');
        
        if (existingFormGroup) {
            existingFormGroup.remove();
        } else {
            createTextField(name, placeholder, button);
        }
    }

    function createTextField(name, placeholder, button) {
        var newInput = document.createElement('input');
        newInput.type = 'text';
        newInput.name = name;
        newInput.placeholder = placeholder;
        newInput.className = 'form-control';
    
        var addButton = document.createElement('button');
        addButton.type = 'button';
        addButton.innerText = 'Legg til';
        addButton.className = 'btn btn-primary';
    
        addButton.addEventListener('click', function() {
            var inputValue = newInput.value;
            var itemType = (name === 'newTag' ? 'tag' : 'ingredient');
            sendAjaxRequest(inputValue, itemType);
            newInput.value = '';
        });
    
        var inputGroup = document.createElement('div');
        inputGroup.className = 'col-8';
        inputGroup.appendChild(newInput);
    
        var buttonGroup = document.createElement('div');
        buttonGroup.className = 'col-4';
        buttonGroup.appendChild(addButton);
    
        var formGroup = document.createElement('div');
        formGroup.id = name + 'FormGroup';
        formGroup.className = 'form-group row';
        formGroup.appendChild(inputGroup);
        formGroup.appendChild(buttonGroup);
    
        button.parentNode.insertBefore(formGroup, button.nextSibling);
    }
    

    function sendAjaxRequest(value, type) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/recipe/additem/', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

        xhr.onload = function() {
            if (xhr.status === 200 || xhr.status === 201) {
                console.log('Item added:', xhr.responseText);
                updateSelectList(value, type)
            } else {
                console.error('Error adding item:', xhr.status, xhr.statusText);
            }
        };

        xhr.send('type=' + encodeURIComponent(type) + '&value=' + encodeURIComponent(value));
    }

    function updateSelectList(value, type) {
        var selectId = (type === 'tag' ? 'tagsSelect' : 'ingredientsSelect');
        var selectElement = document.getElementById(selectId);
        
        if (selectElement) {
            var newOption = document.createElement('option');
            newOption.value = value;
            newOption.text = value;
            newOption.selected = true;
            selectElement.appendChild(newOption);
        }
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var selectElement = document.getElementById('ingredientsSelect');
    if (selectElement) {
        selectElement.addEventListener('mousedown', function(event) {
            event.preventDefault();
            var option = event.target;
            if (option.tagName === 'OPTION') {
                option.selected = !option.selected;
            }
        });

        selectElement.addEventListener('mousemove', function(event) {
            event.preventDefault();
        });
    }
});
