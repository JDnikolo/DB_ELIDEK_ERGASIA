<template>
    <div>
        Common Research Field Pairings
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
            <table>
                <thead>
                    <th>Count</th>
                    <th>Field 1</th>
                    <th>Field 2</th>
                </thead>
                <tr v-for="(result, index) in results" :key="index">
                    <td>{{ result[0] }}</td>
                    <td>{{ result[1] }}</td>
                    <td>{{ result[2] }}</td>

                </tr>
            </table>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            active: true,
            inactive: true,
            results: [],
        };
    },
    methods: {
        getResults() {
            const path = `http://localhost:5000/fieldPairs?active=${this.active}&inactive=${this.inactive}`;
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
