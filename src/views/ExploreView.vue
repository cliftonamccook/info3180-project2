<script setup>
  import { ref, onMounted } from "vue";
  import Post from '../components/Post.vue';
  import router from '../router/index.js';
  
    var hasErrors = ref("")
    var posts = ref([])

  function getPosts(){
    const token = sessionStorage.getItem('jwt')
    if (token == null){
        return router.push({ name: 'login'})
    }
    fetch("/api/v1/posts", {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('jwt')}`
        }
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        if (data) {
            hasErrors.value = false;
            posts.value = data
            console.log(data);
        }
        if (data.errors) {
            hasErrors.value = true;
            errors.value = data.errors;
            console.log(data.errors);
        }
    })
    .catch(function (error) {
        console.log(error);
    });
}


onMounted(() => {
    getPosts();
});
</script>

<template>
    <div id="post-page">
        <button id="new-post-button" @click="$router.push('/posts/new')">New Post</button>
        <div>
            <Post v-bind:post="post" v-for="post in posts" :key="post.id" />
        </div>
    </div>
</template>

<style scoped>
    #new-post-button {
        position: fixed;
        border: none;
        border-radius: 5px;
        height: 2.5em;
        width: 100px;
        margin: 0 auto;
        color: #fff;
        font-weight: bold;
        font-size: 1em;
        background: #6fb4e2;
        z-index: 5;
        right: 0;
    }
</style>