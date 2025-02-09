/*     Version: $Revision: 970 $
      (C) COPYRIGHT 2015-2022   Ahasuerus
         ALL RIGHTS RESERVED
      Date: $Date: 2022-08-15 12:47:52 -0400 (Mon, 15 Aug 2022) $ */

document.addEventListener('DOMContentLoaded', function() {
	var title = document.title;
	createOnclick(title);
});

function createOnclick(title)	{
	if (document.getElementById('divothersites')) {
		document.getElementById('divothersites').onclick = function(event){
			void(0);
		};
	}

	if (document.getElementById('external_id.addsign')) {
		document.getElementById('external_id.addsign').onclick = function(event){
			addNewExternalID('external_id');
		};
	}

	if (document.getElementById('trans_names.addsign')) {
		document.getElementById('trans_names.addsign').onclick = function(event){
			AddMultipleField('Transliterated Name', 'trans_names');
		};
	}

	if (document.getElementById('trans_legal_names.addsign')) {
		document.getElementById('trans_legal_names.addsign').onclick = function(event){
			AddMultipleField('Trans. Legal Name', 'trans_legal_names');
		};
	}

	if (document.getElementById('author_webpages.addsign')) {
		document.getElementById('author_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'author_webpages');
		};
	}

	if (document.getElementById('publisher_webpages.addsign')) {
		document.getElementById('publisher_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'publisher_webpages');
		};
	}

	if (document.getElementById('pub_series_webpages.addsign')) {
		document.getElementById('pub_series_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'pub_series_webpages');
		};
	}

	if (document.getElementById('title_webpages.addsign')) {
		document.getElementById('title_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'title_webpages');
		};
	}

	if (document.getElementById('shared_title_webpages.addsign')) {
		document.getElementById('shared_title_webpages.addsign').onclick = function(event){
			AddMultipleField('Title Web Page', 'shared_title_webpages');
		};
	}

	if (document.getElementById('shared_pub_webpages.addsign')) {
		document.getElementById('shared_pub_webpages.addsign').onclick = function(event){
			AddMultipleField('Pub Web Page', 'shared_pub_webpages');
		};
	}

	if (document.getElementById('pub_webpages.addsign')) {
		document.getElementById('pub_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'pub_webpages');
		};
	}

	if (document.getElementById('award_type_webpages.addsign')) {
		document.getElementById('award_type_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'award_type_webpages');
		};
	}

	if (document.getElementById('award_cat_webpages.addsign')) {
		document.getElementById('award_cat_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'award_cat_webpages');
		};
	}

	if (document.getElementById('series_webpages.addsign')) {
		document.getElementById('series_webpages.addsign').onclick = function(event){
			AddMultipleField('Web Page', 'series_webpages');
		};
	}

	if (document.getElementById('author_emails.addsign')) {
		document.getElementById('author_emails.addsign').onclick = function(event){
			AddMultipleField('Email Address', 'author_emails');
		};
	}

	if (document.getElementById('title_author.addsign')) {
		document.getElementById('title_author.addsign').onclick = function(event){
			AddMultipleField('Author', 'title_author');
		};
	}

	if (document.getElementById('trans_titles.addsign')) {
		document.getElementById('trans_titles.addsign').onclick = function(event){
			AddMultipleField('Transliterated Title', 'trans_titles');
		};
	}

	if (document.getElementById('pub_author.addsign')) {
		document.getElementById('pub_author.addsign').onclick = function(event){
			AddMultipleField('Author', 'pub_author');
		};
	}

	if (document.getElementById('trans_publisher_names.addsign')) {
		document.getElementById('trans_publisher_names.addsign').onclick = function(event){
			AddMultipleField('Transliterated Name', 'trans_publisher_names');
		};
	}

	if (document.getElementById('trans_pub_series_names.addsign')) {
		document.getElementById('trans_pub_series_names.addsign').onclick = function(event){
			AddMultipleField('Transliterated Name', 'trans_pub_series_names');
		};
	}

	if (document.getElementById('trans_series_names.addsign')) {
		document.getElementById('trans_series_names.addsign').onclick = function(event){
			AddMultipleField('Transliterated Name', 'trans_series_names');
		};
	}

	if (document.getElementById('interviewee_author1..addsign')) {
		document.getElementById('interviewee_author1..addsign').onclick = function(event){
			AddMultipleField('Interviewee', 'interviewee_author1.');
		};
	}

	if (document.getElementById('interviewer_author1..addsign')) {
		document.getElementById('interviewer_author1..addsign').onclick = function(event){
			AddMultipleField('Interviewer', 'interviewer_author1.');
		};
	}

	if (document.getElementById('review_author1..addsign')) {
		document.getElementById('review_author1..addsign').onclick = function(event){
			AddMultipleField('Author', 'review_author1.');
		};
	}

	if (document.getElementById('review_reviewer1..addsign')) {
		document.getElementById('review_reviewer1..addsign').onclick = function(event){
			AddMultipleField('Reviewer', 'review_reviewer1.');
		};
	}

	if (document.getElementById('tag_name.addsign')) {
		document.getElementById('tag_name.addsign').onclick = function(event){
			AddMultipleField('Tag', 'tag_name');
		};
	}

	if (document.getElementById('ImportTitles.addsign')) {
		document.getElementById('ImportTitles.addsign').onclick = function(event){
			AddMultipleField('Title', 'ImportTitles');
		};
	}

	if (document.getElementById('addNewBriefCover')) {
		document.getElementById('addNewBriefCover').onclick = function(event){
			addNewBriefCover();
		};
	}

	if (document.getElementById('addNewFullCover')) {
		document.getElementById('addNewFullCover').onclick = function(event){
			addNewFullCover();
		};
	}

	if (document.getElementById('addNewTitle')) {
		document.getElementById('addNewTitle').onclick = function(event){
			addNewTitle();
		};
	}

	if (document.getElementById('addNewReview')) {
		document.getElementById('addNewReview').onclick = function(event){
			addNewReview();
		};
	}

	if (document.getElementById('addNewInterview')) {
		document.getElementById('addNewInterview').onclick = function(event){
			addNewInterview();
		};
	}

	var row_id = '';
	var add_button1 = '';
	var add_button2 = '';
	for (var i = 1 ; i < 2000 ; i++) {
		row_id = 'cover_id' + i + '.row';
		add_button1 = 'addArtist.button.' + i;
		if (document.getElementById(row_id)) {
			if (document.getElementById(add_button1)) {
				document.getElementById(add_button1).onclick = function(event){
					addArtist(event);
				};
			}
		}
		else {
			break;
		}
	}

	for (var i = 1 ; i < 2000 ; i++) {
		row_id = 'title_id' + i + '.row';
		add_button1 = 'addContentTitleAuthor.button.' + i;
		if (document.getElementById(row_id)) {
			if (document.getElementById(add_button1)) {
				document.getElementById(add_button1).onclick = function(event){
					addContentTitleAuthor(event);
				};
			}
		}
		else {
			break;
		}
	}

	for (var i = 1 ; i < 2000 ; i++) {
		row_id = 'review_id' + i + '.row';
		add_button1 = 'addReviewee.button.' + i;
		add_button2 = 'addReviewer.button.' + i;
		if (document.getElementById(row_id)) {
			if (document.getElementById(add_button1)) {
				document.getElementById(add_button1).onclick = function(event){
					addReviewee(event);
				};
			}
			if (document.getElementById(add_button2)) {
				document.getElementById(add_button2).onclick = function(event){
					addReviewer(event);
				};
			}
		}
		else {
			break;
		}
	}

	for (var i = 1 ; i < 2000 ; i++) {
		row_id = 'interview_id' + i + '.row';
		add_button1 = 'addInterviewee.button.' + i;
		add_button2 = 'addInterviewer.button.' + i;
		if (document.getElementById(row_id)) {
			if (document.getElementById(add_button1)) {
				document.getElementById(add_button1).onclick = function(event){
					addInterviewee(event);
				};
			}
			if (document.getElementById(add_button2)) {
				document.getElementById(add_button2).onclick = function(event){
					addInterviewer(event);
				};
			}
		}
		else {
			break;
		}
	}

}

function validateURL(field_name) {
	// Retrieve the URL field - use [0] because JS returns an array in case there are many fields with this name
	var element_name = document.getElementsByName(field_name)[0];
	// If there is no URL field, validation is successful
	if (element_name == null) {
		return true;
	}
	// Retrieve the value of the field
	var element_value = element_name.value.trim();
	// If the value is empty, then validation passes
	if (element_value == "") {
		return true;
	}
	// Check that the URL starts with "http://" or "https://" (case insensitive)
	if (element_value.match(/^https?:\/\//gi) == null) {
		alert("URLs must start with \"http://\" or \"https://\".");
		element_name.focus();
		return false;
	}
	// Check that the URL doesn't contain angle brackets, double quotes or spaces
	if ((/\</.test(element_value) == true) || (/\>/.test(element_value) == true) || (/\"/.test(element_value) == true) || (/\ /.test(element_value) == true)) {
		alert("URLs must not contain angle brackets, double quotes or spaces");
		element_name.focus();
		return false;
	}
	return true;
}

function validateWebPages(field_name) {
	var last_row = GetLastRow(field_name);
	var web_page_field;
	for (i = 1 ; i < (last_row +1) ; i++) {
		web_page_field = field_name + i;
		// Validate each URL
		if (validateURL(web_page_field) == false) {
			return false;
		}
	}
	return true;
}

function validateRequired(field_name, display_name) {
	// Retrieve the Title field - use [0] because JS returns an array in case there are many fields with this name
	var element_name = document.getElementsByName(field_name)[0];
	// Retrieve the value of the field
	var element_value = element_name.value;
	// Strip all spaces to check for titles that consist of nothing but spaces
	element_value = element_value.split(" ").join("");
	//  Check if the resulting string is empty and generate an alert error
	if (element_value == "") {
		alert(display_name + " is a required field.");
		element_name.focus();
		return false;
	}
	return true;
}

function validateDate(value, display_name, type_of_date) {
	// Check that the entered string follows the YYYY-MM-DD format
	if ((value.match(/^\d{4}-{1}\d{2}-{1}\d{2}$/) == null) && (value.match(/^\d{4}$/) == null) && (value.match(/^\d{4}-{1}\d{2}$/) == null)) {
		if (type_of_date == "title") {
			alert(display_name + " must be in YYYY, YYYY-MM or YYYY-MM-DD format. 0000-00-00 means \"Unknown\", 8888-00-00 means \"Unpublished\" and 9999-00-00 means \"Forthcoming\".");
		}
		if (type_of_date == "award") {
			alert(display_name + " must be in YYYY, YYYY-MM or YYYY-MM-DD format. 8888-00-00 means \"Unpublished\" and 9999-00-00 means \"Forthcoming\".");
		}
		// For author dates, allow 0000-MM-DD dates
		if (type_of_date == "author") {
			if (value.match(/^0{4}-{1}\d{2}-{1}\d{2}$/) == null) {
				alert(display_name + " must be in YYYY, YYYY-MM or YYYY-MM-DD format.");
			}
		}
	return false;
	}
	// Parse the entered string and move the components to 'year', 'month' and 'day'
	var dateParts = new Array();
	dateParts = value.split("-");
	var year = dateParts[0];
	if (dateParts.length < 2) {
		var month = "00";
	}
	else {
		var month = dateParts[1];
	}
	if (dateParts.length < 3) {
		var day = "00";
	}
	else {
		var day = dateParts[2];
	}
	var currentDate = new Date();
	var currentYear = currentDate.getFullYear();
	if ((type_of_date == "author") && (year > currentYear)) {
		alert("For authors, dates later than the current year are not allowed.");
		return false;
	}
	if (type_of_date == "award") {
		if (year == "0000") {
			alert("For awards, 0000 years are not allowed.");
			return false;
		}
		if ((month != "00") || (day != "00")) {
			alert("Bad YEAR value. Only YYYY and YYYY-00-00 values are valid for awards.");
			return false;
		}
	}
	var nextYear = currentYear + 1;
	if ((year > nextYear) && (year != "0000") && (year != "9999") && (year != "8888")) {
		alert("Dates more than 1 year in the future are not allowed. Use 8888-00-00 for \"Unpublished\" and 9999-00-00 for \"Forthcoming\".");
		return false;
	}
	if ((year == "0000") || (year == "9999") || (year == "8888")) {
		if (((month != "00") || (day != "00")) && (type_of_date != "author")) {
			alert("Month and day must be 00 when entering 0000-00-00, 8888-00-00 or 9999-00-00.");
			return false;
		}
	}
	if (month > 12) {
		alert("Months must be between 01 and 12.");
		return false;
	}
	// Determine the last day in the entered month
	switch(month) {
	case "00":
		max_day = 31;
		break;
	case "01":
		max_day = 31;
		break;
	case "02":
		max_day = 28;
		break;
	case "03":
		max_day = 31;
		break;
	case "04":
		max_day = 30;
		break;
	case "05":
		max_day = 31;
		break;
	case "06":
		max_day = 30;
		break;
	case "07":
		max_day = 31;
		break;
	case "08":
		max_day = 31;
		break;
	case "09":
		max_day = 30;
		break;
	case "10":
		max_day = 31;
		break;
	case "11":
		max_day = 30;
		break;
	case "12":
		max_day = 31;
		break;
	default:
		alert("Bad month " + month + ".");
		return false;
	}
	/*If the year is a leap year and the month is February, change the last day from 28 to 29
	Note that this doesn't work correctly for the Julian calendar, which was superseded (in
	Europe) by the Gregorian calendar between 1582 and 1923. MySQL only allows Gregorian dates,
	so any YYYY-02-29 dates that follow the Julian calendar would cause errors at file time. */
	if ((month == "02") && (((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0))) {
		max_day = 29;
	}
	if (day > max_day) {
		alert("Day greater than the last day in the entered month.");
		return false;
	}
	return true;
}

function validateRequiredDate(field_name, display_name, required, type_of_date) {
	// Retrieve the Title field - use [0] because JS returns an array in case there are many fields with this name
	var element_name = document.getElementsByName(field_name)[0];
	// Retrieve the value of the field
	var element_value = element_name.value;
	// Strip all spaces to check for years that consist of nothing but spaces
	element_value = element_value.split(" ").join("");
	// Check if the resulting string is empty
	if (element_value == "") {
		// If a value is required, generate an error if no value was entered
		if (required == "required") {
			alert(display_name + " is a required field.");
			element_name.focus();
			return false;
		}
		else {
			return true;
		}
	}
	// If a value was entered, call validateDate, which performs detailed validation
	if (validateDate(element_value, display_name, type_of_date) == false) {
		element_name.focus();
		return false;
	}
	return true;
}

function validateAuthors(field_name, display_name, at_least_one) {
	var last_row = GetLastRow(field_name);
	var count = 0;
	var author_field;
	var author_field_handle;
	var author_data;
	var author_value;
	for (i = 1 ; i < (last_row +1) ; i++) {
		author_field = field_name + i;
		author_field_handle = document.getElementsByName(author_field)[0]
		author_value = author_field_handle.value;
		if (author_value.indexOf("+") !== -1) {
			alert("Plus signs are currently not allowed in " + display_name + ".");
			author_field_handle.focus();
			return false;
		}
		// Strip all spaces to check for authors that consist of nothing but spaces
		author_value = author_value.split(" ").join("");
		if (author_value != "") {
			count++;
		}
	}
	if ((at_least_one == "yes") && (count == 0)) {
		alert("At least one " + display_name + " must be entered. See Help for details.");
		var first_field_name = field_name + "1";
		var first_field_handle = document.getElementsByName(first_field_name)[0];
		first_field_handle.focus();
		return false;
	}
	return true;
}

function validateSeriesNumber() {
	// Retrieve the id of the Series Number field
	var element_name = document.getElementsByName("title_seriesnum")[0];
	// If there is no Series Number field in the form, validation is successful
	if (element_name == null) {
		return true;
	}
	// Retrieve the value of the field
	var element_value = element_name.value.split(" ").join("");
	// If the value doesn't match 0-9 numbers (the first one can't be 0), display an error
	if (element_value != "") {
		if (element_value.match(/^[0-9]{1,9}([\.]{1}[0-9]{1,4}){0,1}$/) == null) {
			alert("Series numbers must be between 1 and 999999999. You can use a decimal point and up to 4 digits after it to position titles in between other titles in the series, e.g. 3.5 will appear between 3 and 4");
			element_name.focus();
			return false;
		}
	}
	return true;
}

function validateContentIndicator() {
	// Retrieve the id of the Content field
	var content_name = document.getElementsByName("title_content")[0];
	// If there is no Content field in the form (pub edit forms), validation is successful
	if (content_name == null) {
		return true;
	}

	// Retrieve the value of the Content field; strip spaces
	var content_value = content_name.value.split(" ").join("");
	// If the Content field is empty, then no additional validation is needed
	if (content_value == "") {
		return true;
	}

	// Slash can't be the first character of the Content value
	if (content_value[0] == "/") {
		alert("Content value cannot begin with a slash.");
		content_name.focus();
		return false;
	}

	if (content_value.length > 254) {
		alert("Content value must be 254 characters or less.");
		content_name.focus();
		return false;
	}

	// Retrieve the id of the Title Type field
	var type_name = document.getElementsByName("title_ttype")[0];
	// If there is no Title Type field in the form (New Pub), validation is successful
	if (type_name == null) {
		return true;
	}
	// Retrieve the value of the Title Type field
	var type_value = type_name.value;
	// If the title type is not OMNIBUS, Content data is not allowed
	if (type_value != "OMNIBUS") {
		alert("Only OMNIBUS titles can have Content data.");
		content_name.focus();
		return false;
	}

	return true;
}

function AddMultipleField(field_label, field_name) {
	var last_row = GetLastRow(field_name);
	var addpoint = document.getElementById(field_name + last_row + '.row');
	var tbody = addpoint.parentNode;
	var next = last_row + 1;
	var tr   = document.createElement("tr");
	var td1  = document.createElement("td");
	var td2  = document.createElement("td");
	var b  = document.createElement("b");
	var label = field_label + " " + next + ":";
	var txt1 = document.createTextNode(label);
	var input = document.createElement("input");
	var attr = field_name + next;
	tr.setAttribute("id", attr + '.row');
	input.setAttribute("id", attr);
	input.setAttribute("name", attr);
	input.setAttribute("class", "metainput");
	input.setAttribute("tabindex", "1");
	td1.appendChild(b);
	b.appendChild(txt1);
	var add_button = document.getElementById(field_name + '.addbutton');
	td1.appendChild(add_button);
	td2.appendChild(input);
	tr.appendChild(td1);
	tr.appendChild(td2);
	tbody.insertBefore(tr, addpoint.nextSibling);
}

function GetLastRow(field_name) {
	for (i = 1 ; i < 2000 ; i++) {
		row_data = document.getElementById(field_name + i + '.row');
		if (row_data == null) {
			return i-1;
		}
	}
	return 1999;
}

function determineArticle(word) {
	var article = 'a';
	switch(word[0]) {
	case "A":
		article = 'an';
		break;
	case "E":
		article = 'an';
		break;
	case "O":
		article = 'an';
		break;
	default:
		article = 'a';
		break;
	}
	return article;
}

document.addEventListener('DOMContentLoaded', function() {
	var title = document.title;
	createOnsubmit(title);
});

function createOnsubmit(title)	{
	if (title.indexOf('Award Editor') == 0) {
		document.getElementById('data').onsubmit = function(event){
			if (validateAwardForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Add New Award Type') {
		document.getElementById('data').onsubmit = function(event){
			if (validateAwardTypeForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title.indexOf('New Award Category') == 0) {
		document.getElementById('data').onsubmit = function(event){
			if (validateAwardCatForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Add Publication') {
		document.getElementById('data').onsubmit = function(event){
			if (validatePubForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Delete Publication') {
		document.getElementById('data').onsubmit = function(event){
			if (validateModNoteRequired() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Add Variant Title') {
		document.getElementById('data').onsubmit = function(event){
			if (validateVariantTitleForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Import/Export Contents') {
		document.getElementById('data').onsubmit = function(event){
			if (validatePubForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Clone Publication') {
		document.getElementById('data').onsubmit = function(event){
			if (validatePubForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Author Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validateAuthorForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Award Category Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validateAwardCatForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Award Type Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validateAwardTypeForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Publication Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validatePubForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Publisher Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validatePublisherForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Publication Series Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validatePubSeriesForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Series Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validateSeriesForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Title Editor') {
		document.getElementById('data').onsubmit = function(event){
			if (validateTitleForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title == 'Make Variant Title') {
		document.getElementById('data').onsubmit = function(event){
			if (validateParentTitle() == false) {
				event.preventDefault();
			}
		};
		document.getElementById('data2').onsubmit = function(event){
			if (validateVariantTitleForm() == false) {
				event.preventDefault();
			}
		};
	}

	else if (title.indexOf('New ') == 0) {
		document.getElementById('data').onsubmit = function(event){
			if (validatePubForm() == false) {
				event.preventDefault();
			}
		};
	}
}
