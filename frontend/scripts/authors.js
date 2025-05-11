// frontend/scripts/authors.js
const API_URL = 'http://localhost:8000/api/authors';

document.addEventListener('DOMContentLoaded', () => {
    fetchAuthors();

    const form = document.getElementById('author-form');
    const cancelButton = document.getElementById('cancel-update');

    form.addEventListener('submit', handleSubmit);
    cancelButton.addEventListener('click', resetForm);
});

async function fetchAuthors() {
    try {
        const response = await axios.get(API_URL);
        const authors = response.data;
        const tbody = document.getElementById('authors-tbody');
        tbody.innerHTML = '';

        authors.forEach(author => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${author.id}</td>
                <td>${author.first_name}</td>
                <td>${author.last_name}</td>
                <td>${author.biography || 'N/A'}</td>
                <td>${new Date(author.created_at).toLocaleString()}</td>
                <td>${new Date(author.updated_at).toLocaleString()}</td>
                <td>
                    <button class="edit" onclick="editAuthor(${author.id})">Edit</button>
                    <button class="delete" onclick="deleteAuthor(${author.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching authors:', error);
        alert('Failed to fetch authors');
    }
}

async function handleSubmit(event) {
    event.preventDefault();

    const authorId = document.getElementById('author-id').value;
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const biography = document.getElementById('biography').value || null;

    const authorData = {
        first_name: firstName,
        last_name: lastName,
        biography: biography
    };

    try {
        if (authorId) {
            await axios.put(`${API_URL}/${authorId}`, authorData);
            alert('Author updated successfully');
        } else {
            await axios.post(API_URL, authorData);
            alert('Author created successfully');
        }
        resetForm();
        fetchAuthors();
    } catch (error) {
        console.error('Error saving author:', error);
        alert(`Failed to save author: ${error.response?.data?.detail || error.message}`);
    }
}

async function editAuthor(id) {
    try {
        const response = await axios.get(`${API_URL}/${id}`);
        const author = response.data;

        document.getElementById('author-id').value = author.id;
        document.getElementById('first-name').value = author.first_name;
        document.getElementById('last-name').value = author.last_name;
        document.getElementById('biography').value = author.biography || '';

        document.getElementById('form-title').textContent = 'Update Author';
        document.getElementById('cancel-update').style.display = 'inline';
    } catch (error) {
        console.error('Error fetching author:', error);
        alert('Failed to fetch author for editing');
    }
}

async function deleteAuthor(id) {
    if (confirm(`Are you sure you want to delete author with ID ${id}?`)) {
        try {
            await axios.delete(`${API_URL}/${id}`);
            alert('Author deleted successfully');
            fetchAuthors();
        } catch (error) {
            console.error('Error deleting author:', error);
            alert(`Failed to delete author: ${error.response?.data?.detail || error.message}`);
        }
    }
}

function resetForm() {
    document.getElementById('author-form').reset();
    document.getElementById('author-id').value = '';
    document.getElementById('form-title').textContent = 'Create Author';
    document.getElementById('cancel-update').style.display = 'none';
}