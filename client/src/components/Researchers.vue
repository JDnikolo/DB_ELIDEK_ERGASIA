<template>
    <div>
        Researchers
        <div>
            Age in years:
            <input v-model="age" placeholder="age" v-on:input="getResults">

            <label for="durationOverThan">
                <input type="checkbox" id="durationOverThan" v-model="greater" :disabled="this.lesser"
                    v-on:change="getResults" />
                Or More
            </label>
            <label for="durationLessThan">
                <input type="checkbox" id="durationLessThan" v-model="lesser" :disabled="this.greater"
                    v-on:change="getResults" />
                Or Less
            </label>
        </div>
        <div>
            <label for="excludeWithoutD">
                <input type="checkbox" id="excludeWithoutD" v-model="exclude" v-on:change="getResults">
                Exclude Projects without Deliverables
            </label>
        </div>
        <div>Sort by:
            <label for="reverse">
                <input type="checkbox" id="reverse" v-bind="reverse" :disabled="!byProj && !byActive && !byAge"
                    v-on:change="reverseResults">Reverse order
            </label>
        </div>
        <label for="byProj">
            <input type="checkbox" id="byProj" v-model="byProj" v-on:change="getResults" :disabled="this.byActive">
            all projects they have worked on
        </label>
        <label for="byActive">
            <input type="checkbox" id="byActive" v-model="byActive" v-on:change="getResults" :disabled="this.byProj">
            active projects they are working on
        </label>
        <label for="byAge">
            <input type="checkbox" id="byAge" v-model="byAge" v-on:change="getResults">
            age
        </label>
        <table v-if="!byProj && !byActive">
            <thead>
                <th>Name</th>
                <th>Surname</th>
                <th>Age</th>
            </thead>
            <tr v-for="(result, index) in results" :key="index">
                <td>{{ result[1] }}</td>
                <td>{{ result[2] }}</td>
                <td>{{ result[3] }}</td>
            </tr>
        </table>
        <table v-if="byProj || byActive">
            <thead>
                <th>Projects:</th>
                <th>Name</th>
                <th>Surname</th>
                <th>Age</th>
            </thead>
            <tr v-for="(result, index) in results" :key="index">
                <td>{{ result[0] }}</td>
                <td>{{ result[1] }}</td>
                <td>{{ result[2] }}</td>
                <td>{{ result[3] }}</td>
            </tr>
        </table>
        <div>{{ results }}</div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Researcher_Search',
    data() {
        return {
            age: '',
            greater: false,
            lesser: false,
            exclude: false,
            reverse: false,
            byProj: false,
            byActive: false,
            byAge: false,
            results: [],
        };
    },
    methods: {
        getResults() {
            let path = 'http://localhost:5000/researchers?';
            if (this.age !== '') {
                path += `age=${this.age}&more=${this.greater}&less=${this.lesser}&`;
            }
            if (this.byProj) {
                path += `byProj=${this.byProj}&`;
            }
            if (this.byActive) {
                path += `byActive=${this.byActive}&`;
            }
            if (this.byAge) {
                path += `byAge=${this.byAge}&`;
            }
            if (this.exclude) {
                path += `exclude=${this.exclude}&`;
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
        reverseResults() {
            this.results.reverse();
        },
    },
    created() {
        this.getResults();
    },
};
</script>
