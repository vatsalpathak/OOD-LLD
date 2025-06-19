# Question
# Design a simplified Browser History Manager.
#
# Your system should:
# - Allow visiting a new URL.
# - Allow going back and forward through the history (like a real browser).
#
# Constraints:
# - Going back or forward should update the current page pointer.
# - Visiting a new URL should erase all forward history.
#
# Think about:
# - How to store history.
# - How to manage the current position.
# - Which data structures to use for efficient navigation.

class BrowserHistory:
    def __init__(self, url) -> None:
        self.current = url
        self.prev = []
        self.forward = []

    def visit(self, url):
        self.prev.append(self.current)
        self.current = url
        self.forward.clear()

    def back(self):
        if not self.prev:
            return "No previous page"
        self.forward.append(self.current)
        self.current = self.prev.pop()
        return self.current
        
    def forward_page(self):
        if not self.forward:
            return "No forward page"
        self.prev.append(self.current)
        self.current = self.forward.pop()
        return self.current
        
    def get_current_page(self):
        return self.current
    

if __name__ == "__main__":
    bh = BrowserHistory("google.com")
    print(bh.get_current_page())  # google.com

    bh.visit("github.com")
    bh.visit("stackoverflow.com")
    print(bh.get_current_page())  # stackoverflow.com

    print(bh.back())              # github.com
    print(bh.back())              # google.com
    print(bh.forward_page())      # github.com

    bh.visit("openai.com")
    print(bh.forward_page())      # No forward page
    print(bh.get_current_page())  # openai.com
