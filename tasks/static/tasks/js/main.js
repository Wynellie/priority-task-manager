class Manager {
    #makeRequest = async (url, {csrf = null, body = null} = {}) => {
        const reqData = {
            method : 'POST',
            headers : {
                'X-Requested-With': 'XMLHttpRequest',
            }
        }

        if (body) reqData.body = body;
        else if (csrf) {reqData.headers['X-CSRFToken'] = csrf}

        const response = await fetch(url, reqData);

        return await response.json()
    }
    showNotification = async (mes) => {
        const notif = document.createElement('div');
        notif.className = 'notif';
        notif.innerHTML = mes;
        document.body.append(notif);
        notif.addEventListener('animationend', () => {notif.remove()});
    }
    
    async deleteTask(url, csrf){
        return await this.#makeRequest(url, {csrf});
    }
    async updateTask(url, body){
        return await this.#makeRequest(url, {body});
    }
    async createTask(url, body){
        return await this.#makeRequest(url, {body});
    }
}