import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from library.models import Author, Book

print("\n" + "="*70)
print("  STEP 10 - DELETE BEHAVIOR DEMONSTRATION")
print("="*70)

print("\n--- Model Definition ---")
print("Book.author field: ForeignKey(Author, on_delete=models.CASCADE, related_name='books')")
print("\nMeaning: When an Author is deleted, ALL their Books are ALSO deleted (CASCADE)")

print("\n" + "-"*70)
print("BEFORE DELETE - Current data:")
print("-"*70)
print(f"Total Authors: {Author.objects.count()}")
print(f"Total Books: {Book.objects.count()}")
print("\nAuthors:")
for a in Author.objects.all():
    print(f"  - {a} ({a.books.count()} books)")

print("\n" + "="*70)
print("  TEST 1: Default on_delete=CASCADE")
print("="*70)
print("\nAttempting to delete author: George Orwell")
print("(Author has 2 books: '1984' and 'Animal Farm')")

author_to_delete = Author.objects.get(first_name="George", last_name="Orwell")
print(f"\nBooks before delete:")
for b in author_to_delete.books.all():
    print(f"  - {b.title}")

try:
    author_to_delete.delete()
    print(f"\n[OK] Author '{author_to_delete}' DELETED successfully (CASCADE)")
    print(f"  Remaining Authors: {Author.objects.count()}")
    print(f"  Remaining Books: {Book.objects.count()}")
    print(f"\nBooks remaining:")
    for b in Book.objects.all():
        print(f"  - {b.title} (by {b.author})")
except Exception as e:
    print(f"\n[ERR] Error: {e}")

print("\n" + "="*70)
print("  TEST 2: Switching to on_delete=PROTECT")
print("="*70)
print("\nNow we demonstrate what happens if on_delete=PROTECT was used:")
print("(PROTECT prevents deletion of Authors that have associated books)")

print("\n--- PROTECT Behavior (simulated explanation) ---")
print("If Book.author had on_delete=models.PROTECT:")
current_author = Author.objects.first()
if current_author:
    print(f"  Attempting to delete '{current_author}' (has {current_author.books.count()} books)...")
    print("  Result: django.db.models.ProtectedError exception")
    print("  Message: Cannot delete some instances of model 'Author' because they are")
    print("           related to a model 'Book' through the 'author' foreign key.")
    print("  The author would NOT be deleted.")

print("\n" + "="*70)
print("  COMPARISON TABLE")
print("="*70)
print("""
+-----------------+--------------------------------------------------+--------------------------------------------------+
| on_delete       | What happens when author is deleted?              | Can you delete the author?                       |
+-----------------+--------------------------------------------------+--------------------------------------------------+
| CASCADE         | Author AND all their books are permanently deleted| YES - cascading delete                           |
+-----------------+--------------------------------------------------+--------------------------------------------------+
| PROTECT         | Raises ProtectedError - nothing is deleted         | NO - blocks the deletion                         |
+-----------------+--------------------------------------------------+--------------------------------------------------+
| SET_NULL        | Books remain but author_id is set to NULL          | YES - books become authorless (if null=True)     |
+-----------------+--------------------------------------------------+--------------------------------------------------+
| RESTRICT        | Like PROTECT but checked at save time              | NO - blocks until all related books are removed  |
+-----------------+--------------------------------------------------+--------------------------------------------------+

CHOOSE BASED ON YOUR NEEDS:
- CASCADE: When books shouldn't exist without an author
- PROTECT: When you need to manually reassign books before deleting an author
- SET_NULL: When books might be authorless during transitions

OBSERVATION:
With CASCADE (current implementation), George Orwell and his 2 books (1984, Animal Farm)
were permanently deleted when we deleted the author record.
With PROTECT, the deletion would have been blocked entirely, requiring manual intervention.
""")

print("="*70)
print("  DEMO COMPLETE - Author data after tests:")
print("="*70)
print(f"Total Authors: {Author.objects.count()}")
for a in Author.objects.all():
    print(f"  - {a} ({a.books.count()} books)")
