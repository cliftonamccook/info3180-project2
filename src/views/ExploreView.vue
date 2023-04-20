<template>
  <div class="explore container">
    <h2>Explore</h2>
    <p>This is the explore page.</p>
  </div>
</template>

<script>
import { RouterLink } from "vue-router";
export default {
    name: "ExploreView"
}

const token = localStorage.getItem('token')
if (!token) {
  window.location.href = '/'
}
</script>
<style>
</style>
