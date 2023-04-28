<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Photogram</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/profile">My Profile</RouterLink>
            </li>
            <li class="nav-item">
              <button class="nav-link" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { ref, onMounted } from "vue";

let csrf_token = ref("");
let error = ref("");

const getCsrfToken = () => {
  fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    });
};

const logout = () => {
  fetch('/api/v1/auth/logout', {
    method: "POST",
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
    .then(response => {
      return response.json();
    })
    .then(data => {
      if(data.message === "User successfully logged out.") {
        localStorage.removeItem('token');
        window.location.href = '/'
      }
      error.messages = data;
    })
    .catch(error => {
      console.log(error);
    });
};

onMounted(() => {
  getCsrfToken();
});
</script>

<style>
/* Add any component specific styles here */
</style>
