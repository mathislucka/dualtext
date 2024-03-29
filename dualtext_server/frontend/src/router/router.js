import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/authentication/Login.vue'
import Logout from '../components/authentication/Logout.vue'
import AnnotationDetail from './../views/annotation_detail/AnnotationDetail.vue'
import AnnotationDecider from './../views/annotation_detail/AnnotationDecider.vue'
import Dashboard from './../views/dashboard/Dashboard.vue'
import ProjectDetail from './../views/project_detail/ProjectDetail.vue'
import ExploreCorpora from './../views/explore_corpora/ExploreCorpora.vue'
import Search from '../store/Search.js'
import CorpusDetail from './../views/corpus_detail/CorpusDetail.vue'
import GroupDetail from './../views/group_detail/GroupDetail.vue'
import SharingDetail from './../views/sharing_detail/SharingDetail.vue'

const routes = [
    {
        path: '/corpus/:corpusId',
        name: 'corpus_detail',
        component: CorpusDetail,
        props: route => ({ corpusId: parseInt(route.params.corpusId) })
    },
    {
        path: '/dashboard',
        name: 'dashboard',
        component: Dashboard
    },
    {
        path: '/explore',
        name: 'explore_corpora',
        component: ExploreCorpora
    },
    {
        path: '/project/:projectId',
        name: 'project_detail',
        component: ProjectDetail,
        props: route => ({ projectId: parseInt(route.params.projectId) })
    },
    {
        path: '/project/:projectId/task/:taskId/annotation',
        name: 'annotation_decider',
        component: AnnotationDecider,
        beforeEnter: (to, from, next) => {
            if (from.name === 'annotation_detail' && from.params.taskId === to.params.taskId) {
                next({ name: 'project_detail', params: { projectId: to.params.projectId }})
            } else {
                next()
            }
        }
    },
    {
        path: '/project/:projectId/task/:taskId/annotation/:annotationId',
        name: 'annotation_detail',
        component: AnnotationDetail,
        beforeEnter: () => {
            Search.actions.resetSearchResults()
            return true
        }
    },
    {
        path: '/project/:projectId/task/:taskId/review',
        name: 'review_decider',
        component: AnnotationDecider,
        beforeEnter: (to, from, next) => {
            if (from.name === 'review_detail' && from.params.taskId === to.params.taskId) {
                next({ name: 'project_detail', params: { projectId: to.params.projectId }})
            } else {
                next()
            }
        }
    },
    {
        path: '/project/:projectId/task/:taskId/review/:annotationId',
        name: 'review_detail',
        component: AnnotationDetail,
    },
    {
        path: '/project/:projectId/task/:taskId/group-review',
        name: 'group_review_decider',
        component: AnnotationDecider,
        beforeEnter: (to, from, next) => {
            if (from.name === 'group_review_detail'  && from.params.taskId === to.params.taskId) {
                next({ name: 'project_detail', params: { projectId: to.params.projectId }})
            } else {
                next()
            }
        }
    },
    {
        path: '/project/:projectId/task/:taskId/group-review/:annotationGroupId',
        name: 'group_review_detail',
        component: GroupDetail,
        props: route => ({
            projectId: parseInt(route.params.projectId),
            taskId: parseInt(route.params.taskId),
            annotationGroupId: parseInt(route.params.annotationGroupId)
        })
    },
    {
        path: '/project/:projectId/task/:taskId/group',
        name: 'group_decider',
        component: AnnotationDecider,
        beforeEnter: (to, from, next) => {
            if (from.name === 'group_detail' && from.params.taskId === to.params.taskId) {
                next({ name: 'project_detail', params: { projectId: to.params.projectId }})
            } else {
                next()
            }
        }
    },
    {
        path: '/project/:projectId/task/:taskId/group/:annotationGroupId',
        name: 'group_detail',
        component: GroupDetail,
        props: route => ({
            projectId: parseInt(route.params.projectId),
            taskId: parseInt(route.params.taskId),
            annotationGroupId: parseInt(route.params.annotationGroupId)
        })
    },
        {
        path: '/share/project/:projectId/task/:taskId/annotation/:annotationId',
        name: 'sharing_detail',
        component: SharingDetail,
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
    },
    {
        path: '/logout',
        name: 'logout',
        component: Logout
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