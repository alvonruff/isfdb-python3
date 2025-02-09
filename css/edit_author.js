/*     Version: $Revision: 970 $
      (C) COPYRIGHT 2015-2022   Ahasuerus
         ALL RIGHTS RESERVED
      Date: $Date: 2022-08-15 12:47:52 -0400 (Mon, 15 Aug 2022) $ */

function validateAuthorForm() {
	// Validate that a non-empty author name has been entered
	if (validateRequired("author_canonical","Canonical Name") == false) {
		return false;
	}
	// Validate that a non-empty directory entry has been entered
	if (validateRequired("author_lastname","Directory Entry") == false) {
		return false;
	}
	// Validate that the author's canonical name doesn't contain double quotes or plus signs
	if (validateDoubleQuotesAndPlusSigns("author_canonical","Canonical Name") == false) {
		return false;
	}
	// Validate the birth date
	if (validateRequiredDate("author_birthdate", "Birth Date", "not required", "author") == false) {
		return false;
	}
	// Validate the death date
	if (validateRequiredDate("author_deathdate", "Death Date", "not required", "author") == false) {
		return false;
	}
	// Validate the author image URL
	if (validateURL("author_image") == false) {
		return false;
	}
	// Validate emails
	if (validateEmails("author_emails") == false) {
		return false;
	}
	// Validate the Web Page URLs
	if (validateWebPages("author_webpages") == false) {
		return false;
	}
	// If validation passes, return "true", which will let the form submit
	return true;
}

function validateDoubleQuotesAndPlusSigns(field_name, display_name) {
	// Retrieve the Title field - use [0] because JS returns an array in case there are many fields with this name
	var element_name = document.getElementsByName(field_name)[0];
	// Retrieve the value of the field
	var element_value = element_name.value;
	// Check if the resulting string contains double quotes and generate an alert error
	if (element_value.indexOf("\"") !== -1) {
		alert("Double quotes are not allowed in " + display_name + ". Use single quotes instead.");
		element_name.focus();
		return false;
	}
	if (element_value.indexOf("+") !== -1) {
		alert("Plus signs are currently not allowed in " + display_name + ".");
		element_name.focus();
		return false;
	}
	return true;
}

function validateEmails(field_name) {
	var last_row = GetLastRow(field_name);
	var email_field;
	for (i = 1 ; i < (last_row +1) ; i++) {
		email_field = field_name + i;
		// Validate each email
		if (validateEmail(email_field) == false) {
			return false;
		}
	}
	return true;
}

function validateEmail(field_name) {
	// Retrieve the URL field - use [0] because JS returns an array in case there are many fields with this name
	var element_name = document.getElementsByName(field_name)[0];
	// If there is no email field, validation fails
	if (element_name == null) {
		return false;
	}
	// Retrieve the value of the field
	var element_value = element_name.value;
	// If the value is empty, then validation passes
	if (element_value == "") {
		return true;
	}
	// Check that the email follows the "name@domain.top-level-domain" format
	if (element_value.match(/\S+@\S+\.\S+/gi) == null) {
		alert("Email addresses must use a valid format.");
		element_name.focus();
		return false;
	}
	return true;
}
