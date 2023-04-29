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

function postNew(){
    const token = sessionStorage.getItem('jwt')
    if (token == null){
        return router.push({ name: 'login'})
    }
    const tokenParts = token.split('.')
    const payload = JSON.parse(atob(tokenParts[1]))
    const userid = payload['subject']
    let newPostForm = document.getElementById('newPostForm');
    let form_data = new FormData(newPostForm);
    fetch(`/api/v1/users/${userid}/posts`, {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value,
            'Authorization': `Bearer ${sessionStorage.getItem('jwt')}`
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
    <h2>Make A New Post</h2>
    <div v-if="success" class="alert alert-success">{{ successMessage }}</div>
    <div v-if="hasErrors" class="alert alert-danger">
        <ul>
            <li v-for="err in errors">{{ err }}</li>
        </ul>    
    </div>
    <form @submit.prevent="postNew" enctype="multipart/form-data" id="newPostForm">
        <div class="form-group mb-3">
            <label for="photo" class="form-label">Photo</label>
            <input type="file" name="photo" class="form-control" />
        </div>
        <div class="form-group mb-3">
            <label for="caption" class="form-label">Caption</label>
            <textarea name="caption" class="form-control" rows="3"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
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