<script setup>
    const props = defineProps(['post'])
</script>

<template>
    <div id="post-container" class="mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title" @click="$router.push({ name: 'profile', params: { user_id: `${post.user_id}` } })">{{ post.username }}</h5>
            <img v-bind:src="post.photo" class="card-img" alt="...">
            <p class="card-text">{{ post.caption }}</p>
            <div id="likes-date">
                <p class="card-text"><small class="text-muted">{{ post.likes }} likes</small></p>
                <p class="card-text"><small class="text-muted">{{ post.created_on }}</small></p>
            </div>
          </div>
        </div>
    </div>
</template>

<style scoped>
    #post-container {
        width: 500px;
        margin: auto;
    }

    #likes-date {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }

    img {
        width: 100%;
        height: auto;
        object-fit: fill;
    }
</style>