# Design and implement a Comment Filtering System that allows users to:
# Add comments with username, text, votes, and posted date.
# Filter comments by username or keywords in the text.
# Combine multiple filters using AND / OR logic.
# Sort comments by votes or date, in ascending or descending order.
# Apply multiple sorting strategies (e.g., sort by votes then date).
# Use the Strategy Pattern for sorting and Filter/Predicate Pattern for filtering.
# Ensure only one instance manages all comments using the Singleton Pattern.

import datetime
from abc import ABC, abstractmethod

# ---------- Comment Class ----------
class Comment:
    def __init__(self,username,text) -> None:
        self.username = username
        self.text = text
        self.votes = 0
        self.date_posted = datetime.datetime.now()

    def up_vote(self):
        self.votes += 1
    
    def __str__(self):
        return f"{self.username} ({self.votes} votes on {self.date_posted.strftime('%Y-%m-%d')}): {self.text}"

# ---------- Sorting Strategy Pattern ----------

class SortingStrategy(ABC):
    @abstractmethod
    def sort(self,comments):
        pass

class VoteSorting(SortingStrategy):
    def __init__(self,ascending) -> None:
        self.ascending = ascending

    def sort(self, comments):
        return sorted(comments,key=lambda c: c.votes,reverse= not self.ascending)
    
class DateSorting(SortingStrategy):
    def __init__(self,ascending) -> None:
        self.ascending = ascending

    def sort(self, comments):
        return sorted(comments,key=lambda c: c.date_posted,reverse= not self.ascending)
    
# ---------- Filter Pattern ----------

class Filter(ABC):
    @abstractmethod
    def check(self,comment):
        pass

class UsernameFilter(Filter):
    def __init__(self,username) -> None:
        self.username = username.lower()

    def check(self, comment):
        return self.username in comment.username.lower()
    
class KeywordFilter(Filter):
    def __init__(self,key) -> None:
        self.key = key.lower()

    def check(self, comment):
        return self.key in comment.text.lower()
    
class AndFilter(Filter):
    def __init__(self,filter1,filter2) -> None:
        self.filter1 = filter1
        self.filter2 = filter2

    def check(self,comment):
        self.filter1.check(comment) and self.filter2.check(comment)

class OrFilter(Filter):
    def __init__(self,filter1,filter2) -> None:
        self.filter1 = filter1
        self.filter2 = filter2

    def check(self,comment):
        self.filter1.check(comment) or self.filter2.check(comment)

# ---------- Singleton Comment Manager ---------- 
class AmazonCommentManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AmazonCommentManager,cls).__new__(cls)
            cls._instance.comments = []
        return cls._instance

    def add_comment(self, username,text):
        comment = Comment(username,text)
        self.comments.append(comment)

    def get_comments(self,filter_obj = None,sorting_strategy = None):
        result = self.comments 

        #apply filtering
        if filter_obj:
            result = [c for c in result if filter_obj.check(c)]

        if sorting_strategy:
            result = sorting_strategy.sort(result)

        return result
    
# ---------- Example Usage ----------
if __name__ == "__main__":
    print("Running Tests for AmazonCommentManager")

    # Singleton Test
    print("\nTesting Singleton...")
    m1 = AmazonCommentManager()
    m2 = AmazonCommentManager()
    assert m1 is m2, "Singleton test failed: Multiple instances created."

    # Clear any previous comments
    m1.comments.clear()

    # Add Comments
    print("\nAdding Comments...")
    m1.add_comment("JohnDoe", "These are great headphones!")
    m1.add_comment("SarahK", "Battery life could be better.")
    m1.add_comment("JohnDoe", "Great value and sound quality.")
    m1.add_comment("EmilyZ", "Poor build quality.")
    m1.add_comment("MikeR", "Sound quality is amazing!")

    # Upvote some comments
    print("\nUpvoting Comments...")
    m1.comments[0].up_vote()
    m1.comments[0].up_vote()
    m1.comments[2].up_vote()
    m1.comments[4].up_vote()
    m1.comments[4].up_vote()
    m1.comments[4].up_vote()

    print("Votes:")
    for c in m1.comments:
        print(f"{c.username}: {c.votes} votes - {c.text}")

    # Username Filter Test
    print("\nFiltering by Username 'JohnDoe'...")
    username_filter = UsernameFilter("JohnDoe")
    john_comments = m1.get_comments(filter_obj=username_filter)
    for c in john_comments:
        print(c)
    assert all("JohnDoe" in c.username for c in john_comments)

    # Keyword Filter Test
    print("\nFiltering by Keyword 'quality'...")
    keyword_filter = KeywordFilter("quality")
    quality_comments = m1.get_comments(filter_obj=keyword_filter)
    for c in quality_comments:
        print(c)
    assert all("quality" in c.text.lower() for c in quality_comments)

    # AND Filter
    print("\nAND Filter (JohnDoe AND 'quality')...")
    and_filter = AndFilter(username_filter, keyword_filter)
    combined = m1.get_comments(filter_obj=and_filter)
    for c in combined:
        print(c)
    assert all("JohnDoe" in c.username and "quality" in c.text.lower() for c in combined)

    # OR Filter
    print("\nOR Filter (JohnDoe OR 'quality')...")
    or_filter = OrFilter(username_filter, keyword_filter)
    combined = m1.get_comments(filter_obj=or_filter)
    for c in combined:
        print(c)
    assert all("JohnDoe" in c.username or "quality" in c.text.lower() for c in combined)

    # Sort by Votes Descending
    print("\nSort by Votes (Descending)...")
    sorted_by_votes = m1.get_comments(sorting_strategy=VoteSorting(ascending=False))
    for c in sorted_by_votes:
        print(c)
    assert sorted_by_votes == sorted(sorted_by_votes, key=lambda x: x.votes, reverse=True)

    # Sort by Date Ascending
    print("\nSort by Date (Ascending)...")
    sorted_by_date = m1.get_comments(sorting_strategy=DateSorting(ascending=True))
    for c in sorted_by_date:
        print(c)
    assert sorted_by_date == sorted(sorted_by_date, key=lambda x: x.date_posted)

    # Combined Filter + Sort
    print("\nFilter (quality) + Sort by Votes...")
    final = m1.get_comments(filter_obj=keyword_filter, sorting_strategy=VoteSorting(False))
    for c in final:
        print(c)

    print("\nAll tests completed.")
