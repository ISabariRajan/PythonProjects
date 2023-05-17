class Core:
    text = ""
    def set_text(self, text):
        self.text = text
    
    def find_patterns_in_text(self, pattern, ignorecase=True):
        if ignorecase:
            pattern = pattern.lower()
            self.text = self.text.lower()

        pattern_index = self.text.find(pattern)
        pattern_indexes = []
        while pattern_index != -1:
            pattern_indexes.append(pattern_index)
            pattern_index = self.text.find(pattern, pattern_index + len(pattern))
        return pattern_indexes
