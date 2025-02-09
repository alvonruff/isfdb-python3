#!_PYTHONLOC
#
#     (C) COPYRIGHT 2018-2022   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 419 $
#     Date: $Date: 2019-05-15 10:54:53 -0400 (Wed, 15 May 2019) $

from library import *
from SQLparsing import *


class awardTitles():
        def __init__(self):
                self.awards = {}
                self.titles = {}
                # Parent title IDs
                self.parents = {}
                self.poll_awards = []
                self.repeating_awards = []
                # Load lists of poll-based awards and awards considered "repeating"
                self.loadPollAwardTypes()
                self.loadRepeatingAwardTypes()

        def buildAwardTitles(self):
                self.loadAwards()
                self.loadParents()
                self.calculateScores()
                self.fileAllScores()

        def loadPollAwardTypes(self):
                query = "select award_type_id, award_type_poll from award_types where award_type_poll='Yes'"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                while record:
                        award_type_id = record[0][0]
                        award_type_poll = record[0][1]
                        self.poll_awards.append(award_type_id)
                        record = result.fetch_row()

        def loadRepeatingAwardTypes(self):
                """Load repeating award types."""
                # Some awards are a special case since titles can be nominated
                # multiple times until they win. We will record them in a separate
                # dictionary and count them once per title (wins trump nominations.)
                # At this time, the only "repeating" award is Prometheus Hall of Fame
                award_data = SQLGetAwardTypeByName('Prometheus Award')
                self.repeating_awards.append(award_data[AWARD_TYPE_ID])

        def loadAwards(self):
                """Load title data for all known awards/nominations."""
                query = """select ta.title_id, t.title_parent, YEAR(title_copyright), t.title_ttype,
                           ta.award_id, a.award_level, a.award_type_id
                           from titles t, title_awards as ta, awards as a
                           where ta.award_id = a.award_id
                           and ta.title_id = t.title_id"""
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                while record:
                        title_id = record[0][0]
                        if title_id not in self.titles:
                                self.titles[title_id] = {}
                        self.titles[title_id]['parent'] = record[0][1]
                        self.titles[title_id]['year'] = record[0][2]
                        self.titles[title_id]['type'] = record[0][3]
                        award_id = record[0][4]
                        self.awards[award_id] = {}
                        self.awards[award_id]['title_id'] = title_id
                        self.awards[award_id]['level'] = int(record[0][5])
                        self.awards[award_id]['award_type'] = int(record[0][6])
                        record = result.fetch_row()

        def loadParents(self):
                """Load parent titles without awards/nominations."""
                # Build a list of parent IDs that are not in self.titles
                parent_ids = []
                for title_id in self.titles:
                        parent_id = self.titles[title_id]['parent']
                        if not parent_id or parent_id in self.titles or parent_id in parent_ids:
                                continue
                        parent_ids.append(parent_id)

                # Retrieve the parent titles from the database
                query = """select title_id, title_parent, YEAR(title_copyright), title_ttype
                           from titles where title_id in (%s)""" % list_to_in_clause(parent_ids)
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                while record:
                        title_id = record[0][0]
                        self.titles[title_id] = {}
                        self.titles[title_id]['parent'] = record[0][1]
                        self.titles[title_id]['year'] = record[0][2]
                        self.titles[title_id]['type'] = record[0][3]
                        record = result.fetch_row()

        def calculateScores(self):
                """Calculate the award scores for title IDs with awards/nominations.

                For variant titles, use their parent title's ID."""
                repeating = {}
                for award_id in self.awards:
                        award_level = self.awards[award_id]['level']
                        award_type_id = self.awards[award_id]['award_type']
                        title_id = self.awards[award_id]['title_id']
                        if self.titles[title_id]['parent']:
                                title_id = self.titles[title_id]['parent']
                        year = self.titles[title_id]['year']
                        title_type = self.titles[title_id]['type']

                        score = 0
                        # Wins and 1st places get 50 points
                        if award_level == 1:
                                score = 50
                        # "Special" awards get 1 point
                        elif award_level > 70:
                                score = 1
                        # Nominations for non-poll awards get 35 points
                        elif award_type_id not in self.poll_awards:
                                score = 35
                        # For polls, use 35 for the second place and
                        # "33-place" for third and lower places with a minimum of 1 point
                        else:
                                if award_level == 2:
                                        score = 35
                                else:
                                        score = 33 - award_level
                                        if score < 1:
                                                score = 1
                        # For "repeating" awards, save the highest score for this title ID
                        # for further processing
                        if award_type_id in self.repeating_awards:
                                if title_id not in repeating:
                                        repeating[title_id] = score
                                elif score > repeating[title_id]:
                                        repeating[title_id] = score
                        # For all other awards, add this award's score to the cumulative score for the title
                        else:
                                self.titles[title_id]['score'] = self.titles[title_id].get('score', 0) + score
                # Add "repeating" scores for each title
                for title_id in repeating:
                        self.titles[title_id]['score'] = self.titles[title_id].get('score', 0) + repeating[title_id]

        def fileAllScores(self):
                """File title-specific award scores into the database."""
                db.query("truncate award_titles_report")
                values = []
                for title_id in self.titles:
                        # Skip variant titles without a score
                        if 'score' not in self.titles[title_id]:
                                continue
                        score = self.titles[title_id]['score']
                        year = self.titles[title_id]['year']
                        if year < 1950 and year:
                                decade = 'pre1950'
                        else:
                                decade = str(year)[:3] + '0'
                        title_type = self.titles[title_id]['type']
                        values.append((int(title_id), int(score), int(year), decade, title_type))
                        if len(values) > 300:
                                self.fileOneScoreTuple(values)
                                values = []
                if values:
                        self.fileOneScoreTuple(values)

        def fileOneScoreTuple(self, values):
                mycursor = db.cursor()
                insert = """insert into award_titles_report(title_id, score, year, decade, title_type)
                             VALUES(%s, %s, %s, %s, %s)"""
                mycursor.executemany(insert, values)
                db.commit()
