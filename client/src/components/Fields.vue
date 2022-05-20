<template>
    <div>
        <div>
            <p>Projects & Researchers by Field</p>
        </div>
        <div>Select Field:
            <select v-model="selectedField" v-on:change="getResults">
                <option value="" disabled>-</option>
                <option v-for="(field, index) in allFields" :key="index">{{ field }}</option>
            </select>
        </div>
        <div>
            {{ selectedField }}
        </div>
        <div>
            Show:
            <label for="project">
                <input type="radio" id="project" value="project" v-model="mode" v-on:change="getResults">Projects
            </label>
            <label for="researcher">
                <input type="radio" id="researcher" value="researcher" v-model="mode"
                    v-on:change="getResults">Researchers
            </label>
        </div>
        <div>
            Date Since:
            <select v-model="since" v-on:change="getResults">
                <option value=""></option>
                <option v-for="year in years" v-bind="year" :key="year">{{ year }}</option>
            </select>
        </div>
        <div></div>
        <table v-show="mode === 'project'">
            <tr>
                <th>Title</th>
                <th>Summary</th>
                <th>Funds</th>
                <th>Start Date</th>
                <th>End Date</th>
            </tr>
            <tr v-for="project in results" :key="project[0]">
                <td>{{ project[1] }}</td>
                <td>{{ project[2].substr(0, 50) }}...</td>
                <td>{{ project[3] }}</td>
                <td>{{ project[4].substr(5, 11) }}</td>
                <td>{{ project[5].substr(5, 11) }}</td>
            </tr>
        </table>
        <table v-show="mode === 'researcher'">
            <thead>
                <th>Name</th>
                <th>Surname</th>
            </thead>
            <tr v-for="(result, index) in results" :key="index">
                <td>{{ result[1] }}</td>
                <td>{{ result[2] }}</td>
            </tr>
        </table>
    </div>
</template>

<script>
import axios from 'axios';
// TODO: Present Results
export default {
    name: 'Fields_Page',
    data() {
        return {
            mode: '',
            selectedField: '',
            allFields: [],
            results: [],
            since: '',
            years: [2050, 2049, 2048, 2047, 2046, 2045, 2044, 2043, 2042, 2041, 2040,
                2039, 2038, 2037, 2036, 2035, 2034, 2033, 2032, 2031, 2030,
                2029, 2028, 2027, 2026, 2025, 2024, 2023,
                2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015,
                2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006,
                2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997,
                1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988,
                1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979,
                1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970,
                1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961,
                1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950],
        };
    },
    methods: {
        getFields() {
            const path = 'http://localhost:5000/fields';
            axios.get(path)
                .then((res) => {
                    this.allFields = res.data;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
        getResults() {
            if (this.mode === '' || this.selectedField === '') {
                return;
            }
            let path = `http://localhost:5000/byField?mode=${this.mode}&name=${this.selectedField}`;
            if (this.since !== '') {
                path += `&since=${this.since}`;
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
        this.getFields();
    },

};
</script>
