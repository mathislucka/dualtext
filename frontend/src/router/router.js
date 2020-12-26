import { createRouter, createWebHistory } from 'vue-router'
import Login from './../components/login/Login.vue'
import AnnotationDetail from './../views/annotation_detail/AnnotationDetail.vue'
import Dashboard from './../views/dashboard/Dashboard.vue'
const routes = [
    {
        path: '/dashboard',
        name: 'dashboard',
        component: Dashboard
    },
    {
        path: '/project',
        name: 'project_detail',
        component: Dashboard
    },
    {
        path: '/project/:projectId/task/:taskId/annotation/:annotationId',
        name: 'annotation_detail',
        component: AnnotationDetail,
        props: route => ({ projectId: parseInt(route.params.projectId), taskId: parseInt(route.params.taskId), annotationId: parseInt(route.params.annotationId) })
    },
    {
        path: '/',
        component: Login,
    },
  ]
  
  const router = createRouter({
    history: createWebHistory(),
    routes,
  })

  export { router }