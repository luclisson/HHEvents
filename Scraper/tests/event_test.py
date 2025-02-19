import pytest
from datetime import datetime
import sys
import os

# Add the parent folder (Scraper) to the search path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
from event import Event

def test_event_initialization():
    event = Event(
        source_url="https://example.com",
        title="Test Event",
        link="https://example.com/event",
        event_date="01.03.2025",
        time="20:00",
        category="Test Category",
        location="Test Location",
        price="10.50€",
        img_url="https://example.com/image.jpg"
    )
    
    assert event.source_url == "https://example.com"
    assert event.title == "Test Event"
    assert event.link == "https://example.com/event"
    assert event.event_date == "01.03.2025"  # German date format
    assert event.time == "20:00"
    assert event.category == "Test Category"
    assert event.location == "Test Location"
    assert event.price == 10.50
    assert event.img_url == "https://example.com/image.jpg"

def test_date_time_parsing():
    # Test with combined date-time string
    event1 = Event(
        source_url="", 
        title="", 
        link="", 
        event_date="01.03.2025 20:30",  # German format with time
        time="", 
        category="", 
        location=""
    )
    
    # Test ISO format with time
    event2 = Event(
        source_url="", 
        title="", 
        link="", 
        event_date="2025-03-01T20:30", 
        time="", 
        category="", 
        location=""
    )
    
    assert event1.event_date == "01.03.2025"
    assert event1.time == "20:30"  # Time should be extracted
    
    assert event2.event_date == "01.03.2025"
    assert event2.time == "20:30"  # Time should be extracted

def test_price_parsing():
    event1 = Event(
        source_url="", 
        title="", 
        link="", 
        event_date="", 
        time="", 
        category="", 
        location="", 
        price="10.50€"
    )
    event2 = Event(
        source_url="", 
        title="", 
        link="", 
        event_date="", 
        time="", 
        category="", 
        location="", 
        price="10,50 EUR"
    )
    event3 = Event(
        source_url="", 
        title="", 
        link="", 
        event_date="", 
        time="", 
        category="", 
        location="", 
        price=None
    )
    
    assert event1.price == 10.50
    assert event2.price == 10.50
    assert event3.price is None

def test_to_dict():
    event = Event(
        source_url="https://example.com",
        title="Test Event",
        link="https://example.com/event",
        event_date="01.03.2025",
        time="20:00",
        category="Test Category",
        location="Test Location",
        price="10.50€",
        img_url="https://example.com/image.jpg"
    )
    event_dict = event.to_dict()
    
    assert isinstance(event_dict, dict)
    assert event_dict['event_date'] == "01.03.2025"
    assert event_dict['time'] == "20:00"
    assert event_dict['price'] == 10.50

def test_event_equality():
    event1 = Event(
        source_url="", 
        title="Event", 
        link="https://example.com", 
        event_date="01.03.2025", 
        time="20:00", 
        category="", 
        location=""
    )
    event2 = Event(
        source_url="", 
        title="Event", 
        link="https://example.com", 
        event_date="01.03.2025", 
        time="20:00", 
        category="", 
        location=""
    )
    event3 = Event(
        source_url="", 
        title="Different Event", 
        link="https://example.com", 
        event_date="02.03.2025", 
        time="21:00", 
        category="", 
        location=""
    )
    
    assert event1 == event2
    assert event1 != event3

def test_time_parsing_edge_cases():
    # Test time without leading zero
    event1 = Event(
        source_url="", 
        title="", 
        link="", 
        event_date="01.03.2025 9:30", 
        time="", 
        category="", 
        location=""
    )
    
    # Test midnight
    event2 = Event(
        source_url="", 
        title="", 
        link="", 
        event_date="01.03.2025 00:00", 
        time="", 
        category="", 
        location=""
    )
    
    assert event1.time == "09:30"  # Leading zero added
    assert event2.time == "00:00"

if __name__ == "__main__":
    pytest.main()
