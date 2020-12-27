import { createRouter, createWebHistory } from 'vue-router'
import Login from './../components/login/Login.vue'
import AnnotationDetail from './../views/annotation_detail/AnnotationDetail.vue'
import Dashboard from './../views/dashboard/Dashboard.vue'
import ProjectDetail from './../views/project_detail/ProjectDetail.vue'
const routes = [
    {
        path: '/dashboard',
        name: 'dashboard',
        component: Dashboard
    },
    {
        path: '/project/:projectId',
        name: 'project_detail',
        component: ProjectDetail,
        props: route => ({ projectId: parseInt(route.params.projectId) })
    },
    {
        path: '/project/:projectId/task/:taskId/annotation/:annotationId',
        name: 'annotation_detail',
        component: AnnotationDetail,
        props: route => ({ projectId: parseInt(route.params.projectId), taskId: parseInt(route.params.taskId), annotationId: parseInt(route.params.annotationId) })
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
    },
    {
        path: '/',
        redirect: { name: 'dashboard' }
    }
  ]
  
  const router = createRouter({
    history: createWebHistory(),
    routes,
  })

  router.beforeEach((to, from) => {
    const token = sessionStorage.getItem('auth_token')
    return token || to.name === 'login' ? true : { name: 'login' }
  })

  export { router }