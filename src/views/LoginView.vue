<script setup>
  import { ref, onMounted } from "vue";
  import router from '../router/index.js'

  var success = ref("");
  var hasErrors = ref("");
  var errors = ref([]);

let csrf_token = ref("");

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
    })
}

function login(){
    let loginForm = document.getElementById('loginForm');
    let form_data = new FormData(loginForm);
    fetch("/api/v1/auth/login", {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value
        }
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        if (data.message) {
            success.value = true;
            hasErrors.value = false;
            sessionStorage.setItem('jwt', data.token)
            router.push({name: 'explore'})
            console.log(data);
        }
        if (data.errors) {
            hasErrors.value = true;
            success.value = false;
            errors.value = data.errors;
            console.log(data.errors);
            clearForm();
        }
    })
    .catch(function (error) {
        console.log(error);
    });
}

function clearForm(){
    var inputs = document.querySelectorAll('input');
    var textArea = document.querySelectorAll('textarea');
    inputs.forEach(input =>  input.value = '');
    textArea.forEach(input =>  input.value = '');
}

onMounted(() => {
    clearForm();
    getCsrfToken();
});

</script>

<template>
  <div class="form-container">
    <h2>Login</h2>
    <div v-if="hasErrors" class="alert alert-danger">
        <ul>
            <li v-for="err in errors">{{ err }}</li>
        </ul>    
    </div>
    <form @submit.prevent="login" id="loginForm">
        <div class="form-group mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="text" name="username" class="form-control" />
        </div>
        <div class="form-group mb-3">
        <label for="password" class="form-label">Password</label>
        <input name="password" class="form-control" type="password"/>
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
    </form>
    </div>
</template>

<style scoped>
  div.form-container {
        width: 400px;
        margin-left: 50px;
        margin-right: 50px;
        margin: auto;
    }
</style>
