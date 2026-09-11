from django.core.management.base import BaseCommand
from library.models import Author, AuthorProfile, Category, Publisher, Book, Publication


class Command(BaseCommand):
    help = 'Load test data for the library project'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading test data...')

        # Categories
        categories_data = [
            ('Fiction', 'Novels and fictional works'),
            ('Science', 'Scientific literature'),
            ('History', 'Historical documents and analyses'),
        ]
        categories = []
        for name, desc in categories_data:
            cat, created = Category.objects.get_or_create(name=name, defaults={'description': desc})
            if created:
                self.stdout.write(f'  Created Category: {name}')
            else:
                self.stdout.write(f'  Found Category: {name}')
            categories.append(cat)

        # Authors
        author_data = [
            ('Gabriel', 'García Márquez', '1927-03-06', 'Colombian novelist, Nobel Prize winner'),
            ('George', 'Orwell', '1903-06-25', 'English novelist and essayist'),
        ]
        authors = []
        for first, last, dob, bio in author_data:
            author, created = Author.objects.get_or_create(
                first_name=first,
                last_name=last,
                defaults={'date_of_birth': dob, 'biography': bio}
            )
            if created:
                self.stdout.write(f'  Created Author: {first} {last}')
                # Create profile
                AuthorProfile.objects.get_or_create(
                    author=author,
                    defaults={
                        'email': f'{first.lower()}@example.com',
                        'phone_number': '+1234567890',
                        'website': f'https://{first.lower()}-{last.lower()}.example.com',
                    }
                )
                self.stdout.write(f'    Created Profile for {first} {last}')
            else:
                self.stdout.write(f'  Found Author: {first} {last}')
                if not AuthorProfile.objects.filter(author=author).exists():
                    AuthorProfile.objects.get_or_create(
                        author=author,
                        defaults={
                            'email': f'{first.lower()}@example.com',
                            'phone_number': '+1234567890',
                        }
                    )
                    self.stdout.write(f'    Created Profile for {first} {last}')
            authors.append(author)

        # Publishers
        publisher_data = [
            ('Penguin Books', 'London, UK', 'https://www.penguin.com'),
            ('HarperCollins', 'New York, USA', 'https://www.harpercollins.com'),
        ]
        publishers = []
        for name, addr, site in publisher_data:
            pub, created = Publisher.objects.get_or_create(
                name=name,
                defaults={'address': addr, 'website': site}
            )
            if created:
                self.stdout.write(f'  Created Publisher: {name}')
            else:
                self.stdout.write(f'  Found Publisher: {name}')
            publishers.append(pub)

        # Books
        books_data = [
            ('One Hundred Years of Solitude', '9780060883287', '1967-05-30', authors[0], [categories[0], categories[2]]),
            ('Love in the Time of Cholera', '9780307389732', '1985-09-01', authors[0], [categories[0]]),
            ('1984', '9780451524935', '1949-06-08', authors[1], [categories[0], categories[1]]),
            ('Animal Farm', '9780451526342', '1945-08-17', authors[1], [categories[0], categories[2]]),
        ]
        books = []
        for title, isbn, pub_date, author, cats in books_data:
            book, created = Book.objects.get_or_create(
                isbn=isbn,
                defaults={'title': title, 'publication_date': pub_date, 'author': author}
            )
            if created:
                self.stdout.write(f'  Created Book: {title}')
            else:
                self.stdout.write(f'  Found Book: {title}')
            book.categories.set(cats)
            books.append(book)

        # Publications (Book-Publisher intermediate)
        publications_data = [
            (books[0], publishers[0], '1970-01-01', '1st Edition'),
            (books[1], publishers[0], '1988-01-01', '2nd Edition'),
            (books[2], publishers[1], '1950-01-01', '1st US Edition'),
            (books[2], publishers[0], '1951-01-01', 'UK Edition'),
            (books[3], publishers[1], '1946-01-01', '1st Edition'),
        ]
        for book, publisher, pub_date, edition in publications_data:
            pub, created = Publication.objects.get_or_create(
                book=book,
                publisher=publisher,
                defaults={'publication_date': pub_date, 'edition': edition}
            )
            if created:
                self.stdout.write(f'  Created Publication: {book} - {publisher} ({edition})')
            else:
                self.stdout.write(f'  Found Publication: {book} - {publisher} ({edition})')

        self.stdout.write(self.style.SUCCESS('Test data loaded successfully!'))
        self.stdout.write('\n=== SUMMARY ===')
        self.stdout.write(f'  Authors: {Author.objects.count()}')
        self.stdout.write(f'  Author Profiles: {AuthorProfile.objects.count()}')
        self.stdout.write(f'  Categories: {Category.objects.count()}')
        self.stdout.write(f'  Publishers: {Publisher.objects.count()}')
        self.stdout.write(f'  Books: {Book.objects.count()}')
        self.stdout.write(f'  Publications: {Publication.objects.count()}')
