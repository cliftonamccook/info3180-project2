<template>
    <div class="reg-container">
        <form @submit.prevent="saveUser" id="registerForm" action="Post" enctype="multipart/form-data">
            <div class="form-group mb-3">
                <label for="username">Username</label>
                <input v-model="title" name="username" type="text" class="form-control" placeholder="Enter username">
                <label for="password">Password</label>
                <input v-model="title" name="password" type="password" class="form-control" placeholder="Enter password">
                <label for="firstname">First Name</label>
                <input v-model="title" name="firstname" type="text" class="form-control" placeholder="Enter first name">
                <label for="lastname">Last Name</label>
                <input v-model="title" name="lastname" type="text" class="form-control" placeholder="Enter lastname">
                <label for="email">Email</label>
                <input v-model="title" name="email" type="text" class="form-control" placeholder="Enter email">
                <label for="email">Location</label>
                <input v-model="title" name="location" type="text" class="form-control" placeholder="Enter location">
                <label for="biography">Biography</label>
                <textarea v-model="description" name="biography" id="biography" cols="30" rows="10"></textarea>
                <label for="image">Photo</label>
                <input id="file" name="image" type="file" @change="onSelect" class="form-control">
                <button @click="" class="user-button" type="submit" value="submit">Submit</button>
            </div>
        </form>
    </div>
</template>
<script>
import { ref } from "vue";
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/register',
      redirect: '/login'
    }
  ]
})

let csrf_token = ref("");
let error = ref("");
function getCsrfToken() {
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            csrf_token.value = data.csrf_token;
        });
}
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
name: "RegisterForm",
methods: {
    onSelect(event) {
    this.image = event.target.files[0];
    },
    saveUser() {
        let userForm = document.getElementById('registerForm');
        let form_data = new FormData(userForm);
        form_data.append("username", this.username);
        form_data.append("password", this.password);
        form_data.append("firstname", this.firstName);
        form_data.append("lastname", this.lastName);
        form_data.append("email", this.email);
        form_data.append("location", this.location);
        form_data.append("biography", this.biography);
        form_data.append("photo", this.image);
        fetch("/api/v1/register", {
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
            if(data.message === "User successfully registered."){
                this.$router.push('/login');
            }
            error.messages = data
        })
        .catch(error => {
            console.log(error);
        });
    }
    },
    mounted() {
        getCsrfToken();
    }
};
</script>
<style>
    .reg-container{
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
        margin-bottom: 2em;
        font-weight: bold;
        color: #fff;
    }

    label{
        font-weight: bold;
    }

</style>