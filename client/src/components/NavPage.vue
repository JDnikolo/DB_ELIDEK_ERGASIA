<template>
    <div>
        <router-link to="/programs">ELIDEK Programs</router-link>
        <p></p>
        <router-link to="/projects">Project Search</router-link>
        <p></p>
        <router-link to="/projectPerResearcher">View 1: Projects per Researcher</router-link>
        <p></p>
        <router-link to="/fields">Researchers & Projects By Field</router-link>
        <p></p>
        <router-link to="/orgsByProjectNum">Organizations By Project Count</router-link>
        <p></p>
        <router-link to="/fieldPairs">Common Research Field Pairs</router-link>
        <p></p>
        <router-link to="/researchers">Researcher Search</router-link>
        <p></p>
        <router-link to="/adminsByFunding">ELIDEK Admins By Funding Given</router-link>
        <p></p>

    </div>
</template>

<script>

export default {
    name: 'Navigation_Page',
    data() {
        return {

        };
    },
    methods: {

    },
    created() {

    },
};
</script>
