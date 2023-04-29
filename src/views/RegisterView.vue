<script setup>
  import { ref, onMounted } from "vue";
  var success = ref("");
  var successMessage = ref("")
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

function register(){
    let registerForm = document.getElementById('registerForm');
    let form_data = new FormData(registerForm);
    fetch("/api/v1/register", {
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
            successMessage = data.message
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
    <h2>Register</h2>
    <div v-if="success" class="alert alert-success">{{ successMessage }} Go to Login page.</div>
    <div v-if="hasErrors" class="alert alert-danger">
        <ul>
            <li v-for="err in errors">{{ err }}</li>
        </ul>    
    </div>
    <form @submit.prevent="register" enctype="multipart/form-data" id="registerForm">
        <div class="form-group mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="text" name="username" class="form-control" />
        </div>
        <div class="form-group mb-3">
        <label for="password" class="form-label">Password</label>
        <input name="password" class="form-control" type="password"/>
        </div>
        <div class="form-group mb-3">
        <label for="firstname" class="form-label">Firstname</label>
        <input type="text" name="firstname" class="form-control" />
        </div>
        <div class="form-group mb-3">
        <label for="lastname" class="form-label">Lastname</label>
        <input type="text" name="lastname" class="form-control" />
        </div>
        <div class="form-group mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" name="email" class="form-control" />
        </div>
        <div class="form-group mb-3">
        <label for="location" class="form-label">Location</label>
        <input type="text" name="location" class="form-control" />
        </div>
        <div class="form-group mb-3">
        <label for="biography" class="form-label">Biography</label>
        <textarea name="biography" class="form-control" rows="3"></textarea>
        </div>
        <div class="form-group mb-3">
        <label for="photo" class="form-label">Photo</label>
        <input type="file" name="photo" class="form-control" />
        </div>
        <button type="submit" class="btn btn-primary">Register</button>
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
