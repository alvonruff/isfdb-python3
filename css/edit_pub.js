/*     Version: $Revision: 1186 $
      (C) COPYRIGHT 2015-2024   Ahasuerus
         ALL RIGHTS RESERVED
      Date: $Date: 2024-07-24 11:17:13 -0400 (Wed, 24 Jul 2024) $ */

function validatePubURL(field_name) {
	// First check that the entered URL contains only valid URL characters
	if (validateURL(field_name) == false) {
		return false;
	}
	// Retrieve the URL field - use [0] because JS returns an array in case there are many fields with this name
	var element_name = document.getElementsByName(field_name)[0];
	// If there is no URL field, validation is successful
	if (element_name == null) {
		return true;
	}
	// Retrieve the value of the field
	var element_value = element_name.value;
	// Check if the resulting string contains a Wiki page URL and generate an alert error
	if (element_value.indexOf("://www.isfdb.org/wiki/index.php/Image") !== -1) {
		alert("URL for the cover image should be for the image, not the Wiki page that the image is on.");
		element_name.focus();
		return false;
	}
	return true;
}

function validateModNoteRequired() {
	var flag_handle = document.getElementsByName("mod_note_required")[0];
	// If there is no "Mod Note Required" field, validation is successful
	if (flag_handle == null) {
		return true;
	}
	var flag_value = flag_handle.value;
	var mod_note_handle = document.getElementsByName("mod_note")[0];
	var mod_note_value = mod_note_handle.value;
	// Strip all spaces in case the mod note consists of nothing but spaces
	mod_note_value = mod_note_value.trim();
	if ((flag_value == 1) && (mod_note_value == "")) {
		alert("This publication has been primary verified by at least one editor other than you. Please enter a moderator note to document the submitted changes.");
		mod_note_handle.focus();
		return false;
	}
	return true;
}

function validateContents(record_id, title_field, title_date, author_add_point, author_field, display_name_author, display_name_title) {
	// Initialize variables
	var add_author;
	var author_data;
	var author_field_handle;
	var defined_authors;
	var current_title_page;
	var i;
	var j;
	var next_author;
	var title_data;
	var title_date_data;
	var title_date_handle;
	var title_handle;
	var title_page_handle;
	var title_page_data;
	var length_field_handle;
	var length_field_data;
	var ttype_field;
	var ttype_field_handle;
	var ttype_field_data;

	// Determine the next available title number
	var next_record = GetLastRow(record_id) + 1;
	// Check each Contents title record
	for (i = 1 ; i < next_record ; i++) {
		// Retrieve the handle of this title record in case we need to focus on it later
		title_handle = document.getElementsByName(title_field + i)[0];
		// Retrieve the title of this title record
		title_data = title_handle.value;
		// Strip all spaces in case the title consists of nothing but spaces
		title_data = title_data.split(" ").join("");
		// Check this title's page number -- must be processed first because it can be defined for greyed out titles
		// Build the name of the page number for the currently processed title
		current_title_page = display_name_title + "_page" + i;
		// Retrieve the handle of the current title page field
		title_page_handle = document.getElementsByName(current_title_page)[0];
		// Retrieve the value of the current title page field
		title_page_data = title_page_handle.value;
		// Strip all spaces in case the page number consists of nothing but spaces
		title_page_data = title_page_data.split(" ").join("");
		if (title_page_data.length > 20) {
			alert("Page number must be 20 character or less.");
			title_page_handle.focus();
			return false;
		}
		if (title_page_data.includes("|")) {
			if (title_page_data.split("|")[1].match(/^[0-9]{0,19}([\.]{1}[0-9]{1,19}){0,1}$/) == null) {
				alert("Sorting numbers that appear after the pipe character must be non-negative numbers like 0, 4 or 12.75");
				title_page_handle.focus();
				return false;
			}
		}
		if ((title_page_data != "") && (title_data == "")) {
			alert("Page number entered, but no title is specified.");
			title_handle.focus();
			return false;
		}
		// Retrieve the Add Author element for this record
		add_author = document.getElementById(author_add_point + i);
		// If there is no Add Author element for this title, then it's read-only and we skip it
		if (add_author == null) {
			continue;
		}
		// Retrieve the next available author number for this title
		next_author = GetLastRow(author_field + i + '.') + 1;
		// Initialize the number of defined authors for this title
		defined_authors = 0;
		// Check each author name defined for this title
		for (j = 1 ; j < next_author ; j++) {
			// Retrieve the name of this author
			author_field_handle = document.getElementsByName(author_field + i + "." + j)[0];
			author_data = author_field_handle.value;
			// Strip all spaces to check for authors that consist of nothing but spaces
			author_value = author_data.split(" ").join("");
			if (author_value.indexOf("+") !== -1) {
				alert("Plus signs are currently not allowed in " + display_name_author + ".");
				author_field_handle.focus();
				return false;
			}
			if (author_value != "") {
				defined_authors++;
			}
		}
		if ((title_data != "") && (defined_authors == 0)) {
			alert("No " + display_name_author + " entered for " + display_name_title + " " + title_data + ". At least one " + display_name_author + " must be entered. See Help for details.");
			title_handle.focus();
			return false;
		}
		if ((title_data == "") && (defined_authors != 0)) {
			alert("No " + display_name_title + " entered, but at least one " + display_name_author + " is specified. See Help for details.");
			title_handle.focus();
			return false;
		}
		// Check this title's date
		// Retrieve the handle of the current title date field
		title_date_handle = document.getElementsByName(title_date + i)[0];
		// Retrieve the value of the current title date field
		title_date_data = title_date_handle.value;
		// Strip all spaces in case the date consists of nothing but spaces
		title_date_data = title_date_data.split(" ").join("");
		if ((title_date_data != "") && (validateDate(title_date_data,"Date","title")) == false) {
			title_date_handle.focus();
			return false;
		}

		if (record_id != "title_id") {
			continue
		}
		// Check this title's Length value against the Title Type value
		// Retrieve the handle of the Length field being processed
		length_field_handle = document.getElementsByName('title_storylen' + i)[0];
		// Retrieve the value of the Length field being processed
		length_field_data = length_field_handle.value;

		// Build the name of the Title Type field being processed
		ttype_field = 'title_ttype' + i;
		// Retrieve the handle of the Title Type field being processed
		ttype_field_handle = document.getElementsByName(ttype_field)[0];
		// Retrieve the value of the Title Type field being processed
		ttype_field_data = ttype_field_handle.value;

		// Only SHORTFICTION titles can have Length values
		if ((ttype_field_data != 'SHORTFICTION') && (length_field_data !='')) {
			alert("Only SHORTFICTION titles can have Length values");
			length_field_handle.focus();
			return false;
		}
	}
	return true;
}

function validateCovers() {
	// Initialize variables
	var artist_addpoint;
	var artist_data;
	var cover_date_data;
	var cover_date_handle;
	var cover_title_data;
	var cover_title_handle;
	var defined_artists;
	var i;
	var j;
	var next_artist;

	// Determine the next available cover ID
	var next_cover = GetLastRow('cover_id') + 1;
	// Check each cover record defined on the page
	for (i = 1 ; i < next_cover ; i++) {
		// Retrieve the Add Artist element for this cover record
		artist_addpoint = document.getElementById("AddArtist" + i);
		// If there is no artist add point for this cover, then it's read-only and
		// validation passes
		if (artist_addpoint == null) {
			continue;
		}

		// Check this cover's date
		// Retrieve the handle of the current cover date field
		cover_date_handle = document.getElementsByName("cover_date" + i)[0];
		// Retrieve the value of the current cover date field; strip spaces
		cover_date_data = cover_date_handle.value.split(" ").join("");
		// Validate date format
		if ((cover_date_data != "") && (validateDate(cover_date_data,"Date","title")) == false) {
			cover_date_handle.focus();
			return false;
		}

		// Check this cover's title
		// Retrieve the handle of this title field in case we need to focus on it later
		cover_title_handle = document.getElementsByName("cover_title" + i)[0];
		// Retrieve the title of this cover record; strip spaces
		cover_title_data = cover_title_handle.value.split(" ").join("");
		// If there was no title and no date entered, then validation passes. (It also
		// happens when the brief cover art format is used on the page.) If one
		// or more artists were entered with no other data, the title and the date will
		// be defaulted to the title and date of the publication
		if ((cover_title_data == "") && (cover_date_data == "")) {
			continue;
		}

		// Retrieve the next available artist number for this cover
		next_artist = GetLastRow('cover_artist' + i + '.') + 1;
		// Initialize the number of defined artists for this cover
		defined_artists = 0;
		// Check each artist name defined for this cover
		for (j = 1 ; j < next_artist ; j++) {
			// Retrieve the name of this artist
			artist_data = document.getElementsByName("cover_artist" + i + "." + j)[0].value;
			// Strip all spaces to check for artist names which consist of nothing but spaces
			artist_data = artist_data.split(" ").join("");
			if (artist_data != "") {
				defined_artists++;
			}
		}
		if (defined_artists == 0) {
			alert("No artists were entered, but other cover data was specified. At least one artist must be entered. See Help for details.");
			cover_title_handle.focus();
			return false;
		}
	}
	return true;
}

function validatePubForm() {
	// Validate that a non-empty Moderator Note was entered for pubs primary verified by users other than the current editor
	if (validateModNoteRequired() == false) {
		return false;
	}
	// Validate that a non-empty pub title has been entered
	if (validateRequired("pub_title","Publication Title") == false) {
		return false;
	}
	// Validate this pub's authors
	if (validateAuthors("pub_author", "author/editor", "yes") == false) {
		return false;
	}
	// Validate the date of the pub
	if (validateRequiredDate("pub_year", "Date", "required", "title") == false) {
		return false;
	}
	// Validate the cover image URL
	if (validatePubURL("pub_image") == false) {
		return false;
	}
	// Validate the Series Number (for NewPubs)
	if (validateSeriesNumber() == false) {
		return false;
	}
	// Validate the Content field (for NewPubs)
	if (validateContentIndicator() == false) {
		return false;
	}
	// Validate the Web Page URLs for Title Web Pages in the NewPub edit form
	if (validateWebPages("shared_title_webpages") == false) {
		return false;
	}
	// Validate the Web Page URLs for Publication Web Pages on the NewPub edit page
	if (validateWebPages("shared_pub_webpages") == false) {
		return false;
	}
	// Validate the Web Page URLs for Publication Web Pages on non-NewPub pages
	if (validateWebPages("pub_webpages") == false) {
		return false;
	}
	// Validate the External IDs
	if (validateExternalIDs() == false) {
		return false;
	}
	// Validate covers
	if (validateCovers() == false) {
		return false;
	}
	// Validate the Title sub-section of the Contents section
	if (validateContents("title_id", "title_title", "title_date", "AddAuthor", "title_author", "author", "title") == false) {
		return false;
	}
	// Validate the revieweEs in the Review sub-section of the Contents section
	if (validateContents("review_id", "review_title", "review_date", "AddReviewee", "review_author", "author", "review") == false) {
		return false;
	}
	// Validate the revieweRs in the Review sub-section of the Contents section
	if (validateContents("review_id", "review_title", "review_date", "AddReviewer", "review_reviewer", "reviewer", "review") == false) {
		return false;
	}
	// Validate the intervieweEs in the Interview sub-section of the Contents section
	if (validateContents("interview_id", "interview_title", "interview_date", "AddInterviewee", "interviewee_author", "interviewee", "interview") == false) {
		return false;
	}
	// Validate the intervieweRs in the Interview sub-section of the Contents section
	if (validateContents("interview_id", "interview_title", "interview_date", "AddInterviewer", "interviewer_author", "interviewer", "interview") == false) {
		return false;
	}
	// Check for mismatch between the publication type and titles in the Content section
	if (validateTypeMismatch() == false) {
		return false;
	}

	return true;
}

function validateExternalIDs() {
	var last_row = GetLastExternalId("external_id");
	for (i = 1 ; i < (last_row +1) ; i++) {
		// Validate each External ID
		if (validateExternalID(i) == false) {
			return false;
		}
	}
	return true;
}

function validateExternalID(i) {
	var id_field = "external_id." + i;
	// Retrieve the External ID field - use [0] because JS returns an array in case there are many fields with this name
	var id_name = document.getElementsByName(id_field)[0];
	// If there is no External ID field, validation is successful
	if (id_name == null) {
		return true;
	}
	// Retrieve the value of the field
	var id_value = id_name.value;
	// If the value is empty, then validation passes
	if (id_value == "") {
		return true;
	}
	// Check that the External ID field doesn't contain angle brackets, double quotes or embedded spaces
	if ((/\</.test(id_value) == true) || (/\>/.test(id_value) == true) || (/\"/.test(id_value) == true) || (/\ /.test(id_value.trim()) == true)) {
		alert("External IDs must not contain angle brackets, double quotes or spaces");
		id_name.focus();
		return false;
	}
	// Check that the External ID Type is not the default 0 value
	var type_field = "external_id_type." + i;
	var type_name = document.getElementsByName(type_field)[0];
	if (type_name.value == "0") {
		alert("An External ID type must be selected from the drop-down list");
		id_name.focus();
		return false;
	}
	return true;
}

function validateTypeMismatch()	{
	// If this page is Publication Editor, then the reference title must be entered explicitly in the Content section.
	// If this page is a Clone/Import/Export page, then the reference title check is not performed.
	// For NewPub and AddPub forms, the reference title is implied and should not be entered in the Content section.
	var reference_title = 'implied';
	if (document.title == 'Publication Editor') {
		reference_title = 'explicit';
	}
	else if (document.title.includes('Import') == true) {
		reference_title = 'ignore';
	}
	else if (document.title.includes('Clone') == true) {
		reference_title = 'ignore';
	}
	// Get the handle of the publication type (pub_ctype) field
	var pub_type_handle = document.getElementsByName("pub_ctype")[0];
	// Retrieve the value of the publication type field
	var pub_type_value = pub_type_handle.value;
	// Determine the next available title number
	var next1 = GetLastRow('title_id') + 1;
	var current_title_name;
	var current_title_handle;
	var title_title;
	var current_type_name;
	var current_type_handle;
	var title_type;
	var reference_title_type = '';
	var current_count;
	var anthology_count = 0;
	var chapbook_count = 0;
	var collection_count = 0;
	var editor_count = 0;
	var essay_count = 0;
	var interiorart_count = 0;
	var nonfiction_count = 0;
	var novel_count = 0;
	var omnibus_count = 0;
	var poem_count = 0;
	var serial_count = 0;
	var shortfiction_count = 0;
	var i;
	// Add the title type of each Content title record to type-specific counters
	for (i = 1 ; i < next1 ; i++) {
		// Build the name of the title field that is being processed
		current_title_name = "title_title" + i;
		// Retrieve the handle of the current title field
		current_title_handle = document.getElementsByName(current_title_name)[0];
		// Retrieve the title value
		title_title = current_title_handle.value;
		// If there is no title, then it's an empty title record and we skip it
		if (title_title == "") {
			continue;
		}
		// Build the name of the title type field that is being processed
		current_type_name = "title_ttype" + i;
		// Retrieve the handle of the current title type field
		current_type_handle = document.getElementsByName(current_type_name)[0];
		// Retrieve the title type value
		title_type = current_type_handle.value;
		if ((pub_type_value == 'FANZINE') || (pub_type_value == 'MAGAZINE')) {
			if (title_type == 'EDITOR') {
				reference_title_type = 'EDITOR';
			}
		}
		else if (title_type == pub_type_value) {
			reference_title_type = title_type;
		}
		if (title_type == 'ANTHOLOGY') {
			anthology_count = anthology_count + 1;
		}
		if (title_type == 'CHAPBOOK') {
			chapbook_count = chapbook_count + 1;
		}
		if (title_type == 'COLLECTION') {
			collection_count = collection_count + 1;
		}
		if (title_type == 'EDITOR') {
			editor_count = editor_count + 1;
		}
		if (title_type == 'ESSAY') {
			essay_count = essay_count + 1;
		}
		if (title_type == 'INTERIORART') {
			interiorart_count = interiorart_count + 1;
		}
		if (title_type == 'NONFICTION') {
			nonfiction_count = nonfiction_count + 1;
		}
		if (title_type == 'NOVEL') {
			novel_count = novel_count + 1;
		}
		if (title_type == 'OMNIBUS') {
			omnibus_count = omnibus_count + 1;
		}
		if (title_type == 'POEM') {
			poem_count = poem_count + 1;
		}
		if (title_type == 'SHORTFICTION') {
			shortfiction_count = shortfiction_count + 1;
		}
		if (title_type == 'SERIAL') {
			serial_count = serial_count + 1;
		}
	}
	if (editor_count > 1) {
		alert("Multiple EDITOR titles are not allowed");
		return false;
	}
	if (chapbook_count > 1) {
		alert("Multiple CHAPBOOK titles are not allowed.");
		return false;
	}

	// Check that the reference title was entered for pub edits and was NOT entered for other types of submissions
	if (reference_title_type != '') {
		if (reference_title == 'implied') {
			var article = determineArticle(reference_title_type);
			var message = 'When creating a new '+pub_type_value+' publication, ';
			message += article+' '+reference_title_type;
			message += ' title should not be entered in the Regular Titles subsection of the Content section. ';
			message += 'It will be added automatically at submission creation time.';
			alert(message);
			return false;
		}
	}
	else {
		if (reference_title == 'explicit') {
			var message = 'When editing publications, the Regular Titles subsection of the Content';
			message += ' section must contain one title whose type matches the publication type.';
			message += ' For Magazine and Fanzine publications the matching title type should be EDITOR.';
			alert(message);
			return false;
		}
	}

	// Check that the entered title types are valid for the specified publication type
	if ((pub_type_value != 'MAGAZINE') && (pub_type_value != 'FANZINE') && (editor_count > 0)) {
		alert("Only MAGAZINE and FANZINE publications can contain EDITOR titles.");
		return false;
	}

	if ((pub_type_value != 'CHAPBOOK') && (chapbook_count > 0)) {
		alert("Only CHAPBOOK publications can contain CHAPBOOK titles.");
		return false;
	}

	if (pub_type_value == "CHAPBOOK") {
		if ((anthology_count + collection_count + nonfiction_count + novel_count + omnibus_count) > 0) {
			alert("ANTHOLOGY, COLLECTION, NONFICTION, NOVEL, and OMNIBUS titles are not allowed within CHAPBOOK publications.");
			return false;
		}
	}

	if ((pub_type_value == 'MAGAZINE') || (pub_type_value == 'FANZINE')) {
		if (novel_count > 0) {
			alert("NOVEL titles are not allowed in MAGAZINE/FANZINE publications. Use (Complete Novel) SERIALs instead. See Help for more details.");
			return false;
		}
	}

	return true;
}

function ExternalIdentifiers() {
	var all_ids = document.getElementById("external_id_type.1");
	var identifiers = [];
	var i;
	var len = all_ids.options.length;
	for (i = 0; i < len; i++) {
		identifiers.push({
			"id": all_ids.options[i].value,
			"name": all_ids.options[i].text
		});
	}
	return identifiers;
}

function addNewExternalID(field_name) {
	var field_name = field_name || 'external_id';
	var identifier_types = ExternalIdentifiers();

	var last_row = GetLastExternalId(field_name);
	var addpoint = document.getElementById(field_name + '.row.' + last_row);
	var tbody = addpoint.parentNode;
	var next = last_row + 1;

	var tr   = document.createElement("tr");
	tr.setAttribute("id", field_name + '.row.' + next);
	var td1  = document.createElement("td");
	var select = document.createElement("select");
	select.setAttribute("name", field_name+"_type."+next);
	select.setAttribute("tabindex", "1");
	for (var i = 0; i < identifier_types.length; i++) {
		var option = document.createElement("option");
		option.value = identifier_types[i]["id"];
		option.text = identifier_types[i]["name"];
		select.appendChild(option);
	}
	td1.appendChild(select);
	var add_button = document.getElementById(field_name + '.addbutton');
	td1.appendChild(add_button);
	tr.appendChild(td1);

	var td2  = document.createElement("td");
	var input = document.createElement("input");
	var attr = "external_id."+next;
	input.setAttribute("name", attr);
	input.setAttribute("id", attr);
	input.setAttribute("class", "metainput");
	input.setAttribute("tabindex", "1");
	td2.appendChild(input);
	tr.appendChild(td2);
	tbody.insertBefore(tr, addpoint.nextSibling);
}

function GetLastExternalId(field_name) {
	for (i = 1 ; i < 1000 ; i++) {
		row_data = document.getElementById(field_name + '.row.' + i);
		if (row_data == null) {
			return i-1;
		}
	}
	return 999;
}

function addNewBriefCover() {
	var record_type = "cover";
	var last_row = GetLastRow('cover_id');
	var addpoint = document.getElementById('cover_id' + last_row + '.row');
	var tbody = addpoint.parentNode;
	var next = last_row + 1;

	// First row - create top-level elements
	var tr1 = document.createElement("tr");
	var td1 = document.createElement("td");
	// Element: input title_idX
	var attr = record_type+"_id"+next;
	var input1 = document.createElement("input");
	input1.setAttribute("name", attr);
	input1.setAttribute("value", "0");
	input1.setAttribute("type", "HIDDEN");
	td1.appendChild(input1);
	// Element: input title_titleX
	attr = record_type+"_title"+next;
	var input2 = document.createElement("input");
	input2.setAttribute("name", attr);
	input2.setAttribute("type", "HIDDEN");
	td1.appendChild(input2);
	// Element: input title_dateX
	attr = record_type+"_date"+next;
	var input3 = document.createElement("input");
	input3.setAttribute("name", attr);
	input3.setAttribute("type", "HIDDEN");
	td1.appendChild(input3);
	tr1.appendChild(td1);
	tbody.insertBefore(tr1, addpoint.nextSibling);

	// Second row for "Artist1" - create top-level elements
	var tr2 = document.createElement("tr");
	tr2.setAttribute("id", "cover_artist"+next+".1.row");
	var td2 = document.createElement("td");
	var bold = document.createElement("b");
	var text1 = document.createTextNode("Artist1:");

	bold.appendChild(text1);
	td2.appendChild(bold);
	tr2.appendChild(td2);

	var td3 = document.createElement("td");
	var input4 = document.createElement("input");
	attr = "cover_artist"+next+".1";
	input4.setAttribute("id", attr);
	input4.setAttribute("name", attr);
	input4.setAttribute("class", "contentinput");
	input4.setAttribute("tabindex", "1");
	td3.appendChild(input4);
	tr2.appendChild(td3);
	tbody.insertBefore(tr2, tr1.nextSibling);

	// Third row - "Add Artist" Button
	var tr3    = document.createElement("tr");
	attr = "AddArtist"+next;
	tr3.setAttribute("id", attr);
	tr3.setAttribute("next", "2");
	var td4   = document.createElement("td");
	tr3.appendChild(td4);

	// <td> button element
	var td5   = document.createElement("td");
	var input5 = document.createElement("input");
	input5.setAttribute("id", "addArtist.button." + next);
	input5.setAttribute("type", "button");
	input5.setAttribute("tabindex", "1");
	input5.setAttribute("value", "Add Artist");
	input5.onclick  = function(event){
		addArtist(event);
	};
	td5.appendChild(input5);
	tr3.appendChild(td5);
	tbody.insertBefore(tr3, tr2.nextSibling);

	// Spacer
	var tr4  = document.createElement("tr");
	tr4.setAttribute("id", "cover_id"+next+".row");
	tr4.className = "titleeditspacer";
	var td6 = document.createElement("td");
	td6.colSpan = 2;
	tr4.appendChild(td6);
	tbody.insertBefore(tr4, tr3.nextSibling);
}

function addNewFullCover() {
	var record_type = "cover";
	var last_row = GetLastRow('cover_id');
	var addpoint = document.getElementById('cover_id' + last_row + '.row');
	var tbody = addpoint.parentNode;
	var next = last_row + 1;

	// First row - create top-level elements
	var tr1    = document.createElement("tr");
	var td1   = document.createElement("td");

	// Element: input title_idX
	var attr = record_type+"_id"+next;
	var input1 = document.createElement("input");
	input1.setAttribute("name", attr);
	input1.setAttribute("value", "0");
	input1.setAttribute("type", "HIDDEN");
	td1.appendChild(input1);

	// Element: input title_titleX
	var td2   = document.createElement("td");
	attr = record_type+"_title"+next;
	var input2 = document.createElement("input");
	input2.setAttribute("id", attr);
	input2.setAttribute("name", attr);
	input2.setAttribute("class", "contentinput");
	input2.setAttribute("tabindex", "1");
	td2.appendChild(input2);

	// Element: input title_dateX
	var td3 = document.createElement("td");
	attr = record_type+"_date"+next;
	var input3 = document.createElement("input");
	input3.setAttribute("name", attr);
	input3.setAttribute("class", "contentyearinput");
	input3.setAttribute("tabindex", "1");
	td3.appendChild(input3);
	tr1.appendChild(td1);
	tr1.appendChild(td2);
	tr1.appendChild(td3);
	tbody.insertBefore(tr1, addpoint.nextSibling);

	// Second row for "Artist1" - create top-level elements
	var tr2    = document.createElement("tr");
	tr2.setAttribute("id", "cover_artist"+next+".1.row");
	var td2   = document.createElement("td");
	var bold   = document.createElement("b");
	var text1 = document.createTextNode("Artist1:");

	bold.appendChild(text1);
	td2.appendChild(bold);
	tr2.appendChild(td2);

	var td3 = document.createElement("td");
	var input4 = document.createElement("input");
	attr = "cover_artist"+next+".1";
	input4.setAttribute("id", attr);
	input4.setAttribute("name", attr);
	input4.setAttribute("class", "contentinput");
	input4.setAttribute("tabindex", "1");
	td3.appendChild(input4);
	tr2.appendChild(td3);
	tbody.insertBefore(tr2, tr1.nextSibling);

	// Third row - "Add Artist" Button
	var tr3    = document.createElement("tr");
	attr = "AddArtist"+next;
	tr3.setAttribute("id", attr);
	tr3.setAttribute("next", "2");
	var td4   = document.createElement("td");
	tr3.appendChild(td4);

	// <td> button element
	var td5   = document.createElement("td");
	var input5 = document.createElement("input");
	input5.setAttribute("id", "addArtist.button." + next);
	input5.setAttribute("type", "button");
	input5.setAttribute("tabindex", "1");
	input5.setAttribute("value", "Add Artist");
	input5.onclick  = function(event){
		addArtist(event);
	};
	td5.appendChild(input5);
	tr3.appendChild(td5);
	tbody.insertBefore(tr3, tr2.nextSibling);

	// Spacer
	var tr4  = document.createElement("tr");
	tr4.setAttribute("id", "cover_id"+next+".row");
	tr4.className = "titleeditspacer";
	var td6 = document.createElement("td");
	td6.colSpan = 3;
	tr4.appendChild(td6);
	tbody.insertBefore(tr4, tr3.nextSibling);
}

function addNewTitle() {
	addRecord("title")
}

function addNewReview() {
	addRecord("review")
}

function addNewInterview() {
	addRecord("interview")
}

function addRecord(record_type) {
	var last_row = GetLastRow(record_type + "_id");
	var addpoint = document.getElementById(record_type + "_id" + last_row + '.row');
	var tbody = addpoint.parentNode;
	var next = last_row + 1;

	// Create top-level elements
	var tr    = document.createElement("tr");
	var input = document.createElement("input");
	var td1   = document.createElement("td");
	var input1 = document.createElement("input");
	var td2   = document.createElement("td");
	var input2 = document.createElement("input");
	var td3   = document.createElement("td");
	var input3 = document.createElement("input");
	var td4   = document.createElement("td");
	var td5   = document.createElement("td");

	// Element: input title_idX
	var attr = record_type+"_id"+next;
	input.setAttribute("name", attr);
	input.setAttribute("value", "-1");
	input.setAttribute("type", "HIDDEN");
	tr.appendChild(input);

	//# Element: input title_pageX
	attr = record_type+"_page"+next;
	input1.setAttribute("name", attr);
	input1.setAttribute("value", "");
	input1.setAttribute("class", "contentpageinput");
	input1.setAttribute("tabindex", "1");
	td1.appendChild(input1);
	tr.appendChild(td1);

	// Element: input title_titleX
	attr = record_type+"_title"+next;
	input2.setAttribute("name", attr);
	input2.setAttribute("value", "");
	input2.setAttribute("class", "contentinput");
	input2.setAttribute("tabindex", "1");
	td2.appendChild(input2);
	tr.appendChild(td2);

	// Element: input title_dateX
	attr = record_type+"_date"+next;
	input3.setAttribute("name", attr);
	input3.setAttribute("value", "");
	input3.setAttribute("class", "contentyearinput");
	input3.setAttribute("tabindex", "1");
	td3.appendChild(input3);
	tr.appendChild(td3);

	if (record_type == "title") {
		// Element: input title_ttypeX
		var select = document.createElement("select");
		var option1 = document.createElement("option");
		var option2 = document.createElement("option");
		var option3 = document.createElement("option");
		var option4 = document.createElement("option");
		var option5 = document.createElement("option");
		var option6 = document.createElement("option");
		var option7 = document.createElement("option");
		var option8 = document.createElement("option");
		var option9 = document.createElement("option");
		var option10 = document.createElement("option");
		var option11 = document.createElement("option");
		var option12 = document.createElement("option");
		var option13 = document.createElement("option");

		// <select name="title_ttypeX">
		attr = "title_ttype"+next;
		select.setAttribute("name", attr);
		select.setAttribute("class", "contenttypeinput");
		select.setAttribute("tabindex", "1");
		option1.setAttribute("selected", "selected");

		// Retrieve the handle of the publication type field
		// Use [0] because JS returns an array in case there are many fields with this name
		var pub_ctype_handle = document.getElementsByName("pub_ctype")[0];

		// Retrieve the value of the pub type field
		var pub_ctype_value = pub_ctype_handle.value;

		if (pub_ctype_value == 'NONFICTION') {
			var text1 = document.createTextNode("ESSAY");
		}
		else if (pub_ctype_value == 'OMNIBUS') {
			var text1 = document.createTextNode("NOVEL");
		}
		else {
			var text1 = document.createTextNode("SHORTFICTION");
		}
		option1.appendChild(text1);
		select.appendChild(option1);

		var text2 = document.createTextNode("ANTHOLOGY");
		option2.appendChild(text2);
		select.appendChild(option2);

		var text3 = document.createTextNode("CHAPBOOK");
		option3.appendChild(text3);
		select.appendChild(option3);

		var text4 = document.createTextNode("COLLECTION");
		option4.appendChild(text4);
		select.appendChild(option4);

		var text5 = document.createTextNode("EDITOR");
		option5.appendChild(text5);
		select.appendChild(option5);

		if (pub_ctype_value != 'NONFICTION') {
			var text6 = document.createTextNode("ESSAY");
			option6.appendChild(text6);
			select.appendChild(option6);
		}

		var text7 = document.createTextNode("INTERIORART");
		option7.appendChild(text7);
		select.appendChild(option7);

		var text8 = document.createTextNode("NONFICTION");
		option8.appendChild(text8);
		select.appendChild(option8);

		if (pub_ctype_value != 'OMNIBUS') {
			var text9 = document.createTextNode("NOVEL");
			option9.appendChild(text9);
			select.appendChild(option9);
		}

		var text10 = document.createTextNode("OMNIBUS");
		option10.appendChild(text10);
		select.appendChild(option10);

		var text11 = document.createTextNode("POEM");
		option11.appendChild(text11);
		select.appendChild(option11);

		var text12 = document.createTextNode("SERIAL");
		option12.appendChild(text12);
		select.appendChild(option12);

		if ((pub_ctype_value == 'OMNIBUS') || (pub_ctype_value == 'NONFICTION')) {
			var text13 = document.createTextNode("SHORTFICTION");
			option13.appendChild(text13);
			select.appendChild(option13);
		}

		td4.appendChild(select);
		tr.appendChild(td4);

		// Element: input title_storylen
		var select2 = document.createElement("select");

		// <td><select name="title_storylenX">
		attr = "title_storylen"+next;
		select2.setAttribute("name", attr);
		select2.setAttribute("tabindex", "1");
		select2.setAttribute("class", "contentleninput");
		td5.appendChild(select2);

		// <option></option>
		var option14 = document.createElement("option");
		var text14 = document.createTextNode("");
		option14.appendChild(text14);

		// <option>novella</option>
		var option15 = document.createElement("option");
		var text15 = document.createTextNode("novella");
		option15.appendChild(text15);

		// <option>short story</option>
		var option16 = document.createElement("option");
		var text16 = document.createTextNode("short story");
		option16.appendChild(text16);

		// <option>novelette</option>
		var option17 = document.createElement("option");
		var text17 = document.createTextNode("novelette");
		option17.appendChild(text17);

		select2.appendChild(option14);
		select2.appendChild(option15);
		select2.appendChild(option16);
		select2.appendChild(option17);
		tr.appendChild(td5);
	}
	// Author section
	var tr2    = document.createElement("tr");
	var tda1   = document.createElement("td");
	var bold   = document.createElement("b");
	if (record_type == "title") {
		var text18 = document.createTextNode("Author1:");
		attr = "title_author"+next+".1";
	}
	else if (record_type == "review") {
		var text18 = document.createTextNode("Author1:");
		attr = "review_author"+next+".1";
	}
	else if (record_type == "interview") {
		var text18 = document.createTextNode("Interviewee1:");
		attr = "interviewee_author"+next+".1";
	}
	tr2.setAttribute("id", attr + ".row");
	bold.appendChild(text18);
	tda1.appendChild(bold);
	tr2.appendChild(tda1);

	var tda2   = document.createElement("td");
	var input4 = document.createElement("input");
	input4.setAttribute("id", attr);
	input4.setAttribute("name", attr);
	input4.setAttribute("class", "contentinput");
	input4.setAttribute("tabindex", "1");
	tda2.appendChild(input4);
	tr2.appendChild(tda2);

	// Add Author Button

	// <tr> table element
	var tr3    = document.createElement("tr");
	if (record_type == "title") {
		attr = "AddAuthor"+next;
	}
	else if (record_type == "review") {
		attr = "AddReviewee"+next;
	}
	else if (record_type == "interview") {
		attr = "AddInterviewee"+next;
	}
	tr3.setAttribute("id", attr);

	// <td> Spacer element
	var tda3   = document.createElement("td");
	var text19 = document.createTextNode(" ");
	tda3.appendChild(text19);
	tr3.appendChild(tda3);

	// <td> button element
	var tda4   = document.createElement("td");
	var input5 = document.createElement("input");
	input5.setAttribute("type", "button");
	input5.setAttribute("tabindex", "1");
	if (record_type == "title") {
		input5.setAttribute("value", "Add Author");
		input5.setAttribute("id", "addContentTitleAuthor.button." + next);
	}
	else if (record_type == "review") {
		input5.setAttribute("value", "Add Author");
		input5.setAttribute("id", "addReviewee.button." + next);
	}
	else if (record_type == "interview") {
		input5.setAttribute("value", "Add Interviewee");
		input5.setAttribute("id", "addInterviewee.button." + next);
	}

	isIE = navigator.userAgent.indexOf("MSIE") > -1;
	if (record_type == "title") {
		input5.onclick  = function(event){
			addContentTitleAuthor(event);
		};
	}
	else if (record_type == "review") {
		input5.onclick  = function(event){
			addReviewee(event);
		};
	}
	else if (record_type == "interview") {
		input5.onclick  = function(event){
			addInterviewee(event);
		};
	}
	if (record_type == "review") {
		// Reviewer section
		var tr4    = document.createElement("tr");
		var tda5   = document.createElement("td");
		var bold2  = document.createElement("b");
		var text20 = document.createTextNode("Reviewer1:");
		attr = "review_reviewer"+next+".1";
		tr4.setAttribute("id", attr + ".row");
		bold2.appendChild(text20);
		tda5.appendChild(bold2);
		tr4.appendChild(tda5);

		var tda6   = document.createElement("td");
		var input4 = document.createElement("input");
		input4.setAttribute("id", attr);
		input4.setAttribute("name", attr);
		input4.setAttribute("class", "contentinput");
		input4.setAttribute("tabindex", "1");
		tda6.appendChild(input4);
		tr4.appendChild(tda6);

		// Add Reviewer Button
		var tr5    = document.createElement("tr");
		attr = "AddReviewer"+next;
		tr5.setAttribute("id", attr);

		var tda7   = document.createElement("td");
		var text21 = document.createTextNode(" ");
		tda7.appendChild(text21);
		tr5.appendChild(tda7);

		var tda8   = document.createElement("td");
		var input6 = document.createElement("input");
		input6.setAttribute("id", "addReviewer.button." + next);
		input6.setAttribute("type", "button");
		input6.setAttribute("value", "Add Reviewer");
		input6.setAttribute("tabindex", "1");
		input6.onclick  = function(event){
			addReviewer(event);
		};

		tda8.appendChild(input6);
		tr5.appendChild(tda8);
	}

	else if (record_type == "interview") {
		// Interviewer section
		var tr4    = document.createElement("tr");
		var tda5   = document.createElement("td");
		var bold2  = document.createElement("b");
		var text22 = document.createTextNode("Interviewer1:");
		attr = "interviewer_author"+next+".1";
		tr4.setAttribute("id", attr + ".row");
		bold2.appendChild(text22);
		tda5.appendChild(bold2);
		tr4.appendChild(tda5);

		var tda6   = document.createElement("td");
		var input4 = document.createElement("input");
		input4.setAttribute("id", attr);
		input4.setAttribute("name", attr);
		input4.setAttribute("class", "contentinput");
		input4.setAttribute("tabindex", "1");
		tda6.appendChild(input4);
		tr4.appendChild(tda6);

		// Add Interviewer Button
		var tr5    = document.createElement("tr");
		attr = "AddInterviewer"+next;
		tr5.setAttribute("id", attr);

		var tda7   = document.createElement("td");
		var text23 = document.createTextNode(" ");
		tda7.appendChild(text23);
		tr5.appendChild(tda7);

		var tda8   = document.createElement("td");
		var input6 = document.createElement("input");
		input6.setAttribute("id", "addInterviewer.button." + next);
		input6.setAttribute("type", "button");
		input6.setAttribute("tabindex", "1");
		input6.setAttribute("value", "Add Interviewer");
		input6.onclick  = function(event){
			addInterviewer(event);
		};

		tda8.appendChild(input6);
		tr5.appendChild(tda8);
	}
	tda4.appendChild(input5);
	tr3.appendChild(tda4);

	tbody.insertBefore(tr, addpoint.nextSibling);
	tbody.insertBefore(tr2, tr.nextSibling);
	tbody.insertBefore(tr3, tr2.nextSibling);
	if (record_type != "title") {
		tbody.insertBefore(tr4, tr3.nextSibling);
		tbody.insertBefore(tr5, tr4.nextSibling);
	}

	var tr6  = document.createElement("tr");
	tr6.setAttribute("id", record_type + "_id"+next+".row");
	tr6.className = "titleeditspacer";
	var tdx = document.createElement("td");
	if (record_type == "title") {
		tdx.colSpan = 5;
	}
	else {
		tdx.colSpan = 3;
	}
	tr6.appendChild(tdx);
	if (record_type != "title") {
		tbody.insertBefore(tr6, tr5.nextSibling);
	}
	else {
		tbody.insertBefore(tr6, tr3.nextSibling);
	}
}

function addContentTitleAuthor(event) {
	addPerson(event, "AddAuthor", "Author", "title_author");
}

function addReviewee(event) {
	addPerson(event, "AddReviewee", "Author", "review_author");
}

function addReviewer(event) {
	addPerson(event, "AddReviewer", "Reviewer", "review_reviewer");
}

function addInterviewee(event) {
	addPerson(event, "AddInterviewee", "Interviewee", "interviewee_author");
}

function addInterviewer(event) {
	addPerson(event, "AddInterviewer", "Interviewer", "interviewer_author");
}

function addArtist(event) {
	addPerson(event, "AddArtist", "Artist", "cover_artist");
}

function addPerson(event, tag, label_name, attr_name) {
	var entry = event.target.id.split('.')[2];
	var addpoint = document.getElementById(tag + entry);
	var tbody = addpoint.parentNode;
	var next = GetLastRow(attr_name+entry+'.') + 1;
	// Create the DOM elements
	var tr   = document.createElement("tr");
	var td1  = document.createElement("td");
	var td2  = document.createElement("td");
	var b  = document.createElement("b");
	var label = label_name+next+":";
	var txt1 = document.createTextNode(label);
	var input = document.createElement("input");
	var attr = attr_name+entry+"."+next;
	tr.setAttribute("id", attr + '.row');
	input.setAttribute("name", attr);
	input.setAttribute("class", 'contentinput');
	input.setAttribute("tabindex", "1");
	input.setAttribute("id", attr);
	// Link the elements into the DOM
	td1.appendChild(b);
	b.appendChild(txt1);
	td2.appendChild(input);
	tr.appendChild(td1);
	tr.appendChild(td2);
	tbody.insertBefore(tr, addpoint);
}
