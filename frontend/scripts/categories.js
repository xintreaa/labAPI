// frontend/scripts/categories.js
const API_URL = 'http://localhost:8000/api/categories';

document.addEventListener('DOMContentLoaded', () => {
    fetchCategories();

    const form = document.getElementById('category-form');
    const cancelButton = document.getElementById('cancel-update');

    form.addEventListener('submit', handleSubmit);
    cancelButton.addEventListener('click', resetForm);
});

async function fetchCategories() {
    try {
        const response = await axios.get(API_URL);
        const categories = response.data;
        const tbody = document.getElementById('categories-tbody');
        tbody.innerHTML = '';

        categories.forEach(category => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${category.id}</td>
                <td>${category.name}</td>
                <td>${category.description || 'N/A'}</td>
                <td>${new Date(category.created_at).toLocaleString()}</td>
                <td>${new Date(category.updated_at).toLocaleString()}</td>
                <td>
                    <button class="edit" onclick="editCategory(${category.id})">Edit</button>
                    <button class="delete" onclick="deleteCategory(${category.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching categories:', error);
        alert('Failed to fetch categories');
    }
}

async function handleSubmit(event) {
    event.preventDefault();

    const categoryId = document.getElementById('category-id').value;
    const name = document.getElementById('name').value;
    const description = document.getElementById('description').value || null;

    const categoryData = {
        name,
        description
    };

    try {
        if (categoryId) {
            await axios.put(`${API_URL}/${categoryId}`, categoryData);
            alert('Category updated successfully');
        } else {
            await axios.post(API_URL, categoryData);
            alert('Category created successfully');
        }
        resetForm();
        fetchCategories();
    } catch (error) {
        console.error('Error saving category:', error);
        alert(`Failed to save category: ${error.response?.data?.detail || error.message}`);
    }
}

async function editCategory(id) {
    try {
        const response = await axios.get(`${API_URL}/${id}`);
        const category = response.data;

        document.getElementById('category-id').value = category.id;
        document.getElementById('name').value = category.name;
        document.getElementById('description').value = category.description || '';

        document.getElementById('form-title').textContent = 'Update Category';
        document.getElementById('cancel-update').style.display = 'inline';
    } catch (error) {
        console.error('Error fetching category:', error);
        alert('Failed to fetch category for editing');
    }
}

async function deleteCategory(id) {
    if (confirm(`Are you sure you want to delete category with ID ${id}?`)) {
        try {
            await axios.delete(`${API_URL}/${id}`);
            alert('Category deleted successfully');
            fetchCategories();
        } catch (error) {
            console.error('Error deleting category:', error);
            alert(`Failed to delete category: ${error.response?.data?.detail || error.message}`);
        }
    }
}

function resetForm() {
    document.getElementById('category-form').reset();
    document.getElementById('category-id').value = '';
    document.getElementById('form-title').textContent = 'Create Category';
    document.getElementById('cancel-update').style.display = 'none';
}