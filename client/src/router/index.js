import Vue from 'vue';
import Router from 'vue-router';
import Project from '../components/Ping.vue';
import Field from '../components/Fields.vue';
import OrgByCount from '../components/OrgByCount.vue';
import fieldPairs from '../components/FieldPairs.vue';
import Researchers from '../components/Researchers.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/projects',
      name: 'Project Search',
      component: Project,
    },
    {
      path: '/fields',
      name: 'Researchers & Projects by Field',
      component: Field,
    },
    {
      path: '/orgsByProjectNum',
      name: 'Organizations By Project Count',
      component: OrgByCount,
    },
    {
      path: '/fieldPairs',
      name: 'Common Research Field Pairs',
      component: fieldPairs,
    },
    {
      path: '/researchers',
      name: 'Researcher Search',
      component: Researchers,
    },
  ],
});
