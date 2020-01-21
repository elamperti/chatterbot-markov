from __future__ import unicode_literals
from chatterbot.conversation import Statement
from chatterbot.logic.best_match import BestMatch

import markovify
import os
import re

class MarkovAdapter(BestMatch):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.confidence_threshold = kwargs.get('threshold', 0.6)
        self.default_response = kwargs.get(
            'default_response',
            "I'm learning..."
        )

    def process(self, input_statement, additional_response_selection_parameters):
        """
        Return a default response with a high confidence if
        a high confidence response is not known.
        """
        # Select the closest match to the input statement
        search_results = self.search_algorithm.search(input_statement)
        closest_match = next(search_results, input_statement)

        # self.add_to_brain(closest_match)
        self.text_model = self.load_brain()
        # Confidence should be high only if it is less than the threshold
        # if confidence < self.confidence_threshold:
        #     confidence = 1
        # else:
        #     confidence = 0

        # if confidence:
        #     output = self.generate_sentence()
        # else:
        #     output = None

        # if output is None:
        #     output = self.default_response

        print ("INPUT STATEMENT:", closest_match)
        print ("CLOSEST MATCH:", closest_match)
        closest_match = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚçÇñÑÀà]', " ", str(closest_match))
        print ("WILL REPLY:", " ".join(str(closest_match).split(" ")[:2]))
        # ToDo: Figure out this shit and pray to god no one sees this horrible code
        try:
            output = self.generate_sentence(str(" ".join(str(closest_match).split(" ")[:2])))
        except:
            output = self.generate_sentence(str(" ".join(str(closest_match).split(" ")[:1])))
        # output.confidence = 1

        return Statement(output)

    def add_to_brain(self, msg):
        f = open('markovified.txt', 'a')
        f.write(str(msg) + '\n')
        f.close()

    def generate_sentence(self, from_text):
        print("GENERATING FROM:", from_text)
        # try:
        return self.text_model.make_sentence_with_start(beginning=from_text)
        # except:
        #     print('EXCEPT')
        #     return self.text_model.make_short_sentence(120)


    def load_brain(self):
        with open("markovified.txt") as f:
            text = f.read()
        f.close()
        return markovify.NewlineText(text)
