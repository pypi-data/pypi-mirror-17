# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of Mathmaker.

# Mathmaker is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Mathmaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Mathmaker; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import random

from mathmaker.lib import shared
from .X_Structure import X_Structure
from .X_Generic import (build_q_dict, build_mixed_q_list,
                        get_nb_sources_from_question_info)
from . import question

# Here the list of available values for the parameter x_kind='' and the
# matching x_subkind values
AVAILABLE_X_KIND_VALUES = {'tabular': 'default', 'slideshow': 'default'}

MAX_NB_OF_QUESTIONS = 40

X_LAYOUT_UNIT = "cm"
# ----------------------  lines_nb    col_widths   questions
X_LAYOUTS = {'default':
             {'exc': [None, 'all'],
              'ans': [None, 'all']
              }
             }

MIN_ROW_HEIGHT = 0.8

SWAPPABLE_QKINDS_QSUBKINDS = {("rectangle", "area"),
                              ("rectangle", "perimeter"),
                              ("square", "area"),
                              ("square", "perimeter")}

KINDS_SUBKINDS_CONTEXTS_TO_TRANSLATE = {
    ('divi', 'direct', 'area_width_length_rectangle'):
    ('rectangle', 'length_or_width', 'from_area')}


# --------------------------------------------------------------------------
##
#   @brief Increases the disorder of the questions' list
#   @param  l           The list
#   @param  sort_key    The list's objects' attribute that will be used to
#                       determine whether the order should be changed or not
def increase_alternation(l, sort_key):
    if len(l) >= 3:
        for i in range(len(l) - 2):
            if getattr(l[i], sort_key) == getattr(l[i + 1], sort_key):
                if getattr(l[i + 2], sort_key) != getattr(l[i], sort_key):
                    l[i + 1], l[i + 2] = l[i + 2], l[i + 1]

    return l


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_MentalCalculation
# @brief Creates a tabular with n questions and answers
class X_MentalCalculation(X_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param **options Options detailed below:
    #          - start_number=<integer>
    #                         (should be >= 1)
    #          - number_of_questions=<integer>
    #            /!\ only useful if you use x_kind and not preformatted
    #                         (should be >= 1)
    #          - x_kind=<string>
    #                         ...
    #                         ...
    #          - preformatted=<string>
    #            /!\ preformatted is useless with short_test
    #            /!\ number_of_questions is useless with preformatted
    #            /!\ if you use it with the x_kind option, ensure there's a
    #                preformatted possibility with this option
    #                         'yes'
    #                         'OK'
    #                         any other value will be understood as 'no'
    #          - short_test=bool
    #            /!\ the x_kind option above can't be used along this option
    #            use subtype if you need to make different short_test exercises
    #                         'yes'
    #                         'OK'
    #                         any other value will be understood as 'no'
    #          - subtype=<string>
    #                         ...
    #                         ...
    #   @todo Complete the description of the possible options !
    #   @return One instance of exercise.X_MentalCalculation
    def __init__(self, x_kind='default_nothing', **options):
        self.derived = True
        from mathmaker.lib.tools.xml_sheet import get_q_kinds_from
        mc_mm_file = options.get('filename')

        (x_kind, q_list) = get_q_kinds_from(
            mc_mm_file,
            sw_k_s=SWAPPABLE_QKINDS_QSUBKINDS,
            k_s_ctxt_tr=KINDS_SUBKINDS_CONTEXTS_TO_TRANSLATE)

        X_Structure.__init__(self,
                             x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                             X_LAYOUT_UNIT, **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------

        # should be default_question = question.Something
        default_question = question.Q_MentalCalculation

        # TEXTS OF THE EXERCISE
        self.text = {'exc': "", 'ans': ""}

        # From q_list, we build a dictionary and then a complete questions'
        # list:
        q_dict, self.q_nb = build_q_dict(q_list)
        for key in q_dict:
            random.shuffle(q_dict[key])
        mixed_q_list = build_mixed_q_list(q_dict)
        mixed_q_list = increase_alternation(mixed_q_list, 'type')
        mixed_q_list.reverse()
        mixed_q_list = increase_alternation(mixed_q_list, 'type')

        # mixed_q_list is organized like this:
        # [('type', 'kind', 'subkind', 'nb_source', 'options'),
        #  ('q_id', 'q_', 'id', 'table_15', {'nb':}),
        #  ('multi_direct', 'multi', 'direct', ['table_2_9'], {'nb':}),
        #  ('multi_reversed', 'multi', 'reversed', ['table_2_9'], {'nb':}),
        #  ('multi_hole', 'multi', 'hole', ['table_2_9'], {'nb':}),
        #  ('multi_direct', 'multi', 'direct', ['table_2_9'], {'nb':}),
        #  ('divi_direct', divi', 'direct', ['table_2_9'], {'nb':}),
        #  etc.
        # ]

        # Now, we generate the numbers & questions, by type of question first
        self.questions_list = []
        last_draw = [0, 0]
        for q in mixed_q_list:
            nb_sources = get_nb_sources_from_question_info(q)
            nb_to_use = tuple()
            for nb_source in nb_sources:
                nb_to_use += shared.mc_source\
                    .next(nb_source,
                          not_in=last_draw,
                          **question.get_modifier(q.type, nb_source))
                last_draw = [str(n) for n in set(nb_to_use)
                             if (isinstance(n, int) or isinstance(n, str))]
                if nb_source in ['decimal_and_10_100_1000_for_divi',
                                 'decimal_and_10_100_1000_for_multi']:
                    # __
                    q.options['10_100_1000'] = True
            self.questions_list += [default_question(q.type,
                                                     q.options,
                                                     numbers_to_use=nb_to_use
                                                     )]

    # --------------------------------------------------------------------------
    ##
    #   @brief Writes the text of the exercise|answer to the output.
    def to_str(self, ex_or_answers):
        M = shared.machine
        result = ""

        if self.slideshow:
            result += M.write_frame("", frame='start_frame')
            for i in range(self.q_nb):
                result += M.write_frame(
                    self.questions_list[i].to_str('exc'),
                    timing=self.questions_list[i].transduration)

            result += M.write_frame("", frame='middle_frame')

            for i in range(self.q_nb):
                result += M.write_frame(_("Question:")
                                        + self.questions_list[i].to_str('exc')
                                        + _("Answer:")
                                        + self.questions_list[i].to_str('ans'),
                                        timing=0)

        # default tabular option:
        else:
            q = [self.questions_list[i].to_str('exc')
                 for i in range(self.q_nb)]
            a = [self.questions_list[i].to_str('ans')
                 for i in range(self.q_nb)]\
                if ex_or_answers == 'ans' \
                else [self.questions_list[i].to_str('hint')
                      for i in range(self.q_nb)]

            n = [M.write(str(i + 1) + ".", emphasize='bold')
                 for i in range(self.q_nb)]

            content = [elt for triplet in zip(n, q, a) for elt in triplet]

            result += M.write_layout((self.q_nb, 3),
                                     [0.5, 14.25, 3.75],
                                     content,
                                     borders='penultimate',
                                     justify=['left', 'left', 'center'],
                                     center_vertically=True,
                                     min_row_height=MIN_ROW_HEIGHT)

        return result

    # INSTRUCTIONS TO CREATE A NEW EXERCISE -----------------------------------
    # - Indicate its name in the header comment
    #   the one of documentation (@class)
    # - Write the @brief description
    # - Replace the Model class name by the chosen one
    # - In the constructor comment, replace Model with the chosen name
    #   at the @return line
    # - Write the class name of the default_question. You must mention it
    #   because it will be used in the OTHER EXERCISES section.
    # - The different sections to rewrite are:
    #   * TEXTS OF THE EXERCISE:
    #       default text for all exercises of this class
    #   * alternate texts section:
    #       if you want to specify a different text for any particular kind
    #       of exercise
    #   * PREFORMATTED EXERCISES
    #       that's where preformatted exercises are described (the ones that
    #       won't repeat n times the same kind of randomly question)
    #   * OTHER EXERCISES section is meant to all exercises that repeat
    #       the same (maybe randomly chosen among many) kind of question.
    #       shouldn't be rewritten
    # - Finally, if the write_* methods from the exercise.Structure don't
    #   match your needs, copy & modify or rewrite them
