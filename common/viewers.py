from __future__ import print_function
#
#     (C) COPYRIGHT 2007-2025   Al von Ruff, Ahasuerus, Bill Longley and Klaus Elsbernd
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1216 $
#     Date: $Date: 2025-01-25 12:15:47 -0500 (Sat, 25 Jan 2025) $

from xml.dom import minidom
from xml.dom import Node
from library import *

class ContentTable():
        def __init__(self, submission):
                self.caption = ''
                self.css_table = 'generic_table'
                self.css_warning = 'warn'
                self.css_blank_warning = 'blankwarning'
                self.empty_cell = '-'
                self.headers = []
                self.rows = []
                self.fragment_separator = '<span class="mergesign">+</span>'
                self.submission = submission
                self.warnings_exist = 0

        def PrintTable(self):
                if not self.rows:
                        return
                if self.caption:
                        print('<h2>%s</h2>' % self.caption)
                print('<table border="2" class="%s">' % self.css_table)
                print('<tr>')
                for header in self.headers:
                        print('<td class="label"><b>%s</b></td>' % header)
                if self.warnings_exist:
                        print('<td class="label"><b>Warnings</b></td>')
                print('</tr>')

                for row in self.rows:
                        print('<tr>')
                        for cell in row.cells:
                                cell_values = []
                                for fragment in cell.fragments:
                                        if fragment.id:
                                                # Link author name if already on file
                                                display_value = ISFDBLink(fragment.link, fragment.id, fragment.value)
                                        else:
                                                display_value = ISFDBText(fragment.value)
                                        cell_values.append(display_value)
                                cell_value = self.fragment_separator.join(cell_values)
                                if not cell_value:
                                        cell_value = self.empty_cell
                                print('<td class="%s">%s</td>' % (cell.background, cell_value))
                        if self.warnings_exist:
                                if row.warnings:
                                        warning_css = self.css_warning
                                else:
                                        warning_css = self.css_blank_warning
                                print('<td class="%s">%s</td>' % (warning_css, '<br>'.join(row.warnings)))
                        print('</tr>')
                print('</table>')

class ContentRow():
        def __init__(self, table):
                self.cells = []
                self.xml_record = ''
                self.table = table
                self.warnings = []

        def AddCell(self, element_name):
                self.element_name = element_name
                value = GetChildValue(self.xml_record, self.element_name)
                cell = ContentCell(self)
                cell.AddFragment(value)
                self.cells.append(cell)

        def AddAuthorCell(self, element_name):
                self.element_name = element_name
                name_list = GetChildValue(self.xml_record, self.element_name)
                names = name_list.split('+')
                cell = ContentCell(self)
                for name in names:
                        cell.AddAuthorFragment(name)
                self.cells.append(cell)

        def AddTitleCell(self, referral_language = ''):
                cell = ContentCell(self)
                cell.referral_language = referral_language
                cell.AddTitleFragment()
                self.cells.append(cell)

        def AddMergeMethod(self):
                cell = ContentCell(self)
                cell.AddMergeMethodFragment()
                self.cells.append(cell)

class ContentCell():
        def __init__(self, row):
                self.drop_background = 'drop'
                self.keep_background = 'keep'
                self.background = self.keep_background
                self.row = row
                self.fragments = []

        def AddFragment(self, value):
                fragment = ContentFragment(self)
                fragment.CheckValue(value)
                self.fragments.append(fragment)

        def AddAuthorFragment(self, name):
                fragment = ContentFragment(self)
                fragment.NormalizeName(name)
                self.fragments.append(fragment)

        def AddTitleFragment(self):
                fragment = ContentFragment(self)
                fragment.Title()
                self.fragments.append(fragment)

        def AddMergeMethodFragment(self):
                fragment = ContentFragment(self)
                fragment.MergeMethod()
                self.fragments.append(fragment)

class ContentFragment():
        def __init__(self, cell):
                self.cell = cell
                self.id = ''
                self.link = ''
                self.value = ''

        def CheckValue(self, value):
                self.value = value
                if self.cell.row.element_name == 'cDate':
                        if ISFDBdaysFromToday(value) > SESSION.max_future_days:
                                self._AddWarning('Date more than %d days in the future' % SESSION.max_future_days)
                        pub_date = self.cell.row.table.submission.metadata.get('Year')
                        if not pub_date and self.cell.row.table.submission.current_record:
                                pub_date = self.cell.row.table.submission.current_record.pub_year
                        if self.value and pub_date and (ISFDBCompare2Dates(pub_date, self.value) == 1):
                                self._AddWarning('Title date after publication date')

        def NormalizeName(self, name):
                # Do not display author warnings for auto-merge titles
                title_id = GetChildValue(self.cell.row.xml_record, 'Record')
                if title_id and title_id != '0':
                        manual_merge = 0
                else:
                        manual_merge = 1

                if manual_merge and SQLMultipleAuthors(name):
                        self._AddWarning('%s is a disambiguated name' % name)
                author_data = SQLgetAuthorData(name)
                if author_data:
                        self.value = author_data[AUTHOR_CANONICAL]
                        self.id = author_data[AUTHOR_ID]
                        self.link = 'ea.cgi'
                        if manual_merge and SQLauthorIsPseudo(author_data[AUTHOR_ID]):
                                self._AddWarning('%s is an alternate name' % name)
                else:
                        self.value = name
                        if manual_merge:
                                self._AddWarning('%s is a new author' % name)

        def Title(self):
                title_id = GetChildValue(self.cell.row.xml_record, 'Record')
                if title_id and int(title_id):
                        title_id = int(title_id)
                        self.cell.row.table.submission._CheckTitleExistence(title_id)
                        self.link = 'title.cgi'
                        self.id = title_id
                        current_title = SQLloadTitle(title_id)
                        self.value = current_title[TITLE_TITLE]
                        imported_referral_language = self.cell.referral_language
                        current_referral_language = current_title[TITLE_LANGUAGE]
                        if (imported_referral_language
                            and current_referral_language
                            and imported_referral_language != current_referral_language):
                                self._AddWarning('Language mismatch')
                else:
                        self.value = GetChildValue(self.cell.row.xml_record, 'cTitle')

        def MergeMethod(self):
                title_id = int(GetChildValue(self.cell.row.xml_record, 'Record'))
                if title_id:
                        self.value = 'Auto Merge'
                else:
                        self.value = 'Manual Merge'
                        self.cell.background = self.cell.drop_background

        def _AddWarning(self, warning, html_escape = 1):
                if not warning:
                        return
                if html_escape:
                        warning = ISFDBText(warning)
                if warning not in self.cell.row.warnings:
                        self.cell.row.warnings.append(warning)
                        self.cell.row.table.warnings_exist = 1

class SubmissionTable():
        def __init__(self, submission):
                self.submission = submission

                self.bold_label_css = 'boldlabel'
                self.border = '2'
                self.display_diffs = 0
                self.display_warnings = 0
                self.empty_cell = '-' # alternatively '&nbsp;'
                self.headers = []
                self.headers_colspan = [1]
                self.row_align = 'left'
                self.row_warnings = []
                self.rows = []
                self.css_active_background = 'keep'
                self.css_info_background = 'info'
                self.css_superseeded_background = 'drop'
                self.css_table = 'generic_table'
                self.css_warning = 'warn'
                self.css_blank_warning = 'blankwarning'
                self.suppress_warnings = 0
                self.update = 1

        def PrintTable(self):
                print('<table border="%s" class="%s">' % (self.border, self.css_table))
                self._PrintHeaders()
                self._PrintBody()
                print('</table>')

        def _PrintHeaders(self):
                print('<tr align="left">')
                if not self.suppress_warnings:
                        for row in self.rows:
                                for cell in row.cells:
                                        for fragment in cell.fragments:
                                                if fragment.warnings:
                                                        row.warnings.extend(fragment.warnings)

                        for row in self.rows:
                                if row.warnings:
                                        self.headers.extend(['Warnings'])
                                        self.display_warnings = 1
                                        break

                for row in self.rows:
                        if row.diffs:
                                self.headers.extend(['Differences'])
                                self.display_diffs = 1
                                break
                
                for count, header in enumerate(self.headers):
                        colspan = 1
                        try:
                                colspan = self.headers_colspan[count]
                        except:
                                pass
                        print('<th colspan="%d" class="%s">%s</th>' % (colspan, self.bold_label_css, header))
                print('</tr>')

        def _PrintBody(self):
                for row in self.rows:
                        if row.type == 'author':
                                separator = '<span class="mergesign">+</span>'
                        else:
                                separator = '<br>'
                        print('<tr align="%s">' % self.row_align)
                        if row.label:
                                print('<td class="%s">%s</td>' % (self.bold_label_css, row.label))
                        for cell in row.cells:
                                cell_values = []
                                for fragment in cell.fragments:
                                        if fragment.type == 'cover':
                                                display_value = ISFDBFormatImage(fragment.value, fragment.id)
                                        elif fragment.type == 'image':
                                                display_value = ISFDBFormatImage(fragment.value)
                                        elif fragment.type == 'webpage':
                                                display_value = '<a href="%s" target="_blank">%s</a>' % (fragment.value, ISFDBText(fragment.value))
                                        elif fragment.type == 'award_imdb':
                                                display_value = IMDBLink(fragment.value, fragment.value)
                                        elif fragment.type == 'prebuilt':
                                                display_value = fragment.value
                                        elif row.note and fragment.value:
                                                display_value = FormatNote(fragment.value, '', 'edit')
                                        elif fragment.link:
                                                display_value = ISFDBLink(fragment.link, fragment.id, fragment.value)
                                        else:
                                                display_value = ISFDBText(fragment.value)
                                        cell_values.append(display_value)
                                cell_value = separator.join(cell_values)
                                if not cell_value:
                                        cell_value = self.empty_cell
                                print('<td class="%s">%s</td>' % (cell.background, cell_value))
                        if self.display_warnings:
                                if row.warnings:
                                        warning_css = self.css_warning
                                else:
                                        warning_css = self.css_blank_warning
                                print('<td class="%s">%s</td>' % (warning_css, '<br>'.join(row.warnings)))
                        if self.display_diffs:
                                print('<td class="%s">%s</td>' % (self.css_info_background, '<br>'.join(row.diffs)))
                        print('</tr>')

        def Add1MetadataRow(self, label, element_name, row_type = 'default', warning = ''):
                row = SubmissionRow(self, label)
                row.element_name = element_name
                row.type = row_type
                row.AddWarning(warning)
                row.Build1MetadataRow()
                self.rows.append(row)

        def Add1MetadataNoteRow(self, label, element_name):
                row = SubmissionRow(self, label)
                row.element_name = element_name
                row.type = 'note'
                row.note = 1
                row.Build1MetadataRow()
                self.rows.append(row)

        def Add1AttributeRow(self, label, attribute_value, row_type = 'default', warning = ''):
                row = SubmissionRow(self, label)
                row.type = row_type
                row.left_value = attribute_value
                row.Build1AttributeRow()
                row.AddWarning(warning)
                self.rows.append(row)

        def Add1AttributeCoverRow(self, label, attribute_value, pub_id):
                row = SubmissionRow(self, label)
                row.type = 'cover'
                row.left_value = attribute_value
                row.pub_id = pub_id
                row.Build1AttributeRow()
                self.rows.append(row)

        def Add1AttributeNoteRow(self, label, attribute_value):
                row = SubmissionRow(self, label)
                row.type = 'note'
                row.note = 1
                row.left_value = attribute_value
                row.Build1AttributeRow()
                self.rows.append(row)

        def Add1MetadataMultiRow(self, multi_type, label, group_name, element_name, warning = ''):
                row = SubmissionRow(self, label)
                row.multi_type = multi_type
                row.group_name = group_name
                row.element_name = element_name
                row.AddWarning(warning)
                row.Build1MetadataMultiRow()
                self.rows.append(row)

        def Add1AttributeMultiRow(self, label, multi_type, attribute_values):
                row = SubmissionRow(self, label)
                row.multi_type = multi_type
                row.left_values = attribute_values
                row.Build1AttributeMultiRow()
                self.rows.append(row)

        def Add2AttributesMultiRow(self, label, multi_type, left_values, right_values):
                row = SubmissionRow(self, label)
                row.multi_type = multi_type
                row.left_values = left_values
                row.right_values = right_values
                row.Build2AttributesMultiRow()
                self.rows.append(row)

        def Add2AttributesRow(self, label, left_value, right_value, row_type = 'default', warning = ''):
                row = SubmissionRow(self, label)
                row.type = row_type
                row.left_value = left_value
                row.right_value = right_value
                row.AddWarning(warning)
                row.Build2AttributesRow()
                self.rows.append(row)

        def Add2AttributesNoteRow(self, label, left_value, right_value, row_type = 'default', warning = ''):
                row = SubmissionRow(self, label)
                row.note = 1
                row.type = row_type
                row.left_value = left_value
                row.right_value = right_value
                row.AddWarning(warning)
                row.Build2AttributesRow()
                self.rows.append(row)

        def AddAttributeToMetadataRow(self, label, property_value, element_name, row_type = 'default', warning = '', note = 0):
                row = SubmissionRow(self, label)
                row.type = row_type
                row.left_value = property_value
                row.element_name = element_name
                row.note = note
                row.AddWarning(warning)
                row.BuildAttributeToMetadataRow()
                self.rows.append(row)

        def AddAttributeToMetadataMultiRow(self, label, multi_type, left_values, group_name, element_name):
                row = SubmissionRow(self, label)
                row.multi_type = multi_type
                row.left_values = left_values
                row.group_name = group_name
                row.element_name = element_name
                row.BuildAttributeToMetadataMultiRow()
                self.rows.append(row)

        def AddAuthorRowFromNames(self, left_names, right_names, warning = ''):
                self.AddNameRowFromNames('Authors', left_names, right_names, warning)

        def AddNameRowFromNames(self, label, left_names, right_names, warning = ''):
                row = SubmissionRow(self, label)
                row.left_values = left_names
                row.right_values = right_names
                row.AddWarning(warning)
                row.BuildAuthorRowFromNames()
                self.rows.append(row)

        def AddAuthorRowNameToXML(self, left_names, group_name, element_name):
                row = SubmissionRow(self, 'Authors')
                row.left_values = left_names
                row.group_name = group_name
                row.element_name = element_name
                row.BuildAuthorRowNameToMetadata()
                self.rows.append(row)

        def AddCoverRowFromIDs(self, variant_id, parent_id):
                row = SubmissionRow(self, 'Covers')
                row.BuildCoverRowFromIDs(variant_id, parent_id)
                self.rows.append(row)

        def DisplayAddRecord(self):
                self.headers.extend(['Field', 'Proposed Value'])
                self.PrintTable()

        def DisplayDeleteRecord(self):
                self.headers.extend(['Field', 'Current Value'])
                self.PrintTable()

        def DisplayMetadataEdit(self):
                self.headers.extend(['Field', 'Current', 'Proposed'])
                self.PrintTable()

class SubmissionRow():
        def __init__(self, table, label):
                self.table = table
                self.label = label

                self.cells = []
                self.diffs = []
                self.element_name = ''
                self.group_name = ''
                self.left_cell = ''
                self.left_value = ''
                self.left_values = []
                self.multi_type = ''
                self.note = 0
                self.pub_id = 0
                self.right_cell = ''
                self.right_value = ''
                self.right_values = []
                self.type = 'default'
                self.warnings = []

        def AddWarning(self, warning):
                if warning:
                        self.warnings.append(warning)

        def Build1MetadataRow(self):
                cell = SubmissionCell(self)
                cell.BuildMetadataCell()
                self.cells.append(cell)

        def Build1AttributeRow(self):
                cell = SubmissionCell(self)
                cell.BuildAttributeCell(self.left_value)
                self.cells.append(cell)

        def Build1MetadataMultiRow(self):
                cell = SubmissionCell(self)
                cell.BuildMetadataMultiCell()
                self.cells.append(cell)

        def Build1AttributeMultiRow(self):
                self.left_cell = SubmissionCell(self)
                self.left_cell.BuildMultiCellFromValues(self.left_values)
                self.cells.append(self.left_cell)

        def Build2AttributesMultiRow(self):
                self.left_cell = SubmissionCell(self)
                self.left_cell.BuildMultiCellFromValues(self.left_values)
                self.cells.append(self.left_cell)
                
                self.right_cell = SubmissionCell(self)
                self.right_cell.BuildMultiCellFromValues(self.right_values)
                self.cells.append(self.right_cell)

        def BuildAttributeToMetadataMultiRow(self):
                self.left_cell = SubmissionCell(self)
                self.left_cell.BuildMultiCellFromValues(self.left_values)
                self.cells.append(self.left_cell)
                
                self.right_cell = SubmissionCell(self)
                self.right_cell.BuildMetadataMultiCell()
                self.cells.append(self.right_cell)

                self._SetBackground()
                self._MultiDiffs()
                
        def BuildAuthorRowFromNames(self):
                self.type = 'author'

                self.left_cell = SubmissionCell(self)
                self.left_cell.BuildAuthorCellFromNames(self.left_values)
                self.cells.append(self.left_cell)

                self.right_cell = SubmissionCell(self)
                self.right_cell.BuildAuthorCellFromNames(self.right_values)
                self.cells.append(self.right_cell)

        def BuildAuthorRowNameToMetadata(self):
                self.type = 'author'
                self.multi_type = 'author'

                self.left_cell = SubmissionCell(self)
                self.left_cell.BuildAuthorCellFromNames(self.left_values)
                self.cells.append(self.left_cell)

                self.right_cell = SubmissionCell(self)
                self.right_cell.BuildMetadataMultiCell()
                self.cells.append(self.right_cell)

                self._SetBackground()

        def BuildCoverRowFromIDs(self, variant_id, parent_id):
                self.type = 'cover'
                
                self.left_cell = SubmissionCell(self)
                self.left_cell.BuildCoverCellForTitle(variant_id)
                self.cells.append(self.left_cell)

                self.right_cell = SubmissionCell(self)
                self.right_cell.BuildCoverCellForTitle(parent_id)
                self.cells.append(self.right_cell)

        def Build2AttributesRow(self):
                self.left_cell = SubmissionCell(self)
                self.left_cell.BuildAttributeCell(self.left_value)
                self.cells.append(self.left_cell)

                self.right_cell = SubmissionCell(self)
                self.right_cell.BuildAttributeCell(self.right_value)
                self.cells.append(self.right_cell)

                self._MismatchWarnings()

        def BuildAttributeToMetadataRow(self):
                self.left_cell = SubmissionCell(self)
                self.left_cell.BuildAttributeCell(self.left_value)
                self.cells.append(self.left_cell)

                self.right_cell = SubmissionCell(self)
                self.right_cell.BuildMetadataCell()
                self.cells.append(self.right_cell)
                
                self._SetBackground()
                self._MismatchWarnings()
                self._NoteDiffs()

        def _NoteDiffs(self):
                if not self.note:
                        return
                if not self.table.update:
                        return
                if not self._CellValuesDiffer():
                        return

                attribute_note = self.left_cell.fragments[0].value
                metadata_note = self.right_cell.fragments[0].value

                self._CreateDiffsFromLists(attribute_note.splitlines(), metadata_note.splitlines())

        def _MultiDiffs(self):
                if self.group_name not in ('Webpages', 'PubSeriesTransNames',
                                           'PublisherTransNames', 'SeriesTransNames',
                                           'AuthorTransNames', 'AuthorTransLegalNames',
                                           'Emails', 'TranslitTitles'):
                        return
                if not self.table.update:
                        return

                attribute_note = []
                for fragment in self.left_cell.fragments:
                        attribute_note.append(fragment.value)
                metadata_note = []
                for fragment in self.right_cell.fragments:
                        metadata_note.append(fragment.value)
                if not attribute_note or not metadata_note:
                        return
                self._CreateDiffsFromLists(attribute_note, metadata_note)

        def _CreateDiffsFromLists(self, before_list, after_list):
                self.diffs = []
                for line in before_list:
                        if line not in after_list:
                                self.diffs.append('- %s' % ISFDBText(line))
                for line in after_list:
                        if line not in before_list:
                                self.diffs.append('+ %s' % ISFDBText(line))

        def _SetBackground(self):
                if self.table.update:
                        if self.right_cell.updated:
                                self.right_cell.background = self.table.css_active_background
                                self.left_cell.background = self.table.css_superseeded_background
                        else:
                                self.right_cell.background = self.table.css_superseeded_background
                                self.left_cell.background = self.table.css_active_background

        def _MismatchWarnings(self):
                if not self.table.update and self._CellValuesDiffer():
                        if self.type == 'nongenre':
                                self.AddWarning('Non-genre flag mismatch')
                        elif self.type == 'juvenile':
                                self.AddWarning('Juvenile flag mismatch')
                        elif self.type == 'novelization':
                                self.AddWarning('Novelization flag mismatch')
                        elif self.type == 'graphic':
                                self.AddWarning('Graphic flag mismatch')
                        elif self.type == 'title_type' and self._TitleTypeMismatch():
                                self.AddWarning('Uncommon title type combination')
                        elif self.type == 'series':
                                self.AddWarning('Series mismatch -- variant title\'s series data will be lost')
                        elif self.type == 'content':
                                self.AddWarning('Content value mismatch')

        def _CellValuesDiffer(self):
                if not self.left_cell.fragments:
                        return 0
                if not self.left_cell.fragments[0].value:
                        return 0
                if not self.right_cell.fragments:
                        return 0
                if not self.right_cell.fragments[0].value:
                        return 0
                if self.left_cell.fragments[0].value != self.right_cell.fragments[0].value:
                        return 1
                return 0

        def _TitleTypeMismatch(self):
                variant_type = self.left_cell.fragments[0].value
                parent_type = self.right_cell.fragments[0].value
                if not parent_type:
                        return 0
                if variant_type == parent_type:
                        return 0
                if variant_type == 'SERIAL' and parent_type in ('NOVEL', 'SHORTFICTION'):
                        return 0
                if variant_type == 'INTERIORART' and parent_type == 'COVERART':
                        return 0
                if variant_type == 'COVERART' and parent_type == 'INTERIORART':
                        return 0
                return 1

class SubmissionCell():
        def __init__(self, row):
                self.row = row
                self.background = self.row.table.css_active_background
                self.fragments = []
                self.updated = 0
                self.warnings = []

        def BuildMetadataCell(self):
                fragment = SubmissionFragment(self)
                fragment.GetValueFromMetadata()
                self.fragments.append(fragment)
                self.updated = self.row.table.submission.updated[self.row.element_name]

        def BuildAttributeCell(self, value):
                fragment = SubmissionFragment(self)
                fragment.GetAttributeValue(value)
                self.fragments.append(fragment)
                
        def BuildMetadataMultiCell(self):
                for value in self.row.table.submission.metadata[self.row.group_name]:
                        fragment = SubmissionFragment(self)
                        fragment.GetMultiValueFromMetadata(value)
                        self.fragments.append(fragment)
                self.updated = self.row.table.submission.updated[self.row.group_name]

        def BuildMultiCellFromValues(self, values):
                for value in values:
                        fragment = SubmissionFragment(self)
                        fragment.GetAttributeValueForMulti(value)
                        self.fragments.append(fragment)
                
        def BuildAuthorCellFromNames(self, names):
                for name in names:
                        fragment = SubmissionFragment(self)
                        fragment.GetAuthorFromName(name)
                        self.fragments.append(fragment)

        def BuildCoverCellForTitle(self, title_id):
                self.type = 'cover'
                cover_pubs = SQLGetCoverPubsByTitle(int(title_id))
                for cover_pub in cover_pubs:
                        if cover_pub[PUB_IMAGE]:
                                fragment = SubmissionFragment(self)
                                fragment.GetCover(cover_pub)
                                self.fragments.append(fragment)

class SubmissionFragment():
        def __init__(self, cell):
                self.cell = cell
                self.id = ''
                self.link = ''
                self.type = self.cell.row.type
                self.value = ''
                self.warnings = []

        def _AddWarning(self, warning, html_escape = 1):
                if not warning:
                        return
                if html_escape:
                        warning = ISFDBText(warning)
                if warning not in self.warnings:
                        self.warnings.append(warning)

        def _CheckHTML(self):
                # HTML tags are allowed in Notes/Synopsis fields
                if self.cell.row.note:
                        return
                # 'Prebuilt' fields are pre-built HTML strings
                if self.type == 'prebuilt':
                        return
                if self.cell.row.table.submission.ui.goodHtmlTagsPresent(self.value):
                        self._AddWarning('Recognized HTML tag(s) outside of Note/Synopsis')

        def _CheckNotes(self):
                if not self.cell.row.note:
                        return
                self._AddWarning(self.cell.row.table.submission.ui.invalidHtmlInNotes(self.value))
                self._AddWarning(self.cell.row.table.submission.ui.mismatchedBraces(self.value))
                self._AddWarning(self.cell.row.table.submission.ui.unrecognizedTemplate(self.value))
                self._AddWarning(self.cell.row.table.submission.ui.mismatchedDoubleQuote(self.value))

        def _CheckDate(self):
                if self.cell.row.type == 'title_date' and ISFDBdaysFromToday(self.value) > SESSION.max_future_days:
                        self._AddWarning('Date is more than %d days in the future' % SESSION.max_future_days)

        def _LinkPublisher(self):
                if not self.value:
                        return
                if self.type != 'publisher':
                        return
                publisher_data = SQLFindPublisher(self.value, 'exact')
                if publisher_data and len(publisher_data) == 1:
                        self.link = 'publisher.cgi'
                        self.value = publisher_data[0][PUBLISHER_NAME]
                        self.id = publisher_data[0][PUBLISHER_ID]

        def _CheckPublisher(self):
                if self.type != 'publisher':
                        return
                if self.cell.row.table.submission.updated[self.cell.row.element_name]:
                        self._CheckOrphanPublisher()

                if not self.value:
                        return
                if not self.id:
                        self._AddWarning('Unknown publisher')
                else:
                        pub_count = SQLCountPubsForPublisher(self.id)
                        if pub_count < 6:
                                self._AddWarning('Only %d publications on file for this publisher' % pub_count)

                disambiguated_publishers = SQLGetDisambiguatedRecords(self.id, self.value, 'publishers', 'publisher_id', 'publisher_name')
                self._AddDisambiguatedWarning(disambiguated_publishers, 'publishers')

                similar_publishers = SQLFindSimilarPublishers(self.id, self.value)
                if similar_publishers:
                        warning = 'There are similar publisher names on file:<br>'
                        for record in similar_publishers:
                                warning += '%s<br>' %ISFDBLink('publisher.cgi', record[0], record[1])
                        self._AddWarning(warning, 0)
                        

        def _CheckOrphanPublisher(self):
                from publisherClass import publishers
                # Check if this pub is the only one associated with its publisher
                pub_id = self.cell.row.table.submission.metadata.get('Record')
                if not pub_id:
                        return
                pub_data = SQLGetPubById(pub_id)
                if not pub_data:
                        return
                publisher_id = pub_data[PUB_PUBLISHER]
                if not publisher_id:
                        return
                pub_count = SQLCountPubsForPublisher(publisher_id)
                if pub_count != 1:
                        return

                current = publishers(db)
                current.load(publisher_id)
                warning = self.cell.row.table.submission._OrphanWarning(current.publisher_name, current.publisher_note, current.publisher_webpages)
                self._AddWarning(warning)

        def _LinkPubSeries(self):
                if not self.value:
                        return
                if self.type != 'pub_series':
                        return
                pub_series_data = SQLFindPubSeries(self.value, 'exact')
                if pub_series_data and len(pub_series_data) == 1:
                        self.link = 'pubseries.cgi'
                        self.value = pub_series_data[0][PUB_SERIES_NAME]
                        self.id = pub_series_data[0][PUB_SERIES_ID]

        def _CheckPubSeries(self):
                if self.type != 'pub_series':
                        return
                if self.cell.row.table.submission.updated[self.cell.row.element_name]:
                        self._CheckOrphanPubSeries()
                if not self.value:
                        return
                if not self.id:
                        self._AddWarning('Unknown publication series')
                disambiguated_pub_series = SQLGetDisambiguatedRecords(self.id, self.value, 'pub_series', 'pub_series_id', 'pub_series_name')
                self._AddDisambiguatedWarning(disambiguated_pub_series, 'publication series')

        def _CheckOrphanPubSeries(self):
                from pubseriesClass import pub_series
                # Check if this pub is the only one associated with its publication series
                pub_id = self.cell.row.table.submission.metadata.get('Record')
                if not pub_id:
                        return
                pub_data = SQLGetPubById(pub_id)
                if not pub_data:
                        return
                pub_series_id = pub_data[PUB_SERIES]
                if not pub_series_id:
                        return
                pub_count = SQLCountPubsForPubSeries(pub_series_id)
                if pub_count != 1:
                        return

                current = pub_series(db)
                current.load(pub_series_id)
                warning = self.cell.row.table.submission._OrphanWarning(current.pub_series_name, current.pub_series_note, current.pub_series_webpages)
                self._AddWarning(warning)

        def _LinkSeries(self):
                if not self.value:
                        return
                if self.type != 'series':
                        return
                series_data = SQLGetSeriesByName(self.value)
                if series_data:
                        self.link = 'pe.cgi'
                        self.value = series_data[SERIES_NAME]
                        self.id = series_data[SERIES_PUBID]
                        
        def _CheckSeries(self):
                if not self.value:
                        return
                if self.type != 'series':
                        return
                if not self.id:
                        self._AddWarning('Unknown series')
                disambiguated_series = SQLGetDisambiguatedRecords(self.id, self.value, 'series', 'series_id', 'series_title')
                self._AddDisambiguatedWarning(disambiguated_series, 'series')

        def _AddDisambiguatedWarning(self, disambiguated_list, record_name):
                if not disambiguated_list:
                        return
                if record_name == 'series':
                        cgi_script = 'pe'
                        id_position = SERIES_PUBID
                        name_position = SERIES_NAME
                elif record_name == 'publishers':
                        cgi_script = 'publisher'
                        id_position = PUBLISHER_ID
                        name_position = PUBLISHER_NAME
                elif record_name == 'publication series':
                        cgi_script = 'pubseries'
                        id_position = PUB_SERIES_ID
                        name_position = PUB_SERIES_NAME
                warning = 'There are other %s with a disambiguated version of this name:<br>' % record_name
                for count, record in enumerate(disambiguated_list):
                        if count == 5:
                                warning += 'There are %d additional matching %s. ' % (len(disambiguated_list) - 5, record_name)
                                warning += 'Follow one of the links above to see all of them.'
                                break
                        warning += '%s<br>' %ISFDBLink('%s.cgi' % cgi_script, record[id_position], record[name_position])
                self._AddWarning(warning, 0)

        def _LinkAwardType(self):
                if not self.value:
                        return
                if self.type != 'award_type_name':
                        return
                award_type_data = SQLGetAwardTypeByShortName(self.value)
                if award_type_data:
                        self.link = 'awardtype.cgi'
                        self.value = award_type_data[AWARD_TYPE_SHORT_NAME]
                        self.id = award_type_data[AWARD_TYPE_ID]

        def _CheckAuthor(self):
                if not self.id:
                        self._AddWarning('%s is a new author' % self.value)
                elif SQLauthorIsPseudo(self.id):
                        self._AddWarning('%s is an alternate name' % self.value)
                if SQLMultipleAuthors(self.value):
                        self._AddWarning('%s is a disambiguated name' % self.value)

        def _CheckImage(self):
                if not self.value:
                        return
                if self.type != 'image':
                        return
                self._CheckImageDomains()
                self._CheckAmazonImages()
                self._CheckISFDBWikiImages()
                self._CheckDuplicateURL()
                
        def _CheckImageDomains(self):
                from urlparse import urlparse
                domains = SQLLoadRecognizedDomains()
                valid_domain = 0
                url_domain = urlparse(self.value).netloc
                for domain in domains:
                        if (domain[DOMAIN_LINKING_ALLOWED] == 1) and url_domain.endswith(domain[DOMAIN_NAME]):
                                # If a required URL segment is not in this URL, it's not valid
                                if domain[DOMAIN_REQUIRED_SEGMENT] and domain[DOMAIN_REQUIRED_SEGMENT] not in self.value:
                                        continue
                                valid_domain = 1
                                if domain[DOMAIN_EXPLICIT_LINK_REQUIRED] and '|' not in self.value:
                                        self._AddWarning("For images hosted by this site, the URL of the associated Web page must be entered after a '|'. ")
                                break
                if not valid_domain:
                        self._AddWarning('Image hosted by a site which we do not have permission to link to.')
                if ('sf-encyclopedia.' in self.value
                    and '/clute/' not in self.value
                    and '/clute_uk/' not in self.value
                    and '/langford/' not in self.value
                    and '/robinson/' not in self.value):
                        self._AddWarning("""For SFE-hosted images, only links to /clute/, /clute_uk/,
                                         /langford/ and /robinson/ sub-directories are allowed.""")

        def _CheckAmazonImages(self):
                from re import match
                if 'amazon.' not in self.value:
                        return
                # For Amazon images, only "cropping" "_CR" formatting codes are allowed
                if (not match('.*/images/[PIG]/[0-9A-Za-z+-]{10}[LS]?(\._CR[0-9]+,[0-9]+,[0-9]+,[0-9]+)?\.(gif|png|jpg)$', self.value.replace('%2B','+'))
                    and not match('.*\.images-amazon\.com/images/G/0[1-3]/ciu/[0-9a-f]{2}/[0-9a-f]{2}/[0-9a-f]{22,24}\.L\.(gif|png|jpg)$', self.value)
                    and not match('.*(m\.media-amazon|\.ssl-images-amazon)\.com/images/S/amzn-author-media-prod/[0-9a-z]{26}\.(gif|png|jpg)$', self.value)):
                        self._AddWarning('Unsupported host name or formatting in an Amazon URL. Only properly structured _CR formatting codes are currently allowed.')
                if not match('.*/images/I/[0-9A-Za-z+-]{10}[LS]', self.value.replace('%2B','+')):
                        self._AddWarning('Note that Amazon URLs that do not start with "/images/I/" may not be stable.')
                if '/images/w/mediax' in self.value.lower():
                        self._AddWarning('Note that Amazon URLs that contain "/images/W/MEDIAX" may not be stable.')

        def _CheckISFDBWikiImages(self):
                from pubClass import pubs
                # The presence of 'Content' indicates that this is a Publication-related and not an Author Edit submission
                # The absense of 'Parent' indicates that this is not a Clone Publication submission
                # The absence of 'ClonedTo' indicates that this is not an Import/Export Content submission
                XmlData = self.cell.row.table.submission.merge
                if ((WIKILOC in self.value or WIKILOC_ALT in self.value)
                    and GetElementValue(XmlData, 'Content')
                    and not GetElementValue(XmlData, 'Parent')
                    and not GetElementValue(XmlData, 'ClonedTo')):
                        pub_id = GetElementValue(XmlData, 'Record')
                        if pub_id:
                                current = pubs(db)
                                current.load(int(pub_id))
                                if current.pub_tag not in self.value:
                                        self._AddWarning('Wiki-hosted image URL %s does not match the internal publication tag %s.' % (self.value, current.pub_tag))
                                if 'px-' in self.value:
                                        self._AddWarning('Wiki-hosted image URL %s contains "px-", which means that it\'s a preview image.' % self.value)

        def _CheckDuplicateURL(self):
                if not SQLDuplicateImageURL(self.value):
                        return
                link = AdvSearchLink((('TYPE', 'Publication'),
                                      ('USE_1', 'pub_frontimage'),
                                      ('O_1', 'exact'),
                                      ('TERM_1', self.value),
                                      ('ORDERBY', 'pub_title'),
                                      ('C', 'AND')))
                self._AddWarning('%sImage URL already on file</a>' % link, 0)

        def _CheckPubDate(self):
                if not self.value:
                        return
                if self.type != 'pub_date':
                        return
                if ISFDBdaysFromToday(self.value) > SESSION.max_future_days:
                        self._AddWarning('Date more than %d days in the future' % SESSION.max_future_days)

                pub_id = self.cell.row.table.submission.metadata.get('Record')
                if pub_id:
                        pub_isbn = self.cell.row.table.submission.metadata.get('Isbn')
                        # If there is no ISBN in the body of the submission,
                        # get it from the publication record on file
                        if not pub_isbn:
                                pub_data = SQLGetPubById(pub_id)
                                if pub_data:
                                        pub_isbn = pub_data[PUB_ISBN]
                                        self._CheckISBNDate(self.value, pub_isbn)

                title_date = self.cell.row.table.submission.metadata.get('TitleDate')
                if not title_date:
                        return
                date_status = ISFDBCompare2Dates(self.value, title_date)
                if date_status == 1:
                        self._AddWarning('Pub date earlier than title date')
                elif date_status == 2:
                        self._AddWarning('Pub date more exact than title date')

        def _CheckISBNDate(self, pub_date, pub_isbn):
                from isbn import ISBNlength
                if not pub_date:
                        return
                if not pub_isbn:
                        return
                if ISFDBCompare2Dates(pub_date, '1967-00-00') == 1:
                        self._AddWarning('ISBNs are not allowed for pre-1967 publications')

                isbn_length = ISBNlength(pub_isbn)
                if (isbn_length == 10) and (ISFDBCompare2Dates('2007-00-00', pub_date) == 1):
                        self._AddWarning('10-digit ISBN for a post-2007 publication')

                if isbn_length == 13:
                        if ISFDBCompare2Dates(pub_date, '2005-00-00') == 1:
                                self._AddWarning('13-digit ISBN for a pre-2005 publication')
                        if ISFDBCompare2Dates(pub_date, '2020-00-00') == 1 and pub_isbn.startswith('979'):
                                self._AddWarning('979 ISBN-13 for a pre-2020 publication')

        def _CheckPubType(self):
                if not self.value:
                        return
                if self.type != 'pub_type':
                        return
                title_type = self.cell.row.table.submission.metadata.get('TitleType')
                if not title_type:
                        return
                if self.value != title_type:
                        if not (self.value in ('MAGAZINE', 'FANZINE') and title_type == 'EDITOR'):
                                self._AddWarning('Publication Type does not match the Title Type')

        def _CheckPrice(self):
                from re import search
                if not self.value:
                        return
                if self.type != 'price':
                        return

                if 'CDN' in self.value.upper():
                        self._AddWarning('CDN is invalid. Use a leading C$ for prices in Canadian dollars.')
                if 'EUR' in self.value.upper():
                        self._AddWarning('EUR is invalid. Use %s for prices in euros.' % SESSION.currency.euro)
                for currency_sign in ('$',
                                      SESSION.currency.baht,
                                      SESSION.currency.euro,
                                      SESSION.currency.peso,
                                      SESSION.currency.pound,
                                      SESSION.currency.yen):
                        if (currency_sign + ' ') in self.value:
                                self._AddWarning('Spaces after the %s sign are not allowed' % currency_sign)
                                break
                if SESSION.currency.euro in self.value and not self.value.startswith(SESSION.currency.euro):
                        self._AddWarning('The Euro sign must be at the beginning of the price value')
                if SESSION.currency.euro in self.value and ',' in self.value:
                        self._AddWarning('Euro prices must not include commas')
                for currency_sign in ('$', 'C$', SESSION.currency.pound):
                        if self.value.startswith(currency_sign) and ',' in self.value and '.' not in self.value:
                                self._AddWarning('For %s prices a period must be used as the decimal separator' % currency_sign)
                                break
                if self.value.lower().startswith('http'):
                        self._AddWarning('Prices must not start with http')
                if self.value.replace('.','').replace(',','').isdigit():
                        self._AddWarning('Prices should contain a currency symbol or abbreviation')
                if search('^[0-9]{1,}', self.value) and '/' not in self.value:
                        self._AddWarning('Prices cannot start with a digit. The only exception is pre-decimilisation UK prices which must contain a slash.')
                if search('\.[0-9]{3,}$', self.value) and not self.value.startswith('BD '):
                        self._AddWarning("""4 or more consecutive digits must be separated with a comma,
                                     not a period. The only exception is currencies which allow
                                     3 digits after the decimal separator, e.g. BD (Bahraini dinars).""")
                if search('[0-9]{4,}$', self.value):
                        self._AddWarning('4 or more consecutive digits must be separated with a comma.')
                if 'jp' in self.value.lower():
                        self._AddWarning('JP is not a valid currency code. Use the Yen sign instead.')
                if '&#20870;' in self.value:
                        self._AddWarning('&#20870; is not a valid currency code. Use the Yen sign instead.')
                if self.value.count(' ') > 1:
                        self._AddWarning('More than one space character is not allowed in the price field')
                if ' $' in self.value:
                        self._AddWarning('The dollar sign cannot follow the space character in the price field')
                if '+' in self.value:
                        self._AddWarning('Plus signs are not allowed in the price field')
                if search('[0-9]{1,} ', self.value):
                        self._AddWarning('A space cannot follow a digit in the price field')

        def _CheckFormat(self):
                if not self.value:
                        return
                if self.type != 'format':
                        return
                if self.value not in SESSION.db.formats:
                        self._AddWarning('Uncommon format')
                if self.value == 'unknown':
                        self._AddWarning('Format is "unknown"')
                elif self.value == 'ebook':
                        pub_date = self.cell.row.table.submission.metadata.get('Year')
                        if ISFDBCompare2Dates(pub_date, '2000-01-01') == 1:
                                self._AddWarning('Pre-2000 e-book submitted')

        def _CheckISBN(self):
                from isbn import isbnVariations, validISBN, ISBNValidFormat
                if not self.value:
                        return
                if self.type != 'isbn':
                        return
                pub_id = self.cell.row.table.submission.metadata.get('Record')
                pub_date = self.cell.row.table.submission.metadata.get('Year')
                # If there is no publication date in the body of the submission,
                # get the publication date from the publication record on file
                if not pub_date:
                        pub_data = SQLGetPubById(pub_id)
                        if pub_data:
                                pub_date = pub_data[PUB_YEAR]
                self._CheckISBNDate(pub_date, self.value)

                if not ISBNValidFormat(self.value):
                        self._AddWarning('Invalid ISBN format')
                elif not validISBN(self.value):
                        self._AddWarning('Bad Checksum')
                # Get possible ISBN variations
                targets = isbnVariations(self.value)
                results = SQLFindPubsByIsbn(targets, pub_id)
                if results:
                        link = AdvSearchLink((('TYPE', 'Publication'),
                                              ('USE_1', 'pub_isbn'),
                                              ('OPERATOR_1', 'exact'),
                                              ('TERM_1', self.value),
                                              ('ORDERBY', 'pub_title'),
                                              ('C', 'AND')))
                        self._AddWarning('%sISBN already on file</a>' % link, 0)
                self._CheckLanguageForISBN()

        def _CheckLanguageForISBN(self):
                title_language = self.cell.row.table.submission.metadata.get('Language')
                if title_language:
                        isbn_languages = {'French': '2',
                                          'German': '3'}
                        for isbn_language in isbn_languages:
                                prefix10 = isbn_languages[isbn_language]
                                prefix13 = '978%s' % prefix10
                                if ((self.value.startswith(prefix10) or self.value.startswith(prefix13))
                                    and title_language != isbn_language):
                                        self._AddWarning("""ISBN-10s that starts with %s and ISBN-13s that
                                                        start with %s are typically in %s (although exceptions exist),
                                                        but the submitted language of this publication's main
                                                        title is %s""" % (prefix10, prefix13, isbn_language, title_language))

        def _CheckCatalogID(self):
                if not self.value:
                        return
                if self.type != 'catalog':
                        return
                if SQLFindPubsByCatalogId(self.value):
                        link = AdvSearchLink((('TYPE', 'Publication'),
                                              ('USE_1', 'pub_catalog'),
                                              ('OPERATOR_1', 'exact'),
                                              ('TERM_1', self.value),
                                              ('ORDERBY', 'pub_title'),
                                              ('C', 'AND')))
                        self._AddWarning('%sCatalog ID already on file</a>' % link, 0)

        def GetValueFromMetadata(self):
                self.value = self.cell.row.table.submission.metadata[self.cell.row.element_name]
                # Use _Link first, then use _Check to test the linked ID for issues
                self._LinkSeries()
                self._CheckSeries()
                self._LinkPublisher()
                self._CheckPublisher()
                self._LinkPubSeries()
                self._CheckPubSeries()

                self._CheckDate()
                self._CheckNotes()
                self._CheckHTML()
                self._CheckImage()
                self._CheckPubDate()
                self._CheckPubType()
                self._CheckPrice()
                self._CheckFormat()
                self._CheckISBN()
                self._CheckCatalogID()

        def GetMultiValueFromMetadata(self, value):
                self.value = value
                self.type = self.cell.row.multi_type
                if self.type == 'author' and self.value:
                        self.GetAuthorFromName(self.value)
                        self._CheckAuthor()
                self._CheckHTML()

        def GetAttributeValueForMulti(self, value):
                self.value = value
                self.type = self.cell.row.multi_type
                if self.type == 'author' and self.value:
                        self.GetAuthorFromName(self.value)
                self._CheckHTML()

        def GetAttributeValue(self, value):
                # Note that this method only LINKs and doesn't CHECK values
                self.value = value
                self._LinkPublisher()
                self._LinkPubSeries()
                self._LinkSeries()
                self._LinkAwardType()
                self._LinkCover()

        def GetAuthorFromName(self, name):
                self.type = 'author'
                self.value = name
                author_data = SQLgetAuthorData(name)
                # If the author is already on file, link to the author record
                if author_data:
                        self.id = author_data[AUTHOR_ID]
                        # Reset the display value to the canonical version - may change the case
                        self.value = author_data[AUTHOR_CANONICAL]
                        self.link = 'ea.cgi'

        def _LinkCover(self):
                if not self.value:
                        return
                if self.type != 'cover':
                        return
                self.id = self.cell.row.pub_id

        def GetCover(self, cover_pub):
                self.type = 'cover'
                self.value = cover_pub[PUB_IMAGE]
                self.id = cover_pub[PUB_PUBID]

class SubmissionViewer():
        def __init__(self, method_name, submission_id):
                self.rows = []
                self.current_record = ''
                self.contents_titles_with_dates = {}
                self.sub_id = submission_id
                self.sub_data = SQLloadSubmission(self.sub_id)
                self.xmlData = self.sub_data[SUB_DATA]
                self.sub_type = self.sub_data[SUB_TYPE]
                try:
                        self.doc = minidom.parseString(XMLunescape2(self.xmlData))
                except:
                        self._InvalidSubmission('Invalid XML in the submission')
                self.root_element = SUBMAP[self.sub_type][1]
                if not self.doc.getElementsByTagName(self.root_element):
                        self._InvalidSubmission('Invalid submission structure - missing root element')
                self.merge = self.doc.getElementsByTagName(self.root_element)
                self.submitter = GetElementValue(self.merge, 'Submitter')
                self.ui = isfdbUI()
                if not self.submitter:
                        self._InvalidSubmission('Invalid submission structure - submitter name not specified')
                self.metadata = {}
                self.updated = {}
                getattr(self, method_name)()
                self.PrintModNote()

        def _OrphanWarning(self, name, note, webpages):
                warning = """The current record, %s, has no other publications on file. If this submission is approved,
                             the record will be automatically deleted.""" % name
                if note or webpages:
                        warning += ' The following field values will be deleted: '
                        if note:
                                warning += 'Note'
                        if webpages:
                                if note:
                                        warning += ' and '
                                warning += '%s Web Page' % len(webpages)
                                if len(webpages) > 1:
                                        warning += 's'
                        warning += '.'
                return warning

        def _InvalidSubmission(self, message = ''):
                from login import GetUserData
                error_text = 'This submission is no longer valid. %s.' % message
                print('<div id="ErrorBox">')
                submission = SQLloadSubmission(self.sub_id)
                submitter_id = submission[SUB_SUBMITTER]
                submitter = SQLgetUserName(submitter_id)
                print('<b>Submitted by:</b> %s' % WikiLink(submitter))
                print('<h3>Error: %s</h3>' % error_text)
                print('<h3>You can view the submission as %s.' % ISFDBLink('dumpxml.cgi', self.sub_id, 'raw XML'))
                (userid, username, usertoken) = GetUserData()
                # If the user is a moderator and the submission is "N"ew, allow the user to hard reject it
                if SQLisUserModerator(userid) and submission[SUB_STATE] == 'N':
                        print('<br>Use %s to reject it.' % ISFDBLink('mod/hardreject.cgi', self.sub_id, 'Hard Reject'))
                print('</h3>')
                print('</div>')
                print('</div>')
                print('</div>')
                sys.exit(0)

        def GetMetadata(self, element_names):
                for element_name in element_names:
                        self.metadata[element_name] = GetElementValue(self.merge, element_name)
                        if TagPresent(self.merge, element_name):
                                self.updated[element_name] = 1
                        else:
                                self.updated[element_name] = 0

        def SetMetaData(self, field_name, field_value):
                if field_value:
                        self.metadata[field_name] = field_value
                        self.updated[field_name] = 1
                else:
                        self.metadata[field_name] = ''
                        self.updated[field_name] = 0

        def GetMetadataMulti(self, group_name, element_name):
                self.metadata[group_name] = []
                if TagPresent(self.merge, group_name):
                        self.updated[group_name] = 1
                        values_list = self.doc.getElementsByTagName(element_name)
                        for value in values_list:
                                self.metadata[group_name].append(XMLunescape(value.firstChild.data.encode('iso-8859-1')))
                else:
                        self.updated[group_name] = 0

        def SetMetaDataMulti(self, group_name, values_list):
                if values_list:
                        self.updated[group_name] = 1
                        self.metadata[group_name] = values_list
                else:
                        self.updated[group_name] = 0
                        self.metadata[group_name] = []

        def GetMetadataMultiNoGroup(self, element_name):
                self.metadata[element_name] = []
                if TagPresent(self.merge, element_name):
                        self.updated[element_name] = 1
                        for value in self.doc.getElementsByTagName(element_name):
                                record = value.firstChild.data
                                self.metadata[element_name].append(XMLunescape(record.encode('iso-8859-1')))
                else:
                        self.updated[element_name] = 0

        def PrintModNote(self, element_name = 'ModNote'):
                mod_note = GetElementValue(self.merge, element_name)
                if mod_note:
                        print('<h3>Note to Moderator: </h3>%s<p><p>' % mod_note)

        def DisplayNewAwardType(self):
                self.GetMetadata(('ShortName', 'FullName', 'AwardedFor',
                                  'AwardedBy', 'Poll', 'NonGenre', 'Note'))
                self.GetMetadataMulti('Webpages', 'Webpage')
                table = SubmissionTable(self)
                table.Add1MetadataRow('Short Name', 'ShortName')
                table.Add1MetadataRow('Full Name', 'FullName')
                table.Add1MetadataRow('Awarded For', 'AwardedFor')
                table.Add1MetadataRow('Awarded By', 'AwardedBy')
                table.Add1MetadataRow('Poll', 'Poll')
                table.Add1MetadataRow('Non-Genre', 'NonGenre')
                table.Add1MetadataMultiRow('webpage', 'Web Pages', 'Webpages', 'Webpage')
                table.Add1MetadataNoteRow('Note', 'Note')
                table.DisplayAddRecord()

        def DisplayAwardTypeDelete(self):
                from awardtypeClass import award_type
                self.GetMetadata(('AwardTypeId', 'Reason'))
                table = SubmissionTable(self)

                award_type_id = self.metadata['AwardTypeId']
                current = award_type()
                current.award_type_id = award_type_id
                current.load()
                if current.error:
                        self._InvalidSubmission('Award Type no longer exists')

                table.headers.extend(['Field', 'Award Type to Delete: %s' % ISFDBLinkNoName('awardtype.cgi', award_type_id, award_type_id)])
                table.Add1AttributeRow('Short Name', current.award_type_short_name)
                table.Add1AttributeRow('Full Name', current.award_type_name)
                table.Add1AttributeRow('Awarded For', current.award_type_for)
                table.Add1AttributeRow('Awarded By', current.award_type_by)
                table.Add1AttributeRow('Poll', current.award_type_poll)
                table.Add1AttributeRow('Covers more than just SF', current.award_type_non_genre)
                table.Add1AttributeMultiRow('Web Pages', 'webpage', current.award_type_webpages)
                table.Add1AttributeNoteRow('Note', current.award_type_note)
                table.Add1MetadataRow('Deletion Reason', 'Reason')
                table.PrintTable()

        def DisplayEditAwardType(self):
                from awardtypeClass import award_type

                self.GetMetadata(('AwardTypeId', 'ShortName', 'FullName', 'AwardedFor',
                                  'AwardedBy', 'Poll', 'NonGenre', 'Note'))
                self.GetMetadataMulti('Webpages', 'Webpage')
                table = SubmissionTable(self)

                current = award_type()
                current.award_type_id = self.metadata['AwardTypeId']
                current.load()
                if current.error:
                        self._InvalidSubmission('Award Type no longer exists')

                table.headers.extend(['Field',
                                      'Current Award Type [#%s]' % ISFDBLinkNoName('awardtype.cgi', current.award_type_id, current.award_type_id),
                                      'Proposed'])
                table.AddAttributeToMetadataRow('Short Name', current.award_type_short_name, 'ShortName')
                table.AddAttributeToMetadataRow('Full Name', current.award_type_name, 'FullName')
                table.AddAttributeToMetadataRow('Awarded For', current.award_type_for, 'AwardedFor')
                table.AddAttributeToMetadataRow('Awarded By', current.award_type_by, 'AwardedBy')
                table.AddAttributeToMetadataRow('Poll', current.award_type_poll, 'Poll')
                table.AddAttributeToMetadataRow('Covers more than just SF', current.award_type_non_genre, 'NonGenre')
                table.AddAttributeToMetadataMultiRow('Web Pages', 'webpage', current.award_type_webpages, 'Webpages', 'Webpage')
                table.AddAttributeToMetadataRow('Note', current.award_type_note, 'Note', note = 1)
                table.PrintTable()

                self._DisplayPendingConflicts(current.award_type_id, 'AwardTypeId')

        def DisplayTemplateAdd(self):
                self.GetMetadata(('TemplateName', 'TemplateDisplayedName', 'TemplateType',
                                  'TemplateURL', 'TemplateMouseoverHelp'))
                table = SubmissionTable(self)
                table.Add1MetadataRow('Name', 'TemplateName')
                table.Add1MetadataRow('Displayed Name', 'TemplateDisplayedName')
                table.Add1MetadataRow('Template Type', 'TemplateType')
                table.Add1MetadataRow('Link URL', 'TemplateURL')
                table.Add1MetadataRow('Mouseover Help', 'TemplateMouseoverHelp')
                table.DisplayAddRecord()

        def DisplayTemplateEdit(self):
                from templateClass import Template
                self.GetMetadata(('Record', 'TemplateName', 'TemplateDisplayedName',
                                  'TemplateType', 'TemplateURL', 'TemplateMouseoverHelp'))
                if not self.metadata['Record']:
                        self._InvalidSubmission('Template ID not specified')

                template = Template()
                template.load(self.metadata['Record'])
                if not template.id:
                        self._InvalidSubmission('This template no longer exists')

                table = SubmissionTable(self)

                table.AddAttributeToMetadataRow('Template Name', template.name, 'TemplateName')
                table.AddAttributeToMetadataRow('Displayed Name', template.displayed_name, 'TemplateDisplayedName')
                table.AddAttributeToMetadataRow('Template Type', template.type, 'TemplateType')
                table.AddAttributeToMetadataRow('Template URL', template.url, 'TemplateURL')
                table.AddAttributeToMetadataRow('Mouseover Help', template.mouseover, 'TemplateMouseoverHelp')

                table.DisplayMetadataEdit()

        def DisplayVerificationSourceAdd(self):
                self.GetMetadata(('SourceLabel', 'SourceName', 'SourceURL'))
                table = SubmissionTable(self)
                table.Add1MetadataRow('Source Label', 'SourceLabel')
                table.Add1MetadataRow('Source Name', 'SourceName')
                table.Add1MetadataRow('Source URL', 'SourceURL')
                table.DisplayAddRecord()

        def DisplayVerificationSourceEdit(self):
                from verificationsourceClass import VerificationSource
                self.GetMetadata(('Record', 'SourceLabel', 'SourceName', 'SourceURL'))
                if not self.metadata['Record']:
                        self._InvalidSubmission('Verification Source ID not specified')

                verification_source = VerificationSource()
                verification_source.load(self.metadata['Record'])
                if not verification_source.id:
                        self._InvalidSubmission('This verification source no longer exists')

                table = SubmissionTable(self)

                table.AddAttributeToMetadataRow('Verification Source Label', verification_source.label, 'SourceLabel')
                table.AddAttributeToMetadataRow('Verification Source Name', verification_source.name, 'SourceName')
                table.AddAttributeToMetadataRow('Verification Source URL', verification_source.url, 'SourceURL')

                table.DisplayMetadataEdit()

        def DisplayNewLanguage(self):
                self.GetMetadata(('LanguageName', 'LanguageCode', 'Latin'))
                table = SubmissionTable(self)
                table.Add1MetadataRow('Language Name', 'LanguageName')
                table.Add1MetadataRow('Language Code', 'LanguageCode')
                table.Add1MetadataRow('Latin-Derived', 'Latin')
                table.DisplayAddRecord()

        def DisplayMakeVariant(self):
                from titleClass import titles
                self.GetMetadata(('Record', 'Parent'))
                if not self.metadata['Record']:
                        self._InvalidSubmission('Variant Title ID not specified')

                theVariant = titles(db)
                theVariant.load(int(self.metadata['Record']))
                if theVariant.error:
                        self._InvalidSubmission(theVariant.error)

                if self.updated['Parent']:
                        self._DisplayVTtoTitleID(theVariant)
                else:
                        self._DisplayVTtoNewTitle(theVariant)

        def _DisplayVTtoTitleID(self, theVariant):
                from titleClass import titles
                table = SubmissionTable(self)
                table.update = 0
                table.headers.extend(['Field', 'Make Title #%s into a Variant' % ISFDBLinkNoName('title.cgi', theVariant.title_id, theVariant.title_id, True)])
                parent = self.metadata['Parent']
                if int(parent) != 0:
                        table.headers.extend(['Proposed Parent Title #%s' % ISFDBLinkNoName('title.cgi', parent, parent, True)])
                else:
                        table.headers.extend(['No Parent'])

                existingParent = titles(db)
                existingParent.load(int(parent))
                if existingParent.error:
                        self._InvalidSubmission(existingParent.error)
                if existingParent.title_parent:
                        self._InvalidSubmission('The proposed parent title is a variant of another title record')

                table.Add2AttributesRow('Title', theVariant.title_title, existingParent.title_title)
                table.Add2AttributesMultiRow('Transliterated Titles', 'multi', theVariant.title_trans_titles, existingParent.title_trans_titles)
                table.AddAuthorRowFromNames(theVariant.title_authors, existingParent.title_authors)
                warning = self.EarlierVariantDate(theVariant.title_year, existingParent.title_year)
                table.Add2AttributesRow('Date', theVariant.title_year, existingParent.title_year, 'title_date', warning = warning)
                table.Add2AttributesRow('Series', theVariant.title_series, existingParent.title_series, 'series')
                table.Add2AttributesRow('Series Number', theVariant.title_seriesnum, existingParent.title_seriesnum)
                table.Add2AttributesMultiRow('Web Pages', 'webpage', theVariant.title_webpages, existingParent.title_webpages)
                table.Add2AttributesRow('Language', theVariant.title_language, existingParent.title_language)
                table.Add2AttributesRow('Title Type', theVariant.title_ttype, existingParent.title_ttype, 'title_type')

                if existingParent.title_ttype == 'COVERART' and theVariant.title_ttype == 'COVERART':
                        table.AddCoverRowFromIDs(theVariant.title_id, parent)

                warning = ''
                if existingParent.title_storylen != theVariant.title_storylen and int(parent):
                        if not (existingParent.title_ttype == 'SHORTFICTION' and theVariant.title_ttype == 'SERIAL'):
                                warning = 'Length mismatch'
                table.Add2AttributesRow('Length', theVariant.title_storylen, existingParent.title_storylen, warning = warning)
                table.Add2AttributesRow('Content', theVariant.title_content, existingParent.title_content, 'content')
                table.Add2AttributesRow('Non-Genre', theVariant.title_non_genre, existingParent.title_non_genre, 'nongenre')
                table.Add2AttributesRow('Juvenile', theVariant.title_jvn, existingParent.title_jvn, 'juvenile')
                table.Add2AttributesRow('Novelization', theVariant.title_nvz, existingParent.title_nvz, 'novelization')
                table.Add2AttributesRow('Graphic', theVariant.title_graphic, existingParent.title_graphic, 'graphic')

                warning = ''
                if existingParent.title_synop and theVariant.title_synop and int(parent):
                        warning = """Both title records have synopsis information. The variant's
                                     synopsis will not be moved to the parent record automatically."""
                table.Add2AttributesNoteRow('Synopsis', theVariant.title_synop, existingParent.title_synop, 'synopsis', warning)

                warning = ''
                if existingParent.title_note and theVariant.title_note and int(parent):
                        warning = 'Both title records have notes. '
                warning += self.NoTrTemplateWarning(existingParent.title_language, theVariant.title_language,
                                                    existingParent.title_ttype, theVariant.title_ttype,
                                                    theVariant.title_note)
                table.Add2AttributesNoteRow('Note', theVariant.title_note, existingParent.title_note, 'note', warning)

                table.PrintTable()

                self._DisplayPendingVTs(theVariant.title_id)

        def _DisplayVTtoNewTitle(self, theVariant):
                self.GetMetadata(('Title', 'Year', 'Series',
                                  'Seriesnum', 'Language', 'TitleType', 'Note'))
                self.GetMetadataMulti('TransTitles', 'TransTitle')
                self.GetMetadataMulti('Authors', 'Author')
                self.GetMetadataMulti('Webpages', 'Webpage')

                table = SubmissionTable(self)
                table.update = 0
                table.headers.extend(['Field',
                                      'Make Title #%s into a Variant' % ISFDBLinkNoName('title.cgi', theVariant.title_id, theVariant.title_id, True),
                                      'Variant of [New Title]'])
                table.AddAttributeToMetadataRow('Title', theVariant.title_title, 'Title')
                table.AddAttributeToMetadataMultiRow('Transliterated Titles', 'multi', theVariant.title_trans_titles, 'TransTitles', 'TransTitle')
                table.AddAuthorRowNameToXML(theVariant.title_authors, 'Authors', 'Author')
                warning = self.EarlierVariantDate(theVariant.title_year, self.metadata['Year'])
                table.AddAttributeToMetadataRow('Date', theVariant.title_year, 'Year', 'title_date', warning = warning)
                table.AddAttributeToMetadataRow('Series', theVariant.title_series, 'Series', 'series')
                table.AddAttributeToMetadataRow('Series #', theVariant.title_seriesnum, 'Seriesnum')
                table.AddAttributeToMetadataMultiRow('Web Pages', 'webpage', theVariant.title_webpages, 'Webpages', 'Webpage')
                table.AddAttributeToMetadataRow('Language', theVariant.title_language, 'Language')
                table.AddAttributeToMetadataRow('Title Type', theVariant.title_ttype, 'TitleType', 'title_type')
                if theVariant.title_ttype == 'COVERART' and self.metadata['TitleType'] == 'COVERART':
                        table.AddCoverRowFromIDs(theVariant.title_id, theVariant.title_id)
                table.Add2AttributesRow('Length', theVariant.title_storylen, theVariant.title_storylen)
                table.Add2AttributesRow('Content', theVariant.title_content, theVariant.title_content, 'content')
                table.Add2AttributesRow('Non-Genre', theVariant.title_non_genre, theVariant.title_non_genre, 'nongenre')
                table.Add2AttributesRow('Juvenile', theVariant.title_jvn, theVariant.title_jvn, 'juvenile')
                table.Add2AttributesRow('Novelization', theVariant.title_nvz, theVariant.title_nvz, 'novelization')
                table.Add2AttributesRow('Graphic', theVariant.title_graphic, theVariant.title_graphic, 'graphic')
                table.Add2AttributesNoteRow('Synopsis', theVariant.title_synop, theVariant.title_synop, 'synopsis')
                warning = self.NoTrTemplateWarning(self.metadata['Language'], theVariant.title_language,
                                                   self.metadata['TitleType'], theVariant.title_ttype,
                                                   theVariant.title_note)
                table.AddAttributeToMetadataRow('Note', theVariant.title_note, 'Note', warning = warning, note = 1)
                table.PrintTable()

                self._DisplayPendingVTs(theVariant.title_id)

        def DisplayAddVariant(self):
                from titleClass import titles
                self.GetMetadata(('Parent', 'Title', 'Year', 'TitleType', 'Storylen', 'Language', 'Note'))
                self.GetMetadataMulti('TransTitles', 'TransTitle')
                self.GetMetadataMulti('Authors', 'Author')

                table = SubmissionTable(self)
                table.update = 0
                Parent = self.metadata['Parent']
                table.headers.extend(['Field',
                                      'Current Record #%s' % ISFDBLinkNoName('title.cgi', Parent, Parent, True),
                                      'Proposed Variant Title'])

                current = titles(db)
                current.load(int(Parent))
                if current.error:
                        self._InvalidSubmission(current.error)
                if current.title_parent:
                        self._InvalidSubmission('The proposed parent title is a variant of another title record')

                table.AddAttributeToMetadataRow('Title', current.title_title, 'Title')
                table.AddAttributeToMetadataMultiRow('Transliterated Titles', 'multi', current.title_trans_titles, 'TransTitles', 'TransTitle')
                table.AddAuthorRowNameToXML(current.title_authors, 'Authors', 'Author')
                warning = self.EarlierVariantDate(self.metadata['Year'], current.title_year)
                table.AddAttributeToMetadataRow('Date', current.title_year, 'Year', 'title_date', warning = warning)
                table.AddAttributeToMetadataRow('Language', current.title_language, 'Language')
                table.AddAttributeToMetadataRow('Title Type', current.title_ttype, 'TitleType', 'title_type')
                table.AddAttributeToMetadataRow('Length', current.title_storylen, 'Storylen')
                warning = self.NoTrTemplateWarning(current.title_language, self.metadata['Language'],
                                                   current.title_ttype, self.metadata['TitleType'],
                                                   self.metadata['Note'])
                table.AddAttributeToMetadataRow('Note', current.title_note, 'Note', warning = warning, note = 1)
                table.PrintTable()

        def EarlierVariantDate(self, variant_date, parent_date):
                warning = ''
                if variant_date != '8888-00-00' and parent_date == '8888-00-00':
                        warning = "Proposed parent's date is 'unpublished'"
                elif ISFDBCompare2Dates(variant_date, parent_date) == 1:
                        warning = 'Proposed variant date before proposed parent date'
                return warning
        
        def NoTrTemplateWarning(self, parent_lang, variant_lang, parent_type, variant_type, variant_note):
                if (parent_lang
                    and variant_lang != parent_lang
                    and '{{tr|' not in variant_note.lower()
                    and variant_type not in ('COVERART', 'INTERIORART')
                    and parent_type not in ('COVERART', 'INTERIORART')):
                        return 'No Tr template in a translated title\'s notes.'
                return ''

        def DisplayNewAwardCat(self):
                from awardcatClass import award_cat
                from awardtypeClass import award_type

                self.GetMetadata(('AwardCatName', 'AwardTypeId', 'DisplayOrder', 'Note'))
                self.GetMetadataMulti('Webpages', 'Webpage')

                awardType = award_type()
                awardType.award_type_id = self.metadata['AwardTypeId']
                awardType.load()
                if awardType.error:
                        self._InvalidSubmission('The award type associated with this category no longer exists')

                table = SubmissionTable(self)
                table.Add1MetadataRow('Award Category', 'AwardCatName')
                table.Add1AttributeRow('Award Type', awardType.award_type_short_name, 'award_type_name')
                table.Add1MetadataRow('Display Order', 'DisplayOrder')
                table.Add1MetadataMultiRow('webpage', 'Web Pages', 'Webpages', 'Webpage')
                table.Add1MetadataNoteRow('Note', 'Note')
                table.DisplayAddRecord()

        def DisplayAwardCatChanges(self):
                from awardcatClass import award_cat

                self.GetMetadata(('AwardCategoryId', 'CategoryName', 'DisplayOrder', 'Note'))
                self.GetMetadataMulti('Webpages', 'Webpage')

                current = award_cat()
                current.award_cat_id = self.metadata['AwardCategoryId']
                current.load()
                if current.error:
                        self._InvalidSubmission('Award Category no longer exists')

                table = SubmissionTable(self)
                table.headers.extend(['Field',
                                      'Current Record %s' % ISFDBLinkNoName('award_category.cgi',
                                                                            current.award_cat_id,
                                                                            current.award_cat_id),
                                      'Proposed'])

                table.AddAttributeToMetadataRow('Category Name', current.award_cat_name, 'CategoryName')
                table.AddAttributeToMetadataRow('Display Order', current.award_cat_order, 'DisplayOrder')
                table.AddAttributeToMetadataMultiRow('Web Pages', 'webpage', current.award_cat_webpages, 'Webpages', 'Webpage')
                table.AddAttributeToMetadataRow('Note', current.award_cat_note, 'Note', note = 1)

                table.PrintTable()

                self._DisplayPendingConflicts(current.award_cat_id, 'AwardCategoryId')

        def DisplayAwardCatDelete(self):
                from awardcatClass import award_cat
                from awardtypeClass import award_type

                self.GetMetadata(('AwardCategoryId', 'Reason'))

                current = award_cat()
                current.award_cat_id = self.metadata['AwardCategoryId']
                current.load()
                if current.error:
                        self._InvalidSubmission('Award Category no longer exists')

                awardType = award_type()
                awardType.award_type_id = current.award_cat_type_id
                awardType.load()
                if awardType.error:
                        self._InvalidSubmission('Award Type no longer exists')

                table = SubmissionTable(self)
                table.headers.extend(['Field',
                                      'Award Category to Delete: %s' % ISFDBLinkNoName('award_category.cgi',
                                                                                       '%d+1' % current.award_cat_id, current.award_cat_id)])
                table.Add1AttributeRow('Category Name', current.award_cat_name)
                table.Add1AttributeRow('Award Type', awardType.award_type_short_name, 'award_type_name')
                table.Add1AttributeRow('Display Order', current.award_cat_order)
                table.Add1AttributeMultiRow('Web Pages', 'webpage', current.award_cat_webpages)
                table.Add1AttributeNoteRow('Note', current.award_cat_note)
                table.Add1MetadataRow('Deletion Reason', 'Reason')
                table.PrintTable()

        def DisplaySeriesDelete(self):
                from seriesClass import series

                self.GetMetadata(('Record', 'Reason'))
                series_id = int(self.metadata['Record'])

                # Check if the series has already been deleted
                seriesRecord = SQLget1Series(series_id)
                if seriesRecord == 0:
                        self._InvalidSubmission('This series no longer exists')

                # Check if any sub-series have been added to this series since the time the submission was created
                subseries = SQLFindSeriesChildren(series_id)
                if len(subseries) > 0:
                        self._InvalidSubmission("""At least one sub-series has been added to this Series
                                                   since the time this submission was created. This series
                                                   can't be deleted until all sub-series have been removed""")

                # Check if any titles have been added to this series since the time the submission was created
                titles = SQLloadTitlesXBS(series_id)
                if len(titles) > 0:
                        self._InvalidSubmission("""At least one title has been added to this series since
                                                   the time this submission was created. This series can't
                                                   be deleted until all titles have been removed""")

                current = series(db)
                current.load(series_id)

                table = SubmissionTable(self)
                table.headers.extend(['Field', 'Series to Delete: %s' % ISFDBLinkNoName('pe.cgi', series_id, series_id)])

                table.Add1AttributeRow('Series Name', current.series_name)
                table.Add1AttributeMultiRow('Transliterated Series Names', '', current.series_trans_names)
                table.Add1AttributeRow('Parent', current.series_parent)
                table.Add1AttributeRow('Parent Position', current.series_parentposition)
                table.Add1AttributeMultiRow('Web Pages', 'webpage', current.series_webpages)
                table.Add1AttributeNoteRow('Note', current.series_note)
                table.Add1MetadataRow('Deletion Reason', 'Reason')
                table.PrintTable()

        def DisplayDeletePub(self):
                from pubClass import pubs
                from publisherClass import publishers
                from pubseriesClass import pub_series

                self.GetMetadata(('Record', 'Reason'))
                pub_id = int(self.metadata['Record'])

                current = pubs(db)
                current.load(pub_id)
                if current.error:
                        self._InvalidSubmission(current.error)

                table = SubmissionTable(self)
                table.headers.extend(['Field', 'Publication to Delete: %s' % ISFDBLinkNoName('pl.cgi', pub_id, pub_id)])

                table.Add1AttributeRow('Title', current.pub_title)
                table.Add1AttributeMultiRow('Transliterated Titles', '', current.pub_trans_titles)
                table.Add1AttributeMultiRow('Authors', 'author', current.pub_authors)
                table.Add1AttributeRow('Tag', current.pub_tag)
                table.Add1AttributeRow('Date', current.pub_year)

                warning = ''
                if current.pub_publisher_id:
                        pub_count = SQLCountPubsForPublisher(current.pub_publisher_id)
                        if pub_count == 1:
                                publisher = publishers(db)
                                publisher.load(current.pub_publisher_id)
                                warning = self._OrphanWarning(publisher.publisher_name, publisher.publisher_note, publisher.publisher_webpages)
                table.Add1AttributeRow('Publisher', current.pub_publisher, 'publisher', warning = warning)

                warning = ''
                if current.pub_series_id:
                        pub_count = SQLCountPubsForPubSeries(current.pub_series_id)
                        if pub_count == 1:
                                pub_series = pub_series(db)
                                pub_series.load(current.pub_series_id)
                                warning = self._OrphanWarning(pub_series.pub_series_name, pub_series.pub_series_note, pub_series.pub_series_webpages)
                table.Add1AttributeRow('Publication Series', current.pub_series, 'pub_series', warning = warning)

                table.Add1AttributeRow('Publication Series #', current.pub_series_num)
                table.Add1AttributeRow('Pages', current.pub_pages)
                table.Add1AttributeRow('Format', current.pub_ptype)
                table.Add1AttributeRow('Publication Type', current.pub_ctype)
                table.Add1AttributeRow('ISBN', current.pub_isbn)
                table.Add1AttributeRow('Catalog', current.pub_catalog)
                table.Add1AttributeRow('Price', current.pub_price, 'price')
                table.Add1AttributeCoverRow('Image', current.pub_image, pub_id)
                table.Add1AttributeMultiRow('Web Pages', 'webpage', current.pub_webpages)
                table.Add1AttributeMultiRow('External IDs', 'prebuilt', current.formatExternalIDs())
                table.Add1AttributeNoteRow('Note', current.pub_note)
                table.Add1MetadataRow('Deletion Reason', 'Reason')
                table.PrintTable()

        def DisplayTitleDelete(self):
                from titleClass import titles

                self.GetMetadata(('Record', 'Reason'))
                title_id = int(self.metadata['Record'])
                reviews = SQLLoadReviewsForTitle(title_id)

                current = titles(db)
                current.load(title_id)
                if current.error:
                        self._InvalidSubmission(current.error)

                table = SubmissionTable(self)
                table.headers.extend(['Field', 'Title to Delete: %s' % ISFDBLinkNoName('title.cgi', title_id, title_id)])

                table.Add1AttributeRow('Title', current.title_title)
                table.Add1AttributeMultiRow('Transliterated Titles', '', current.title_trans_titles)
                table.Add1AttributeMultiRow('Authors', 'author', current.title_authors)
                table.Add1AttributeRow('Date', current.title_year)
                table.Add1AttributeNoteRow('Synopsis', current.title_synop)
                table.Add1AttributeRow('Series', current.title_series, 'series')
                table.Add1AttributeRow('Series Number', current.title_seriesnum)
                table.Add1AttributeRow('Title Type', current.title_ttype)
                table.Add1AttributeRow('Length', current.title_storylen)
                table.Add1AttributeRow('Content', current.title_content)
                table.Add1AttributeRow('Non-Genre', current.title_non_genre)
                table.Add1AttributeRow('Juvenile', current.title_jvn)
                table.Add1AttributeRow('Novelization', current.title_nvz)
                table.Add1AttributeRow('Graphic', current.title_graphic)
                table.Add1AttributeMultiRow('Web Pages', 'webpage', current.title_webpages)
                table.Add1AttributeRow('Language', current.title_language)
                table.Add1AttributeNoteRow('Note', current.title_note)
                table.Add1MetadataRow('Deletion Reason', 'Reason')
                table.PrintTable()

                if reviews:
                        print('<p><div id="WarningBox">')
                        print('<br><b>Reviews of this title:</b>')
                        print('<ul>')
                        for review in reviews:
                                print('<li>%s (%s)' % (ISFDBLinkNoName('title.cgi', review[TITLE_PUBID], review[TITLE_TITLE]),
                                                       review[TITLE_YEAR]))
                        print('</ul>')
                        print('</div>')
                print('<p>')

        def DisplayMakePseudonym(self):
                self.GetMetadata(('Record', 'Parent'))
                alternate_id = int(self.metadata['Record'])
                parent_id = int(self.metadata['Parent'])

                alternate_data = SQLloadAuthorData(alternate_id)
                if not alternate_data:
                        self._InvalidSubmission('Alternate name record no longer exists')

                parent_data = SQLloadAuthorData(parent_id)
                if not parent_data:
                        self._InvalidSubmission('Parent author record no longer exists')

                table = SubmissionTable(self)
                table.headers.extend(['Proposed Alternate Name Record #%s' % ISFDBLinkNoName('ea.cgi', alternate_id, alternate_id, True),
                                      'Proposed Parent Record #%s' % ISFDBLinkNoName('ea.cgi', parent_id, parent_id, True)])
                table.Add2AttributesRow('', alternate_data[AUTHOR_CANONICAL], parent_data[AUTHOR_CANONICAL])
                table.PrintTable()

                other_authors = SQLgetActualFromPseudo(alternate_id)
                if other_authors:
                        duplicate = ''
                        print('This name is currently defined as an alternate name for the following authors:')
                        print('<ul>')
                        for other_author in other_authors:
                                other_author_data = SQLgetAuthorData(other_author[0])
                                print('<li>%s' % ISFDBLink('ea.cgi', other_author_data[AUTHOR_ID], other_author[0]))
                                if parent_id == int(other_author_data[AUTHOR_ID]):
                                        duplicate = other_author_data[AUTHOR_CANONICAL]
                        print('</ul>')
                        if duplicate:
                                self._InvalidSubmission('This author record is already set up as an alternate name of %s' % duplicate)

        def DisplayRemovePseudonym(self):
                self.GetMetadata(('Record', 'Parent'))
                alternate_id = int(self.metadata['Record'])
                parent_id = int(self.metadata['Parent'])

                alternate_data = SQLloadAuthorData(alternate_id)
                if not alternate_data:
                        self._InvalidSubmission('Alternate name record no longer exists')

                parent_data = SQLloadAuthorData(parent_id)
                if not parent_data:
                        self._InvalidSubmission('Parent author record no longer exists')

                pseud_id = SQLGetPseudIdByAuthorAndPseud(parent_id, alternate_id)
                if not pseud_id:
                        self._InvalidSubmission('This alternate name association no longer exists')

                table = SubmissionTable(self)
                table.headers.extend(['Current Alternate Name Record %s' % ISFDBLinkNoName('ea.cgi', alternate_id, alternate_id, True),
                                      'Current Parent Author Record %s' % ISFDBLinkNoName('ea.cgi', parent_id, parent_id, True)])
                table.Add2AttributesRow('', alternate_data[AUTHOR_CANONICAL], parent_data[AUTHOR_CANONICAL])
                table.PrintTable()

                authors = SQLgetActualFromPseudo(alternate_id)
                if authors:
                        print('This name is currently labeled as an alternate name for the following authors:')
                        print('<ul>')
                        for author in authors:
                                author_data = SQLgetAuthorData(author[0])
                                print('<li>%s' % ISFDBLink('ea.cgi', author_data[AUTHOR_ID], author_data[AUTHOR_CANONICAL]))
                        print('</ul>')

        def DisplayAwardLink(self):
                from awardClass import awards
                from titleClass import titles
                self.GetMetadata(('Award', 'Title'))
                award_id = int(self.metadata['Award'])
                title_id = int(self.metadata['Title'])

                award = awards(db)
                award.load(award_id)
                if award.error:
                        self._InvalidSubmission('Award no longer exists')

                title = titles(db)
                title.load(title_id)
                if title.error:
                        self._InvalidSubmission('Title no longer exists')

                table = SubmissionTable(self)
                table.headers.extend(['Field',
                                      ISFDBLinkNoName('award_details.cgi', award_id, 'Award')])
                if title_id:
                        table.headers.extend(['Link Award to Title #%s' % ISFDBLinkNoName('title.cgi', title_id, title_id)])
                else:
                        table.headers.extend(['Unlink Award'])
                table.Add2AttributesRow('Title', award.award_title, title.title_title)
                table.AddAuthorRowFromNames(award.award_authors, title.title_authors)
                table.Add2AttributesRow('Date', award.award_year, title.title_year)
                table.Add2AttributesRow('Award Name', award.award_type_name, '')
                table.Add2AttributesRow('Category', award.award_cat_name, '')
                table.Add2AttributesRow('Award Level', award.award_displayed_level, '')
                table.Add2AttributesRow('IMDB Link', award.award_movie, '')
                table.Add2AttributesNoteRow('Note', award.award_note, '')
                table.PrintTable()

        def DisplayLinkReview(self):
                from titleClass import titles

                self.GetMetadata(('Record', 'Parent'))
                review_id = int(self.metadata['Record'])
                title_id = int(self.metadata['Parent'])

                theReview = titles(db)
                theReview.load(review_id)
                if theReview.error:
                        self._InvalidSubmission(theReview.error)
                
                reviewedTitle = titles(db)
                reviewedTitle.load(title_id)
                if reviewedTitle.error:
                        self._InvalidSubmission(reviewedTitle.error)

                table = SubmissionTable(self)
                table.headers.extend(['Field',
                                      'Review [Record #%s]' % ISFDBLinkNoName('title.cgi', review_id, review_id)])
                if title_id:
                        table.headers.extend(['Link Review to [Title #%s]' % ISFDBLinkNoName('title.cgi', title_id, title_id)])
                else:
                        table.headers.extend(['Unlink the Review'])

                if title_id:
                        if reviewedTitle.title_title != theReview.title_title:
                                warning = 'Title mismatch. Please double-check.'
                        else:
                                warning = ''
                        table.Add2AttributesRow('Title', theReview.title_title, reviewedTitle.title_title, warning = warning)

                        if ISFDBCompare2Dates(theReview.title_year, reviewedTitle.title_year) == 1:
                                warning = 'Review date prior to title date. Please double-check.'
                        else:
                                warning = ''
                        table.Add2AttributesRow('Date', theReview.title_year, reviewedTitle.title_year, warning = warning)

                        if reviewedTitle.title_ttype not in ('ANTHOLOGY','COLLECTION','NOVEL','NONFICTION','OMNIBUS','SHORTFICTION'):
                                warning = 'Uncommon reviewed title type. Please double-check.'
                        else:
                                warning = ''
                        table.Add2AttributesRow('Title Type', theReview.title_ttype, reviewedTitle.title_ttype, warning = warning)

                        if reviewedTitle.title_language != theReview.title_language:
                                warning = 'Language mismatch. Please double-check.'
                        else:
                                warning = ''
                        table.Add2AttributesRow('Language', theReview.title_language, reviewedTitle.title_language, warning = warning)

                        if set(reviewedTitle.title_authors) != set(theReview.title_subjauthors):
                                warning = 'Author mismatch. Please double-check.'
                        else:
                                warning = ''
                        table.AddNameRowFromNames('Book Authors', theReview.title_subjauthors, reviewedTitle.title_authors, warning = warning)

                        table.AddNameRowFromNames('Reviewers', theReview.title_authors, ())

                else:
                        table.Add2AttributesRow('Title', theReview.title_title, '')
                        table.Add2AttributesRow('Date', theReview.title_year, '')
                        table.Add2AttributesRow('Title Type', theReview.title_ttype, '')
                        table.Add2AttributesRow('Language', theReview.title_language, '')
                        table.AddNameRowFromNames('Book Authors', theReview.title_subjauthors, ())
                        table.AddNameRowFromNames('Reviewers', theReview.title_authors, ())
                table.PrintTable()

        def DisplayPubSeriesChanges(self):
                from pubseriesClass import pub_series
                self.GetMetadata(('Record', 'Name', 'Note'))
                self.GetMetadataMulti('PubSeriesTransNames', 'PubSeriesTransName')
                self.GetMetadataMulti('Webpages', 'Webpage')

                pubseries_id = int(self.metadata['Record'])

                current = pub_series(db)
                current.load(pubseries_id)
                if not current.pub_series_id:
                        self._InvalidSubmission('This publication series no longer exists')

                table = SubmissionTable(self)
                table.headers.extend(['Field',
                                      'Publication Series #%s' % ISFDBLinkNoName('pubseries.cgi', pubseries_id, pubseries_id),
                                      'Proposed Changes'])

                table.AddAttributeToMetadataRow('Pub. Series Name', current.pub_series_name, 'Name')
                table.AddAttributeToMetadataMultiRow('Transliterated Names', '',
                                                    current.pub_series_trans_names,
                                                    'PubSeriesTransNames', 'PubSeriesTransName')
                table.AddAttributeToMetadataMultiRow('Web Pages', 'webpage',
                                                    current.pub_series_webpages,
                                                    'Webpages', 'Webpage')
                table.AddAttributeToMetadataRow('Note', current.pub_series_note, 'Note', 'note', note = 1)
                table.PrintTable()

                self._DisplayPendingConflicts(pubseries_id)

        def DisplayPublisherChanges(self):
                from publisherClass import publishers
                self.GetMetadata(('Record', 'Name', 'Note'))
                self.GetMetadataMulti('PublisherTransNames', 'PublisherTransName')
                self.GetMetadataMulti('Webpages', 'Webpage')

                publisher_id = int(self.metadata['Record'])

                current = publishers(db)
                current.load(publisher_id)
                if not current.publisher_id:
                        self._InvalidSubmission('This publisher no longer exists')

                table = SubmissionTable(self)
                table.headers.extend(['Field',
                                      'Publisher #%s' % ISFDBLinkNoName('publisher.cgi', publisher_id, publisher_id),
                                      'Proposed Changes'])

                table.AddAttributeToMetadataRow('Publisher Name', current.publisher_name, 'Name')
                table.AddAttributeToMetadataMultiRow('Transliterated Names', '',
                                                    current.publisher_trans_names,
                                                    'PublisherTransNames', 'PublisherTransName')
                table.AddAttributeToMetadataMultiRow('Web Pages', 'webpage',
                                                    current.publisher_webpages,
                                                    'Webpages', 'Webpage')
                table.AddAttributeToMetadataRow('Note', current.publisher_note, 'Note', 'note', note = 1)
                table.PrintTable()

                self._DisplayPendingConflicts(publisher_id)

        def DisplayUnmergeTitle(self):
                from pubClass import pubs
                self.GetMetadata(('Record', ))
                self.GetMetadataMultiNoGroup('PubRecord')
                title_id = int(self.metadata['Record'])

                title = SQLloadTitle(title_id)
                if not title:
                        self._InvalidSubmission('Title record no longer valid')
                title_authors = SQLTitleBriefAuthorRecords(title_id)
                publications = SQLGetPubsByTitleNoParent(title_id)

                unmergeList = []
                for pub_id in self.metadata['PubRecord']:
                        unmergeList.append(int(pub_id))
                        pub = pubs(db)
                        pub.load(pub_id)
                        if pub.error:
                                self._InvalidSubmission(pub.error)

                print('<h3>Unmerging from the following title:</h3>')
                print('<br><b>Title:</b> %s' % ISFDBLink('title.cgi', title[TITLE_PUBID], title[TITLE_TITLE]))
                print('<br><b>Authors:</b> %s' % FormatAuthors(title_authors))
                print('<br><b>Date:</b>', title[TITLE_YEAR])
                print('<br><b>Type:</b>', title[TITLE_TTYPE])
                print('<hr>')

                print('<h3>Unmerging the following works:</h3>')

                table = SubmissionTable(self)
                table.headers.extend(['Publication', 'Proposed Unmerged Title'])
                for pub in publications:
                        if pub[PUB_PUBID] in unmergeList:
                                publication_cell = ISFDBLink('pl.cgi', pub[PUB_PUBID], pub[PUB_TITLE])
                                if title[TITLE_TTYPE] in ('SHORTFICTION', 'COVERART'):
                                        proposed_title = title[TITLE_TITLE]
                                else:
                                        proposed_title = pub[PUB_TITLE]
                                table.Add2AttributesRow('', publication_cell, ISFDBText(proposed_title), 'prebuilt')
                table.PrintTable()

        def DisplayRemoveTitle(self):
                from pubClass import pubs
                from titleClass import titles
                self.GetMetadata(('Record', ))
                self.GetMetadataMultiNoGroup('CoverRecord')
                self.GetMetadataMultiNoGroup('TitleRecord')
                self.GetMetadataMultiNoGroup('ReviewRecord')
                self.GetMetadataMultiNoGroup('InterviewRecord')
                pub_id = int(self.metadata['Record'])

                pub = pubs(db)
                pub.load(pub_id)
                if pub.error:
                        self._InvalidSubmission(pub.error)
                print('Removing titles from publication %s<p>' % ISFDBLinkNoName('pl.cgi', pub_id, pub.pub_title))

                # Get the list of titles in this publication and sort them by page number
                current_contents = getPubContentList(pub_id)

                self.DisplayRemoveTitleSection('CoverRecord', current_contents, 'Cover Art', 'COVERART')
                self.DisplayRemoveTitleSection('TitleRecord', current_contents, 'Regular Titles', 'TITLE')
                self.DisplayRemoveTitleSection('ReviewRecord', current_contents, 'Reviews', 'REVIEW')
                self.DisplayRemoveTitleSection('InterviewRecord', current_contents, 'Interviews', 'INTERVIEW')

                self._DisplayVerifications(pub_id, 0)
                self._DisplayPendingPubUpdates(pub_id)
                self._DisplayPendingTitleRemovals(pub_id)
                self._DisplayPendingImports(pub_id)

        def DisplayRemoveTitleSection(self, metadata_type, current_contents, header, title_type):
                # Build a list of title IDs of this type to be removed
                removalList = []
                for content_id in self.metadata[metadata_type]:
                        if not self.RemovedTitleInPub(content_id, current_contents):
                                self._InvalidSubmission('At least one title record is no longer present in the publication')
                        removalList.append(int(content_id))

                if not removalList:
                        return
                
                print('<h2>%s</h2>' % header)
                table = SubmissionTable(self)
                table.headers.extend(['Keep', 'Remove'])
                for item in current_contents:
                        (keep, drop) = self.PrintTitleRemoveOneRow(item, removalList, title_type)
                        if not keep and not drop:
                                continue
                        if keep:
                                table.Add2AttributesRow('', keep, '', 'prebuilt')
                        else:
                                table.Add2AttributesRow('', '', drop, 'prebuilt')
                table.PrintTable()

        def RemovedTitleInPub(self, record, current_contents):
                found = 0
                for content_item in current_contents:
                        if int(content_item[PUB_CONTENTS_ID]) == int(record):
                                found = 1
                                break
                return found

        def PrintTitleRemoveOneRow(self, contents_item, removalList, title_type):
                # Get the title id of the current pub_content record
                title_id = contents_item[PUB_CONTENTS_TITLE]
                # Load the title record
                title = SQLloadTitle(title_id)
                authors = []
                if title_type == 'COVERART':
                        if title[TITLE_TTYPE] != 'COVERART':
                                return (None, None)
                        authors = SQLTitleBriefAuthorRecords(title[TITLE_PUBID])

                if title_type == 'TITLE':
                        if title[TITLE_TTYPE] in ('COVERART', 'REVIEW', 'INTERVIEW'):
                                return (None, None)
                        authors = SQLTitleBriefAuthorRecords(title[TITLE_PUBID])
                
                if title_type == "REVIEW":
                        if title[TITLE_TTYPE] != 'REVIEW':
                                return (None, None)
                        authors = SQLReviewBriefAuthorRecords(title[TITLE_PUBID])

                if title_type == "INTERVIEW":
                        if title[TITLE_TTYPE] != 'INTERVIEW':
                                return (None, None)
                        authors = SQLInterviewBriefAuthorRecords(title[TITLE_PUBID])

                page = contents_item[PUB_CONTENTS_PAGE]
                if page:
                        title_data = '%s - ' % page
                else:
                        title_data = ''
                title_data += '%s, %s' % (ISFDBLink('title.cgi', title[TITLE_PUBID], title[TITLE_TITLE]), title[TITLE_TTYPE])
                for author in authors:
                        title_data += ', %s' % ISFDBLink('ea.cgi', author[0], author[1])
                if contents_item[PUB_CONTENTS_ID] in removalList:
                        return (None, title_data)
                else:
                        return (title_data, None)

        def DisplaySeriesChanges(self):
                from seriesClass import series
                self.GetMetadata(('Record', 'Name', 'Parent', 'Parentposition', 'Note'))
                self.GetMetadataMulti('SeriesTransNames', 'SeriesTransName')
                self.GetMetadataMulti('Webpages', 'Webpage')
                series_id = int(self.metadata['Record'])

                current = series(db)
                current.load(series_id)
                if current.error:
                        self._InvalidSubmission('Series no longer exists')

                table = SubmissionTable(self)
                table.headers.extend(['Field',
                                      'Current Series Record #%s' % ISFDBLinkNoName('pe.cgi', series_id, series_id),
                                      'Proposed Changes'])

                table.AddAttributeToMetadataRow('Series Name', current.series_name, 'Name')
                table.AddAttributeToMetadataMultiRow('Transliterated Names', '',
                                                    current.series_trans_names,
                                                    'SeriesTransNames', 'SeriesTransName')
                table.AddAttributeToMetadataRow('Parent', current.series_parent, 'Parent', 'series')
                table.AddAttributeToMetadataRow('Parent Position', current.series_parentposition, 'Parentposition')
                table.AddAttributeToMetadataMultiRow('Web Pages', 'webpage',
                                                    current.series_webpages,
                                                    'Webpages', 'Webpage')
                table.AddAttributeToMetadataRow('Note', current.series_note, 'Note', 'note', note = 1)
                table.PrintTable()

                self._DisplayPendingConflicts(series_id)

        def DisplayAuthorChanges(self):
                from authorClass import authors

                self.GetMetadata(('Record', 'Canonical', 'Legalname',
                                  'Familyname', 'Birthplace', 'Birthdate',
                                  'Deathdate', 'Language', 'Image', 'Note'))
                self.GetMetadataMulti('AuthorTransNames', 'AuthorTransName')
                self.GetMetadataMulti('AuthorTransLegalNames', 'AuthorTransLegalName')
                self.GetMetadataMulti('Emails', 'Email')
                self.GetMetadataMulti('Webpages', 'Webpage')
                author_id = int(self.metadata['Record'])

                current = authors(db)
                current.load(author_id)
                if current.error:
                        self._InvalidSubmission('This author no longer exists')

                table = SubmissionTable(self)
                table.headers.extend(['Field',
                                      'Current Author Record #%s' % ISFDBLinkNoName('ea.cgi', author_id, author_id),
                                      'Proposed Changes'])

                table.AddAttributeToMetadataRow('Canonical Name', current.author_canonical, 'Canonical')
                table.AddAttributeToMetadataMultiRow('Transliterated Names', '',
                                                    current.author_trans_names,
                                                    'AuthorTransNames', 'AuthorTransName')
                table.AddAttributeToMetadataRow('Legal Name', current.author_legalname, 'Legalname')
                table.AddAttributeToMetadataMultiRow('Transliterated legal Names', '',
                                                    current.author_trans_legal_names,
                                                    'AuthorTransLegalNames', 'AuthorTransLegalName')
                table.AddAttributeToMetadataRow('Directory Entry', current.author_lastname, 'Familyname')
                table.AddAttributeToMetadataRow('Birth Place', current.author_birthplace, 'Birthplace')
                table.AddAttributeToMetadataRow('Birth Date', current.author_birthdate, 'Birthdate')
                table.AddAttributeToMetadataRow('Death Date', current.author_deathdate, 'Deathdate')
                table.AddAttributeToMetadataRow('Language', current.author_language, 'Language')
                table.AddAttributeToMetadataRow('Image', current.author_image, 'Image', 'image')
                table.AddAttributeToMetadataMultiRow('Emails', '',
                                                    current.author_emails,
                                                    'Emails', 'Email')
                table.AddAttributeToMetadataMultiRow('Web Pages', 'webpage',
                                                    current.author_webpages,
                                                    'Webpages', 'Webpage')
                table.AddAttributeToMetadataRow('Note', current.author_note, 'Note', 'note', note = 1)
                table.PrintTable()

                self._DisplayPendingConflicts(author_id)

        def DisplayTitleEdit(self):
                from titleClass import titles

                self.GetMetadata(('Record', 'Title', 'Year', 'Synopsis',
                                  'Series', 'Seriesnum', 'TitleType', 'Storylen',
                                  'ContentIndicator', 'NonGenre', 'Juvenile',
                                  'Novelization', 'Graphic', 'Language', 'Note'))
                self.GetMetadataMulti('TranslitTitles', 'TranslitTitle')
                self.GetMetadataMulti('Authors', 'Author')
                self.GetMetadataMulti('BookAuthors', 'BookAuthor')
                self.GetMetadataMulti('Interviewees', 'Interviewee')
                self.GetMetadataMulti('Webpages', 'Webpage')
                title_id = int(self.metadata['Record'])

                current = titles(db)
                current.load(title_id)
                if not current.used_id:
                        self._InvalidSubmission('The title no longer exists in the database')

                table = SubmissionTable(self)
                table.headers.extend(['Field',
                                      'Current Title Record #%s' % ISFDBLinkNoName('title.cgi', title_id, title_id),
                                      'Proposed Changes'])

                table.AddAttributeToMetadataRow('Title', current.title_title, 'Title')
                table.AddAttributeToMetadataMultiRow('Transliterated Titles', '',
                                                    current.title_trans_titles,
                                                    'TranslitTitles', 'TranslitTitle')

                if current.title_ttype == 'REVIEW':
                        table.AddAttributeToMetadataMultiRow('Review Authors', 'author',
                                                            current.title_authors,
                                                            'Authors', 'Author')
                        table.AddAttributeToMetadataMultiRow('Reviewed Authors', 'author',
                                                            current.title_subjauthors,
                                                            'BookAuthors', 'BookAuthor')
                elif current.title_ttype == 'INTERVIEW':
                        table.AddAttributeToMetadataMultiRow('Interview Authors', 'author',
                                                            current.title_authors,
                                                            'Authors', 'Author')
                        table.AddAttributeToMetadataMultiRow('Interviewed Authors', 'author',
                                                            current.title_subjauthors,
                                                            'Interviewees', 'Interviewee')
                else:
                        table.AddAttributeToMetadataMultiRow('Authors', 'author',
                                                            current.title_authors,
                                                            'Authors', 'Author')

                table.AddAttributeToMetadataRow('Title Date', current.title_year, 'Year')
                table.AddAttributeToMetadataRow('Series', current.title_series, 'Series', 'series')
                table.AddAttributeToMetadataRow('Series Number', current.title_seriesnum, 'Seriesnum')
                table.AddAttributeToMetadataMultiRow('Web Pages', 'webpage',
                                                    current.title_webpages,
                                                    'Webpages', 'Webpage')
                table.AddAttributeToMetadataRow('Language', current.title_language, 'Language')
                table.AddAttributeToMetadataRow('Title Type', current.title_ttype, 'TitleType')
                table.AddAttributeToMetadataRow('Length', current.title_storylen, 'Storylen')
                table.AddAttributeToMetadataRow('Content Indicator', current.title_content, 'ContentIndicator')
                table.AddAttributeToMetadataRow('Non-Genre', current.title_non_genre, 'NonGenre')
                table.AddAttributeToMetadataRow('Juvenile', current.title_jvn, 'Juvenile')
                table.AddAttributeToMetadataRow('Novelization', current.title_nvz, 'Novelization')
                table.AddAttributeToMetadataRow('Graphic Format', current.title_graphic, 'Graphic')
                table.AddAttributeToMetadataRow('Synopsis', current.title_synop, 'Synopsis', note = 1)
                table.AddAttributeToMetadataRow('Note', current.title_note, 'Note', note = 1)
                table.PrintTable()

                # Get all publications for this title (but not its parent)
                pubs = SQLGetPubsByTitleNoParent(title_id)
                if not len(pubs):
                        print('<br>There are no publications associated with this title.')
                        print('<br>')
                else:
                        print('<br>This title appears in %d publications:' % len(pubs))
                        self.DisplayPubsForTitle(pubs)
                # Get all publications for this title's parent
                children_pubs = SQLGetPubsForChildTitles(title_id)
                if len(children_pubs):
                        print('<br>This title\'s VARIANTS appear in %d publications:' % len(children_pubs))
                        self.DisplayPubsForTitle(children_pubs)

                self._DisplayPendingConflicts(title_id)

        def DisplayPubsForTitle(self, pub_list):
                print('<table border="1">')
                print('<tr>')
                print('<th>Publication</th>')
                print('<th>Verification Type</th>')
                print('<th>Primary Verifiers</th>')
                print('</tr>')
                for pub in pub_list:
                        print('<tr>')
                        print('<td>%s (%s)</td>' % (ISFDBLink('pl.cgi', pub[PUB_PUBID], pub[PUB_TITLE]), pub[PUB_YEAR]))
                        verificationstatus = SQLVerificationStatus(pub[PUB_PUBID])
                        if verificationstatus == 1:
                                print('<td class="warn">Primary</td>')
                                print('<td>')
                                verifiers = SQLPrimaryVerifiers(pub[PUB_PUBID])
                                for verifier in verifiers:
                                        print('%s<br>' % WikiLink(verifier[1]))
                                print('</td>')                                
                        elif verificationstatus == 2:
                                print('<td>Secondary</td>')
                                print('<td></td>')
                        else:
                                print('<td>Not verified</td>')
                                print('<td></td>')
                print('</table>')

        def DisplayAwardDelete(self):
                from awardClass import awards

                self.GetMetadata(('Record', 'Reason'))
                award_id = int(self.metadata['Record'])
                award = awards(db)
                award.load(award_id)
                if award.error:
                        self._InvalidSubmission(award.error)

                if award.title_id:
                        print('<h3>This submission deletes an award for Title record #%s</h3>' % ISFDBLinkNoName('title.cgi', award.title_id, award.title_id))
                else:
                        print('<h3>This award is not associated with an ISFDB title</h3>')

                table = SubmissionTable(self)
                table.headers.extend(['Field', 'Award to Delete: %s' % ISFDBLinkNoName('award_details.cgi', award_id, award_id)])

                table.Add1AttributeRow('Title', award.award_title)
                table.Add1AttributeMultiRow('Authors', 'author', award.award_authors)
                table.Add1AttributeRow('Date', award.award_year)
                award_type_link = ISFDBLink('awardtype.cgi', award.award_type_id, award.award_type_name)
                table.Add1AttributeRow('Award Type', award_type_link, 'prebuilt')
                award_cat_link = ISFDBLink('award_category.cgi', award.award_cat_id, award.award_cat_name)
                table.Add1AttributeRow('Award Category', award_cat_link, 'prebuilt')
                table.Add1AttributeRow('Award Level', AwardLevelDescription(award.award_level, award.award_type_id))
                table.Add1AttributeRow('IMDB Title', award.award_movie)
                table.Add1AttributeNoteRow('Note', award.award_note)
                table.Add1MetadataRow('Deletion Reason', 'Reason')
                table.PrintTable()

        def DisplayNewAward(self):
                self.GetMetadata(('Record', 'AwardTitle', 'AwardType', 'AwardYear',
                                  'AwardCategory', 'AwardLevel', 'AwardMovie', 'AwardNote'))
                self.GetMetadataMulti('AwardAuthors', 'AwardAuthor')

                try:
                        title_id = int(self.metadata['Record'])
                except:
                        title_id = 0

                table = SubmissionTable(self)
                table.headers.extend(['Field', 'Value'])

                if title_id:
                        title = SQLloadTitle(title_id)
                        if not title:
                                self._InvalidSubmission('Title no longer exists')
                        print('<h3>Adding Award to Title %s</h3>' % ISFDBLinkNoName('title.cgi', title_id, title_id))
                        table.Add1AttributeRow('Award Title', title[TITLE_TITLE])
                        table.Add1AttributeMultiRow('Award Authors', 'author', SQLTitleAuthors(title_id))
                else:
                        table.Add1MetadataRow('Award Title', 'AwardTitle')
                        table.Add1MetadataMultiRow('author', 'Award Authors', 'AwardAuthors', 'AwardAuthor')

                table.Add1MetadataRow('Award Year', 'AwardYear')

                award_type_id = int(self.metadata['AwardType'])
                award_type = SQLGetAwardTypeById(award_type_id)
                award_type_name = award_type[AWARD_TYPE_NAME]
                table.Add1AttributeRow('Award Type', ISFDBLink('awardtype.cgi', award_type_id, award_type_name), 'prebuilt')

                award_cat_id = int(self.metadata['AwardCategory'])
                award_cat_name = SQLGetAwardCatById(award_cat_id)[AWARD_CAT_NAME]
                table.Add1AttributeRow('Award Category', ISFDBLink('award_category.cgi', award_cat_id, award_cat_name), 'prebuilt')

                award_level = self.metadata['AwardLevel']
                table.Add1AttributeRow('Award Level', AwardLevelDescription(award_level, award_type_id), 'prebuilt')

                imdb_code = self.metadata['AwardMovie']
                if imdb_code:
                        table.Add1AttributeRow('IMDB Title', IMDBLink(imdb_code, imdb_code), 'prebuilt')
                else:
                        table.Add1AttributeRow('IMDB Title', '', 'prebuilt')
                table.Add1MetadataNoteRow('Note', 'AwardNote')
                table.PrintTable()

        def DisplayAwardEdit(self):
                from awardClass import awards
                self.GetMetadata(('Record', 'AwardTitle', 'AwardType', 'AwardYear',
                                  'AwardCategory', 'AwardLevel', 'AwardMovie', 'AwardNote'))
                self.GetMetadataMulti('AwardAuthors', 'AwardAuthor')
                award_id = int(self.metadata['Record'])
                current = awards(db)
                current.load(award_id)
                if current.error:
                        self._InvalidSubmission(current.error)

                if current.title_id:
                        print("""<h3>This submission edits a %s award for Title record #%s</h3>
                                """ % (ISFDBLink('awardtype.cgi', current.award_type_id, current.award_type_short_name),
                                       ISFDBLinkNoName('title.cgi', current.title_id, current.title_id)))
                else:
                        print("""<h3>This %s award is not associated with an ISFDB Title record</h3>
                              """ % ISFDBLink('awardtype.cgi', current.award_type_id, current.award_type_short_name))

                table = SubmissionTable(self)
                table.headers.extend(['Field',
                                      'Current Award Record #%s' % ISFDBLinkNoName('award_details.cgi', award_id, award_id),
                                      'Proposed Changes'])

                table.AddAttributeToMetadataRow('Title', current.award_title, 'AwardTitle')
                table.AddAttributeToMetadataMultiRow('Award Authors', 'author', current.award_authors, 'AwardAuthors', 'AwardAuthor')
                table.AddAttributeToMetadataRow('Award Year', current.award_year, 'AwardYear')

                award_cat_id = current.award_cat_id
                new_award_cat_id = self.metadata['AwardCategory']
                if new_award_cat_id:
                        self.metadata['Award Category Name'] = SQLGetAwardCatById(new_award_cat_id)[AWARD_CAT_NAME]
                        self.updated['Award Category Name'] = 1
                else:
                        self.metadata['Award Category Name'] = ''
                        self.updated['Award Category Name'] = 0
                table.AddAttributeToMetadataRow('Award Category', current.award_cat_name, 'Award Category Name')

                new_award_level = self.metadata['AwardLevel']
                if new_award_level:
                        self.metadata['Award Level Description'] = AwardLevelDescription(new_award_level, current.award_type_id)
                        self.updated['Award Level Description'] = 1
                else:
                        self.metadata['Award Level Description'] = ''
                        self.updated['Award Level Description'] = 0
                table.AddAttributeToMetadataRow('Award Level', current.award_displayed_level, 'Award Level Description')

                table.AddAttributeToMetadataRow('IMDB Link', current.award_movie, 'AwardMovie', 'award_imdb')
                table.AddAttributeToMetadataRow('Note', current.award_note, 'AwardNote', note = 1)
                table.PrintTable()

                self._DisplayPendingConflicts(award_id)

        def DisplayPublisherMerge(self):
                from publisherClass import publishers

                KeepId    = 0
                Records   = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                RecordIds = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                MaxIds    = 1

                self.GetMetadata(('KeepId', ))
                KeepId = int(self.metadata['KeepId'])

                RecordIds[0] = KeepId
                dropIds = self.doc.getElementsByTagName('DropId')
                for dropid in dropIds:
                        RecordIds[MaxIds] = int(dropid.firstChild.data)
                        MaxIds += 1

                try:
                        Records[0] = publishers(db)
                        Records[0].load(RecordIds[0])
                        if Records[0].error:
                                raise
                except:
                        self._InvalidSubmission("Can't load record: %s" % KeepId)

                print('<table border="2" class="generic_table">')
                print('<tr>')
                print('<td class="label"><b>Column</b></td>')
                print('<td class="label"><b>KeepId %s</b></td>' % ISFDBLinkNoName('publisher.cgi', KeepId, KeepId, True))
        
                index = 1
                while RecordIds[index]:
                        print('<td class="label"><b>DropId %s</b></td>' % ISFDBLinkNoName('publisher.cgi', RecordIds[index], RecordIds[index], True))
                        index += 1
                print('</tr>')

                index = 1
                while RecordIds[index]:
                        try:
                                Records[index] = publishers(db)
                                Records[index].load(RecordIds[index])
                                if Records[index].error:
                                        raise
                        except:
                                print('</table>')
                                self._InvalidSubmission("Can't load record: %s" % RecordIds[index])
                        index += 1

                for label in ('Publisher', 'Trans_names', 'Webpages', 'Note'):
                        self._PrintPublisherMerge(label, KeepId, Records, RecordIds)

                print('</table>')
                
        def _PrintPublisherMerge(self, Label, KeepId, Records, RecordIds):
                print('<tr>')
                print('<td class="label"><b>%s</b></td>' % Label)

                try:
                        keepId = int(GetElementValue(self.merge, Label))
                except:
                        keepId = KeepId

                index = 0
                while Records[index]:
                        if (RecordIds[index] == keepId) or (Label in ('Webpages', 'Trans_names')):
                                print('<td class="keep">')
                        else:
                                print('<td class="drop">')

                        if Label == 'Publisher':
                                if Records[index].used_name:
                                        print(ISFDBText(Records[index].publisher_name))
                                else:
                                        print('-')
                        elif Label == 'Trans_names':
                                if Records[index].used_trans_names:
                                        for count, trans_name in enumerate(Records[index].publisher_trans_names):
                                                if count:
                                                        print('<br>')
                                                print(ISFDBText(trans_name))
                                else:
                                        print('-')
                        elif Label == 'Webpages':
                                if Records[index].used_webpages:
                                        for count, webpage in enumerate(Records[index].publisher_webpages):
                                                if count:
                                                        print('<br>')
                                                print('<a href="%s" target="_blank">%s</a>' % (webpage, ISFDBText(webpage)))
                                else:
                                        print('-')
                        elif Label == 'Note':
                                if Records[index].used_note:
                                        print(Records[index].publisher_note)
                                else:
                                        print("-")
                        print('</td>')
                        index += 1
                print('</tr>')

        def DisplayAuthorMerge(self):
                from authorClass import authors

                self.GetMetadata(('KeepId', 'DropId'))
                KeepId = int(self.metadata['KeepId'])
                DropId = int(self.metadata['DropId'])

                print('<table border="2" class="generic_table">')
                print('<tr>')
                print('<td class="label"><b>Column</b></td>')
                print('<td class="label"><b>Keepid [Record #%s]</b></td>' % ISFDBLinkNoName('ea.cgi', KeepId, KeepId))
                print('<td class="label"><b>Dropid [Record #%s]</b></td>' % ISFDBLinkNoName('ea.cgi', DropId, DropId))
                print('</tr>')

                keep = authors(db)
                keep.load(int(KeepId))
                if keep.error:
                        print('</table>')
                        self._InvalidSubmission('One of the authors no longer exists')
                drop = authors(db)
                drop.load(int(DropId))
                if drop.error:
                        print('</table>')
                        self._InvalidSubmission('One of the authors no longer exists')

                self._PrintAuthorMergeSingle('Canonical', KeepId, keep.used_canonical, drop.used_canonical, 
                        keep.author_canonical, drop.author_canonical)
                self._PrintAuthorMergeMultiple('Transliterated Names', keep.author_trans_names, drop.author_trans_names)
                self._PrintAuthorMergeSingle('Legalname', KeepId, keep.used_legalname, drop.used_legalname, 
                        keep.author_legalname, drop.author_legalname)
                self._PrintAuthorMergeMultiple('Transliterated Legal Names', keep.author_trans_legal_names, drop.author_trans_legal_names)
                self._PrintAuthorMergeSingle('Familyname', KeepId, keep.used_lastname, drop.used_lastname, 
                        keep.author_lastname, drop.author_lastname)
                self._PrintAuthorMergeSingle('Birthplace', KeepId, keep.used_birthplace, drop.used_birthplace, 
                        keep.author_birthplace, drop.author_birthplace)
                self._PrintAuthorMergeSingle('Birthdate', KeepId, keep.used_birthdate, drop.used_birthdate, 
                        keep.author_birthdate, drop.author_birthdate)
                self._PrintAuthorMergeSingle('Deathdate', KeepId, keep.used_deathdate, drop.used_deathdate, 
                        keep.author_deathdate, drop.author_deathdate)

                self._PrintAuthorMergeMultiple('Emails', keep.author_emails, drop.author_emails)
                self._PrintAuthorMergeMultiple('Web Pages', keep.author_webpages, drop.author_webpages)
                
                self._PrintAuthorMergeSingle('Image', KeepId, keep.used_image, drop.used_image, 
                        keep.author_image, drop.author_image)
                self._PrintAuthorMergeSingle('Language', KeepId, keep.used_language, drop.used_language, 
                        keep.author_language, drop.author_language)
                self._PrintAuthorMergeSingle('Note', KeepId, keep.used_note, drop.used_note, 
                        keep.author_note, drop.author_note)

                print('</table>')
                print('<p>')

        def _PrintAuthorMergeMultiple(self, Label, values1, values2):
                print('<tr>')
                print('<td class="label"><b>%s</b></td>' % Label)
                print('<td class="keep">')
                if values1:
                        for count, value in enumerate(values1):
                                if count:
                                        print('<br>')
                                if Label == 'Web Pages':
                                        print('<a href="%s" target="_blank">%s</a>' % (value, ISFDBText(value)))
                                else:
                                        print(ISFDBText(value))
                else:
                        print('-')
                print('</td>')
                print('<td class="keep">')
                if values2:
                        for count, value in enumerate(values2):
                                if count:
                                        print('<br>')
                                if Label == 'Web Pages':
                                        print('<a href="%s" target="_blank">%s</a>' % (value, ISFDBText(value)))
                                else:
                                        print(ISFDBText(value))
                else:
                        print('-')
                print('</td>')
                print('</tr>')

        def _PrintAuthorMergeSingle(self, Label, KeepId, KeepUsed, DropUsed, KeepData, DropData):
                print('<tr>')
                self._PrintLabel(Label)
                record_id = GetElementValue(self.merge, Label)
                if not record_id:
                        record_id = KeepId
                if int(record_id) != KeepId:
                        print('<td class="drop">')
                        if KeepUsed:
                                if Label == 'Note':
                                        print(KeepData)
                                else:
                                        print(ISFDBText(KeepData))
                        else:
                                print('-')
                        print('</td>')
                        print('<td class="keep">')
                        if DropUsed:
                                if Label == 'Note':
                                        print(DropData)
                                else:
                                        print(ISFDBText(DropData))
                        else:
                                print('-')
                        print('</td>')
                else:
                        print('<td class="keep">')
                        if KeepUsed:
                                if Label == 'Note':
                                        print(KeepData)
                                else:
                                        print(ISFDBText(KeepData))
                        else:
                                print('-')
                        print('</td>')
                        print('<td class="drop">')
                        if DropUsed:
                                if Label == 'Note':
                                        print(DropData)
                                else:
                                        print(ISFDBText(DropData))
                        else:
                                print('-')
                        print('</td>')
                print('</tr>')

        def DisplayMergeTitles(self):
                from titleClass import titles
                KeepId    = 0
                Records   = {}
                Parent    = 0
                self.GetMetadata(('KeepId', ))
                KeepId = int(self.metadata['KeepId'])

                Records[KeepId] = titles(db)
                Records[KeepId].load(KeepId)
                if Records[KeepId].error:
                        self._InvalidSubmission("Can't load title: %s" % KeepId)

                dropIds = self.doc.getElementsByTagName('DropId')
                for dropid in dropIds:
                        title_id = int(dropid.firstChild.data)
                        Records[title_id] = titles(db)
                        Records[title_id].load(title_id)
                        if Records[title_id].error:
                                self._InvalidSubmission("Can't load title: %s" % title_id)

                for title_id_1 in Records:
                        for title_id_2 in Records:
                                if title_id_1 == title_id_2:
                                        continue
                                pubs1 = SQLGetPubsByTitleNoParent(int(title_id_1))
                                pubs2 = SQLGetPubsByTitleNoParent(int(title_id_2))
                                for pub1 in pubs1:
                                        for pub2 in pubs2:
                                                if pub1[PUB_PUBID] == pub2[PUB_PUBID]:
                                                        message = """Records %s and %s both appear in the publication <i>%s</i>.
                                                                Merging two titles that appear in the same publication would cause
                                                                the remaining title to appear twice in the publication, which is not allowed.
                                                                If the submission is trying to remove a duplicate title from a publication, edit
                                                                that publication, click on <b>Remove Titles From This Pub</b>, then select
                                                                the title that you wish to remove""" % (title_id_1, title_id_1, pub1[PUB_TITLE])
                                                        self._InvalidSubmission(message)

                print('<table border="2" class="generic_table">')
                print('<tr>')
                print('<td class="label"><b>Field</b></td>')
                print('<td class="label"><b>KeepId %s</b></td>' % ISFDBLinkNoName('title.cgi', KeepId, KeepId, True))
                for title_id in sorted(Records.keys()):
                        if title_id != KeepId:
                                print('<td class="label"><b>DropId %s</b></td>' % ISFDBLinkNoName('title.cgi', title_id, title_id, True))
                print('</tr>')

                self._PrintMergeField('Title',     KeepId, Records)
                self._PrintMergeField('TranslitTitles',  KeepId, Records)
                self._PrintMergeField('Author',    KeepId, Records)
                self._PrintMergeField('Year',	     KeepId, Records)
                self._PrintMergeField('TitleType', KeepId, Records)
                self._PrintMergeField('Series',    KeepId, Records)
                self._PrintMergeField('Seriesnum', KeepId, Records)
                self._PrintMergeField('Storylen',  KeepId, Records)
                self._PrintMergeField('ContentIndicator', KeepId, Records)
                self._PrintMergeField('NonGenre',  KeepId, Records)
                self._PrintMergeField('Juvenile',  KeepId, Records)
                self._PrintMergeField('Novelization', KeepId, Records)
                self._PrintMergeField('Graphic',   KeepId, Records)
                self._PrintMergeField('Language',  KeepId, Records)
                self._PrintMergeField('Webpages',  KeepId, Records)
                self._PrintMergeField('Synopsis',  KeepId, Records)
                self._PrintMergeField('Note',      KeepId, Records)
                self._PrintMergeField('Parent',    KeepId, Records)
                print('</table>')

                self._DisplayPendingTitleMerges(KeepId, Records)

        def _DisplayPendingTitleMerges(self, KeepId, Records):
                pending_merges = SQLPendingTitleMerges(self.sub_id, KeepId, Records)
                if pending_merges:
                        print('<p><div id="PendingTitleMergesWarning">')
                        print('<b>WARNING:</b> The following pending submissions aim to merge one or more titles in this submission:')
                        print('<ul>')
                        for pending_merge_id in pending_merges:
                                print(('<li>%s' % ISFDBLinkNoName('view_submission.cgi', pending_merge_id, pending_merge_id)))
                        print('</ul>')
                        print('</div><p>')

        def _PrintMergeField(self, Label, KeepId, Records):
                print('<tr>')
                self._PrintLabel(Label)
                # Try to retrieve the title ID whose data we will keep for this field
                keep_id = GetElementValue(self.merge, Label)
                # If the submission doesn't have a title ID for this field, use the default "keep" title ID
                if not keep_id:
                        keep_id = KeepId
                keep_id = int(keep_id)

                for title_id in sorted(Records.keys()):
                        output = '-'
                        kept = '-'
                        if Label == 'Title':
                                if Records[title_id].used_title:
                                        output = Records[title_id].title_title
                                if Records[keep_id].used_title:
                                        kept = Records[keep_id].title_title
                        elif Label == 'TranslitTitles':
                                if Records[title_id].used_trans_titles:
                                        output = ''
                                        for count, value in enumerate(Records[title_id].title_trans_titles):
                                                if count:
                                                        output += '<br>'
                                                output += ISFDBText(value)
                        elif Label == 'Author':
                                # Note that ISFDBText is applied in the "authors" method
                                output = Records[title_id].authors()
                                kept = Records[keep_id].authors()
                        elif Label == 'Year':
                                if Records[title_id].used_year:
                                        output = Records[title_id].title_year
                                if Records[keep_id].used_year:
                                        kept = Records[keep_id].title_year
                        elif Label == 'Series':
                                if Records[title_id].used_series:
                                        output = Records[title_id].title_series
                                if Records[keep_id].used_series:
                                        kept = Records[keep_id].title_series
                        elif Label == 'Seriesnum':
                                if Records[title_id].used_seriesnum:
                                        output = Records[title_id].title_seriesnum
                                if Records[keep_id].used_seriesnum:
                                        kept = Records[keep_id].title_seriesnum
                        elif Label == 'TitleType':
                                if Records[title_id].used_ttype:
                                        if Records[title_id].title_ttype == 'COVERART':
                                                cover_pubs = SQLGetCoverPubsByTitle(title_id)
                                                if cover_pubs:
                                                        for cover_pub in cover_pubs:
                                                                if cover_pub[PUB_IMAGE]:
                                                                        if output == '-':
                                                                                output = ''
                                                                        output += '<br>%s<br>' % ISFDBFormatImage(cover_pub[PUB_IMAGE], cover_pub[PUB_PUBID], 'scans')
                                        else:
                                                output = Records[title_id].title_ttype
                                if Records[keep_id].used_ttype:
                                        kept = Records[keep_id].title_ttype
                        elif Label == 'Storylen':
                                if Records[title_id].used_storylen:
                                        output = Records[title_id].title_storylen
                                if Records[keep_id].used_storylen:
                                        kept = Records[keep_id].title_storylen
                        elif Label == 'ContentIndicator':
                                if Records[title_id].used_content:
                                        output = Records[title_id].title_content
                                if Records[keep_id].used_content:
                                        kept = Records[keep_id].title_content
                        elif Label == 'Juvenile':
                                if Records[title_id].used_jvn:
                                        output = Records[title_id].title_jvn
                                if Records[keep_id].used_jvn:
                                        kept = Records[keep_id].title_jvn
                        elif Label == 'Novelization':
                                if Records[title_id].used_nvz:
                                        output = Records[title_id].title_nvz
                                if Records[keep_id].used_nvz:
                                        kept = Records[keep_id].title_nvz
                        elif Label == 'NonGenre':
                                if Records[title_id].used_non_genre:
                                        output = Records[title_id].title_non_genre
                                if Records[keep_id].used_non_genre:
                                        kept = Records[keep_id].title_non_genre
                        elif Label == 'Graphic':
                                if Records[title_id].used_graphic:
                                        output = Records[title_id].title_graphic
                                if Records[keep_id].used_graphic:
                                        kept = Records[keep_id].title_graphic
                        elif Label == 'Translator':
                                if Records[title_id].used_xlate:
                                        output = Records[title_id].title_xlate
                                if Records[keep_id].used_xlate:
                                        kept = Records[keep_id].title_xlate
                        elif Label == 'Language':
                                if Records[title_id].used_language:
                                        output = Records[title_id].title_language
                                if Records[keep_id].used_language:
                                        kept = Records[keep_id].title_language
                        elif Label == 'Webpages':
                                if Records[title_id].used_webpages:
                                        output = ''
                                        for count, value in enumerate(Records[title_id].title_webpages):
                                                if count:
                                                        output += '<br>'
                                                output += '<a href="%s" target="_blank">%s</a>' % (value, ISFDBText(value))
                        elif Label == 'Synopsis':
                                if Records[title_id].used_synop:
                                        output = Records[title_id].title_synop
                                if Records[keep_id].used_synop:
                                        kept = Records[keep_id].title_synop
                        elif Label == 'Note':
                                if Records[title_id].used_note:
                                        output = Records[title_id].title_note
                                if Records[keep_id].used_note:
                                        kept = Records[keep_id].title_note
                        elif Label == 'Parent':
                                if Records[title_id].used_parent:
                                        output = Records[title_id].title_parent
                                if Records[keep_id].used_parent:
                                        kept = Records[keep_id].title_parent
                                        if kept == KeepId:
                                                self._InvalidSubmission('This submission would result in a title that is a parent of itself, which is not allowed.')
                        if Label not in ('Author', 'TranslitTitles', 'Webpages', 'Synopsis', 'Note', 'TitleType'):
                                output = ISFDBText(output)
                        if Label in ('Webpages', 'TranslitTitles'):
                                css_class = 'keep'
                        elif Label == 'TitleType' and Records[title_id].title_ttype == 'COVERART':
                                css_class = 'keep'
                        elif title_id == keep_id:
                                css_class = 'keep'
                        elif output == kept:
                                css_class = 'keep'
                        else:
                                css_class = 'drop'
                        print('<td class="%s">%s</td>' % (css_class, output))
                print('</tr>')

        def DisplayNewPub(self):
                from titleClass import titles
                from pubClass import pubs
                self.GetMetadata(('Parent', 'Title', 'Language', 'Synopsis', 'TitleNote',
                                  'TitleNote', 'Series', 'SeriesNum', 'Storylen', 'ContentIndicator',
                                  'NonGenre', 'Juvenile', 'Novelization', 'Graphic',
                                  'Year', 'PubType', 'Publisher', 'Pages', 'Binding',
                                  'Isbn', 'Catalog', 'Price', 'PubSeries', 'PubSeriesNum',
                                  'Image', 'Note', 'Source'))
                self.GetMetadataMulti('TransTitles', 'TransTitle')
                self.GetMetadataMulti('Authors', 'Author')
                self.GetMetadataMulti('Webpages', 'Webpage')
                self.GetMetadataMulti('PubWebpages', 'PubWebpage')
                parent_id = self.metadata['Parent']
                
                # Save the submitted publication Title/Author data
                # to be used in the Publication display section below
                self.SetMetaData('PubTitle', self.metadata['Title'])
                self.SetMetaDataMulti('PubTransTitles', self.metadata['TransTitles'])
                self.SetMetaDataMulti('PubAuthors', self.metadata['Authors'])
                self.SetMetaData('TitleDate', self.metadata['Year'])
                self.SetMetaData('TitleType', self.metadata['PubType'])

                title_data = []
                table = SubmissionTable(self)
                if self.updated['Parent']:
                        table.suppress_warnings = 1
                        title_data = SQLloadTitle(int(parent_id))
                        if title_data == []:
                                self._InvalidSubmission('Automerge specified, but target title record %s is missing' % parent_id)
                        # In the Title section, display the CURRENT title data as opposed to what was captured at submission time
                        title = titles(db)
                        title.load(int(parent_id))
                        self.SetMetaData('Title', title.title_title)
                        self.SetMetaDataMulti('TransTitles', title.title_trans_titles)
                        self.SetMetaDataMulti('Authors', title.title_authors)
                        self.SetMetaData('TitleType', title.title_ttype)
                        self.SetMetaData('TitleDate', title.title_year)
                        self.SetMetaData('Language', title.title_language)
                        self.SetMetaData('Synopsis', title.title_synop)
                        self.SetMetaData('TitleNote', title.title_note)
                        self.SetMetaData('Series', title.title_series)
                        self.SetMetaData('SeriesNum', title.title_seriesnum)
                        self.SetMetaData('Storylen', title.title_storylen)
                        self.SetMetaData('ContentIndicator', title.title_content)
                        self.SetMetaData('NonGenre', title.title_non_genre)
                        self.SetMetaData('Juvenile', title.title_jvn)
                        self.SetMetaData('Novelization', title.title_nvz)
                        self.SetMetaData('Graphic', title.title_graphic)
                        self.SetMetaDataMulti('Webpages', title.title_webpages)
                        # Set 'TitleDate', which will be later used by self._CheckPubDate
                        self.SetMetaData('TitleDate', title.title_year)
                        table.headers.extend(['Field', 'Current Value'])
                        print('Automerge with title ')
                        pub = pubs(db)
                        # Specify the pub date to help the print logic decide whether
                        # to display the date of the parent title
                        pub.pub_year = self.metadata['Year']
                        pub.PrintTitleLine(title_data, None, None, 1)
                        print('<h2>Automerge Title Data</h2>')
                else:
                        print('<h2>Title Data</h2>')
                        table.headers.extend(['Field', 'Proposed Value'])

                table.Add1MetadataRow('Title', 'Title')
                table.Add1MetadataMultiRow('', 'Transliterated Titles', 'TransTitles', 'TransTitle')
                table.Add1MetadataMultiRow('author', 'Authors', 'Authors', 'Author')
                table.Add1MetadataRow('Title Date', 'TitleDate')
                table.Add1MetadataRow('Series', 'Series', 'series')
                table.Add1MetadataRow('Series Number', 'SeriesNum')
                table.Add1MetadataMultiRow('webpage', 'Web Pages', 'Webpages', 'Webpage')
                table.Add1MetadataRow('Language', 'Language')
                table.Add1MetadataRow('Title Type', 'TitleType')
                table.Add1MetadataRow('Length', 'Storylen')
                table.Add1MetadataRow('Content Indicator', 'ContentIndicator')
                table.Add1MetadataRow('Non-Genre', 'NonGenre')
                table.Add1MetadataRow('Juvenile', 'Juvenile')
                table.Add1MetadataRow('Novelization', 'Novelization')
                table.Add1MetadataRow('Graphic', 'Graphic')
                table.Add1MetadataNoteRow('Synopsis', 'Synopsis')
                table.Add1MetadataNoteRow('Title Note', 'TitleNote')
                table.PrintTable()

                print('<h2>Publication Data</h2>')

                table = SubmissionTable(self)
                if self.metadata['Title'] != self.metadata['PubTitle']:
                        # This should only happen if the Web API got out of synch or if
                        # the title's title has changed since the submission was created
                        warning = 'Pub title does not match the Title title'
                else:
                        warning = ''
                table.Add1MetadataRow('Pub Title', 'PubTitle', warning = warning)
                table.Add1MetadataMultiRow('', 'Transliterated Pub Titles', 'PubTransTitles', 'PubTransTitle')

                if set(self.metadata['Authors']) != set(self.metadata['PubAuthors']):
                        # This should only happen if the Web API got out of synch or if
                        # the title's author(s) have changed since the submission was created
                        warning = 'Pub authors do not match the Title authors'
                else:
                        warning = ''
                table.Add1MetadataMultiRow('author', 'Pub Authors', 'PubAuthors', 'PubAuthor', warning = warning)

                table.Add1MetadataRow('Pub Date', 'Year', 'pub_date')
                table.Add1MetadataRow('Pub Type', 'PubType', 'pub_type')
                table.Add1MetadataRow('Publisher', 'Publisher', 'publisher')
                table.Add1MetadataRow('Pages', 'Pages')
                table.Add1MetadataRow('Format', 'Binding', 'format')
                table.Add1MetadataRow('ISBN', 'Isbn', 'isbn')
                table.Add1MetadataRow('Catalog ID', 'Catalog', 'catalog')
                table.Add1MetadataRow('Price', 'Price', 'price')
                table.Add1MetadataRow('Pub Series', 'PubSeries', 'pub_series')
                table.Add1MetadataRow('Pub Series #', 'PubSeriesNum')
                table.Add1MetadataRow('Image', 'Image', 'image')
                table.Add1MetadataMultiRow('webpage', 'Pub Web Page', 'PubWebpages', 'PubWebpage')
                table.Add1MetadataNoteRow('Note', 'Note')
                table.Add1AttributeRow('External IDs', self._GetExternalIDValues(), 'prebuilt')
                table.DisplayAddRecord()

                self._DisplayNewCovers()
                self._DisplayNewTitleContent()
                self._DisplayNewReviews()
                self._DisplayNewInterviews()

                self._DisplaySource()

        def _DisplayNewCovers(self):
                cover_records = self.doc.getElementsByTagName('Cover')
                if not cover_records:
                        return
                table = ContentTable(self)
                table.caption = 'Cover Art'
                table.headers.extend(['Title', 'Artists', 'Date'])

                for cover_record in cover_records:
                        row = ContentRow(table)
                        row.xml_record = cover_record
                        row.AddCell('cTitle')
                        row.AddAuthorCell('cArtists')
                        row.AddCell('cDate')
                        table.rows.append(row)
                table.PrintTable()

        def _DisplayNewTitleContent(self):
                title_records = self.doc.getElementsByTagName('ContentTitle')
                if not title_records:
                        return
                table = ContentTable(self)
                table.caption = 'Regular Titles'
                table.headers.extend(['Page', 'Title', 'Authors', 'Date', 'Type', 'Length'])

                for title_record in title_records:
                        row = ContentRow(table)
                        row.xml_record = title_record
                        row.AddCell('cPage')
                        row.AddCell('cTitle')
                        row.AddAuthorCell('cAuthors')
                        row.AddCell('cDate')
                        row.AddCell('cType')
                        row.AddCell('cLength')
                        table.rows.append(row)
                table.PrintTable()

        def _DisplayNewReviews(self):
                review_records = self.doc.getElementsByTagName('ContentReview')
                if not review_records:
                        return
                table = ContentTable(self)
                table.caption = 'Reviews'
                table.headers.extend(['Page', 'Title', 'Authors', 'Reviewers', 'Date'])

                for review_record in review_records:
                        row = ContentRow(table)
                        row.xml_record = review_record
                        row.AddCell('cPage')
                        row.AddCell('cTitle')
                        row.AddAuthorCell('cBookAuthors')
                        row.AddAuthorCell('cReviewers')
                        row.AddCell('cDate')
                        table.rows.append(row)
                table.PrintTable()

        def _DisplayNewInterviews(self):
                interview_records = self.doc.getElementsByTagName('ContentInterview')
                if not interview_records:
                        return
                table = ContentTable(self)
                table.caption = 'Interviews'
                table.headers.extend(['Page', 'Title', 'Interviewees', 'Interviewers', 'Date'])

                for interview_record in interview_records:
                        row = ContentRow(table)
                        row.xml_record = interview_record
                        row.AddCell('cPage')
                        row.AddCell('cTitle')
                        row.AddAuthorCell('cInterviewees')
                        row.AddAuthorCell('cInterviewers')
                        row.AddCell('cDate')
                        table.rows.append(row)
                table.PrintTable()

        def DisplayClonePublication(self):
                from pubClass import pubs
                self.GetMetadata(('Parent', 'Title', 'ClonedPubID', 'ClonedTo',
                                  'Year', 'PubType', 'Publisher', 'Pages', 'Binding',
                                  'Isbn', 'Catalog', 'Price', 'PubSeries', 'PubSeriesNum',
                                  'Image', 'Note', 'Source'))
                self.GetMetadataMulti('TransTitles', 'TransTitle')
                self.GetMetadataMulti('Authors', 'Author')
                self.GetMetadataMulti('Webpages', 'Webpage')
                pub_date = self.metadata['Year']
                import_into_pub_id = self.metadata['ClonedTo']

                table = SubmissionTable(self)

                referral_language = ''
                if self.updated['Parent']:
                        table.headers.extend(['Field', 'Proposed Value'])
                        parent_id = int(self.metadata['Parent'])
                        title_data = SQLloadTitle(parent_id)
                        # If the title that the new pub is supposed to be auto-merged with no longer exists, hard reject the submission
                        if not title_data:
                                self._InvalidSubmission('Title %d is no longer in the database' % parent_id)
                        self.SetMetaData('TitleType', title_data[TITLE_TTYPE])
                        # Set 'TitleDate', which will be later used by self._CheckPubDate
                        self.SetMetaData('TitleDate', title_data[TITLE_YEAR])
                        cloned_pub_id = self.metadata['ClonedPubID']
                        if cloned_pub_id:
                                print("""Cloning Publication ID %s. New pub will be automerged with title 
                                """ % ISFDBLinkNoName('pl.cgi', cloned_pub_id, cloned_pub_id))
                        else:
                                print("""Cloning Publication. New pub will be automerged with title """)
                        pub = pubs(db)
                        # Specify the new pub date to help PrintTitleLine decide whether
                        # to display the date of the parent title
                        pub.pub_year = pub_date
                        pub.PrintTitleLine(title_data, None, None, 1)
                elif import_into_pub_id:
                        table.suppress_warnings = 1
                        table.headers.extend(['Field', 'Current Value'])
                        pub = SQLGetPubById(import_into_pub_id)
                        if not pub:
                                self._InvalidSubmission('Publication %s is no longer in the database' % import_into_pub_id)
                        print('Importing content into publication record %s' % ISFDBLink('pl.cgi', pub[PUB_PUBID], pub[PUB_TITLE]))
                        referral_title_id = SQLgetTitleReferral(pub[PUB_PUBID], pub[PUB_CTYPE], 1)
                        if referral_title_id:
                                referral_title = SQLloadTitle(referral_title_id)
                                referral_language = referral_title[TITLE_LANGUAGE]

                print('<h2>Publication Data</h2>')

                table.Add1MetadataRow('Title', 'Title')
                table.Add1MetadataMultiRow('', 'Transliterated Titles', 'TransTitles', 'TransTitle')
                table.Add1MetadataMultiRow('author', 'Authors', 'Authors', 'Author')
                table.Add1MetadataRow('Pub Date', 'Year', 'pub_date')
                table.Add1MetadataRow('Pub Type', 'PubType', 'pub_type')
                table.Add1MetadataRow('Publisher', 'Publisher', 'publisher')
                table.Add1MetadataRow('Pages', 'Pages')
                table.Add1MetadataRow('Format', 'Binding', 'format')
                table.Add1MetadataRow('ISBN', 'Isbn', 'isbn')
                table.Add1MetadataRow('Catalog ID', 'Catalog', 'catalog')
                table.Add1MetadataRow('Price', 'Price', 'price')
                table.Add1MetadataRow('Pub. Series', 'PubSeries', 'pub_series')
                table.Add1MetadataRow('Pub. Series #', 'PubSeriesNum')
                table.Add1MetadataRow('Image', 'Image', 'image')
                table.Add1MetadataMultiRow('webpage', 'Web Page', 'Webpages', 'Webpage')
                table.Add1MetadataNoteRow('Note', 'Note')
                table.Add1AttributeRow('External IDs', self._GetExternalIDValues(), 'prebuilt')
                table.PrintTable()

                self._DisplayCoverClone(referral_language)
                self._DisplayTitleContentClone(referral_language)
                self._DisplayReviewClone(referral_language)
                self._DisplayInterviewClone(referral_language)

                self._DisplaySource()

                if import_into_pub_id:
                        self._DisplayVerifications(pub[PUB_PUBID])
                        self._DisplayPendingPubUpdates(pub[PUB_PUBID])
                        self._DisplayPendingTitleRemovals(pub[PUB_PUBID])
                        self._DisplayPendingImports(pub[PUB_PUBID])

        def _DisplayCoverClone(self, referral_language):
                cover_records = self.doc.getElementsByTagName('Cover')
                if not cover_records:
                        return
                table = ContentTable(self)
                table.caption = 'Cover Art'
                table.headers.extend(['Title', 'Artists', 'Date', 'Merge Method'])

                for cover_record in cover_records:
                        row = ContentRow(table)
                        row.xml_record = cover_record
                        row.AddTitleCell(referral_language)
                        row.AddAuthorCell('cArtists')
                        row.AddCell('cDate')
                        row.AddMergeMethod()
                        table.rows.append(row)
                table.PrintTable()

        def _DisplayTitleContentClone(self, referral_language):
                title_records = self.doc.getElementsByTagName('ContentTitle')
                if not title_records:
                        return
                table = ContentTable(self)
                table.caption = 'Regular Titles'
                table.headers.extend(['Page', 'Title', 'Authors', 'Date', 'Type', 'Length', 'Merge Method'])

                for title_record in title_records:
                        row = ContentRow(table)
                        row.xml_record = title_record
                        row.AddCell('cPage')
                        row.AddTitleCell(referral_language)
                        row.AddAuthorCell('cAuthors')
                        row.AddCell('cDate')
                        row.AddCell('cType')
                        row.AddCell('cLength')
                        row.AddMergeMethod()
                        table.rows.append(row)
                table.PrintTable()

        def _DisplayReviewClone(self, referral_language):
                review_records = self.doc.getElementsByTagName('ContentReview')
                if not review_records:
                        return
                table = ContentTable(self)
                table.caption = 'Reviews'
                table.headers.extend(['Page', 'Title', 'Authors', 'Reviewers', 'Date', 'Merge Method'])

                for review_record in review_records:
                        row = ContentRow(table)
                        row.xml_record = review_record
                        row.AddCell('cPage')
                        row.AddTitleCell(referral_language)
                        row.AddAuthorCell('cBookAuthors')
                        row.AddAuthorCell('cReviewers')
                        row.AddCell('cDate')
                        row.AddMergeMethod()
                        table.rows.append(row)
                table.PrintTable()

        def _DisplayInterviewClone(self, referral_language):
                interview_records = self.doc.getElementsByTagName('ContentInterview')
                if not interview_records:
                        return
                table = ContentTable(self)
                table.caption = 'Interviews'
                table.headers.extend(['Page', 'Title', 'Interviewees', 'Interviewers', 'Date', 'Merge Method'])

                for interview_record in interview_records:
                        row = ContentRow(table)
                        row.xml_record = interview_record
                        row.AddCell('cPage')
                        row.AddTitleCell(referral_language)
                        row.AddAuthorCell('cInterviewees')
                        row.AddAuthorCell('cInterviewers')
                        row.AddCell('cDate')
                        row.AddMergeMethod()
                        table.rows.append(row)
                table.PrintTable()

        def DisplayEditPub(self):
                from pubClass import pubs
                from titleClass import titles

                submission_id = self.sub_id

                self.GetMetadata(('Record', 'Title', 'Year', 'Publisher',
                                  'PubSeries', 'PubSeriesNum', 'Pages', 'Binding',
                                  'PubType', 'Isbn', 'Catalog',
                                  'Price', 'Image', 'Note'))
                self.GetMetadataMulti('TransTitles', 'TransTitle')
                self.GetMetadataMulti('Authors', 'Author')
                self.GetMetadataMulti('Webpages', 'Webpage')

                pub_id = int(self.metadata['Record'])

                current = pubs(db)
                current.load(pub_id)
                if current.error:
                        self._InvalidSubmission(current.error)
                self.current_record = current

                table = SubmissionTable(self)
                table.headers.extend(['Field',
                                      'Current Pub Record #%s' % ISFDBLinkNoName('pl.cgi', pub_id, pub_id),
                                      'Proposed Changes'])

                table.AddAttributeToMetadataRow('Title', current.pub_title, 'Title')
                table.AddAttributeToMetadataMultiRow('Transliterated Titles', '',
                                                    current.pub_trans_titles,
                                                    'TransTitles', 'TransTitle')
                table.AddAttributeToMetadataMultiRow('Authors', 'author',
                                                    current.pub_authors,
                                                    'Authors', 'Author')
                table.AddAttributeToMetadataRow('Date', current.pub_year, 'Year', 'pub_date')
                table.AddAttributeToMetadataRow('Pub. Type', current.pub_ctype, 'PubType')
                table.AddAttributeToMetadataRow('Publisher', current.pub_publisher, 'Publisher', 'publisher')
                table.AddAttributeToMetadataRow('Pages', current.pub_pages, 'Pages')
                table.AddAttributeToMetadataRow('Format', current.pub_ptype, 'Binding', 'format')
                table.AddAttributeToMetadataRow('ISBN', current.pub_isbn, 'Isbn', 'isbn')
                table.AddAttributeToMetadataRow('Catalog ID', current.pub_catalog, 'Catalog', 'catalog')
                table.AddAttributeToMetadataRow('Price', current.pub_price, 'Price', 'price')
                table.AddAttributeToMetadataRow('Pub. Series', current.pub_series, 'PubSeries', 'pub_series')
                table.AddAttributeToMetadataRow('Pub. Series #', current.pub_series_num, 'PubSeriesNum')
                table.AddAttributeToMetadataRow('Image', current.pub_image, 'Image', 'image')
                table.AddAttributeToMetadataMultiRow('Web Pages', 'webpage',
                                                    current.pub_webpages,
                                                    'Webpages', 'Webpage')
                table.AddAttributeToMetadataRow('Note', current.pub_note, 'Note', note = 1)

                if TagPresent(self.merge, 'External_IDs'):
                        self.updated['External IDs String'] = 1
                else:
                        self.updated['External IDs String'] = 0
                external_ids = self._GetExternalIDValues()
                if external_ids:
                        self.metadata['External IDs String'] = external_ids
                else:
                        self.metadata['External IDs String'] = ''
                table.AddAttributeToMetadataRow('External IDs', '<br>'.join(current.formatExternalIDs()),
                                                'External IDs String', 'prebuilt')
                table.PrintTable()

                if self.doc.getElementsByTagName('Content'):

                        ##########################################################
                        # Modified Cover Art
                        ##########################################################
                        children = self.doc.getElementsByTagName('Cover')
                        if len(children):
                                needCover = 1
                                for child in children:
                                        record = GetChildValue(child, 'Record')
                                        if record:
                                                if needCover:
                                                        needCover = 0
                                                        print('<h2>Modified Cover Art</h2>')
                                                        print('<table border="2" class="generic_table">')
                                                self._DisplayCoverChanged(child, record)
                                if needCover == 0:
                                        print('</table>')

                        ##########################################################
                        # Modified Regular Titles
                        ##########################################################
                        children = self.doc.getElementsByTagName('ContentTitle')
                        if len(children):
                                needTitle = 1
                                for child in children:
                                        record  = GetChildValue(child, 'Record')
                                        if record:
                                                if needTitle:
                                                        needTitle = 0
                                                        print('<h2>Modified Regular Titles</h2>')
                                                        print('<table border="2" class="generic_table">')
                                                self._DisplayTitleContentChanged(child, record, current)
                                if needTitle == 0:
                                        print('</table>')
                                
                        ##########################################################
                        # Modified Reviews
                        ##########################################################
                        children = self.doc.getElementsByTagName('ContentReview')
                        if len(children):
                                needTitle = 1
                                for child in children:
                                        record  = GetChildValue(child, 'Record')
                                        if record:
                                                if needTitle:
                                                        needTitle = 0
                                                        print('<h2>Modified Reviews</h2>')
                                                        print('<table border="2" class="generic_table">')
                                                self._DisplayOtherContentChanged(child, 'review', record, current)
                                if needTitle == 0:
                                        print('</table>')

                        ##########################################################
                        # Modified Interviews
                        ##########################################################
                        children = self.doc.getElementsByTagName('ContentInterview')
                        if len(children):
                                needTitle = 1
                                for child in children:
                                        record  = GetChildValue(child, 'Record')
                                        if record:
                                                if needTitle:
                                                        needTitle = 0
                                                        print('<h2>Modified Interviews</h2>')
                                                        print('<table border="2" class="generic_table">')
                                                self._DisplayOtherContentChanged(child, 'interview', record, current)
                                if needTitle == 0:
                                        print('</table>')

                        self._DisplayCoverAdded()
                        self._DisplayTitleContentAdded()
                        self._DisplayReviewAdded()
                        self._DisplayInterviewAdded()
                        
                self._DisplayDateMismatches(pub_id)

                self._DisplayVerifications(pub_id)

                self._DisplayRecentSubmissionsConflicts(pub_id)

                self._DisplayPendingConflicts(pub_id)

                self._DisplayPendingTitleRemovals(pub_id)

                self._DisplayPendingImports(pub_id)

        def _DisplayRecentSubmissionsConflicts(self, pub_id):
                recent_submissions = SQLRecentSubmissions(pub_id, self.sub_data[SUB_TIME])
                if recent_submissions:
                        print('<p><div id="RecentSubmissionWarning">')
                        print("""<b>WARNING:</b> This publication has been modified by the following
                                submissions since this submission was created:""")
                        print('<ul>')
                        for recent_submission_id in recent_submissions:
                                print(('<li>%s' % ISFDBLinkNoName('view_submission.cgi', recent_submission_id, recent_submission_id)))
                        print('</ul>')
                        print('</div><p>')

        def _DisplayDateMismatches(self, pub_id):
                if not self.metadata['Year']:
                        return
                titles = SQLloadTitlesXBT(pub_id)
                problem_titles = {}
                for title in titles:
                        title_id = str(title[TITLE_PUBID])
                        title_date = title[TITLE_YEAR]
                        if self.contents_titles_with_dates.get(title_id):
                                title_date = self.contents_titles_with_dates[title_id]
                        if ISFDBCompare2Dates(self.metadata['Year'], title_date) == 1:
                                problem_titles[title_id] = title[TITLE_TITLE]
                if problem_titles:
                        print('<p><div id="DateMismatchWarning">')
                        print('<b>WARNING:</b> The following Contents titles have dates after the proposed publication date:')
                        print('<ul>')
                        for problem_title_id in sorted(problem_titles, key=problem_titles.get):
                                print(('<li>%s' % ISFDBLink('title.cgi', problem_title_id, problem_titles[problem_title_id])))
                        print('</ul>')
                        print('</div><p>')

        def _DisplayPendingConflicts(self, record_id, element_name = 'Record'):
                pending_submissions = SQLPendingSubmissions(self.sub_id, self.sub_type, record_id, element_name)
                if pending_submissions:
                        print('<p><div id="PendingSubmissionWarning">')
                        print('<b>WARNING:</b> The following pending submissions also aim to change this record:')
                        print('<ul>')
                        for pending_submission_id in pending_submissions:
                                print(('<li>%s' % ISFDBLinkNoName('view_submission.cgi', pending_submission_id, pending_submission_id)))
                        print('</ul>')
                        print('</div><p>')

        def _DisplayPendingVTs(self, title_id):
                pending_vts = SQLPendingVTs(self.sub_id, title_id)
                if pending_vts:
                        print('<p><div id="PendingVTs">')
                        print('<b>WARNING:</b> The following pending submissions aim to turn this title into a variant:')
                        print('<ul>')
                        for pending_vt in pending_vts:
                                print(('<li>%s' % ISFDBLinkNoName('view_submission.cgi', pending_vt, pending_vt)))
                        print('</ul>')
                        print('</div><p>')

        def _DisplayPendingPubUpdates(self, pub_id):
                pending_pub_updates = SQLPendingPubUpdates(self.sub_id, pub_id)
                if pending_pub_updates:
                        print('<p><div id="PendingSubmissionWarning">')
                        print('<b>WARNING:</b> The following pending submissions aim to change this record:')
                        print('<ul>')
                        for pending_pub_update_id in pending_pub_updates:
                                print(('<li>%s' % ISFDBLinkNoName('view_submission.cgi', pending_pub_update_id, pending_pub_update_id)))
                        print('</ul>')
                        print('</div><p>')

        def _DisplayPendingTitleRemovals(self, pub_id):
                pending_title_removals = SQLPendingTitleRemovals(self.sub_id, pub_id)
                if pending_title_removals:
                        print('<p><div id="PendingTitleRemovalWarning">')
                        print('<b>WARNING:</b> The following pending submissions aim to remove title(s) from this record:')
                        print('<ul>')
                        for pending_title_removal_id in pending_title_removals:
                                print(('<li>%s' % ISFDBLinkNoName('view_submission.cgi', pending_title_removal_id, pending_title_removal_id)))
                        print('</ul>')
                        print('</div><p>')

        def _DisplayPendingImports(self, pub_id):
                pending_imports = SQLPendingImports(self.sub_id, pub_id)
                if pending_imports:
                        print('<p><div id="PendingImportWarning">')
                        print('<b>WARNING:</b> The following pending submissions aim to import title(s) into this record:')
                        print('<ul>')
                        for pending_import_id in pending_imports:
                                print(('<li>%s' % ISFDBLinkNoName('view_submission.cgi', pending_import_id, pending_import_id)))
                        print('</ul>')
                        print('</div><p>')

        def _DisplayCoverChanged(self, child, record):
                title   = GetChildValue(child, 'cTitle')
                artists = GetChildValue(child, 'cArtists')
                date    = GetChildValue(child, 'cDate')
                self.contents_titles_with_dates[record] = date
                self._CheckTitleExistence(record)
                titleData = SQLloadTitle(record)

                self._DisplayEditContentHeaders(record)

                self._PrintComparison2('Title', title, titleData[TITLE_TITLE])
                oldartists = '+'.join(SQLTitleAuthors(record))
                self._PrintComparison2('Artists', artists, oldartists)
                warning = ''
                if ISFDBCompare2Dates(self.current_record.pub_year, date) == 1:
                        warning = 'Title date after publication date'
                self._PrintComparison2('Year', date, titleData[TITLE_YEAR], warning)

        def _DisplayEditContentHeaders(self, record):
                print('<tr>')
                print('<td class="label"> </td>')
                print('<td class="label"><b>Title #%s</b></td>' % ISFDBLinkNoName('title.cgi', record, record))
                print('<td class="label"><b>Proposed Value</b></td>')
                print('<td class="label"><b>Warnings</b></td>')
                print('</tr>')

        def _DisplayTitleContentChanged(self, child, record, current):
                title   = GetChildValue(child, 'cTitle')
                authors = GetChildValue(child, 'cAuthors')
                date    = GetChildValue(child, 'cDate')
                self.contents_titles_with_dates[record] = date
                page    = GetChildValue(child, 'cPage')
                type    = GetChildValue(child, 'cType')
                length  = GetChildValue(child, 'cLength')
                if page == '' and TagPresent(child, 'cPage'):
                        page = '-'
                if length == '' and TagPresent(child, 'cLength'):
                        length = '-'

                self._CheckTitleExistence(record)
                titleData = SQLloadTitle(record)
                self._DisplayEditContentHeaders(record)

                oldauthors = '+'.join(SQLTitleAuthors(record))
                oldPage = SQLGetPageNumber(record, current.pub_id)

                self._PrintComparison2('Title', title, titleData[TITLE_TITLE])
                self._PrintComparison2('Authors', authors, oldauthors)
                warning = ''
                if ISFDBCompare2Dates(current.pub_year, date) == 1:
                        warning = 'Title date after publication date'
                self._PrintComparison2('Year', date, titleData[TITLE_YEAR], warning)
                self._PrintComparison2('Type', type, titleData[TITLE_TTYPE])
                self._PrintComparison2('Length', length, titleData[TITLE_STORYLEN])
                self._PrintComparison2('Page', page, oldPage)

        def _DisplayOtherContentChanged(self, child, record_type, record, current):
                title = GetChildValue(child, 'cTitle')
                page = GetChildValue(child, 'cPage')
                if (page == '') and TagPresent(child, 'cPage'):
                        page = '-'
                date = GetChildValue(child, 'cDate')
                self.contents_titles_with_dates[record] = date
                if record_type == 'review':
                        primary_authors   = GetChildValue(child, 'cBookAuthors')
                        secondary_authors = GetChildValue(child, 'cReviewers')
                else:
                        primary_authors = GetChildValue(child, 'cInterviewees')
                        secondary_authors = GetChildValue(child, 'cInterviewers')

                self._CheckTitleExistence(record)
                titleData = SQLloadTitle(record)

                self._DisplayEditContentHeaders(record)

                self._PrintComparison2('Title', title, titleData[TITLE_TITLE])

                if titleData[TITLE_TTYPE] == 'REVIEW':
                        oldauthors = self._GetReviewees(record)
                        self._PrintComparison2('Book Authors', primary_authors, oldauthors)
                        oldreviewers = '+'.join(SQLTitleAuthors(record))
                        self._PrintComparison2('Reviewers', secondary_authors, oldreviewers)
                elif titleData[TITLE_TTYPE] == 'INTERVIEW':
                        oldauthors = self._GetInterviewees(record)
                        self._PrintComparison2('Interviewees', primary_authors, oldauthors)
                        oldinterviewers = '+'.join(SQLTitleAuthors(record))
                        self._PrintComparison2('Interviewers', secondary_authors, oldinterviewers)

                warning = ''
                if ISFDBCompare2Dates(current.pub_year, date) == 1:
                        warning = 'Title date after publication date'
                self._PrintComparison2('Year', date, titleData[TITLE_YEAR], warning)
                oldPage = SQLGetPageNumber(record, current.pub_id)
                self._PrintComparison2('Page', page, oldPage)

        def _DisplayCoverAdded(self):
                cover_records = self.doc.getElementsByTagName('Cover')
                table = ContentTable(self)
                table.caption = 'New Cover Art'
                table.headers.extend(['Title', 'Artists', 'Date'])

                for cover_record in cover_records:
                        # Skip pre-existing covers since they are displayed separately
                        if GetChildValue(cover_record, 'Record'):
                                continue
                        row = ContentRow(table)
                        row.xml_record = cover_record
                        row.AddTitleCell()
                        row.AddAuthorCell('cArtists')
                        row.AddCell('cDate')
                        table.rows.append(row)
                table.PrintTable()

        def _DisplayTitleContentAdded(self):
                title_records = self.doc.getElementsByTagName('ContentTitle')
                table = ContentTable(self)
                table.caption = 'New Regular Titles'
                table.headers.extend(['Page', 'Title', 'Authors', 'Date', 'Type', 'Length'])

                for title_record in title_records:
                        # Skip pre-existing titles since they are displayed separately
                        if GetChildValue(title_record, 'Record'):
                                continue
                        row = ContentRow(table)
                        row.xml_record = title_record
                        row.AddCell('cPage')
                        row.AddTitleCell()
                        row.AddAuthorCell('cAuthors')
                        row.AddCell('cDate')
                        row.AddCell('cType')
                        row.AddCell('cLength')
                        table.rows.append(row)
                table.PrintTable()

        def _DisplayReviewAdded(self):
                review_records = self.doc.getElementsByTagName('ContentReview')
                table = ContentTable(self)
                table.caption = 'New Reviews'
                table.headers.extend(['Page', 'Title', 'Authors', 'Reviewers', 'Date'])

                for review_record in review_records:
                        # Skip pre-existing reviews since they are displayed separately
                        if GetChildValue(review_record, 'Record'):
                                continue
                        row = ContentRow(table)
                        row.xml_record = review_record
                        row.AddCell('cPage')
                        row.AddTitleCell()
                        row.AddAuthorCell('cBookAuthors')
                        row.AddAuthorCell('cReviewers')
                        row.AddCell('cDate')
                        table.rows.append(row)
                table.PrintTable()

        def _DisplayInterviewAdded(self):
                interview_records = self.doc.getElementsByTagName('ContentInterview')
                if not interview_records:
                        return
                table = ContentTable(self)
                table.caption = 'New Interviews'
                table.headers.extend(['Page', 'Title', 'Interviewees', 'Interviewers', 'Date'])

                for interview_record in interview_records:
                        # Skip pre-existing interviews since they are displayed separately
                        if GetChildValue(interview_record, 'Record'):
                                continue
                        row = ContentRow(table)
                        row.xml_record = interview_record
                        row.AddCell('cPage')
                        row.AddTitleCell()
                        row.AddAuthorCell('cInterviewees')
                        row.AddAuthorCell('cInterviewers')
                        row.AddCell('cDate')
                        table.rows.append(row)
                table.PrintTable()

        def _DisplaySource(self):
                source = self.metadata['Source']
                if source:
                        print('<h3>Source used:</h3>')
                        if source == 'Primary': 
                                print('Data from an owned primary source (will be auto-verified)')
                        elif source == 'Transient': 
                                print('Data from a transient primary source (will be auto-verified)')
                        elif source == 'PublisherWebsite': 
                                print('Data from publisher\'s website (Note will be updated accordingly)')
                        elif source == 'AuthorWebsite': 
                                print('Data from author\'s website (Note will be updated accordingly)')
                        elif source == 'Other':
                                print('Data from another source (details should be provided in the submitted Note)')
                                if not self.metadata['Note']:
                                        print(' - <span class="warn">No Note data</span>')
                        print('<p>')

        def _DisplayVerifications(self, pub_id, include_secondary = 1):
                from pubClass import pubs
                pub = pubs(db)
                pub.pub_id = pub_id
                verificationstatus = SQLVerificationStatus(pub_id)
                if verificationstatus == 1:
                        print('<p><div id="WarningBox">')
                        print('<b>WARNING:</b> This publication has been verified against the primary source.')
                        print('</div><p>')
                pub.PrintPrimaryVerifications()
                if include_secondary:
                        pub.PrintActiveSecondaryVerifications()

        def _GetExternalIDValues(self):
                formatted_lines = ''
                display_values = {}
                id_types = SQLLoadIdentifierTypes()
                id_elements = self.doc.getElementsByTagName('External_ID')
                sites = SQLLoadIdentifierSites()

                for id_element in id_elements:
                        try:
                                type_id = int(GetChildValue(id_element, 'IDtype'))
                                type_name = id_types[type_id][0]
                                full_name = id_types[type_id][1]
                        except:
                                self._InvalidSubmission('Submitted external ID type does not exist')
                        id_value = XMLunescape(GetChildValue(id_element, 'IDvalue'))
                        if type_name not in display_values:
                                display_values[type_name] = []
                        display_values[type_name].append((id_value, full_name, type_id))

                for type_name in sorted(display_values.keys()):
                        formatted_line = FormatExternalIDType(type_name, id_types)
                        for value in display_values[type_name]:
                                id_value = value[0]
                                type_full_name = value[1]
                                type_id = value[2]
                                formatted_id = FormatExternalIDSite(sites, type_id, id_value)
                                formatted_line += formatted_id
                        formatted_lines += '%s<br>' % formatted_line
                return formatted_lines

        def _CheckTitleExistence(self, title_id):
                # Check that the about-to-be-merged title is still in the database
                # If the title ID is not specified, skip this check
                if not int(title_id):
                        return
                title_data = SQLloadTitle(int(title_id))
                # If the title record is no longer on file, display an error and abort
                if not title_data:
                        print('</table>')
                        self._InvalidSubmission('Title %d is no longer in the database' % int(title_id))

        def _GetInterviewees(self, interview_id):
                interviewees = SQLInterviewAuthors(int(interview_id))
                newinterviewees = ''
                count = 1
                for interviewee in interviewees:
                        if count == 1:
                                newinterviewees += interviewee
                        else:
                                newinterviewees += '+'+interviewee
                        count += 1
                return newinterviewees

        def _GetReviewees(self, review_id):
                reviewees = SQLReviewAuthors(int(review_id))
                newreviewees = ''
                count = 1
                for reviewee in reviewees:
                        if count == 1:
                                newreviewees += reviewee
                        else:
                                newreviewees += '+'+reviewee
                        count += 1
                return newreviewees

        def _PrintComparison2(self, Label, Proposed, Original, warning = ''):
                if Proposed:
                        if Original:
                                self._PrintField2(Label, Proposed, 1, 1, Original, warning)
                        else:
                                self._PrintField2(Label, Proposed, 1, 0, '', warning)
                else:
                        if Original:
                                self._PrintField2(Label, '', 0, 1, Original, warning)
                        else:
                                self._PrintField2(Label, '', 0, 0, '', warning)

        def _PrintField2(self, Label, value, Changed, ExistsNow, Current, warning = ''):
                if warning:
                        self.row_warnings = [warning]
                else:
                        self.row_warnings = []
                if Label in ('Artists', 'Authors', 'Book Authors', 'Reviewers', 'Interviewees', 'Interviewers'):
                        display_author = 1
                else:
                        display_author = 0
                print('<tr>')
                self._PrintLabel(Label)
                if Changed:
                        print('<td class="drop">')
                        if ExistsNow:
                                if display_author:
                                        self._PrintAuthorNames(Current)
                                else:
                                        print(ISFDBText(Current))
                        else:
                                print('-')
                        print('</td>')
                        print('<td class="keep">')
                        if display_author:
                                self._PrintAuthorNames(value, 1)
                        else:
                                print(ISFDBText(value))
                        print('</td>')
                        # If the editor is trying to change a "container" title type, display a warning
                        if Label == 'Type' and (value != Current):
                                if Current in ('ANTHOLOGY', 'COLLECTION', 'CHAPBOOK', 'EDITOR', 'OMNIBUS'):
                                        self._AddRowWarning('Changed container title type')
                        elif Label == 'Year':
                                if ISFDBdaysFromToday(value) > SESSION.max_future_days:
                                        self._AddRowWarning('Date more than %d days in the future' % SESSION.max_future_days)
                else:
                        print('<td class="keep">')
                        if ExistsNow:
                                if display_author:
                                        self._PrintAuthorNames(Current)
                                else:
                                        print(ISFDBText(Current))
                        else:
                                print('-')
                        print('</td>')
                        print('<td class="drop">')
                        print('-')
                        print('</td>')

                if self.row_warnings:
                        print('<td class="warn">%s</td>' % '<br>'.join(self.row_warnings))
                else:
                        print('<td class="blankwarning">&nbsp;</td>')
                print('</tr>')

        def _AddRowWarning(self, warning):
                if not warning:
                        return
                warning = ISFDBText(warning)
                if warning not in self.row_warnings:
                        self.row_warnings.append(warning)

        def _PrintAuthorNames(self, name_list, display_warning = 0):
                names = name_list.split('+')
                Separator = '<span class="mergesign">+</span>'

                displayed_names = ''
                for name in names:
                        if display_warning and SQLMultipleAuthors(name):
                                self._AddRowWarning('%s is a disambiguated name' % name)
                        author = SQLgetAuthorData(name)
                        if author:
                                if display_warning and SQLauthorIsPseudo(author[AUTHOR_ID]):
                                        self._AddRowWarning('%s is an alternate name' % name)
                                # If the author is already on file, change the plain text name to an HTML link to the author record
                                name = ISFDBLink('ea.cgi', author[AUTHOR_ID], author[AUTHOR_CANONICAL])
                        else:
                                if display_warning:
                                        self._AddRowWarning('%s is a new author' % name)
                                name = ISFDBText(name)
                        
                        if displayed_names == '':
                                displayed_names = name
                        else:
                                displayed_names = displayed_names + Separator + name
                print(displayed_names)

        def _PrintLabel(self, Label):
                if Label in SUBMISSION_DISPLAY:
                        display_label = SUBMISSION_DISPLAY[Label]
                else:
                        display_label = Label
                print('<td class="label"><b>%s</b></td>' % display_label)

        def DisplayRecognizedDomainEdit(self):
                from recognizeddomainClass import RecognizedDomain
                self.GetMetadata(('Record', 'DomainName', 'SiteName', 'SiteURL', 'LinkingAllowed', 'RequiredSegment', 'ExplicitLinkRequired'))
                if not self.metadata['Record']:
                        self._InvalidSubmission('Recognized Domain ID not specified')

                recognized_domain = RecognizedDomain()
                recognized_domain.load(self.metadata['Record'])
                if not recognized_domain.domain_id:
                        self._InvalidSubmission('Specifed Recognized Domain does not exists')

                table = SubmissionTable(self)

                table.AddAttributeToMetadataRow('Recognized Domain Name', recognized_domain.domain_name, 'DomainName')
                table.AddAttributeToMetadataRow('Web Site Name', recognized_domain.site_name, 'SiteName')
                table.AddAttributeToMetadataRow('Web Site URL', recognized_domain.site_url, 'SiteURL')
                table.AddAttributeToMetadataRow('Linking Allowed', recognized_domain.linking_allowed_display, 'LinkingAllowed')
                table.AddAttributeToMetadataRow('Required URL Segment', recognized_domain.required_segment, 'RequiredSegment')
                table.AddAttributeToMetadataRow('Explicit Credit Page Link Required', recognized_domain.explicit_link_required_display, 'ExplicitLinkRequired')

                table.DisplayMetadataEdit()

        def DisplayRecognizedDomainDelete(self):
                from recognizeddomainClass import RecognizedDomain
                self.GetMetadata(('Record',))
                table = SubmissionTable(self)

                recognized_domain = RecognizedDomain()
                recognized_domain.load(self.metadata['Record'])
                if not recognized_domain.domain_id:
                        self._InvalidSubmission('Specifed Recognized Domain does not exists')

                table.headers.extend(['Field', 'Recognized Domain to Delete'])
                table.Add1AttributeRow('Recognized Domain Name', recognized_domain.domain_name)
                table.Add1AttributeRow('Web Site Name', recognized_domain.site_name)
                table.Add1AttributeRow('Web Site URL', recognized_domain.site_url)
                table.Add1AttributeRow('Linking Allowed', recognized_domain.linking_allowed_display)
                table.Add1AttributeRow('Required URL Segment', recognized_domain.required_segment)
                table.Add1AttributeRow('Explicit Credit Page Link Required', recognized_domain.explicit_link_required_display)
                table.PrintTable()

        def DisplayRecognizedDomainAdd(self):
                self.GetMetadata(('DomainName', 'SiteName', 'SiteURL', 'LinkingAllowed', 'RequiredSegment', 'ExplicitLinkRequired'))
                table = SubmissionTable(self)
                table.Add1MetadataRow('Recognized Domain Name', 'DomainName')
                table.Add1MetadataRow('Web Site Name', 'SiteName')
                table.Add1MetadataRow('Web Site URL', 'SiteURL')
                table.Add1MetadataRow('Linking Allowed', 'LinkingAllowed')
                table.Add1MetadataRow('Required URL Segment', 'RequiredSegment')
                table.Add1MetadataRow('Explicit Credit Page Link Required', 'ExplicitLinkRequired')
                table.DisplayAddRecord()
