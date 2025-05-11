// frontend/scripts/users.js
const API_URL = 'http://localhost:8000/api/users';

document.addEventListener('DOMContentLoaded', () => {
    fetchUsers();

    const form = document.getElementById('user-form');
    const cancelButton = document.getElementById('cancel-update');

    form.addEventListener('submit', handleSubmit);
    cancelButton.addEventListener('click', resetForm);
});

async function fetchUsers() {
    try {
        const response = await axios.get(API_URL);
        const users = response.data;
        const tbody = document.getElementById('users-tbody');
        tbody.innerHTML = '';

        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.first_name}</td>
                <td>${user.last_name}</td>
                <td>${user.email}</td>
                <td>${user.is_active ? 'Yes' : 'No'}</td>
                <td>${new Date(user.registration_date).toLocaleString()}</td>
                <td>${new Date(user.updated_at).toLocaleString()}</td>
                <td>
                    <button class="edit" onclick="editUser(${user.id})">Edit</button>
                    <button class="delete" onclick="deleteUser(${user.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching users:', error);
        alert('Failed to fetch users');
    }
}

async function handleSubmit(event) {
    event.preventDefault();

    const userId = document.getElementById('user-id').value;
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const email = document.getElementById('email').value;
    const isActive = document.getElementById('is-active').checked;

    const userData = {
        first_name: firstName,
        last_name: lastName,
        email: email,
        is_active: isActive
    };

    try {
        if (userId) {
            await axios.put(`${API_URL}/${userId}`, userData);
            alert('User updated successfully');
        } else {
            await axios.post(API_URL, userData);
            alert('User created successfully');
        }
        resetForm();
        fetchUsers();
    } catch (error) {
        console.error('Error saving user:', error);
        alert(`Failed to save user: ${error.response?.data?.detail || error.message}`);
    }
}

async function editUser(id) {
    try {
        const response = await axios.get(`${API_URL}/${id}`);
        const user = response.data;

        document.getElementById('user-id').value = user.id;
        document.getElementById('first-name').value = user.first_name;
        document.getElementById('last-name').value = user.last_name;
        document.getElementById('email').value = user.email;
        document.getElementById('is-active').checked = user.is_active;

        document.getElementById('form-title').textContent = 'Update User';
        document.getElementById('cancel-update').style.display = 'inline';
    } catch (error) {
        console.error('Error fetching user:', error);
        alert('Failed to fetch user for editing');
    }
}

async function deleteUser(id) {
    if (confirm(`Are you sure you want to delete user with ID ${id}?`)) {
        try {
            await axios.delete(`${API_URL}/${id}`);
            alert('User deleted successfully');
            fetchUsers();
        } catch (error) {
            console.error('Error deleting user:', error);
            alert(`Failed to delete user: ${error.response?.data?.detail || error.message}`);
        }
    }
}

function resetForm() {
    document.getElementById('user-form').reset();
    document.getElementById('user-id').value = '';
    document.getElementById('form-title').textContent = 'Create User';
    document.getElementById('cancel-update').style.display = 'none';
    document.getElementById('is-active').checked = true;
}