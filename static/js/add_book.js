document.getElementById('book-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");

            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();

                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrfToken = getCookie('csrftoken');
  
    const response = await fetch('/api/books/add/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken,
        },
        body: formData
    });

    const data = await response.json();

    if (response.ok) {
        form.reset();

        const messageContainer = document.getElementById('django-messages');
        const msgDiv = document.createElement('div');
        msgDiv.className = 'alert alert-success alert-dismissible fade show';
        msgDiv.role = 'alert';
        msgDiv.innerHTML = `
            Książka została dodana!
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        messageContainer.appendChild(msgDiv);

        setTimeout(() => {
            msgDiv.classList.remove('show');
            setTimeout(() => msgDiv.remove(), 300);
        }, 3000);
    }
});

async function loadCategories() {
    try {
        const response = await fetch('/api/categories/');
        const data = await response.json();

        const select = document.getElementById('category');
        data.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.id;
            option.textContent = cat.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error("Błąd ładowania kategorii:", error);
    }
}
document.addEventListener('DOMContentLoaded', loadCategories);