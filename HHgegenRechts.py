class EventHHgegenRechts:
    def __init__(self, title, time, link, description, categories):
        self.title = title
        self.time = time
        self.link = link
        self.description = description
        self.categories = categories

    def __str__(self):
        return f'Event(title={self.title}, time={self.time}, link={self.link}, description={self.description}, categories={self.categories})'
    
    
