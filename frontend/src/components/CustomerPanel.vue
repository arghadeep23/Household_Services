<template>
    <div class="customer-profile">
        <CustomerNavbar />
        <router-view />
    </div>
</template>
<script>
import CustomerNavbar from '@/components/CustomerNavbar.vue';
export default {
    name: "CustomerPanel",
    components: {
        CustomerNavbar
    }
};
</script>