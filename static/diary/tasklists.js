

var ERROR_SAVING_TASKLIST = 'Error saving the task list';
var newNoteCounter = 0;

function updateTaskList(tasklistId) {
	tasklistElem = document.getElementById("tasklist-" + tasklistId);
	var tasks = [];
	var taskElemArray = Array.from(tasklistElem.children);
	var task;
	taskElemArray.forEach((taskElem) => {
		task = {
			text: taskElem.getAttribute('data-text'),
			is_finished: taskElem.classList.contains('finished')};
			
		tasks.push(task);
	});
	

	fetch(window.location.origin + '/diaries/update-task-list/' + tasklistId, {
		method: 'post',
		headers: {
		'Accept': '*/*',
		'Content-Type': 'application/json',
		'X-CSRFToken': window.CSRF_TOKEN
		},
		body: JSON.stringify(tasks)
	})
		.then(response => {
			if(response.ok) {
				alert('Task list has been successfully saved.')
			}
			else {
				alert(ERROR_SAVING_TASKLIST + '- ' + response.statusText);
			}
			
		})
		.catch(error => alert(ERROR_SAVING_TASKLIST + '- ' + error));
}

function taskClicked(taskElem) {
	iconElem = taskElem.querySelector('i');
	
	if(taskElem.classList.contains('finished')) {
		taskElem.classList.remove('finished');
		iconElem.classList.add('hidden');
	}
	else {
		taskElem.classList.add('finished');
		iconElem.classList.remove('hidden');
		console.log(taskElem);
		console.log(iconElem);
	}
}

function addTask(tasklistId) {
	newNoteCounter++;
	
	var taskTA = document.getElementById('taskTA-' + tasklistId);
	if(taskTA.value === "") {
		alert("Task content cannot be empty");
		return;
	}
	tasklistElem = document.getElementById("tasklist-" + tasklistId);
	var buttonElem = document.createElement("button");
	buttonElem.className = "list-group-item list-group-item-action d-flex justify-content-between";
	buttonElem.onclick = function(event) {
		taskClicked(event.currentTarget);
	}
	buttonElem.setAttribute("data-text", taskTA.value);
	buttonElem.id = `new-task-${newNoteCounter}`;
	//wrap it so that inner text can be set so that line breaks are kept
	/*var textWrapper = document.createElement("div");
	textWrapper.innerText = taskTA.value;
	
	buttonElem.innerHTML = '<i class="fas fa-check hidden"></i>';
	buttonElem.appendChild(textWrapper);*/
	buttonElem.innerHTML = `<div class="d-flex align-items-center gap-2">
                    <i class="fas fa-check hidden"></i>
                    <div class="task-text">${taskTA.value}</div>
                </div>
                <div onclick="deleteTask('${buttonElem.id}')">
                    <i class="fas fa-times"></i>
                </div>`
	tasklistElem.appendChild(buttonElem);
	taskTA.value = "";
}

function deleteTask(taskElemId) {
	var taskElem = document.getElementById(taskElemId);
	taskElem.parentElement.removeChild(taskElem);
}
	