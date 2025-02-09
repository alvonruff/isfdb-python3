#
#     (C) COPYRIGHT 2014-2023 Ahasuerus
#     ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1161 $
#     Date: $Date: 2023-12-05 19:08:38 -0500 (Tue, 05 Dec 2023) $


from isfdb import *
from login import *
from library import *
from navbar import *


def HelpGeneral():

        ##################################################################################
        # This function defines Help text that is shared by all data entry forms
        ##################################################################################
        help = {}

        # If the current user has chosen not to display mouseover help, do not build the Help dictionary
        user = User()
        user.load()
        if user.suppress_help_bubbles:
                return {}

        text = 'For short fiction titles, select appropriate length from the drop-down list.'
        text += ' A short story contains under 7,500 words (roughly 20 or fewer pages in a book.)'
        text += ' A novelette contains between 7,500 and 17,500 words (roughly between 20 and 50 pages in a book.)'
        text += ' A novella contains between 17,500 and 40,000 words (roughly between 50 and 100 pages in a book.)'
        text += ' Follow this link for more details.'
        help['Length'] = [text, ISFDBWikiTemplate('TitleFields:Length')]

        text = 'Optional additional information for the reviewing moderator. This note '
        text += 'is seen only by the moderator handling the submission and does not become a part '
        text += 'of the database record. However, it will be visible on submission history pages, '
        text += 'so confidential information should not be entered in it. Follow this link for more details.'
        help['Note to Moderator'] = [text, ISFDBWikiTemplate('ModNote')]
        return help

def HelpSeries():

        ##################################################################################
        # This function defines Help text for the Edit Series entry form
        ##################################################################################

        help = HelpGeneral()
        if not help:
                return help

        text = 'The name of this series.'
        help['Name'] = [text, '']

        text = 'If the name of this series is spelled using a non-Latin alphabet/script,'
        text += ' enter the Romanized form of the name in this field.'
        text += ' If there is more than one possible Romanization, click the +'
        text += ' button, which will create a new input field, and enter the other spellings of the name.'
        text += ' Follow this link for more details.'
        link = ISFDBWikiPage('Help:Screen:EditSeries')
        help['Transliterated Name 1'] = [text, link]

        text = 'The name of the series that contains this series. You can nest series as deeply as necessary.'
        help['Parent'] = [text, link]

        text = 'If you want a sub-series to appear in a certain location within the parent series, enter its'
        text += ' relative position in this field. This is particularly useful when one series clearly follows'
        text += ' another within its parent superseries. For example, if one trilogy follows another, then'
        text += ' you can put both trilogies in the same super-series and enter a value of 1 for the first trilogy and 2 for the second trilogy.'
        help['Series Parent Position'] = [text, link]

        text = 'URL of a Web site about this series. This is a repeating field and you can enter as many Web pages as necessary.'
        help['Web Page 1'] = [text, link]

        text = 'A free text note describing this series.'
        help['Note'] = [text, link]

        return help

def HelpPublisher():

        ##################################################################################
        # This function defines Help text for the Edit Publisher entry form
        ##################################################################################

        help = HelpGeneral()
        if not help:
                return help

        text = 'The name of this publisher. Only moderators can edit publisher names.'
        text += ' Follow this link for more details.'
        link = ISFDBWikiPage('Help:Screen:EditPublisher')
        help['Publisher Name'] = [text, link]

        text = 'If the name of this publisher is spelled using a non-Latin alphabet/script,'
        text += ' enter the Romanized form of the name in this field.'
        text += ' If there is more than one possible Romanization, click the +'
        text += ' button, which will create a new input field, and enter the other spellings of the name.'
        text += ' Follow this link for more details.'
        help['Transliterated Name 1'] = [text, link]

        text = 'URL of a Web site about this publisher. This is a repeating field and you can enter as many Web pages as necessary.'
        help['Web Page 1'] = [text, link]

        text = 'A free text note describing this publisher. Follow this link for more details.'
        help['Note'] = [text, link]

        return help

def HelpPubSeries():

        ##################################################################################
        # This function defines Help text for the Edit Publication Series entry form
        ##################################################################################

        help = HelpGeneral()
        if not help:
                return help

        text = 'The name of this publication series.'
        link = ISFDBWikiPage('Help:Screen:PublicationSeries')
        help['Pub. Series Name'] = [text, link]

        text = 'If the name of this publication series is spelled using a non-Latin alphabet/script,'
        text += ' enter the Romanized form of the name in this field.'
        text += ' If there is more than one possible Romanization, click the +'
        text += ' button, which will create a new input field, and enter the other spellings of the name.'
        text += ' Follow this link for more details.'
        help['Transliterated Name 1'] = [text, link]

        text = 'URL of a Web site about this publication series. This is a repeating field and you can enter as many Web pages as necessary.'
        help['Web Page 1'] = [text, link]

        text = 'A free text note describing this publication series.'
        help['Note'] = [text, link]

        return help

def HelpAwardType():

        ##################################################################################
        # This function defines Help text for the Edit Award Type data entry form
        ##################################################################################

        help = HelpGeneral()
        if not help:
                return help

        text = 'The short name of this award.'
        help['Short Name'] = [text, '']

        text = 'The full formal name of this award as defined by the organization that gives the award.'
        help['Full Name'] = [text, '']

        text = 'What this award is given for, e.g. best work of horror, best SF work published in a certain country, etc.'
        help['Awarded For'] = [text, '']

        text = 'The name of the organization that gives the award. Common types of organizations include '
        text += 'conventions, professional associations and fan associations.'
        help['Awarded By'] = [text, '']

        text = 'Select No if this award is limited to wins and nominations. Select Yes if this award assigns numeric places, e.g. 1, 2, 10, etc.'
        help['Poll'] = [text, '']

        text = 'Select No if this award is limited to genre (SF) works like the Hugo award. '
        text += 'Select Yes if this award is not limited to genre works like the Newbery award.'
        help['Non-Genre'] = [text, '']

        text = 'URL of a Web page or a Web site about this award type. This is a repeating field and you can enter as many Web pages as necessary.'
        help['Web Page 1'] = [text, '']

        text = 'A free text note describing this award. This note will become a part of the permanent record for this award type.'
        help['Note'] = [text, '']

        return help

def HelpAwardCat():

        ##################################################################################
        # This function defines Help text for the New Award Category data entry form
        ##################################################################################

        help = HelpGeneral()
        if not help:
                return help

        text = 'The name of this award category for the selected award type.'
        help['Award Category'] = [text, '']

        text = 'The relative numeric position of this award category on this award type\'s annual pages.'
        help['Display Order'] = [text, '']

        text = 'URL of a Web page or a Web site about this award category. This is a repeating field and you can enter as many Web pages as necessary.'
        help['Web Page 1'] = [text, '']

        text = 'A free text note describing this award category. This note will become a part of the permanent record for this award category.'
        help['Note'] = [text, '']

        return help

def HelpLanguage():

        ##################################################################################
        # This function defines Help text for the New Language data entry form
        ##################################################################################

        help = HelpGeneral()
        if not help:
                return help

        text = 'Full name of the new language according to the ISO 639-2 Standard.'
        help['Language Name'] = [text, '']

        text = '3-letter language code of the new language assigned by the ISO 639-2 Standard. Not displayed on ISFDB pages at this time.'
        help['Language Code'] = [text, '']

        text = 'A Yes/No flag indicating whether the language uses a Latin-derived script. If the language supports multiple scripts'
        text += ' (e.g. Serbian) and one of them is Latin-derived, the flag is set to \'Yes\'. This flag is used by nightly cleanup'
        text += ' reports to find records that may have been entered using the wrong script.'
        help['Latin-Derived'] = [text, '']

        return help

def HelpVerificationSource():

        ########################################################################################
        # This function defines Help text for the Add/Edit Verification Sources data entry forms
        ########################################################################################

        help = HelpGeneral()
        if not help:
                return help

        text = 'Short label describing this secondary verification source.'
        help['Source Label'] = [text, '']

        text = 'Full name of this secondary verification source.'
        help['Source Name'] = [text, '']

        text = 'URL of this secondary verification source.'
        help['Source URL'] = [text, '']

        return help

def HelpRecognizedDomain():

        ############################################################################################
        # This function defines Help text for the Edit/Delete/Add Recognized Domain data entry forms
        ############################################################################################

        help = HelpGeneral()
        if not help:
                return help

        text = 'Name of this Internet domain recognized by the ISFDB.'
        help['Domain Name'] = [text, '']

        text = 'Displayed Web site name associated with this domain name.'
        help['Web Site Name'] = [text, '']

        text = 'URL of the Web site which will be linked when crediting images hosted by this domain.'
        help['Web Site URL'] = [text, '']

        text = 'Yes if image linking is allowed for this domain, No otherwise.'
        help['Linking Allowed'] = [text, '']

        text = 'Optional URL segment which must be present in the image URL in order for the domain name to be recognized by the ISFDB.'
        help['Required URL Segment'] = [text, '']

        text = 'Yes if the URL of a credit page must be appended to the image URL after a vertical bar (|), No otherwise.'
        help['Explicit Credit Page Link Required'] = [text, '']

        return help

def HelpTemplate():

        ##################################################################################
        # This function defines Help text for the Add/Edit ISFDB template data entry forms
        ##################################################################################

        help = HelpGeneral()
        if not help:
                return help

        text = 'Name of this ISFDB template.'
        help['Name'] = [text, '']

        text = 'Displayed name of this ISFDB template.'
        help['Displayed Name'] = [text, '']

        text = 'Internal URL for an Internal ISFDB URL, External URL for'
        text += ' a link to a third party Web site, Substitute String for no URL.'
        help['Template Type'] = [text, '']

        text = 'Link URL if defined. For internal links, do not include http(s)'
        text += ' or the ISFDB domain name. Use %s for the template parameter.'
        help['Link URL'] = [text, '']

        text = 'Mouseover help for this ISFDB template.'
        help['Mouseover Help'] = [text, '']

        return help
        
def HelpAuthor():

        ##################################################################################
        # This function defines Help text for the Edit Author data entry form
        ##################################################################################

        help = HelpGeneral()
        if not help:
                return help

        text = 'The name under which a particular author\'s bibliography is organized.'
        text += ' For authors who publish under multiple names, the canonical name is the most'
        text += ' recognized name for that author. It does not have to be the author\'s legal name.'
        text += ' Only moderators can edit this field at this time.'
        text += ' Follow this link for more details.'
        help['Canonical Name'] = [text, ISFDBWikiTemplate('AuthorFields:CanonicalName')]

        text = 'If the author\'s canonical name is spelled using a non-Latin alphabet/script in the author\'s'
        text += ' working language, enter the Romanized form of the canonical name in this field.'
        text += ' If there is more than one possible Romanization, click the +'
        text += ' button below, which will create a new input field, and enter the other Romanized spellings of the canonical name.'
        text += ' Follow this link for more details.'
        help['Transliterated Name 1'] = [text, ISFDBWikiTemplate('AuthorFields:TransName')]

        text = 'The most recent legal name for the author in the "Lastname, Firstname Middlenames"'
        text += ' format, with all names being given in full. No suffixes or prefixes should be used.'
        text += ' Use the alphabet/script of the author\'s working language. Follow this link for more details.'
        help['Legal Name'] = [text, ISFDBWikiTemplate('AuthorFields:LegalName')]

        text = 'If the author\'s legal name is spelled using a non-Latin alphabet/script in the author\'s'
        text += ' working language, enter the Romanized form of the legal name in this field.'
        text += ' If there is more than one possible Romanization, click the + button,'
        text += ' which will create a new input field, and enter the other spellings of the legal name. If the author has lived in'
        text += ' countries or regions that use additional alphabets/scripts, enter those spellings of the'
        text += ' legal name as well. Follow this link for more details.'
        help['Trans. Legal Name 1'] = [text, ISFDBWikiTemplate('AuthorFields:TransLegalName')]

        text = 'The name (usually the family name) under which this author will appear in the Author Directory.'
        text += ' Use Latin transliteration for non-Latin characters. Follow this link for more details.'
        help['Directory Entry'] = [text, ISFDBWikiTemplate('AuthorFields:DirectoryEntry')]

        text = 'The place where this person was born in the "city, municipality/state, country, empire" format.'
        text += ' Follow this link for more details.'
        help['Birth Place'] = [text, ISFDBWikiTemplate('AuthorFields:BirthPlace')]

        text = 'The date when this person was born in the YYYY-MM-DD format. If the day is unknown, use YYYY-MM-00.'
        text += ' If the month is unknown, use YYYY-00-00. If the birthdate is unknown, leave the field blank. Do'
        text += ' not enter guesstimates (1956?) or approximations (c1956).'
        text += ' Follow this link for more details.'
        help['Birth Date'] = [text, ISFDBWikiTemplate('AuthorFields:BirthDate')]

        text = 'The date when this person died in the YYYY-MM-DD format. If the day is unknown, use YYYY-MM-00.'
        text += ' If the month is unknown, use YYYY-00-00. If the author is known to be alive or if there is no'
        text += ' reliable information about the author, leave the field blank. However, if the author was born'
        text += ' more than 125 years ago and is therefore presumably dead, you can enter a death date of 0000-00-00.'
        text += ' Follow this link for more details.'
        help['Death Date'] = [text, ISFDBWikiTemplate('AuthorFields:DeathDate')]

        text = 'This person\'s working language, i.e. the language that he or she used to write most of'
        text += ' his or her works. Select the appropriate language from the drop-down list.'
        text += ' Follow this link for more details.'
        help['Working Language'] = [text, ISFDBWikiTemplate('AuthorFields:Language')]

        text = 'If you know the author\'s email address and the author does not mind making the email'
        text += ' address public, enter it here. This is a repeating field and you can enter as many'
        text += ' e-mail addresses as necessary.'
        text += ' Follow this link for more details.'
        help['Email Address 1'] = [text, ISFDBWikiTemplate('AuthorFields:EmailAddress')]

        text = 'URL of the author\'s personal Web site(s) or a site about his or her work.'
        text += 'This is a repeating field and you can enter as many Web pages as necessary.'
        text += ' Follow this link for more details.'
        help['Web Page 1'] = [text, ISFDBWikiTemplate('AuthorFields:WebPage')]

        text = 'URL of this author\'s image on the Internet. Follow this link for more details.'
        help['Author Image'] = [text, ISFDBWikiTemplate('AuthorFields:AuthorImage')]

        text = 'A brief bibliographic or biographical comment about this author.'
        text += ' Follow this link for more details.'
        help['Note'] = [text, ISFDBWikiTemplate('AuthorFields:Note')]

        return help
        
def HelpTitlePub():

        ###################################################################################
        # This function defines Help text which is shared by Title and Pub data entry forms
        ###################################################################################

        help = HelpGeneral()
        if not help:
                return help

        text = 'Transliterated Title. Populate only if the title is spelled using'
        text += ' a non-Latin alphabet/script. If you know the Romanized form of the'
        text += ' name, enter it in this field. If there is more than one possible'
        text += ' Romanization, click the + button, which will create a new input field,'
        text += ' and enter the other Romanized spellings of the title. You can click'
        text += ' on the + button as many times as necessary.'
        help['Transliterated Title 1'] = [text, '']

        text = 'An optional short non-spoiler synopsis. This field is not a place for criticism or reviews'
        text += ' and should maintain a neutral point of view. This field is disabled for CHAPBOOKS and'
        text += ' variant titles. Follow this link for more details.'
        help['Synopsis'] = [text, ISFDBWikiTemplate('TitleFields:Synopsis')]

        text = 'A free text note describing this title such as the name of the translator.'
        text += ' Information about this particular publication/edition should be entered'
        text += ' in the Pub Note field further down the page. Follow this link for more details.'
        help['Title Note'] = [text, ISFDBWikiTemplate('TitleFields:Note')]

        text = 'This publication\'s language. Select the appropriate language from the drop-down list.'
        text += ' Follow this link for more details.'
        help['Language'] = [text, ISFDBWikiTemplate('TitleFields:Language')]

        text = 'The name of the series to which this work belongs, if any. Note that variant titles and translations cannot be put in a series;'
        text += ' use their parent titles instead. CHAPBOOKs cannot be put in series. Follow this link for more details.'
        help['Series'] = [text, ISFDBWikiTemplate('TitleFields:Series')]

        text = 'The number of this work within its series. Series numbers must be between 1 and 999999999. You can use a decimal point'
        text += ' and up to 4 digits after it to position titles in between other titles in the series, e.g. 3.5 will appear between 3 and 4.'
        text += ' Note that variant titles and translations cannot be put in a series; use their parent titles instead.'
        text += ' CHAPBOOKs cannot be put in series. Follow this link for more details.'
        help['Series Num'] = [text, ISFDBWikiTemplate('TitleFields:SeriesNum')]

        text = 'For omnibuses that contain numbered titles belonging to the same series, enter their respective numbers within'
        text += ' the series, e.g. \'1,2\' or \'4-6\'. For other types of omnibuses, enter the count of included titles, e.g.'
        text += ' \'3N\' or \'2N+2C\' where \'N\' stands for \'Novel\' and \'C\' stands for "Collection".'
        text += ' Follow this link for more details.'
        help['Content'] = [text, ISFDBWikiTemplate('TitleFields:Content')]

        return help

def HelpMakeVariant():

        ##################################################################################
        # This function defines Help text displayed by Make Variant Title
        ##################################################################################

        help = HelpTitle()
        if not help:
                return help

        text = 'The title of the new work that you want to create.'
        help['Title'] = [text, '']

        text = 'Note associated with the new work that you want to create. Follow this link for more details.'
        help['Title Note'] = [text, ISFDBWikiTemplate('TitleFields:Note')]

        return help

def HelpTitle(title_type = 'NOVEL'):

        ##################################################################################
        # This function defines Help text displayed by Edit Title entry forms
        ##################################################################################

        help = HelpTitlePub()
        if not help:
                return help

        text = 'The title of this work. The title should appear exactly as published. Note that if you'
        text += ' change the title on this page, the change will affect all publications'
        text += ' in which this work appears. Follow this link for more details.'
        help['Title'] = [text, ISFDBWikiTemplate('TitleFields:Title')]

        text = 'The title of this review. The title should appear exactly as published. Note that if you'
        text += ' change the title on this page, the change will affect all publications'
        text += ' in which this review appears. Follow this link for more details.'
        help['Review of'] = [text, ISFDBWikiTemplate('TitleFields:Title')]

        text = 'The title of this interview. The title should appear exactly as published. Note that if you'
        text += ' change the title on this page, the change will affect all publications'
        text += ' in which this interview appears. Follow this link for more details.'
        help['Interview Title'] = [text, ISFDBWikiTemplate('TitleFields:Title')]

        text = 'URL of a Web site about this title. This is a repeating field and you can enter as many '
        text += ' Web pages as necessary. To add another Web Page, click the + button.'
        text += ' Follow this link for more details.'
        help['Web Page 1'] = [text, ISFDBWikiTemplate('TitleFields:WebPage')]

        text = 'The name of the author of this title. To add another author, click the + button.'
        text += ' Follow this link for more details.'
        if title_type == 'REVIEW':
                link = ISFDBWikiTemplate('TitleFields:ReviewAuthor')
        else:
                link = ISFDBWikiTemplate('TitleFields:Author')
        help['Author 1'] = [text, link]

        text = 'The name of the reviewer exactly as it appears on the title page.'
        text += ' This includes pseudonyms, abbreviated names, etc. If no author is stated, use \'uncredited\'.'
        text += ' To add another reviewer, click the + button. Follow this link for more details.'
        help['Reviewer 1'] = [text, ISFDBWikiTemplate('TitleFields:Reviewer')]

        text = 'The name of the person who was interviewed. To add another interviewee, click the + button.'
        text += ' Follow this link for more details.'
        help['Interviewee 1'] = [text, ISFDBWikiTemplate('TitleFields:Interviewee')]

        text = 'The name of the interviewer exactly as it appears on the title page.'
        text += ' This includes pseudonyms, abbreviated names, etc. If no author is stated, use \'uncredited\'.'
        text += ' To add another interviewer, click the + button. Follow this link for more details.'
        help['Interviewer 1'] = [text, ISFDBWikiTemplate('TitleFields:Interviewer')]

        text = 'The date of the first appearance of this title in the form of YYYY-MM-DD. If the month or day is not known, use 00.'
        text += ' If the year is also unknown, use 0000-00-00. Follow this link for more details.'
        help['Date'] = [text, ISFDBWikiTemplate('TitleFields:Date')]

        text = 'This work\'s language. Select the appropriate language from the drop-down list.'
        text += ' Follow this link for more details.'
        help['Language'] = [text, ISFDBWikiTemplate('TitleFields:Language')]

        text = 'The type of the title being entered. Select the appropriate type from the drop-down list.'
        text += ' Follow this link for more details.'
        help['Title Type'] = [text, ISFDBWikiTemplate('TitleFields:TitleType')]

        text = 'Check this check-box if this title is written for a juvenile audience.'
        text += ' Follow this link for more details.'
        help['Juvenile'] = [text, ISFDBWikiTemplate('TitleFields:Juvenile')]

        text = 'Check this check-box if this title is a novelization.'
        text += ' Follow this link for more details.'
        help['Novelization'] = [text, ISFDBWikiTemplate('TitleFields:Novelization')]

        text = 'Check this check-box if this title is not speculative fiction'
        text += ' or about speculative fiction. Follow this link for more details.'
        help['Non-Genre'] = [text, ISFDBWikiTemplate('TitleFields:NonGenre')]

        text = 'Check this check-box if this title is a graphic format work.'
        text += ' COVERART, INTERIORART, REVIEW, and INTERVIEW titles can\'t be graphic.'
        text += ' Follow this link for more details.'
        help['Graphic Format'] = [text, ISFDBWikiTemplate('TitleFields:GraphicFormat')]

        text = 'A free text note describing this title.'
        help['Note'] = [text, ISFDBWikiTemplate('TitleFields:Note')]

        return help

def HelpPub():

        ##################################################################################
        # This function defines Help text displayed by Pub data entry forms
        ##################################################################################

        help = HelpTitlePub()
        if not help:
                return help
        
        text = 'The title of the publication exactly as it appears on the title page.'
        text += ' Follow this link for more details.'
        help['Title'] = [text, ISFDBWikiTemplate('PublicationFields:Title')]

        text = 'The name of the author of the publication exactly as it appears on the title page.'
        text += ' This includes pseudonyms, abbreviated names, etc. If no author is stated, use \'uncredited\'.'
        text += ' To add another author, click the + button. Follow this link for more details.'
        help['Author 1'] = [text, ISFDBWikiTemplate('PublicationFields:Author')]

        text = 'The name of the editor of the publication exactly as it appears on the title page.'
        text += ' This includes pseudonyms, abbreviated names, etc. If no editor is stated, use \'uncredited\'.'
        text += ' To add another editor, click the + button. Follow this link for more details.'
        help['Editor 1'] = [text, ISFDBWikiTemplate('PublicationFields:Author')]

        text = 'Click this button to add additional authors, if any.'
        help['Add Author'] = [text, '']

        text = 'Click this button to add additional editors, if any.'
        help['Add Editor'] = [text, '']

        text = 'The date of publication in the form of YYYY-MM-DD. If the month or day is not known, use 00.'
        text += ' If the year is also unknown, use 0000-00-00. Follow this link for more details.'
        help['Date'] = [text, ISFDBWikiTemplate('PublicationFields:Date')]

        text = 'The name of the publisher. Follow this link for more details.'
        help['Publisher'] = [text, ISFDBWikiTemplate('PublicationFields:Publisher')]

        text = 'The page count of the publication. For books, use the last printed page number. '
        text += 'For magazines, use the actual page count including the cover. Follow this link for more details.'
        help['Pages'] = [text, ISFDBWikiTemplate('PublicationFields:Pages')]

        text = 'The format of the publication. hc stands for hardcovers, pb for '
        text += '7\'\' by 4.25\'\' (18 cm by 11 cm) paperbacks, tp for other paperbacks, ph for pamphlets. '
        text += 'Follow this link for an explanation of the other supported formats.'
        help['Format'] = [text, ISFDBWikiTemplate('PublicationFields:Format')]

        text = 'Type of publication. Follow this link for more details.'
        help['Pub Type:'] = [text, ISFDBWikiTemplate('PublicationFields:PubType')]

        text = 'ISBN if the publication has one. Follow this link for more details.'
        help['ISBN'] = [text, ISFDBWikiTemplate('PublicationFields:ISBN')]

        text = 'Catalog ID if the publication has one. Follow this link for more details.'
        help['Catalog ID'] = [text, ISFDBWikiTemplate('PublicationFields:CatalogID')]
        
        text = 'If this publication is listed by a recognized third party Web site'
        text += ' which has assigned a permanent ID to it, select the Web site from the'
        text += ' drop-down list on the left and enter the ID in the field on the right.'
        text += ' To add more External IDs, click the + button. Follow this link for more details.'
        help['External IDs'] = [text, ISFDBWikiTemplate('PublicationFields:ExternalIDs')]

        text = 'The original cover price of this publication. Follow this link for more details.'
        help['Price'] = [text, ISFDBWikiTemplate('PublicationFields:Price')]

        text = 'Enter the cover artist if known, otherwise leave blank. Follow this link for more details.'
        help['Artist1'] = [text, ISFDBWikiTemplate('PublicationFields:CoverArt')]

        text = 'Click this button to add additional cover artists, if any.'
        help['Add Artist'] = [text, '']

        text = 'A URL to an image of the cover art. URLs should only be entered if ISFDB has permission '
        text += 'to link to the hosting Web site. Follow this link for more details and a list of sites that ISFDB is allowed to link to.'
        help['Image URL'] = [text, ISFDBWikiTemplate('PublicationFields:ImageURL')]

        text = 'The name of the publication series that this publication belongs to, e.g. \'\'Ballantine Adult Fantasy\'\'.'
        text += ' Publication series, which group related publications, are not to be confused with regular series, which group related titles.'
        text += ' Follow this link for more details.'
        help['Pub Series'] = [text, ISFDBWikiTemplate('PublicationFields:PubSeries')]

        text = 'The number or ID of this publication within its publication series. Follow this link for more details.'
        help['Pub Series #'] = [text, ISFDBWikiTemplate('PublicationFields:PubSeries')]

        text = 'Check this check-box if the main title in this publication is written for a juvenile audience.'
        text += ' Follow this link for more details.'
        help['Juvenile'] = [text, ISFDBWikiTemplate('PublicationFields:Juvenile')]

        text = 'Check this check-box if the main title in this publication is a novelization.'
        text += ' Follow this link for more details.'
        help['Novelization'] = [text, ISFDBWikiTemplate('PublicationFields:Novelization')]

        text = 'Check this check-box if the main title in this publication'
        text += ' is not speculative fiction or about speculative fiction.'
        text += ' Follow this link for more details.'
        help['Non-Genre'] = [text, ISFDBWikiTemplate('PublicationFields:NonGenre')]

        text = 'Check this check-box if the main title in this publication'
        text += ' is a graphic format work. Follow this link for more details.'
        help['Graphic Format'] = [text, ISFDBWikiTemplate('PublicationFields:GraphicFormat')]

        text = 'Select the choice that matches the source of your data and enter any'
        text += ' additional information in the Note field.'
        help['Source'] = [text, '']

        text = 'A note specific to this publication. This note will become a permanent part of the record.'
        text += ' Follow this link for more details.'
        help['Pub Note'] = [text, ISFDBWikiTemplate('PublicationFields:PubNote')]

        text = 'URL of a Web site about this title. This is a repeating field and you can enter as many '
        text += ' Web pages as necessary. To add another Web Page, click the + button.'
        text += ' Follow this link for more details.'
        help['Title Web Page 1'] = [text, ISFDBWikiTemplate('TitleFields:WebPage')]

        text = 'URL of a Web site about this publication. This is a repeating field and you can enter as many '
        text += ' Web pages as necessary. To add another Web Page, click the + button.'
        text += ' Follow this link for more details.'
        # The label of this field is normally "Web Page", but the NewPub edit form
        # uses "Pub Web Page" in order to distinguish this field from title-specific Web Pages
        help['Pub Web Page 1'] = [text, ISFDBWikiTemplate('PubFields:WebPage')]
        help['Web Page 1'] = [text, ISFDBWikiTemplate('PubFields:WebPage')]

        return help

def HelpCoverArt():
        ###############################################################
        # This function defines Help text displayed by the Cover Art 
        # subsection of the Content section of the Pub data entry forms
        ###############################################################

        help = HelpGeneral()
        if not help:
                return help
        
        text = """The title of the cover art exactly as it appears on the cover
                  of this publication. Follow this link for more details."""
        help['Title'] = [text, ISFDBWikiTemplate('PublicationFields:CoverArt')]

        text = 'The original publication date of this cover art. If you leave this field blank, the date'
        text += ' will default to the date of the publication. Follow this link for more details.'
        help['Date'] = [text, ISFDBWikiTemplate('TitleFields:Date')]

        text = 'The name of the artist as it appears in the publication. Follow this link for more details.'
        help['Artist1:'] = [text, ISFDBWikiTemplate('PublicationFields:CoverArt')]

        text = 'Click this button to add additional artists for this cover. You can add as many artists as needed.'
        help['Add Artist'] = [text, '']

        return help

def HelpTitleContent():
        ##################################################################################
        # This function defines Help text displayed by the Title subsection of the Content
        # section of Pub data entry forms
        ##################################################################################

        help = HelpGeneral()
        if not help:
                return help
        
        text = 'The page on which this item of content can be found. Follow this link for more details.'
        help['Page'] = [text, ISFDBWikiTemplate('PubContentFields:Page')]
        
        text = 'The title of the work exactly as it appears in this publication. Follow this link for more details.'
        help['Title'] = [text, ISFDBWikiTemplate('TitleFields:Title')]

        text = 'The original publication date of this title. If you leave this field blank, the date'
        text += ' will default to the date of the publication. Follow this link for more details.'
        help['Date'] = [text, ISFDBWikiTemplate('TitleFields:Date')]

        text = 'The name of the author of the work exactly as it appears in the publication. Follow this link for more details.'
        help['Author1:'] = [text, ISFDBWikiTemplate('TitleFields:Author')]

        text = 'Click this button to add additional authors. You can add as many authors as needed.'
        help['Add Author'] = [text, '']

        text = 'The type of the title being entered. Select the appropriate type from the drop-down list.'
        text += ' Follow this link for more details.'
        help['Title Type'] = [text, ISFDBWikiTemplate('TitleFields:TitleType')]

        return help

def HelpReviewContent():
        ##################################################################################
        # This function defines Help text displayed by the Review subsection of the Content
        # section of Pub data entry forms
        ##################################################################################

        help = HelpGeneral()
        if not help:
                return help
        
        text = 'The page on which this review can be found. Follow this link for more details.'
        help['Page'] = [text, ISFDBWikiTemplate('PubContentFields:ReviewPage')]

        text = 'The title of the review. Follow this link for more details.'
        help['Title'] = [text, ISFDBWikiTemplate('TitleFields:ReviewTitle')]

        text = 'The original publication date of this review. If you leave this field blank, the date'
        text += ' will default to the date of the publication. Follow this link for more details.'
        help['Date'] = [text, ISFDBWikiTemplate('TitleFields:ReviewDate')]

        text = 'The name of the author of the reviewed work. Follow this link for more details.'
        help['Author1:'] = [text, ISFDBWikiTemplate('TitleFields:ReviewAuthor')]

        text = 'The name of the reviewer exactly as it appears in the publication.'
        text += ' Follow this link for more details.'
        help['Reviewer1:'] = [text, ISFDBWikiTemplate('TitleFields:Reviewer')]

        text = 'Click this button to add additional authors of the reviewed work. You can add as many authors as needed.'
        help['Add Author'] = [text, '']

        text = 'Click this button to add additional reviewers. You can add as many reviewers as needed.'
        help['Add Reviewer'] = [text, '']

        return help

def HelpInterviewContent():
        ######################################################################################
        # This function defines Help text displayed by the Interview subsection of the Content
        # section of Pub data entry forms
        ######################################################################################

        help = HelpGeneral()
        if not help:
                return help

        text = 'The page on which this interview can be found. Follow this link for more details.'
        help['Page'] = [text, ISFDBWikiTemplate('PubContentFields:InterviewPage')]

        text = 'The title of the interview exactly as published. Follow this link for more details.'
        help['Interview Title'] = [text, ISFDBWikiTemplate('TitleFields:InterviewTitle')]

        text = 'The original publication date of this interview. If you leave this field blank, the date'
        text += ' will default to the date of the publication. Follow this link for more details.'
        help['Date'] = [text, ISFDBWikiTemplate('TitleFields:InterviewDate')]

        text = 'The name of the interviewed person. Follow this link for more details.'
        help['Interviewee1:'] = [text, ISFDBWikiTemplate('TitleFields:Interviewee')]

        text = 'The name of the interviewer exactly as it appears in the publication.'
        text += ' Follow this link for more details.'
        help['Interviewer1:'] = [text, ISFDBWikiTemplate('TitleFields:Interviewer')]

        text = 'Click this button to add additional interviewed persons. You can add as many interviewees as needed.'
        help['Add Interviewee'] = [text, '']

        text = 'Click this button to add additional interviewers. You can add as many interviewers as needed.'
        help['Add Interviewer'] = [text, '']

        return help

def HelpAward(poll):
        ##################################################################################
        # This function defines Help text displayed by Award data entry forms
        ##################################################################################
        
        help = HelpGeneral()
        if not help:
                return help
        
        text = 'If the award was given to something that has a title (publication, movie, TV show, etc) but is not eligible for inclusion in ISFDB, '
        text += 'enter the title in this field. '
        text += 'If the award was given to someone or something that does not have a title, e.g. Best Artist, Best Editor, Best Publisher, then enter '
        text += 'the word \'untitled\' in this field. When the award is displayed, a \'----\' will be displayed in the title column. '
        text += 'Follow this link for more details.'
        link = ISFDBWikiPage('Help:Screen:AddAward')
        help['Title'] = [text, link]

        text = 'Enter the canonical name of the person associated with this award as it currently exists in ISFDB. '
        text += 'To add another person, click the + button. Follow this link for more details.'
        help['Author1'] = [text, link]

        text = 'Enter the year of the award using the YYYY-00-00 format. This should be the year of the award, not the year of publication. '
        text += 'Follow this link for more details.'
        help['Year'] = [text, link]

        text = 'Name of the award. Make sure not to confuse the John W. Campbell Award with the John W. Campbell Memorial Award. '
        text += 'Follow this link for more details.'
        help['Award Name'] = [text, link]

        text = 'The category of the award, such as \'Best Novel\', \'Best SF Novel\', or \'Best Novelette\'. When the awards are displayed '
        text += 'for a particular year (say 1993 Hugo Award), they will be grouped according to categories. '
        text += 'Follow this link for more details.'
        help['Category'] = [text, link]

        if poll == 'No':
                text = 'Select \'Win\' for winners and \'Nomination\' for nominees. Award records can be entered as nominees when the nominees '
                text += 'are first announced (that is, when there are no winners yet) and changed when the winner is announced at a later date. '
        else:
                text = 'For regular awards, select the \'Poll place\' radio button and enter the award ranking between 1 and 70. '
        
        text += 'For withdrawn, preliminary and other types of special nominees, choose the \'Special\' radio button and select the appropriate '
        text += 'choice from the drop-down list. '
        text += 'Follow this link for more details.'
        help['Award Level'] = [text, link]
        
        text = 'A note specific to this award. This note will become a permanent part of the record.'
        text += ' Follow this link for more details.'
        help['Note'] = [text, link]

        text = 'When entering an award given to a movie or a TV show, enter its IMDB title code, e.g. tt0533409. '
        text += 'Follow this link for more details.'
        help['IMDB Title'] = [text, link]

        return help

def HelpTag():
        ##################################################################################
        # This function defines Help text displayed by Tag Editor entry forms
        ##################################################################################
        
        help = HelpGeneral()
        if not help:
                return help
        
        text = 'Tags are user-defined words and short phrases that help categorize titles in the ISFDB. '
        text += 'To add another tag, click the + button. Follow this link for more details.'
        help['Tag 1'] = [text, ISFDBWikiPage('Help:Screen:TagEditor')]

        return help
