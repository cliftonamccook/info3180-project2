<script setup>
import { onMounted } from 'vue';

    const props = defineProps(['userdata'])

// function getFollowers(id){
//     fetch(`/api/v1/users/${id}/follow`, {
//     method: 'GET',
//     headers: {
//         'Authorization': `Bearer ${sessionStorage.getItem('jwt')}`
//     }
//     })
//     .then(function (response) {
//         return response.json();
//     })
//     .then(function (data) {
//         document.getElementById('followers').innerText = data.followers
//      })
//     .catch(function (error) {
//         console.log(error);
//     });
// }


</script>

<template>
    <div id="header-container">
        <div id="user">
            <img v-bind:src="userdata.profile_photo" alt="..."/>
            <div id="user-details">
                <h5>{{ userdata.firstname }} {{ userdata.lastname }}</h5>
                <div>{{ userdata.location }}</div>
                <div>Member since {{ userdata.joined_on }}</div>
                <div>{{ userdata.biography }}</div>
            </div>
        </div>
        <div id="posts-followers-button">
            <div id="posts-followers">
                <div id="posts">
                    <div>Posts</div>
                    <div id="post-count">#</div>
                </div>
                <div id="followers">
                    <div>Followers</div>
                    <div id="follower-count">#</div>
                </div>
            </div>
            <div>
                <button id="follow-button">Follow</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
    img {
        width: 200px;
    }

    #follow-button {
        border: none;
        border-radius: 5px;
        height: 2.5em;
        width: 100%;
        margin: 0 auto;
        color: #fff;
        font-weight: bold;
        font-size: 1em;
        background: #6fb4e2;
  }

  #header-container {
    border: solid 1px black;
    padding: 20px;
    display: flex; 
    flex-direction: row; 
    justify-content: space-between; 
    width: 70%; 
    margin: auto; 
    flex-wrap: wrap;
  }

  #user {
    display: flex; 
    flex-direction: row; 
    column-gap: 20px;
  }

  #user-details, #followers, #posts-followers-button, #posts {
    display: flex; 
    flex-direction: column;
  }

  #posts-followers {
    display: flex; 
    flex-direction: row;
    column-gap: 20px;
  }

</style>