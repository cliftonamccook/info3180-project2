<script setup>
    import { ref, computed, onMounted } from "vue";
    import {useRoute} from "vue-router";
    import router from '../router/index.js';
    import ProfileHeader from '../components/ProfileHeader.vue';
    import ProfileBody from "../components/ProfileBody.vue";

    var udata = ''

function getUserDetails(){
    const t = getparam()
    console.log(t)
    const token = sessionStorage.getItem('jwt')
    if (token == null){
        return router.push({ name: 'login'})
    }
    const tokenParts = token.split('.')
    const payload = JSON.parse(atob(tokenParts[1]))
    const userid = payload['subject']
    fetch(`/api/v1/users/${userid}`, {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${sessionStorage.getItem('jwt')}`
    }
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        udata = data
        console.log(udata)
        router.replace({ name: 'profile', params: { user_id: `${udata.id}` } })
     })
    .catch(function (error) {
        console.log(error);
    });
}


function getparam(){
    const route = useRoute()
    const id = computed(() => { return route.params.user_id})
    return id.value
}


onMounted(() => {
    getUserDetails();
    // console.log(getparam())
});
</script>

<template>
    <div class="container">
        <ProfileHeader v-bind:userdata="udata"></ProfileHeader>
        <ProfileBody v-bind:posts="udata.posts"></ProfileBody>
    </div>
</template>

<style scoped>
    .container {
        display: flex;
        flex-direction: column;
        row-gap: 30px;
    }
</style>