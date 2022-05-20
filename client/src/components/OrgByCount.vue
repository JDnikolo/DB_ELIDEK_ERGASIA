<template>
    <div>
        Organizations by Projects Acquired
        <div>
            In year:
            <select v-model="year" v-on:change="getResults">
                <option value=""></option>
                <option v-for="ayear in years" v-bind="ayear" :key="ayear">{{ ayear }}</option>
            </select>
            <label for="includeConsecutive">
                <input type="checkbox" id="includeConsecutive" v-model="consecutive" :disabled="year === ''"
                    v-on:change="getResults" />
                Include the consecutive year
            </label>
        </div>
        <div>
            Projects acquired (per year):
            <input v-model="num" placeholder="number" v-on:input="getResults">

            <label for="numberOverThan">
                <input type="checkbox" id="numberOverThan" v-model="more" :disabled="this.less"
                    v-on:change="getResults" />
                Or More
            </label>
            <label for="numberLessThan">
                <input type="checkbox" id="numberLessThan" v-model="less" :disabled="this.more"
                    v-on:change="getResults" />
                Or Less
            </label>
            <label for="equalInConsec">
                <input type="checkbox" id="equalInConsec" v-model="equalCons" :disabled="!consecutive"
                    v-on:change="getResults" />
                Equal Acquisitions over Consecutive Years?
            </label>
        </div>
        <div>
            <table>
                <thead>
                    <th>Organisation</th>
                    <th>Projects</th>
                </thead>
                <tr v-for="(result, index) in results" :key="index">
                    <td v-if="!consecutive">
                        {{ result[2] }}
                    </td>
                    <td v-if="!consecutive">
                        {{ result[0] }}
                    </td>
                    <td v-if="consecutive">
                        {{ result[3] }}
                    </td>
                    <td v-if="consecutive">
                        {{ result[0] + result[1] }}
                    </td>
                </tr>
            </table>
        </div>
    </div>
</template>

<script>
// TODO: format results, maybe some improvements?
import axios from 'axios';

export default {
    name: 'Organizations_by_Project_Count',
    data() {
        return {
            consecutive: false,
            equalCons: false,
            more: false,
            less: false,
            num: '',
            results: [],
            year: '',
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
        getResults() {
            let path = 'http://localhost:5000/byProjCount?';
            path += `more=${this.more}&less=${this.less}&`;
            path += `consecutive=${this.consecutive}&equal=${this.equalCons}&`;
            if (this.year !== '') {
                path += `year=${this.year}&`;
            }
            if (this.num !== '') {
                path += `num=${this.num}`;
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
