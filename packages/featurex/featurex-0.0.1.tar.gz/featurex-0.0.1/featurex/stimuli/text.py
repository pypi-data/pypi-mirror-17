from featurex.stimuli import Stim
from featurex.core import Timeline, Event, Value
from featurex.support.decorators import requires_nltk_corpus
import pandas as pd
from six import string_types
import re
import unicodedata


class TextStim(Stim):

    ''' Any simple text stimulus--most commonly a single word. '''

    def __init__(self, filename=None, text=None):
        if filename is not None:
            text = open(filename).read()
        self.text = text

    def extract(self, extractors):
        vals = {}
        for e in extractors:
            vals[e.name] = e.apply(self)
        return Value(self, e, vals)


class DynamicTextStim(TextStim):

    ''' A text stimulus with timing/onset information. '''

    def __init__(self, text, order, onset=None, duration=None):
        self.order = order
        self.onset = onset
        self.duration = duration
        super(DynamicTextStim, self).__init__(text=text)


class ComplexTextStim(object):

    ''' A collection of text stims (e.g., a story), typically ordered and with
    onsets and/or durations associated with each element.
    Args:
        filename (str): The filename to read from. Must be tab-delimited text.
            Files must always contain a column containing the text of each
            stimulus in the collection. Optionally, additional columns can be
            included that contain duration and onset information. If a header
            row is present in the file, valid columns must be labeled as
            'text', 'onset', and 'duration' where available (though only text
            is mandatory). If no header is present in the file, the columns
            argument will be used to infer the indices of the key columns.
        columns (str): Optional specification of column order. An abbreviated
            string denoting the column position of text, onset, and duration
            in the file. Use t for text, o for onset, d for duration. For
            example, passing 'ot' indicates that the first column contains
            the onsets and the second contains the text. Passing 'tod'
            indicates that the first three columns contain text, onset, and
            duration information, respectively. Note that if the input file
            contains a header row, the columns argument will be ignored.
        default_duration (float): the duration to assign to any text elements
            in the collection that do not have an explicit value provided
            in the input file.
    '''

    def __init__(self, filename=None, columns='tod', default_duration=None):

        self.elements = []

        if filename is not None:
            if filename.endswith("srt"):
                self._from_srt(filename)
            else:
                self._from_file(filename, columns, default_duration)

    def _from_file(self, filename, columns, default_duration):
        tod_names = {'t': 'text', 'o': 'onset', 'd': 'duration'}

        first_row = open(filename).readline().strip().split('\t')
        if len(set(first_row) & set(tod_names.values())):
            col_names = None
        else:
            col_names = [tod_names[x] for x in columns]

        data = pd.read_csv(filename, sep='\t', names=col_names)

        for i, r in data.iterrows():
            if 'onset' not in r:
                elem = TextStim(r['text'])
            else:
                duration = r.get('duration', None)
                if duration is None:
                    duration = default_duration
                elem = DynamicTextStim(r['text'], i, r['onset'], duration)
            self.elements.append(elem)

    def _from_srt(self, filename):
        import pysrt
        
        data = pysrt.open(filename)
        list_ = [[] for _ in data]
        for i, row in enumerate(data):
            start = tuple(row.start)
            start_time = self.__to_sec__(start)
            
            end_ = tuple(row.end)
            duration = self.__to_sec__(end_) - start_time
            
            line = row.text
            line = line.replace("\r\n", " ").replace("\n", " ").replace("\r", " ").replace("\t", " ")
            list_[i] = [line, start_time, duration]
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(columns=["text", "onset", "duration"], data=list_)

        for i, r in df.iterrows():
            elem = DynamicTextStim(r['text'], i, r['onset'], r["duration"])
            self.elements.append(elem)

    def __iter__(self):
        """ Iterate text elements. """
        for elem in self.elements:
            yield elem

    def __to_sec__(self, tup):
        hours = tup[0]
        mins = tup[1]
        secs = tup[2]
        msecs = tup[3]
        total_msecs = (hours * 60 * 60 * 1000) + (mins * 60 * 1000) + (secs * 1000) + msecs
        total_secs = total_msecs / 1000.
        return total_secs

    def extract(self, extractors, merge_events=True):
        timeline = Timeline()
        # Extractors can either take ComplexTextStim input, in which case we
        # pass the current instance, or TextStim input, in which case we loop
        # over all elements.
        for ext in extractors:
            if ext.target.__name__ == self.__class__.__name__:
                events = ext.apply(self)
                for ev in events:
                    timeline.add_event(ev, merge=merge_events)
            else:
                for elem in self.elements:
                    # If no onset is available, index with order
                    onset = elem.onset or elem.order
                    event = Event(onset=onset, values=[ext.apply(elem)])
                    timeline.add_event(event, merge=merge_events)
        return timeline

    @classmethod
    def from_text(cls, text, unit='word', tokenizer=None, language='english'):
        """ Initialize from a single string, by automatically segmenting into
        individual strings. Requires nltk unless tokenizer argument is passed.
            text (str): The text to convert to a ComplexTextStim.
            unit (str): The unit of segmentation. Either 'word' or 'sentence'.
            tokenizer: Optional tokenizer to use. If passed, will override
                the default nltk tokenizers. If a string is passed, it is
                interpreted as a capturing regex and passed to re.findall().
                Otherwise, must be an object that implements a tokenize()
                method and returns a list of tokens.
            language (str): The language to use; passed to nltk. Only used if
                tokenizer is None. Defaults to English.
        Returns:
            A ComplexTextStim instance.
        """

        if tokenizer is not None:
            if isinstance(tokenizer, string_types):
                tokens = re.findall(tokenizer, text)
            else:
                tokens = tokenizer.tokenize(text)
        else:
            import nltk

            @requires_nltk_corpus
            def tokenize_text(text):
                if unit == 'word':
                    return nltk.word_tokenize(text, language)
                elif unit.startswith('sent'):
                    return nltk.sent_tokenize(text, language)
                else:
                    raise ValueError(
                        "unit must be either 'word' or 'sentence'")

            tokens = tokenize_text(text)

        cts = ComplexTextStim()
        for i, t in enumerate(tokens):
            cts.elements.append(DynamicTextStim(text=t, order=i, onset=i,
                                                duration=1))
        return cts
