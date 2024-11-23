<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Admin Panel</a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link to="/admin" class="nav-link" exact-active-class="active-link">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/search" class="nav-link" exact-active-class="active-link">Search</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/summary" class="nav-link" exact-active-class="active-link">Summary</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/logout" class="nav-link" exact-active-class="active-link">Logout</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "AdminNavbar",
};
</script>

<style scoped>
.navbar-brand {
  font-weight: bold;
}

.active-link {
  color: #ffffff !important;
  font-weight: bold;
}
</style>
