import { createRouter, createWebHistory } from 'vue-router';
import LoginForm from '@/components/LoginForm.vue';
import SignupProfessionalForm from '@/components/SignupProfessionalForm.vue';
import SignupCustomerForm from '@/components/SignupCustomerForm.vue';
import AdminPanel from '@/components/AdminPanel.vue';
import AdminHome from '@/components/AdminHome.vue';
import AdminSearch from '@/components/AdminSearch.vue';
import AdminSummary from '@/components/AdminSummary.vue';
import ProfessionalPanel from '@/components/ProfessionalPanel.vue';
import ProfessionalHome from '@/components/ProfessionalHome.vue';
import ProfessionalSearch from '@/components/ProfessionalSearch.vue';
import ProfessionalSummary from '@/components/ProfessionalSummary.vue';
import ProfessionalProfile from '@/components/ProfessionalProfile.vue';
import CustomerPanel from '@/components/CustomerPanel.vue';
import CustomerHome from '@/components/CustomerHome.vue';
import CustomerSearch from '@/components/CustomerSearch.vue';
import CustomerSummary from '@/components/CustomerSummary.vue';
import CustomerProfile from '@/components/CustomerProfile.vue';

const routes = [
    {
        path: '/',
        redirect: '/login',
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginForm,
    },
    {
        path: '/signup-professional',
        name: 'SignupProfessional',
        component: SignupProfessionalForm,
    },
    {
        path: '/signup-customer',
        name: 'SignupCustomer',
        component: SignupCustomerForm,
    },
    {
        path: '/admin',
        name: 'Admin',
        component: AdminPanel,
        children: [
            {
                path: '',
                name: 'AdminHome',
                component: AdminHome,
            },
            {
                path: 'search',
                name: 'AdminSearch',
                component: AdminSearch
            },
            {
                path: 'summary',
                name: 'AdminSummary',
                component: AdminSummary
            },
            {
                path: 'logout',
                name: 'Logout',
                beforeEnter: (to, from, next) => {
                    localStorage.removeItem('token');
                    next('/login');
                }
            }
        ]
    },
    {
        path: '/professional/:id',
        name: 'Professional',
        component: ProfessionalPanel,
        children: [
            {
                path: '',
                name: 'ProfessionalHome',
                component: ProfessionalHome,
            },
            {
                path: 'search',
                name: 'ProfessionalSearch',
                component: ProfessionalSearch
            },
            {
                path: 'summary',
                name: 'ProfessionalSummary',
                component: ProfessionalSummary
            },
            {
                path: 'logout',
                name: 'Logout',
                beforeEnter: (to, from, next) => {
                    localStorage.removeItem('token');
                    next('/login');
                }
            },
            {
                path: 'profile',
                name: 'ProfessionalProfile',
                component: ProfessionalProfile

            }
        ]
    },
    {
        path: '/customer/:id',
        name: 'Customer',
        component: CustomerPanel,
        children: [
            {
                path: '',
                name: 'CustomerHome',
                component: CustomerHome,
            },
            {
                path: 'search',
                name: 'CustomerSearch',
                component: CustomerSearch
            },
            {
                path: 'summary',
                name: 'CustomerSummary',
                component: CustomerSummary
            },
            {
                path: 'logout',
                name: 'Logout',
                beforeEnter: (to, from, next) => {
                    localStorage.removeItem('token');
                    next('/login');
                }
            },
            {
                path: 'profile',
                name: 'CustomerProfile',
                component: CustomerProfile
            }
        ]
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
