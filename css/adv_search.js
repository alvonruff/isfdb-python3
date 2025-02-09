/*     Version: $Revision: 19 $
      (C) COPYRIGHT 2017-2019   Ahasuerus
         ALL RIGHTS RESERVED
      Date: $Date: 2017-10-31 19:26:25 -0400 (Tue, 31 Oct 2017) $ */


document.addEventListener('DOMContentLoaded', function() {
	createOnchange();
});

function YesNo() {
	var formats = ["Yes", "No"];
	return formats;
}

function PubFormats()	{
	return GetValidValues('Formats');
}

function PubTypes()	{
	return GetValidValues('PubTypes');
}

function TitleTypes()	{
	return GetValidValues('TitleTypes');
}

function StoryLengths()	{
	return GetValidValues('StoryLengths');
}

function AllLanguages()	{
	return GetValidValues('AllLanguages');
}

function AwardLevels()	{
	return GetValidValues('AwardLevels');
}

function SecondaryVerSources()	{
	return GetValidValues('SecondaryVerSources');
}

function GetValidValues(select_name)	{
	var field = document.getElementById(select_name);
	var field_values = [];
	var i;
	var len = field.options.length;
	for (i = 0; i < len; i++) {
		field_values.push(field.options[i].value);
	}
	return field_values;
}

function Selectors(selector_number, new_value, record_type) {
	var value_id = record_type + 'term';
	// Create a handle for the search value field
	var search_value = document.getElementById(value_id + '_' + selector_number);
	// Create a handle for the operatore field
	var operator = document.getElementById(record_type + '_operator_' + selector_number);
	// Get the parent element's row object
	var parent_row = document.getElementById(record_type + '_selectors' + '_' + selector_number);
	var values = "";
	var whitespace = document.createTextNode(' ');
	switch(new_value) {
	case "pub_ptype":
		values = PubFormats();
		break;
	case "pub_ctype":
		values = PubTypes();
		break;
	case "title_ttype":
		values = TitleTypes();
		break;
	case "title_storylen":
		values = StoryLengths();
		break;
	case "title_jvn":
		values = YesNo();
		break;
	case "title_nvz":
		values = YesNo();
		break;
	case "title_non_genre":
		values = YesNo();
		break;
	case "title_graphic":
		values = YesNo();
		break;
	case "title_language":
		values = AllLanguages();
		break;
	case "author_language":
		values = AllLanguages();
		break;
	case "award_type_poll":
		values = YesNo();
		break;
	case "award_type_non_genre":
		values = YesNo();
		break;
	case "award_level":
		values = AwardLevels();
		break;
	case "secondary_ver_source":
		values = SecondaryVerSources();
		break;
	default:
		values = "";
		break;
	}
	if (values != "") {
		parent_row.removeChild(search_value);
		var new_search_value = document.createElement('select');
		new_search_value.name = 'TERM_' + selector_number;
		new_search_value.id = value_id + '_'+selector_number;
		for (var i = 0; i < values.length; i++) {
			var option = document.createElement("option");
			option.value = values[i];
			option.text = values[i];
			new_search_value.appendChild(option);
		}
		parent_row.insertBefore(new_search_value, operator.nextSibling);
		parent_row.insertBefore(whitespace, new_search_value);
	}
	else {
		// If we are switching from a text input field to another text input field,
		// don't change the field value
		if (search_value.type == 'text') {
			return true;
		}
		parent_row.removeChild(search_value);
		var new_search_value = document.createElement('input');
		new_search_value.type = 'text';
		new_search_value.name = 'TERM_' + selector_number;
		new_search_value.size = 50;
		new_search_value.id = value_id + '_' + selector_number;
		parent_row.insertBefore(new_search_value, operator.nextSibling);
		parent_row.insertBefore(whitespace, new_search_value);
	}
	return true;
}

function createOnchange()	{
	if (document.getElementById('author_1')) {
		document.getElementById('author_1').onchange = function(event){
			Selectors(1, this.value, 'author');
		};
		document.getElementById('author_2').onchange = function(event){
			Selectors(2, this.value, 'author');
		};
		document.getElementById('author_3').onchange = function(event){
			Selectors(3, this.value, 'author');
		};
		document.getElementById('author_4').onchange = function(event){
			Selectors(4, this.value, 'author');
		};
		document.getElementById('author_5').onchange = function(event){
			Selectors(5, this.value, 'author');
		};
		document.getElementById('author_6').onchange = function(event){
			Selectors(6, this.value, 'author');
		};
		document.getElementById('author_7').onchange = function(event){
			Selectors(7, this.value, 'author');
		};
		document.getElementById('author_8').onchange = function(event){
			Selectors(8, this.value, 'author');
		};
		document.getElementById('author_9').onchange = function(event){
			Selectors(9, this.value, 'author');
		};
		document.getElementById('author_10').onchange = function(event){
			Selectors(10, this.value, 'author');
		};
	}
	if (document.getElementById('title_1')) {
		document.getElementById('title_1').onchange = function(event){
			Selectors(1, this.value, 'title');
		};
		document.getElementById('title_2').onchange = function(event){
			Selectors(2, this.value, 'title');
		};
		document.getElementById('title_3').onchange = function(event){
			Selectors(3, this.value, 'title');
		};
		document.getElementById('title_4').onchange = function(event){
			Selectors(4, this.value, 'title');
		};
		document.getElementById('title_5').onchange = function(event){
			Selectors(5, this.value, 'title');
		};
		document.getElementById('title_6').onchange = function(event){
			Selectors(6, this.value, 'title');
		};
		document.getElementById('title_7').onchange = function(event){
			Selectors(7, this.value, 'title');
		};
		document.getElementById('title_8').onchange = function(event){
			Selectors(8, this.value, 'title');
		};
		document.getElementById('title_9').onchange = function(event){
			Selectors(9, this.value, 'title');
		};
		document.getElementById('title_10').onchange = function(event){
			Selectors(10, this.value, 'title');
		};
	}
	if (document.getElementById('pub_1')) {
		document.getElementById('pub_1').onchange = function(event){
			Selectors(1, this.value, 'pub');
		};
		document.getElementById('pub_2').onchange = function(event){
			Selectors(2, this.value, 'pub');
		};
		document.getElementById('pub_3').onchange = function(event){
			Selectors(3, this.value, 'pub');
		};
		document.getElementById('pub_4').onchange = function(event){
			Selectors(4, this.value, 'pub');
		};
		document.getElementById('pub_5').onchange = function(event){
			Selectors(5, this.value, 'pub');
		};
		document.getElementById('pub_6').onchange = function(event){
			Selectors(6, this.value, 'pub');
		};
		document.getElementById('pub_7').onchange = function(event){
			Selectors(7, this.value, 'pub');
		};
		document.getElementById('pub_8').onchange = function(event){
			Selectors(8, this.value, 'pub');
		};
		document.getElementById('pub_9').onchange = function(event){
			Selectors(9, this.value, 'pub');
		};
		document.getElementById('pub_10').onchange = function(event){
			Selectors(10, this.value, 'pub');
		};
	}
	if (document.getElementById('award_type_1')) {
		document.getElementById('award_type_1').onchange = function(event){
			Selectors(1, this.value, 'award_type');
		};
		document.getElementById('award_type_2').onchange = function(event){
			Selectors(2, this.value, 'award_type');
		};
		document.getElementById('award_type_3').onchange = function(event){
			Selectors(3, this.value, 'award_type');
		};
		document.getElementById('award_type_4').onchange = function(event){
			Selectors(4, this.value, 'award_type');
		};
		document.getElementById('award_type_5').onchange = function(event){
			Selectors(5, this.value, 'award_type');
		};
		document.getElementById('award_type_6').onchange = function(event){
			Selectors(6, this.value, 'award_type');
		};
		document.getElementById('award_type_7').onchange = function(event){
			Selectors(7, this.value, 'award_type');
		};
		document.getElementById('award_type_8').onchange = function(event){
			Selectors(8, this.value, 'award_type');
		};
		document.getElementById('award_type_9').onchange = function(event){
			Selectors(9, this.value, 'award_type');
		};
		document.getElementById('award_type_10').onchange = function(event){
			Selectors(10, this.value, 'award_type');
		};
	}
	if (document.getElementById('award_1')) {
		document.getElementById('award_1').onchange = function(event){
			Selectors(1, this.value, 'award');
		};
		document.getElementById('award_2').onchange = function(event){
			Selectors(2, this.value, 'award');
		};
		document.getElementById('award_3').onchange = function(event){
			Selectors(3, this.value, 'award');
		};
		document.getElementById('award_4').onchange = function(event){
			Selectors(4, this.value, 'award');
		};
		document.getElementById('award_5').onchange = function(event){
			Selectors(5, this.value, 'award');
		};
		document.getElementById('award_6').onchange = function(event){
			Selectors(6, this.value, 'award');
		};
		document.getElementById('award_7').onchange = function(event){
			Selectors(7, this.value, 'award');
		};
		document.getElementById('award_8').onchange = function(event){
			Selectors(8, this.value, 'award');
		};
		document.getElementById('award_9').onchange = function(event){
			Selectors(9, this.value, 'award');
		};
		document.getElementById('award_10').onchange = function(event){
			Selectors(10, this.value, 'award');
		};
	}
}
