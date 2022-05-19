<template>
    <div>
        ELIDEK Admins by Benefitting Organization and Funding Authorized
        <div>
            Organization:
            <select v-model="org" v-on:change="getResults">
                <option value="">-</option>
                <option v-for="admin in orgs" :key="admin[0]" :value="admin[0]">{{ admin[1] }}
                </option>
            </select>
        </div>
        <table>
            <thead>
                <th>#</th>
                <th>Admin Name</th>
                <th>Organisation Name</th>
                <th>Total Funds Authorized</th>
            </thead>
            <tr v-for="(result, index) in results" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ result[0] }} {{ result[1] }}</td>
                <td>{{ result[3] }}</td>
                <td>{{ Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(result[4]) }}</td>
            </tr>
        </table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'ELIDEK_Admins_By_Funds_Authorized',
    data() {
        return {
            results: [],
            org: '',
            orgs: [],
        };
    },
    methods: {
        getResults() {
            let path = 'http://localhost:5000/adminsByFunds?';
            if (this.org !== '') {
                path += `org=${this.org}&`;
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
        getOrganisations() {
            const path = 'http://localhost:5000/orgs';
            axios.get(path)
                .then((res) => {
                    this.orgs = res.data;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
    },
    created() {
        this.getOrganisations();
        this.getResults();
    },
};
</script>
