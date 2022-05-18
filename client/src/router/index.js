import Vue from 'vue';
import Router from 'vue-router';
import Project from '../components/Ping.vue';
import Field from '../components/Fields.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/projects',
      name: 'Project_Page',
      component: Project,
    },
    {
      path: '/fields',
      name: 'Fields_Page',
      component: Field,
    },
  ],
});
