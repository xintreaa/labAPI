// frontend/scripts/books.js
const API_URL = 'http://localhost:8000/api/books';

document.addEventListener('DOMContentLoaded', () => {
    fetchBooks();

    const form = document.getElementById('book-form');
    const cancelButton = document.getElementById('cancel-update');

    form.addEventListener('submit', handleSubmit);
    cancelButton.addEventListener('click', resetForm);
});

async function fetchBooks() {
    try {
        const response = await axios.get(API_URL, {
            headers: {
                'Access-Control-Allow-Origin': '*'
            }
        });
        const books = response.data;
        const tbody = document.getElementById('books-tbody');
        tbody.innerHTML = '';

        if (!Array.isArray(books)) {
            throw new Error('Unexpected response format: expected an array of books');
        }

        books.forEach(book => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${book.id || 'N/A'}</td>
                <td>${book.title || 'N/A'}</td>
                <td>${book.publication_year || 'N/A'}</td>
                <td>${book.isbn || 'N/A'}</td>
                <td>${book.quantity || 'N/A'}</td>
                <td>${book.authors && book.authors.length ? book.authors.map(a => a.first_name + ' ' + a.last_name).join(', ') : 'No authors'}</td>
                <td>${book.categories && book.categories.length ? book.categories.map(c => c.name).join(', ') : 'No categories'}</td>
                <td>${book.created_at ? new Date(book.created_at).toLocaleString() : 'N/A'}</td>
                <td>${book.updated_at ? new Date(book.updated_at).toLocaleString() : 'N/A'}</td>
                <td>
                    <button class="edit" onclick="editBook(${book.id || 0})">Edit</button>
                    <button class="delete" onclick="deleteBook(${book.id || 0})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching books:', {
            message: error.message,
            status: error.response?.status,
            data: error.response?.data,
            request: error.request
        });
        alert('Failed to fetch books: ' + (error.response?.data?.detail || error.message || 'Unknown error'));
    }
}

// Решта коду без змін...
async function handleSubmit(event) {
    event.preventDefault();

    const bookId = document.getElementById('book-id').value;
    const title = document.getElementById('title').value;
    const publicationYear = parseInt(document.getElementById('publication-year').value);
    const isbn = document.getElementById('isbn').value;
    const quantity = parseInt(document.getElementById('quantity').value);
    const authorIds = document.getElementById('author-ids').value.split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id));
    const categoryIds = document.getElementById('category-ids').value.split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id));

    const bookData = {
        title,
        publication_year: publicationYear,
        isbn,
        quantity,
        author_ids: authorIds,
        category_ids: categoryIds
    };

    try {
        if (bookId) {
            await axios.put(`${API_URL}/${bookId}`, bookData);
            alert('Book updated successfully');
        } else {
            await axios.post(API_URL, bookData);
            alert('Book created successfully');
        }
        resetForm();
        fetchBooks();
    } catch (error) {
        console.error('Error saving book:', error);
        alert(`Failed to save book: ${error.response?.data?.detail || error.message}`);
    }
}

async function editBook(id) {
    try {
        const response = await axios.get(`${API_URL}/${id}`);
        const book = response.data;

        document.getElementById('book-id').value = book.id;
        document.getElementById('title').value = book.title;
        document.getElementById('publication-year').value = book.publication_year;
        document.getElementById('isbn').value = book.isbn;
        document.getElementById('quantity').value = book.quantity;
        document.getElementById('author-ids').value = book.authors && book.authors.length ? book.authors.map(a => a.id).join(', ') : '';
        document.getElementById('category-ids').value = book.categories && book.categories.length ? book.categories.map(c => c.id).join(', ') : '';

        document.getElementById('form-title').textContent = 'Update Book';
        document.getElementById('cancel-update').style.display = 'inline';
    } catch (error) {
        console.error('Error fetching book:', error);
        alert('Failed to fetch book for editing');
    }
}

async function deleteBook(id) {
    if (confirm(`Are you sure you want to delete book with ID ${id}?`)) {
        try {
            await axios.delete(`${API_URL}/${id}`);
            alert('Book deleted successfully');
            fetchBooks();
        } catch (error) {
            console.error('Error deleting book:', error);
            alert(`Failed to delete book: ${error.response?.data?.detail || error.message}`);
        }
    }
}

function resetForm() {
    document.getElementById('book-form').reset();
    document.getElementById('book-id').value = '';
    document.getElementById('form-title').textContent = 'Create Book';
    document.getElementById('cancel-update').style.display = 'none';
    document.getElementById('quantity').value = 1;
}