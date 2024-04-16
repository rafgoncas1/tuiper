const { createApp } = Vue;

const app = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            username: null,
            password: null,
            errorMessage: null,
            successMessage: null,
            tuips: null,
            isLoading: true,
            newTuip: {title: null, content: null},
        }
    },

    mounted() {
        if (window.location.pathname == '/') {
            this.fetchTuips();
        }
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
        },
        fetchTuips() {
            fetch('/api/tuips')
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
                this.tuips = data;
                this.isLoading = false;
            })
            .catch(error => {
                this.errorMessage = error.message;
            });
        },
        postTuip() {
            fetch('/api/tuips', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({title: this.newTuip.title, content: this.newTuip.content})
            })
            .then(response => {
                if (response.status == 201) {
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
        likeDislikeTuip(tuipId) {
            const tuip = this.tuips.find(tuip => tuip.id == tuipId);
            if (tuip.like) {
                this.dislikeTuip(tuip);
            } else {
                this.likeTuip(tuip);
            }
        },
        likeTuip(tuip) {
            tuip.likes += 1;
            tuip.like = true;

            fetch('/api/like/' + tuip.id, {
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
            })
            .catch(error => {
                this.errorMessage = error.message;
            });
        },
        dislikeTuip(tuip) {
            tuip.likes -= 1;
            tuip.like = false;

            fetch('/api/like/' + tuip.id, {
                method: 'DELETE',
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
            })
            .catch(error => {
                this.errorMessage = error.message;
            });
        },
        isValidTuip() {
            if (this.newTuip.title == null || this.newTuip.content == null) {
                return false;
            }
            return this.newTuip.title.length >= 4 && this.newTuip.content.length >= 10;
        }
    }
};

const mounted = createApp(app).mount('#app')