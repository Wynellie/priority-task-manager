class Manager {
    #makeRequest = async (url, csrf, form = null) => {
        const reqData = {
            method : 'POST',
            headers : {
                'X-Requested-With': 'XMLHttpRequest',
            }
        }

        if (form) {reqData.body = form}
        else {reqData.headers['X-CSRFToken'] = csrf}

        const response = await fetch(url, reqData);

        return response.json()
    }
    showNotification = async (mes) => {
        let notif = document.createElement('div');
        notif.className = 'notif';
        notif.innerHTML = mes;
        document.body.append(notif);
        notif.style.opacity = 0;
        notif.addEventListener('animationend', () => {notif.remove()});
    }
    
    async deleteTask(url, form, csrf){
        let response = this.#makeRequest(url, csrf);
        response.then((json) => {
            if (json.status == 'ok'){
                form.closest('.task-card').remove();
            }
        })
        return response;
    }
    async updateTask(url, form){
        // довольно странно отправлять null всегда вторым аргументом, хз
        return this.#makeRequest(url, null, form)
    }
    async createTask(url, form){
        let response = this.#makeRequest(url, null, form);
        response.then((json) => {
            this.showNotification(json.message);
        })
        return 
    }
}