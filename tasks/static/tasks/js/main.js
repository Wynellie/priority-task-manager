class TaskManager {
    constructor() {
        this.init();
    }

    init() {
        document.addEventListener('click', (e) => {
            if (e.target.closest('.js-delete-btn')) {
                this.deleteTask(e);
            }
        });
    }

    async deleteTask(e) {
        e.preventDefault();
        const btn = e.target.closest('.js-delete-btn');
        const url = btn.dataset.url;
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrf
            }
        });

        const data = await response.json();
        if (data.status === 'ok') {
            btn.closest('.task-card').remove();
            // Тут можно вызвать метод показа уведомления
            this.showNotification(data.message);
        }
    }

    showNotification(text) {
        console.log("Уведомление:", text);
    }
}
