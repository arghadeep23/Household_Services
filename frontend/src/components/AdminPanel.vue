<template>
    <div class="admin-panel">
        <AdminNavbar/>
        <router-view/>
    </div>
</template>

<script>
import AdminNavbar from '@/components/AdminNavbar.vue';
export default {
  name: "AdminPanel",
  components : {
    AdminNavbar
  }
};
</script>