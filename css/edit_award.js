/*     Version: $Revision: 970 $
      (C) COPYRIGHT 2015-2018   Ahasuerus
         ALL RIGHTS RESERVED
      Date: $Date: 2022-08-15 12:47:52 -0400 (Mon, 15 Aug 2022) $ */

function validateAwardForm() {
	// Validate the award year
	if (validateRequiredDate("award_year", "Award Year", "required", "award") == false) {
		return false;
	}
	// Validate authors
	if (validateAuthors("title_author", "Award author", "no") == false) {
		return false;
	}

	// Check if the Award Level radio button is set to "Level"
	if ((document.getElementById("LEVEL_LEVEL")) && (document.getElementById("LEVEL_LEVEL").checked)) {
		// Validate the award level
		if (validateAwardLevel("award_level","Award Level (when the Poll place button is selected)") == false) {
			return false;
		}
	}
	return true;
}

function validateAwardLevel(field_name, display_name) {
	if (validateRequired(field_name, display_name) == false) {
		return false;
	}
	// Check the value of the "LEVEL" field
	var field_value = document.getElementsByName(field_name)[0].value;
	var num = parseInt(field_value, 10);
	if ((field_value.match(/^\d+$/) == null) || (num < 1) || (num > 70)) {
		alert(display_name + " must be an integer number between 1 and 70.");
		return false;
	}
	return true;
}

function validateAwardTypeForm() {
	if (validateRequired("award_type_short_name", "Short Name") == false) {
		return false;
	}
	if (validateRequired("award_type_name", "Full Name") == false) {
		return false;
	}
	// Validate the Web Page URLs
	if (validateWebPages("award_type_webpages") == false) {
		return false;
	}
	return true;
}

function validateAwardCatForm() {
	if (validateRequired("award_cat_name", "Category Name") == false) {
		return false;
	}
	// Retrieve the id of the Display Order field
	var element_name = document.getElementsByName("award_cat_order")[0];
	// Retrieve the value of the field
	var element_value = element_name.value.split(" ").join("");
	// If the value doesn't match 0-9 numbers (the first one can't be 0), display an error
	if (element_value != "") {
		if (element_value.match(/^[1-9]{1}[0-9]{0,8}$/) == null) {
			alert("Display Order must be an integer greater than 0 and contain 1-9 digits.");
			element_name.focus();
			return false;
		}
	}
	// Validate the Web Page URLs
	if (validateWebPages("award_cat_webpages") == false) {
		return false;
	}
	return true;
}
