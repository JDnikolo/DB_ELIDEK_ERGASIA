<template>
    <div>
        Projects, grades and evaluators
        <div>
            <div>
                Search Project Names:
                <label for="name">
                    <input id="name" v-model="name" placeholder="enter a name here" v-on:input="getResults">
                </label>
            </div>
            Sort By: <label for="reverse">
                <input type="checkbox" id="reverse" v-model="reverse" :disabled="!byProj && !byGrade && !byName"
                    v-on:change="reverseResults">Reverse order
            </label>
            <div>
                <label for="byProj">
                    <input type="checkbox" id="byProj" v-model="byProj" v-on:change="getResults">
                    Project Title
                </label>
                <label for="byGrade">
                    <input type="checkbox" id="byGrade" v-model="byGrade" v-on:change="getResults">
                    Grade
                </label>
                <label for="byName">
                    <input type="checkbox" id="byName" v-model="byName" v-on:change="getResults">
                    Evaluating Researcher Name
                </label>
            </div>
        </div>
        <table>
            <thead>
                <th>Project Title</th>
                <th>Grade</th>
                <th>Evaluating Researcher</th>
            </thead>
            <tr v-for="(result, index) in results" :key="index">
                <td>{{ result[3] }}</td>
                <td>{{ result[4] }}</td>
                <td>{{ result[5] }} {{ result[6] }}</td>
            </tr>
        </table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Project_grade_and_evaluator',
    data() {
        return {
            name: '',
            byName: false,
            byGrade: false,
            byProj: false,
            reverse: false,
            results: [],
        };
    },
    methods: {
        getResults() {
            let path = 'http://localhost:5000/projectGradeEvaluators?';
            if (this.name !== '') {
                path += `name=${this.name}&`;
            }
            if (this.byProj) {
                path += `byProj=${this.byProj}&`;
            }
            if (this.byName) {
                path += `byName=${this.byName}&`;
            }
            if (this.byGrade) {
                path += `byGrade=${this.byGrade}&`;
            }
            axios.get(path)
                .then((res) => {
                    this.results = res.data;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
            this.reverse = false;
        },
        reverseResults() {
            this.results.reverse();
        },
    },
    created() {
        this.getResults();
    },
};
</script>
