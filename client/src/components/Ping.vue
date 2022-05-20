<template>
    <div>
        <div>
            <p>Projects : {{ msg.length }}</p>
            <p>Search Options:</p>
        </div>
        <div>
            Start Year:
            <select v-model="start_year" v-on:change="getMessage">
                <option value=""></option>
                <option v-for="year in years" v-bind="year" :key="year">{{ year }}</option>
            </select>
        </div>
        <div>
            End Year:
            <select v-model="end_year" v-on:change="getMessage">
                <option value=""></option>
                <option v-for="year in years" v-bind="year" :key="year">{{ year }}</option>
            </select>
        </div>
        <div>
            Project Duration(in years):
            <input v-model="dur" placeholder="duration" v-on:input="getMessage">

            <label for="durationOverThan">
                <input type="checkbox" id="durationOverThan" v-model="greater" :disabled="this.lesser"
                    v-on:change="getMessage" />
                Or More
            </label>
            <label for="durationLessThan">
                <input type="checkbox" id="durationLessThan" v-model="lesser" :disabled="this.greater"
                    v-on:change="getMessage" />
                Or Less
            </label>
        </div>
        <div>
            Funding: Min
            <input v-model="fund_min" placeholder="minimum" v-on:input="getMessage">
            Max
            <input v-model="fund_max" placeholder="maximum" v-on:input="getMessage">
        </div>
        <div>
            ELIDEK Administrator:
            <select v-model="admin" v-on:change="getMessage">
                <option value="">-</option>
                <option v-for="admin in allAdmins" :key="admin[0]" :value="admin[0]">{{ admin[1] }} {{ admin[2] }}
                </option>
            </select>
        </div>
        <div>
            Status
            <label for="selectActive">
                <input type="checkbox" id="selectActive" v-model="active" v-on:change="getMessage">
                Active
            </label>
            <label for="selectInactive">
                <input type="checkbox" id="selectInactive" v-model="inactive" v-on:change="getMessage">
                Inactive
            </label>
        </div>
        <div id="details" v-show="showInfo" v-on:click="showInfo = false" @keyup.escape="showInfo = false">
            <div>
                <p></p> Project: {{ this.nameShown }}<p></p>
            </div>
            <p>Director: {{ staff[0][0] }} {{ staff[0][1] }}</p>
            <p>Researchers:</p>
            <p v-for="(name, index) in staff[1]" :key="index"> {{ name[0] }} {{ name[1] }}
            </p>
        </div>
        <div v-show="!showInfo">___</div>
        <div></div>
        <table>
            <tr>
                <th>Title</th>
                <th>Summary</th>
                <th>Funds</th>
                <th>Start Date</th>
                <th>End Date</th>

            </tr>
            <tr v-for="project in msg" :key="project[0]" v-on:click="getStaff(project)">
                <td>{{ project[1] }}</td>
                <td>{{ project[2].substr(0, 50) }}...</td>
                <td>{{ project[3] }}</td>
                <td>{{ project[4].substr(5, 11) }}</td>
                <td>{{ project[5].substr(5, 11) }}</td>
            </tr>
        </table>
        <p v-for="project in msg" :key="project[0]">
            {{ project }}
            {{ project[0] }}
        </p>
    </div>
</template>
<script>
import axios from 'axios';

export default {
    name: 'Project_Page',
    data() {
        return {
            showInfo: false,
            active: true,
            inactive: true,
            fund_min: '',
            fund_max: '',
            greater: false,
            lesser: false,
            dur: 0,
            msg: '',
            admin: '',
            allAdmins: [],
            staff: [[], []],
            nameShown: '',
            start_year: '',
            end_year: '',
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
        getMessage() {
            this.showInfo = false;
            let path = `http://localhost:5000/ping?active=${this.active}&inactive=${this.inactive}&`;
            if (this.fund_min !== '' && this.fund_min > 0) {
                path += `fund_min=${this.fund_min}&`;
            }
            if (this.fund_max !== '') {
                path += `fund_max=${this.fund_max}&`;
            }
            if (this.admin !== '') {
                path += `admin=${this.admin}&`;
            }
            if (this.start_year !== '') {
                path += `start=${this.start_year}&`;
            }
            if (this.end_year !== '') {
                path += `end=${this.end_year}&`;
            }
            if (this.dur !== 0) {
                path += `duration=${this.dur}&greater=${this.greater}&lesser=${this.lesser}`;
            }
            axios.get(path)
                .then((res) => {
                    this.msg = res.data;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
        getAdmins() {
            const path = 'http://localhost:5000/admins';
            axios.get(path)
                .then((res) => {
                    this.allAdmins = res.data;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
        getStaff(project) {
            let path = 'http://localhost:5000/staff?';
            this.showInfo = false;
            let target = '';
            [target, this.nameShown] = project;
            const directorID = project[8];
            path += `project=${target}&director=${directorID}`;
            axios.get(path)
                .then((res) => {
                    this.staff = res.data;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
            this.showInfo = true;
        },
    },
    created() {
        this.getMessage();
        this.getAdmins();
    },
};
</script>
