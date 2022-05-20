<template>
    <div>
        ELIDEK Programs
        <div v-if="showProject">
            <p>Program Name: {{ program }}</p>
            <p>Projects:</p>
            <table>
                <tr>
                    <th>Title</th>
                    <th>Summary</th>
                    <th>Funds</th>
                    <th>Start Date</th>
                    <th>End Date</th>

                </tr>
                <tr v-for="project in projects" :key="project[0]">
                    <td>{{ project[1] }}</td>
                    <td>{{ project[2].substr(0, 100) }}...</td>
                    <td>{{ Intl.NumberFormat('el-GR', { style: 'currency', currency: 'EUR' }).format(project[3]) }}</td>
                    <td>{{ project[4].substr(5, 11) }}</td>
                    <td>{{ project[5].substr(5, 11) }}</td>
                </tr>
            </table>
        </div>
        <div>
            <table>
                <thead>
                    <th>Program Name</th>
                    <th>ELIDEK Division</th>
                </thead>
                <tr v-for="(result, index) in results" :key="index" v-on:click="getProjects(result)">
                    <td>{{ result[1] }}</td>
                    <td>{{ result[2] }}</td>
                </tr>
            </table>
        </div>
        <div>{{ projects }}</div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'ELIDEK_Programs',
    data() {
        return {
            results: [],
            showProject: false,
            program: '',
            projects: [],
        };
    },
    methods: {
        getResults() {
            const path = 'http://localhost:5000/programs';
            axios.get(path)
                .then((res) => {
                    this.results = res.data;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
        getProjects(program) {
            let a = '';
            [a, this.program] = program;
            const path = `http://localhost:5000/projectOfProgram?p_id=${program[0]}`;
            axios.get(path)
                .then((res) => {
                    this.projects = res.data;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
            this.showProject = true;
            a = 0;
            window.scrollTo(0, a);
        },
    },
    created() {
        this.getResults();
    },
};
</script>
