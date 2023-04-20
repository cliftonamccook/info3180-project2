<template>
    <div class="log-container">
        <form @submit.prevent="saveUser" id="loginForm" action="Post" enctype="multipart/form-data">
            <div class="form-group mb-3">
                <label for="username">Username</label>
                <input v-model="title" name="username" type="text" class="form-control" placeholder="Enter username">
                <label for="password">Password</label>
                <input v-model="title" name="password" type="password" class="form-control" placeholder="Enter password">
                <button @click="" class="user-button" type="submit" value="submit">Submit</button>
            </div>
        </form>
    </div>
</template>
<script>
import { ref } from "vue";
// let csrf_token = ref("");
// let error = ref("");
// function getCsrfToken() {
//     fetch('/api/v1/csrf-token')
//         .then((response) => response.json())
//         .then((data) => {
//             csrf_token.value = data.csrf_token;
//         });
// }
export default {
data() {
    return {
    username: '',
    password: '',
    firstName: '',
    lastName: '',
    email: '',
    location: '',
    biography: '',
    image: null
    };
},
name: "LoginForm",
methods: {
    onSelect(event) {
    this.image = event.target.files[0];
    },
    saveUser() {
        let userForm = document.getElementById('loginForm');
        let form_data = new FormData(userForm);
        form_data.append("title", this.title);
        form_data.append("description", this.description);
        form_data.append("poster", this.poster);
        fetch("/api/v1/movies", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token.value
        },
        body: form_data
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            error.messages = data
        })
        .catch(error => {
            console.log(error);
        });
    }
}
// mounted() {
//     getCsrfToken();
// }
};
</script>
<style>
    .log-container{
        width: 25%;
        margin: 2em auto 0 auto;
        background: #fff;
        border-radius: 5px;
    }

    .form-group{
        display: flex;
        flex-direction: column;
        gap: 0.5em;
        width: 85%;
        margin: 0 auto;
        padding-top: 2em;
    }

    .user-button{
        border: none;
        border-radius: 5px;
        height: 2.5em;
        background: rgb(92, 221, 122);
        margin-top: 3em;
        margin-bottom: 2em;
        font-weight: bold;
        color: #fff;
    }

    label{
        font-weight: bold;
    }

</style>