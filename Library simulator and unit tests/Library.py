# Melissa J Johnson
# 04/20/2021
# CS162 Project 3
# Library simulator containing the following classes: LibraryItem, Patron, and Library.
# LibraryItem has subclasses Book, Movie, and Album.
# Patrons of the Library can check out LibraryItems as one would in a normal library. The Library
# class keeps track of most of the logic such as checking out/requesting/returning a LibraryItem,
# adding items and patrons to the Library, and paying fines.

class LibraryItem:
    """ Represents a LibraryItem"""
    ON_SHELF = "ON_SHELF"
    ON_HOLD_SHELF = "ON_HOLD_SHELF"
    CHECKED_OUT = "CHECKED_OUT"

    def __init__(self, library_item_id, title):
        """
        Initializes a LibraryItem object with ID and title.
        A new LibraryItem's location is on the shelf.
        :param library_item_id: library item ID, unique identifier
        :param title: title, cannot be assumed to be unique
        """
        self._library_item_id = library_item_id
        self._title = title
        self._checked_out_by = None
        self._requested_by = None
        self._location = LibraryItem.ON_SHELF
        self._date_checked_out = 0

    def get_library_item_id(self):
        """return: LibraryItem ID """
        return self._library_item_id

    def get_title(self):
        """returns title"""
        return self._title

    def get_location(self):
        """returns location of item"""
        return self._location

    def get_checked_out_by(self):
        """returns patron ID of who checked out item"""
        return self._checked_out_by

    def get_requested_by(self):
        """returns patron ID of who requested item"""
        return self._requested_by

    def get_date_checked_out(self):
        """returns date on how long item has been checked out"""
        return self._date_checked_out

    def set_location(self, location):
        """ set new location of Library Item """
        self._location = location

    def set_checked_out_by(self, patron_id):
        """ set patron that checked out item """
        self._checked_out_by = patron_id

    def set_requested_by(self, patron_id):
        """ set patron who requested item """
        self._requested_by = patron_id

    def set_date_checked_out(self, date):
        """ set date when library item is checked out """
        self._date_checked_out = date


class Book(LibraryItem):
    """
    Book inherits from/is a subclass of LibraryItem.
    """

    def __init__(self, library_item_id, title, author):
        """initializes book object"""
        super().__init__(library_item_id, title)
        self._author = author

    def get_author(self):
        """ returns author of book"""
        return self._author

    def get_check_out_length(self):
        """ A book can be checked out for 21 days """
        return 21


class Album(LibraryItem):
    """ Album is a type of LibraryItem """

    def __init__(self, library_item_id, title, artist):
        """ Constructor for Album subclass """
        super().__init__(library_item_id, title)
        self._artist = artist

    def get_artist(self):
        """ returns artist of Album """
        return self._artist

    def get_check_out_length(self):
        """ Returns allowable checkout length for an album"""
        return 14


class Movie(LibraryItem):
    """Movie is a type of LibraryItem """

    def __init__(self, library_item_id, title, director):
        """ Constructor for Movie subclass"""
        super().__init__(library_item_id, title)
        self._director = director

    def get_director(self):
        """ returns director """
        return self._director

    def get_check_out_length(self):
        """returns allowable time Movie can be checked out"""
        return 7


class Patron:
    """represents a Patron"""
    def __init__(self, patron_id, name):
        """Constructor for Patron class. """
        self._patron_id = patron_id
        self._name = name
        self._checked_out_items = []
        self._fine_amount = 0

    def get_patron_id(self):
        """ returns ID of patron """
        return self._patron_id

    def get_name(self):
        """returns patron's name """
        return self._name

    def get_fine_amount(self):
        """ returns fine amount """
        return self._fine_amount

    def get_checked_out_items(self):
        """ returns a copy of the list of checked out items"""
        return list(self._checked_out_items)

    def add_library_item(self, library_item):
        """ adds library_item to checked_out_items """
        self._checked_out_items.append(library_item)

    def remove_library_item(self, library_item):
        """ removes a library item from checked_out_items"""
        self._checked_out_items.remove(library_item)

    def amend_fine(self, fine):
        """ amends fine """
        self._fine_amount += fine


class Library:
    """ Library which holds a collection of LibraryItems and members of the library"""

    def __init__(self):
        """
        Constructor for Library class. The library is represented by a dictionary of items (holdings)
        and a dictionary of members. A Library object will have a current date initialized to zero.
        """
        self._holdings = {} #key: library_item_id, value: libraryitem object
        self._members = {} #key: patronID, value: patron object
        self._current_date = 0

    def add_library_item(self, library_item):
        """
        Adds Library Item object as item to Library's holdings.
        :param library_item: library item to be added
        """
        self._holdings[library_item.get_library_item_id()] = library_item

    def add_patron(self, patron):
        """
        Adds patron to Library. Patron ID is key and patron object is value.
        """
        self._members[patron.get_patron_id()] = patron

    def lookup_library_item_from_id(self, library_item_id):
        """
        Returns LibraryItem object corresponding to the ID parameter.
        Returns None if no such libraryItem is in the holdings.
        """
        return self._holdings.get(library_item_id)

    def lookup_patron_from_id(self, patron_id):
        """
        Returns Patron object corresponding to the ID parameter.
        Returns none if Patron_ID isn't in dictionary of members.
        """
        return self._members.get(patron_id)

    def check_out_library_item(self, patron_id, library_item_id):
        """
        Checks out LibraryItem if patron is a member and LibraryItem is available.
        :return: returns that the patron wasn't found, the library item wasn't found,
                that the item is already checked out, or that it's on hold by another patron.
        """
        patron = self.lookup_patron_from_id(patron_id) #retrieve patron object

        if not patron:
            return "patron not found"

        library_item = self.lookup_library_item_from_id(library_item_id)

        if not library_item:
            return "item not found"

        if library_item.get_location() == LibraryItem.CHECKED_OUT:
            return "item already checked out"

        if library_item.get_location() == LibraryItem.ON_HOLD_SHELF and library_item.get_requested_by() != patron:
            return "item on hold by other patron"

        if library_item.get_location() == LibraryItem.ON_HOLD_SHELF and library_item.get_requested_by() == patron: #if the same patron who requested item is checking out item
            library_item.set_requested_by(None)

        library_item.set_checked_out_by(patron)
        library_item.set_date_checked_out(patron)
        library_item.set_date_checked_out(self._current_date)
        library_item.set_location(LibraryItem.CHECKED_OUT)

        patron.add_library_item(library_item)

        return "check out successful"

    def return_library_item(self, library_item_id):
        """
        Returns LibraryItem, updates LibraryItem's location
        """
        library_item = self.lookup_library_item_from_id(library_item_id)

        if not library_item:
            return "item not found"

        if library_item.get_location() != LibraryItem.CHECKED_OUT:
            return "item already in library"

        patron = library_item.get_checked_out_by() #in order to remove the library item, we retrieve the patron by calling the method 'get_checked_out_by' on the library_item
        patron.remove_library_item(library_item)

        if library_item.get_requested_by() is not None:
            library_item.set_location(LibraryItem.ON_HOLD_SHELF)
        else:
            library_item.set_location(LibraryItem.ON_SHELF)

        library_item.set_checked_out_by(None)
        return "return successful"

    def request_library_item(self, patron_id, library_item_id):
        """ Function to request LibraryItem if patron is a member and LibraryItem is available"""

        patron = self.lookup_patron_from_id(patron_id)
        if not patron:
            return "patron not found"

        library_item = self.lookup_library_item_from_id(library_item_id)
        if not library_item:
            return "item not found"

        if library_item.get_requested_by() is not None:
            return "item already on hold"

        library_item.set_requested_by(patron)

        if library_item.get_location() == LibraryItem.ON_SHELF:
            library_item.set_location(LibraryItem.ON_HOLD_SHELF)
        return "request successful"

    def pay_fine(self, patron_id, amount):
        """
        Function for patron to pay fine.
        """
        patron = self.lookup_patron_from_id(patron_id)
        if not patron:
            return "patron not found"

        patron.amend_fine(-amount)
        return "payment successful"

    def increment_current_date(self):
        # increment current date
        self._current_date += 1

        for patron in self._members.values(): #note to self: iterate through dictionary values with .values(). Without it, you'll iterate through keys.
            for library_item in patron.get_checked_out_items():
                if(self._current_date - library_item.get_date_checked_out()) > library_item.get_check_out_length():
                    patron.amend_fine(0.1)
                continue


if __name__ == '__main__':
    b1 = Book("345", "Phantom Tollbooth", "Juster")
    a1 = Album("456", "...And His Orchestra", "The Fastbacks")
    m1 = Movie("567", "Laputa", "Miyazaki")
    print(b1.get_author())
    print(a1.get_artist())
    print(m1.get_director())

    p1 = Patron("abc", "Felicity")
    p2 = Patron("bcd", "Waldo")

    lib = Library()
    lib.add_library_item(b1)
    lib.add_library_item(a1)
    lib.add_patron(p1)
    lib.add_patron(p2)

    lib.check_out_library_item("bcd", "456")
    loc = a1.get_location()
    lib.request_library_item("abc", "456")
    for i in range(57):
        lib.increment_current_date()  # 57 days pass
    p2_fine = p2.get_fine_amount()
    print(lib.pay_fine("bcd", p2_fine))
    print(lib.return_library_item("456"))
    print(p1.get_fine_amount())








