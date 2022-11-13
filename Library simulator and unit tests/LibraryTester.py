# Melissa J Johnson
# 04/17/2021
# Project 3
# Unittest code for Library.py

import unittest

from Library import LibraryItem, Book, Movie, Album, Patron, Library

class LibraryItemTests(unittest.TestCase):
    """Unit tests for LibraryItem"""
    def test_library_item_init(self):
        """ Tests initializer of LibraryItem class"""
        library_item = LibraryItem("456", "See Spot")

        self.assertEqual("456", library_item.get_library_item_id())
        self.assertEqual("See Spot", library_item.get_title())


class BookTests(unittest.TestCase):
    """ Unit tests for Book subclass"""
    def test_book_subclass_init(self):
        """ tests initializer """
        book = Book("456", "See Spot Run", "John Smith")
        self.assertEqual("456", book.get_library_item_id())
        self.assertEqual("See Spot Run", book.get_title())
        self.assertEqual("John Smith", book.get_author())

    def test_get_book_check_out_length(self):
        """ tests get_book_check_out_length """
        book = Book("456", "See Spot Run", "John Smith")
        self.assertEqual(21, book.get_check_out_length())

class AlbumTests(unittest.TestCase):
    """ unit tests for Album subclass """
    def test_album_init(self):
        """ tests initializer for Album subclass """
        album = Album("123", "Evening Jamz", "Spotify")
        self.assertEqual("123", album.get_library_item_id())
        self.assertEqual("Evening Jamz", album.get_title())
        self.assertEqual("Spotify", album.get_artist())

    def test_album_get_check_out_length(self):
        """ tests get_check_out_length for album """
        album = Album("123", "Evening Jamz", "Spotify")
        self.assertEqual(14, album.get_check_out_length())


class MovieTests(unittest.TestCase):
    """
    Unit tests for Movie subclass
    """
    def test_movie_init(self):
        """ tests Movie initializer """
        movie = Movie("1256", "North by Northwest", "Hitchcock")
        self.assertEqual("1256", movie.get_library_item_id())
        self.assertEqual("North by Northwest", movie.get_title())
        self.assertEqual("Hitchcock", movie.get_director())

    def test_movie_get_check_out_length(self):
        """Tests check out length allowed for movie. """
        movie = Movie("1256", "North by Northwest", "Hitchcock")
        self.assertEqual(7, movie.get_check_out_length())


class PatronTests(unittest.TestCase):
    """
    Unit tests for Patron class.
    """
    def test_patron_init(self):
        """ Tests Patron initializer """
        patron = Patron("abc", "Melissa")
        self.assertEqual("abc", patron.get_patron_id())
        self.assertEqual("Melissa", patron.get_name())

    def test_get_checked_out_items(self):
        """ Tests that get_checked_out_items retrieves expected results """
        patron = Patron("abc", "Melissa")
        book1 = Book("456", "See Spot Run", "John Smith")
        book2 = Book("789", "See Spot Run Faster", "John Smith")

        self.assertListEqual([], patron.get_checked_out_items())
        patron.add_library_item(book1)
        self.assertListEqual([book1], patron.get_checked_out_items())

        patron.add_library_item(book2)
        self.assertListEqual([book1, book2], patron.get_checked_out_items())

    def test_add_library_item(self):
        """tests if LibraryItem is added to checked out items"""
        patron = Patron("cde", "Muhlissa")
        book1 = Book("456", "See Spot Run", "John Smith")
        movie1 = Movie("1256", "North by Northwest", "Hitchcock")

        self.assertListEqual([], patron.get_checked_out_items())
        patron.add_library_item(book1)

        self.assertNotEqual([], patron.get_checked_out_items())
        self.assertListEqual([book1], patron.get_checked_out_items())

        patron.add_library_item(movie1)

        self.assertListEqual([book1, movie1], patron.get_checked_out_items())

    def test_remove_library_item(self):
        """Tests if a LibraryItem is removed from checked out items"""
        patron = Patron("cde", "Muhlissa")
        book1 = Book("456", "See Spot Run", "John Smith")
        movie1 = Movie("1256", "North by Northwest", "Hitchcock")

        self.assertListEqual([], patron.get_checked_out_items())

        patron.add_library_item(book1)
        patron.add_library_item(movie1)
        self.assertListEqual([book1, movie1], patron.get_checked_out_items())

        patron.remove_library_item(book1)

        self.assertListEqual([movie1], patron.get_checked_out_items())

    def test_amend_fine(self):
        patron = Patron("cde", "Muhlissa")
        fine = 1

        self.assertEqual(0, patron.get_fine_amount())
        patron.amend_fine(fine)

        self.assertEqual(1, patron.get_fine_amount())


class LibraryTests(unittest.TestCase):
    """ Unit test for Library class """

    def test_add_library_and_lookup_library_item_from_id(self):
        """Tests that a LibraryItem is added to the Library's holdings"""
        library = Library()

        book1 = Book("456", "See Spot Run", "John Smith")
        movie1 = Movie("1256", "North by Northwest", "Hitchcock")

        found_library_item = library.lookup_library_item_from_id("1256")
        self.assertIsNone(found_library_item)
        library.add_library_item(movie1)
        found_library_item = library.lookup_library_item_from_id("1256")
        self.assertEqual(movie1, found_library_item)

        found_library_item = library.lookup_library_item_from_id("456")
        self.assertIsNone(found_library_item)
        library.add_library_item(book1)
        found_library_item = library.lookup_library_item_from_id("456")
        self.assertEqual(found_library_item, book1)

    def test_add_patron(self):
        """ Tests that a patron is added to the Library"""
        library = Library()

        patron = Patron("abc", "Mel")
        patron2 = Patron("1234", "Jay")

        found_patron = library.lookup_patron_from_id("abc")
        self.assertIsNone(found_patron)
        library.add_patron(patron)
        found_patron = library.lookup_patron_from_id("abc")
        self.assertEqual(patron, found_patron)

        found_patron = library.lookup_patron_from_id("1234")
        self.assertIsNone(found_patron)
        library.add_patron(patron2)
        found_patron = library.lookup_patron_from_id("1234")
        self.assertEqual(found_patron, patron2)


    def test_check_out_library_item_when_patron_not_found(self):
        """Tests checkout if patron is not found"""
        library = Library()
        checkout_result = library.check_out_library_item("abc", "1256")
        self.assertEqual(checkout_result, "patron not found")


    def test_check_out_library_item_when_item_not_found(self):
        """Tests checkout if library item is not found"""
        library = Library()
        patron = Patron("abc", "Melissa")

        library.add_patron(patron)
        checkout_results = library.check_out_library_item("abc", "1256")

        self.assertEqual(checkout_results, "item not found")


    def test_check_out_library_item_when_item_is_available(self):
        """ Tests checkout if LibraryItem is not on hold"""
        library = Library()
        patron = Patron("abc", "Mel")
        movie = Movie("1256", "North by Northwest", "Hitchcock")
        library.add_patron(patron)
        library.add_library_item(movie)

        checkout_result = library.check_out_library_item("abc", "1256")

        self.assertEqual(checkout_result, "check out successful")
        self.assertEqual(patron, movie.get_checked_out_by())
        self.assertEqual(0, movie.get_date_checked_out())
        self.assertEqual(LibraryItem.CHECKED_OUT, movie.get_location())
        self.assertListEqual([movie], patron.get_checked_out_items())

    def test_check_out_when_item_is_on_hold_by_same_patron_who_is_checking_out(self):
        """Tests checkout when item is hold by same patron who is checking out"""
        library = Library()

        patron = Patron("abc", "Mel")
        movie = Movie("1256", "North by Northwest", "Hitchcock")
        library.add_patron(patron)
        library.add_library_item(movie)

        requested_library_item = library.request_library_item("abc", "1256")

        self.assertEqual("request successful", requested_library_item)
        self.assertEqual(LibraryItem.ON_HOLD_SHELF, movie.get_location())
        self.assertEqual(patron, movie.get_requested_by())

        checkout_result = library.check_out_library_item("abc", "1256")

        self.assertEqual(checkout_result, "check out successful")
        self.assertEqual(patron, movie.get_checked_out_by())
        self.assertEqual(0, movie.get_date_checked_out())
        self.assertIsNone(movie.get_requested_by())
        self.assertEqual(LibraryItem.CHECKED_OUT, movie.get_location())
        self.assertListEqual([movie], patron.get_checked_out_items())

    def test_check_out_library_item_when_item_already_checked_out(self):
        """
        Function to test checking out a LibraryItem when it's alreayd checked out.
        """
        library = Library()
        patron1 = Patron("abc", "Mel")
        patron2 = Patron("meow", "Mora")
        book = Book("2750", "Tiny Hats for Cats", "Someone")
        library.add_patron(patron1)
        library.add_patron(patron2)
        library.add_library_item(book)

        patron1_checkout_result = library.check_out_library_item("meow", "2750")
        self.assertEqual("check out successful", patron1_checkout_result)

        patron2_checkout_result = library.check_out_library_item("abc", "2750")
        self.assertEqual(patron2_checkout_result, "item already checked out")

    def test_return_library_item_when_not_on_hold_by_another_patron(self):
        library = Library()
        patron1 = Patron("abc", "Mel")
        book = Book("2750", "Tiny Hats for Cats", "Someone")
        library.add_patron(patron1)
        library.add_library_item(book)

        checkout_result = library.check_out_library_item("abc", "2750")

        self.assertEqual(checkout_result, "check out successful")

        return_library_item_result = library.return_library_item("2750")

        self.assertEqual("return successful", return_library_item_result)
        self.assertEqual(LibraryItem.ON_SHELF, book.get_location())

    def test_return_library_item_when_on_hold_by_another_patron(self):
        """Tests trying to return a LibraryItem that's on hold by a different patron"""
        library = Library()
        patron1 = Patron("abc", "Mel")
        patron2 = Patron("meow", "Mora")
        book = Book("2750", "Tiny Hats for Cats", "Someone")
        library.add_patron(patron1)
        library.add_patron(patron2)
        library.add_library_item(book)

        checkout_result = library.check_out_library_item("abc", "2750")

        self.assertEqual(checkout_result, "check out successful")

        request_library_item_result = library.request_library_item("meow", "2750")

        self.assertEqual(request_library_item_result, "request successful")

        return_library_item_result = library.return_library_item("2750")

        self.assertEqual("return successful", return_library_item_result)
        self.assertEqual(LibraryItem.ON_HOLD_SHELF, book.get_location())

    def test_return_library_item_when_item_not_found(self):
        """ Tests returning a LibraryItem that is not found"""
        library = Library()

        return_library_item_result = library.return_library_item("2750")

        self.assertEqual("item not found", return_library_item_result)

    def test_return_library_item_when_item_already_in_library(self):
        """ Tests returning a LibraryItem that's already in the library"""
        library = Library()
        book = Book("2750", "Tiny Hats for Cats", "Someone")
        library.add_library_item(book)

        return_library_item_result = library.return_library_item("2750")
        self.assertEqual("item already in library", return_library_item_result)

    def test_request_library_item_when_item_is_on_shelf(self):
        """ Tests requesting a LibraryItem when it is on the shelf"""
        library = Library()
        patron1 = Patron("abc", "Mel")
        book = Book("2750", "Tiny Hats for Cats", "Someone")
        library.add_patron(patron1)
        library.add_library_item(book)

        request_library_item_result = library.request_library_item("abc", "2750")

        self.assertEqual("request successful", request_library_item_result)
        self.assertEqual(LibraryItem.ON_HOLD_SHELF, book.get_location())
        self.assertEqual(patron1, book.get_requested_by())

    def test_request_library_item_when_item_is_checked_out(self):
        """tests requesting LibraryItem that is checked out"""
        library = Library()
        patron1 = Patron("abc", "Mel")
        book = Book("2750", "Tiny Hats for Cats", "Someone")
        library.add_patron(patron1)
        library.add_library_item(book)

        checkout_result = library.check_out_library_item("abc", "2750")
        self.assertEqual(checkout_result, "check out successful")

        request_library_item_result = library.request_library_item("abc", "2750")
        self.assertEqual(LibraryItem.CHECKED_OUT, book.get_location())
        self.assertEqual(patron1, book.get_requested_by())

    def test_request_library_item_when_item_not_found(self):
        """ Tests requesting LibraryItem when item isn't found"""
        library = Library()
        patron1 = Patron("abc", "Mel")
        library.add_patron(patron1)

        request_library_item_result = library.request_library_item("abc", "2750")

        self.assertEqual("item not found", request_library_item_result)

    def test_request_library_item_when_patron_is_not_found(self):
        """Tests requesting a LibraryItem if Patron is not found"""
        library = Library()
        book = Book("2750", "Tiny Hats for Cats", "Someone")

        request_library_item_result = library.request_library_item("abc", "2750")

        self.assertEqual("patron not found", request_library_item_result)

    def test_request_library_item_when_item_already_on_hold(self):
        """ Tests requesting LibraryItem that's on hold"""
        library = Library()
        patron1 = Patron("abc", "Mel")
        patron2 = Patron("meow", "Mora")
        book = Book("2750", "Tiny Hats for Cats", "Someone")
        library.add_patron(patron1)
        library.add_patron(patron2)
        library.add_library_item(book)

        patron1_request_library_item_result = library.request_library_item("abc", "2750")

        self.assertEqual("request successful", patron1_request_library_item_result)

        patron2_request_library_item_result = library.request_library_item("meow", "2750")

        self.assertEqual("item already on hold", patron2_request_library_item_result)

    def test_pay_fine_when_patron_is_not_found(self):
        """Tests paying a fine when the patron is not found"""
        library = Library()

        payment_result = library.pay_fine("abc", 10)

        self.assertEqual("patron not found", payment_result)

    def test_pay_fine(self):
        """Tests paying fine"""
        library = Library()
        patron1 = Patron("abc", "Mel")
        library.add_patron(patron1)

        payment_result = library.pay_fine("abc", 10)

        self.assertEqual("payment successful", payment_result)
        self.assertEqual(-10, patron1.get_fine_amount())

    def test_increment_current_date(self):
        library = Library()
        patron1 = Patron("abc", "Mel")
        patron2 = Patron("meow", "Mora")
        book = Book("2750", "Tiny Hats for Cats", "Someone") #adding elements to the library
        movie = Movie("1256", "North by Northwest", "Hitchcock") #adding elements to the library
        album = Album("009", "All Mirrors", "Angel Olsen") #adding elements to the library
        library.add_patron(patron1)
        library.add_patron(patron2)
        library.add_library_item(book)
        library.add_library_item(movie)
        library.add_library_item(album)

        patron1_checkout_result = library.check_out_library_item("abc", "1256") #patron1 checks out movie

        self.assertEqual(patron1_checkout_result, "check out successful") #checking out patron1
        self.assertEqual(0, patron1.get_fine_amount()) #checking that patron1's fine is 0 after checkout

        self._increment_library_date_by(library, 7) #increase the current date to check that amount owed by Patrons is properly increased
        self.assertEqual(0, patron1.get_fine_amount())

        self._increment_library_date_by(library, 1) # A movie can be checked out for 7 days before adding fine,
        # so this adds 1 day (making total 8 days) and checks that the amount due is correct
        self.assertAlmostEqual(0.1, patron1.get_fine_amount())

        patron1_checkout_result = library.check_out_library_item("abc", "009") #patron1 checking out another item (album)
        patron2_checkout_result = library.check_out_library_item("meow", "2750") #patron2 checks out (book)

        self.assertEqual(patron1_checkout_result, "check out successful") #Check that checkout was successful
        self.assertEqual(patron2_checkout_result, "check out successful") #Check that checkout was successful
        self.assertAlmostEqual(0.1, patron1.get_fine_amount()) #check to see that Patron1 still only owes fee from overdue movie
        self.assertEqual(0, patron2.get_fine_amount())

        self._increment_library_date_by(library, 14) #adding two weeks to date

        self.assertAlmostEqual(1.5, patron1.get_fine_amount()) #patron1's fine after 15 days overdue on movie
        self.assertEqual(0, patron2.get_fine_amount()) #patron2 checked out a book which is allowed 21 days before a late fee

        self._increment_library_date_by(library, 1)

        self.assertAlmostEqual(1.7, patron1.get_fine_amount()) #Patron1's fine after 16 days late on a movie and 1 day late on an album
        self.assertEqual(0, patron2.get_fine_amount())

        self._increment_library_date_by(library, 6)

        self.assertAlmostEqual(2.9, patron1.get_fine_amount()) #29 days overdue for Patron 1
        self.assertEqual(0, patron2.get_fine_amount()) #Patron 2 is at 21 days

        self._increment_library_date_by(library, 1) #day 22 for Patron2

        self.assertAlmostEqual(3.1, patron1.get_fine_amount())
        self.assertAlmostEqual(0.1, patron2.get_fine_amount()) #patron2 is one day overdue

        self._increment_library_date_by(library, 10)

        self.assertAlmostEqual(5.1, patron1.get_fine_amount())
        self.assertAlmostEqual(1.1, patron2.get_fine_amount())





    def _increment_library_date_by(self, library, num_days):
        """method to increase the library date for testing purposes"""
        for i in range(num_days):
            library.increment_current_date()



if __name__ == '__main__':
    unittest.main()
