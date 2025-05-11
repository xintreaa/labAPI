// frontend/scripts/borrowed-books.js
const API_URL = 'http://localhost:8000/api/borrowed-books';

document.addEventListener('DOMContentLoaded', () => {
    fetchBorrowedBooks();

    const form = document.getElementById('borrowed-book-form');
    const cancelButton = document.getElementById('cancel-update');

    form.addEventListener('submit', handleSubmit);
    cancelButton.addEventListener('click', resetForm);
});

async function fetchBorrowedBooks() {
    try {
        const response = await axios.get(API_URL);
        const borrowedBooks = response.data;
        const tbody = document.getElementById('borrowed-books-tbody');
        tbody.innerHTML = '';

        borrowedBooks.forEach(borrow => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${borrow.id}</td>
                <td>${borrow.book_id}</td>
                <td>${borrow.user_id}</td>
                <td>${new Date(borrow.borrow_date).toLocaleString()}</td>
                <td>${new Date(borrow.due_date).toLocaleString()}</td>
                <td>${borrow.return_date ? new Date(borrow.return_date).toLocaleString() : 'Not Returned'}</td>
                <td>${new Date(borrow.created_at).toLocaleString()}</td>
                <td>${new Date(borrow.updated_at).toLocaleString()}</td>
                <td>
                    <button class="edit" onclick="editBorrowedBook(${borrow.id})">Edit</button>
                    <button class="delete" onclick="deleteBorrowedBook(${borrow.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching borrowed books:', error);
        alert('Failed to fetch borrowed books');
    }
}

async function handleSubmit(event) {
    event.preventDefault();

    const borrowId = document.getElementById('borrowed-book-id').value;
    const bookId = parseInt(document.getElementById('book-id').value);
    const userId = parseInt(document.getElementById('user-id').value);
    const returnDate = document.getElementById('return-date').value || null;

    const borrowData = {
        book_id: bookId,
        user_id: userId,
        return_date: returnDate ? new Date(returnDate).toISOString() : null
    };

    try {
        if (borrowId) {
            await axios.put(`${API_URL}/${borrowId}`, { return_date: borrowData.return_date });
            alert('Borrowed book updated successfully');
        } else {
            await axios.post(API_URL, borrowData);
            alert('Book borrowed successfully');
        }
        resetForm();
        fetchBorrowedBooks();
    } catch (error) {
        console.error('Error saving borrowed book:', error);
        alert(`Failed to save borrowed book: ${error.response?.data?.detail || error.message}`);
    }
}

async function editBorrowedBook(id) {
    try {
        const response = await axios.get(`${API_URL}/${id}`);
        const borrow = response.data;

        document.getElementById('borrowed-book-id').value = borrow.id;
        document.getElementById('book-id').value = borrow.book_id;
        document.getElementById('user-id').value = borrow.user_id;
        document.getElementById('return-date').value = borrow.return_date ? borrow.return_date.split('T')[0] : '';

        document.getElementById('form-title').textContent = 'Update Borrow';
        document.getElementById('cancel-update').style.display = 'inline';
        document.getElementById('book-id').disabled = true;
        document.getElementById('user-id').disabled = true;
    } catch (error) {
        console.error('Error fetching borrowed book:', error);
        alert('Failed to fetch borrowed book for editing');
    }
}

async function deleteBorrowedBook(id) {
    if (confirm(`Are you sure you want to delete borrowed book record with ID ${id}?`)) {
        try {
            await axios.delete(`${API_URL}/${id}`);
            alert('Borrowed book record deleted successfully');
            fetchBorrowedBooks();
        } catch (error) {
            console.error('Error deleting borrowed book:', error);
            alert(`Failed to delete borrowed book: ${error.response?.data?.detail || error.message}`);
        }
    }
}

function resetForm() {
    document.getElementById('borrowed-book-form').reset();
    document.getElementById('borrowed-book-id').value = '';
    document.getElementById('form-title').textContent = 'Borrow a Book';
    document.getElementById('cancel-update').style.display = 'none';
    document.getElementById('book-id').disabled = false;
    document.getElementById('user-id').disabled = false;
}