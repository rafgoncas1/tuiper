const { createApp } = Vue;

const app = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            username: null,
            password: null,
            errorMessage: null,
            successMessage: null,
        }
    },

    mounted() {
        
    },

    methods: {
        login() {
            fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({username: this.username, password: this.password})
            })
            .then(response => {
                if (response.status == 200) {
                    
                    return response.json();
                } else {
                    return response.json().then(data => {
                        throw new Error(data.message);
                    });
                }
            })
            .then(data => {
                this.errorMessage = null;
                this.successMessage = data.message;
                setTimeout(function() {
                    window.location.href = '/';
                }, 2000);
            })
            .catch(error => {
                this.successMessage = null;
                this.errorMessage = error.message;
            });
        },

        logout() {
            fetch('/api/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.status == 200) {
                    return response.json();
                } else {
                    return response.json().then(data => {
                        throw new Error(data.message);
                    });
                }
            })
            .then(data => {
                this.errorMessage = null;
                this.successMessage = data.message;
                window.location.href = '/login';
            })
            .catch(error => {
                this.successMessage = null;
                this.errorMessage = error.message;
            });
        },
        register() {
            fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({username: this.username, password: this.password})
            })
            .then(response => {
                if (response.status == 200) {
                    return response.json();
                } else {
                    return response.json().then(data => {
                        throw new Error(data.message);
                    });
                }
            })
            .then(data => {
                this.errorMessage = null;
                this.successMessage = 'Registro exitoso. Redirigiendo a la página de inicio de sesión...'
                setTimeout(function() {
                    window.location.href = '/login';
                }, 2000);
            })
            .catch(error => {
                this.successMessage = null;
                this.errorMessage = error.message;
            });
        }
    }
};

const mounted = createApp(app).mount('#app')