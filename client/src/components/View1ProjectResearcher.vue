<template>
    <div>
        Projects per Researcher
        <div>
            Project Status:
            <label for="selectActive">
                <input type="checkbox" id="selectActive" v-model="active" v-on:change="getResults">
                Active
            </label>
            <label for="selectInactive">
                <input type="checkbox" id="selectInactive" v-model="inactive" v-on:change="getResults">
                Inactive
            </label>
        </div>
        <div>
            Sort By:
            <label for="byProj">
                <input type="checkbox" id="byProj" v-model="byProj" v-on:change="getResults" :disabled="this.byActive">
                Project Title
            </label>
            <label for="byActive">
                <input type="checkbox" id="byActive" v-model="byName" v-on:change="getResults" :disabled="this.byProj">
                Researcher Name
            </label>
        </div>
        <table>
            <thead>
                <th>Full Name</th>
                <th>Project Title</th>
                <th>Project Summary</th>
            </thead>
            <tr v-for="(result, index) in results" :key="index">
                <td>{{ result[2] }} {{ result[3] }}</td>
                <td>{{ result[4] }}</td>
                <td>{{ result[4].substr(0, 100) }}</td>
            </tr>
        </table>
        <div>{{ results }}</div>
    </div>
</template>

<script>
import axios from 'axios';
// path = 'http://localhost:5000/'
export default {
    name: 'Projects_by_Researcher',
    data() {
        return {
            active: true,
            inactive: true,
            byProj: false,
            byName: false,
            results: [],
        };
    },
    methods: {
        getResults() {
            let path = `http://localhost:5000/projectPerResearcher?active=${this.active}&inactive=${this.inactive}&`;
            if (this.byProj) {
                path += `byProj=${this.byProj}&`;
            }
            if (this.byName) {
                path += `byName=${this.byName}&`;
            }
            axios.get(path)
                .then((res) => {
                    this.results = res.data;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
    },
    created() {
        this.getResults();
    },
};
</script>
