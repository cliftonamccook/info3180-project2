<template>
    <div class="newpost-container">
        <form @submit.prevent="" id="newPostForm" action="Post" enctype="multipart/form-data">
            <div class="group">
                <label for="image">Photo</label>
                <input id="photo" name="photo" type="file" class="form-control">
            </div>
            
            <div class="group">
                <label for="caption">Caption</label>
                <textarea id="caption" name="caption" type="text" class="form-control" placeholder="Write a caption..."></textarea>
            </div>
            
            <div class="group button-div">
                <button @click="savePost" class="user-button" type="submit" value="submit">Submit</button>
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
      path: '/post/new',
      redirect: '/users/' // HERE
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
        caption: '',
        photo: ''
    };
},
name: "NewPostForm",
methods: {
    savePost() {
        let userForm = document.getElementById('newPostForm');
        let form_data = new FormData(userForm);
        form_data.append("caption", this.caption);
        form_data.append("photo", this.photo);
      
        fetch("/api/v1/users/<user_id>/posts", { // HERE
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
            if(data.message === "Posted."){
                this.$router.push('/users/');
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
    .newpost-container {
        width: 25%;
        height: fit-content;
        padding: 20px;

        margin: 2em auto 0 auto;
        background: #fff;
        border-radius: 5px;
    }

    form {
        display: flex;
        flex-direction: column;
        row-gap: 25px;
    }

    .group {
        display: flex;
        flex-direction: column;
        row-gap: 10px;
    }
    
    label {
        font-weight: bold;
    }

    #caption {
        height: 90px;
        resize: none;        
    }

    .button-div {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    button {
        border: none;
        border-radius: 5px;
        height: 2.5em;
        background: rgb(92, 221, 122);
        font-weight: bold;
        color: #fff;
        width: 100%
    }
</style>