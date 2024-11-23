<template>
    <div class="professional-panel">
        <ProfessionalNavbar />
        <router-view />
    </div>
</template>
<script>
import ProfessionalNavbar from '@/components/ProfessionalNavbar.vue';
export default {
    name: "ProfessionalPanel",
    components: {
        ProfessionalNavbar
    }
};
</script>