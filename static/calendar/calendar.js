
function generate_year_range(start, end) {
  var years = "";
  for (var year = start; year <= end; year++) {
      years += "<option value='" + year + "'>" + year + "</option>";
  }
  return years;
}

var today = new Date();	
var currentDate = today.getDate();
var currentMonth = today.getMonth();
var currentYear = today.getFullYear();
var selectMonth, selectYear, monthAndYear;


var createYear = generate_year_range(currentYear - 40, currentYear + 40);

document.getElementById("year").innerHTML = createYear;

var calendar = document.getElementById("calendar");
var lang = calendar.getAttribute('data-lang');

var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

var dayHeader = "<tr>";
for (day in days) {
  dayHeader += "<th data-days='" + days[day] + "'>" + days[day] + "</th>";
}
dayHeader += "</tr>";

document.getElementById("thead-month").innerHTML = dayHeader;


function next() {
  currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
  currentMonth = (currentMonth + 1) % 12;
  showCalendar();
}

function previous() {
  currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
  currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
  showCalendar();
}

function jump() {
  currentYear = parseInt(selectYear.value);
  currentMonth = parseInt(selectMonth.value);
  showCalendar();
}

function showCalendar() {

  var firstDay = ( new Date( currentYear, currentMonth ) ).getDay();

  tbl = document.getElementById("calendar-body");

  
  tbl.innerHTML = "";

  
  monthAndYear.innerHTML = months[currentMonth] + " " + currentYear;
  selectYear.value = currentYear;
  selectMonth.value = currentMonth;

  // creating all cells
  var date = 1;
  for ( var i = 0; i < 6; i++ ) {
      var row = document.createElement("tr");

      for ( var j = 0; j < 7; j++ ) {
          if ( i === 0 && j < firstDay ) {
              cell = document.createElement( "td" );
              cellText = document.createTextNode("");
              cell.appendChild(cellText);
              row.appendChild(cell);
          } else if (date > daysInMonth(currentMonth, currentYear)) {
              break;
          } else {
              cell = document.createElement("td");
              cell.setAttribute("data-date", date);
              cell.setAttribute("data-month", currentMonth + 1);
              cell.setAttribute("data-year", currentYear);
              cell.setAttribute("data-month_name", months[currentMonth]);
              cell.className = "date-picker";
              cell.innerHTML = date; //"<span>" + date + "</span>"; //the click event didn't bubble up from the span for some reason...

			  cell.id = "date-" + date;
              cell.onclick= function(event) {
				  selectChapter(event.target)
			  }

              if (date === currentDate) {
                  cell.className = "date-picker selected";
              }
              row.appendChild(cell);
              date++;
          }


      }

      tbl.appendChild(row);
  }

}

function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
    //this should work as well: return new Date(iYear, iMonth + 1, 0).getDate();
}


//my additions:
function fetchChapter() {
    var chapterPath = `chapter/${currentDate}/${currentMonth + 1}/${currentYear}/json`;
	var regex = new RegExp(/chapter\/[0-9]+\/[0-9]+\/[0-9]+.*/);
	var url;
	if(regex.test(window.location.href)) {
		url = window.location.href.replace(regex, chapterPath);
	}
	else {
		url = new URL(chapterPath, window.location.href).toString();
	}

	if(window.history) {
		var shownUrl = url.replace(/\/json.*/, "");
		//console.log(shownUrl);
		history.pushState({}, null, shownUrl);
	}
	//console.log(url);
	//var url = new URL(chapterPath, window.location.href);

    fetch(url)
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        //console.log(data);
        let storiesElem = document.getElementById("stories");
        let notesElem = document.getElementById("notes");
        let tasklitsElem = document.getElementById("tasklists");
        storiesElem.innerHTML = data.stories;
        notesElem.innerHTML = data.notes;
        tasklitsElem.innerHTML = data.tasklists;
    });
}

function selectChapter(cell) {
    selected = document.getElementsByClassName("date-picker selected");
    if (selected.length > 0) {
        selected[0].classList.remove("selected");
    }
    cell.classList.add("selected");
	/*var date = cell.getAttribute('data-date');
	var month = cell.getAttribute('data-month');
	var year = cell.getAttribute('data-year');*/
	currentDate = parseInt(cell.getAttribute('data-date'));

	fetchChapter();
}


//load the chapter for the current day once the html document is loaded (css etc. doesn'tt have to be loaded)
document.addEventListener("DOMContentLoaded", function(){
	var chapterElem = document.getElementById('chapter');
	var date = chapterElem.getAttribute('data-date');
	if(date) {
		currentDate = parseInt(date);
		currentMonth = parseInt(chapterElem.getAttribute('data-month')) - 1;
		currentYear = parseInt(chapterElem.getAttribute('data-year'));
	}
	
	selectYear = document.getElementById("year");
	selectMonth = document.getElementById("month");
	monthAndYear = document.getElementById("monthAndYear");

	
	fetchChapter();
	showCalendar();
});


function buildChapterUrl(path) {
	var chapterPath = `chapter/${currentDate}/${currentMonth + 1}/${currentYear}/${path}`;
	var url = new URL(chapterPath, window.location.href);
	return url;
}

/*function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');*/


/*function modifyNote(id) {
    var noteElem = document.getElementById(id);
	var originalNoteHTML = noteElem.innerHTML;
	var formElem = document.createElement("form");
	formElem.method = "POST";
	formElem.action = buildChapterUrl("update-note").toString();
	var textArea = document.createElement("textarea");
	textArea.value = noteElem.innerText;
	textArea.className = "form-control";
	textArea.rows = noteElem.offsetHeight / 16;
	
	var submitBtn = document.createElement("input");
	submitBtn.type = "submit";
	submitBtn.className = "btn btn-primary";
	submitBtn.value = "Confirm";
	//in case it was sent dynamically:
	// submitBtn.addEventListener('click', function() {
		// //set last modified date
		// var now = new Date();
		// var timeStr = now.getHours() + ':' + now.getMinutes();
		// documentElement.getElementById('last-modified').innerHTML = timeStr;
		// noteElem.innerHTML = originalNoteHTML;
	// });
	
	var cancelBtn = document.createElement("input");
	cancelBtn.type = "button";
	cancelBtn.className = "btn btn-secondary";
	cancelBtn.value = "Cancel";
	cancelBtn.addEventListener('click', function() {
		noteElem.innerHTML = originalNoteHTML;
	});

    var textAreaP = document.createElement("p");
    textAreaP.appendChild(textArea);
	formElem.appendChild(textAreaP);
	var btnDiv = document.createElement("div");
	btnDiv.className = "d-flex flex-row-reverse gap-2";
	btnDiv.appendChild(submitBtn);
	btnDiv.appendChild(cancelBtn);
	formElem.appendChild(btnDiv);
	noteElem.innerHTML = "";
	noteElem.appendChild(formElem);

}*/


function modifyNote(id) {
	var noteText = document.getElementById(`note-text-${id}`);
	var approxRows = noteText.offsetHeight / 16;
	noteText.style.display = 'none';
	var noteForm = document.getElementById(`note-form-${id}`);
	noteForm.style.display = 'block';
	var noteTextarea = document.getElementById(`note-textarea-${id}`);
	noteTextarea.value = noteText.innerText;
	noteTextarea.rows = approxRows;
	
}

function cancelNoteModification(id) {
	noteText = document.getElementById(`note-text-${id}`);
	noteText.style.display = 'block';
	noteForm = document.getElementById(`note-form-${id}`);
	noteForm.style.display = 'none';
}

function jumpToToday() {
	currentDate = today.getDate();
	currentMonth = today.getMonth();
	currentYear = today.getFullYear();
	fetchChapter();
	showCalendar();
}


function deleteNote(note_id) {
    var result = confirm("Are you sure you want to delete the note?");
    if (result) {
        document.getElementById("deleteNoteForm-" + note_id ).submit();
    }

}
