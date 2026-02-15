from database.drug_db import db

class DrugMatcher:
    def __init__(self):
        pass

    def match(self, input_text):
        """
        Attempts to find a drug in the database that matches the input text.
        Returns a tuple (DrugName, Instruction, Category) or None.
        """
        if not input_text:
            return None
        
        # 1. Exact match attempt
        # 2. Fuzzy/Like match
        
        results = db.search_drug(input_text)
        
        if results:
            # For now, just return the first result
            # result format: (id, name, instruction, category)
            return {
                "name": results[0][1],
                "instruction": results[0][2],
                "category": results[0][3]
            }
        
        return None

    def fuzzy_match(self, input_text):
        # Placeholder for more advanced Levenshtein distance matching if needed
        return self.match(input_text)
