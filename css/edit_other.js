/*     Version: $Revision: 418 $
      (C) COPYRIGHT 2015-2018   Ahasuerus
         ALL RIGHTS RESERVED
      Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $ */

function validateSeriesForm() {
	if (validateRequired("series_name", "Series Name") == false) {
		return false;
	}
	// Retrieve the id of the Series Number field
	var element_name = document.getElementsByName("series_parentposition")[0];
	// Retrieve the value of the field
	var element_value = element_name.value.split(" ").join("");
	// If the value doesn't match 0-9 numbers (the first one can't be 0), display an error
	if (element_value != "") {
		if (element_value.match(/^[1-9]{1}[0-9]{0,8}$/) == null) {
			alert("Series Parent Position must be an integer greater than 0 and contain 1-9 digits.");
			element_name.focus();
			return false;
		}
	}
	// Validate the Web Page URLs
	if (validateWebPages("series_webpages") == false) {
		return false;
	}
	return true;
}

function validatePubSeriesForm() {
	if (validateRequired("pub_series_name", "Publication Series Name") == false) {
		return false;
	}
	// Validate the Web Page URLs
	if (validateWebPages("pub_series_webpages") == false) {
		return false;
	}
	return true;
}

function validatePublisherForm() {
	if (validateRequired("publisher_name", "Publisher Name") == false) {
		return false;
	}
	// Validate the Web Page URLs
	if (validateWebPages( "publisher_webpages") == false) {
		return false;
	}
	return true;
}
