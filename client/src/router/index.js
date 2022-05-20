import Vue from 'vue';
import Router from 'vue-router';
import Project from '../components/Ping.vue';
import Field from '../components/Fields.vue';
import OrgByCount from '../components/OrgByCount.vue';
import fieldPairs from '../components/FieldPairs.vue';
import Researchers from '../components/Researchers.vue';
import AdminsByFunds from '../components/AdminByFunds.vue';
import NavPage from '../components/NavPage.vue';
import Programs from '../components/Programs.vue';
import View1 from '../components/View1ProjectResearcher.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Navigation_Page',
      component: NavPage,
    },
    {
      path: '/programs',
      name: 'ELIDEK_Programs',
      component: Programs,
    },
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
    {
      path: '/adminsByFunding',
      name: 'ELIDEK_Admins_By_Funding_Given',
      component: AdminsByFunds,
    },
    {
      path: '/projectPerResearcher',
      name: 'Projects_Per_Researcher_View',
      component: View1,
    },
  ],
});
