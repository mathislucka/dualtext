const preparePageChangeHandler = (routerInstance, routeName, routeParams) => (additionalRouteParams) => {
    routerInstance.push({
        name: routeName,
        params: { ...routeParams, ...additionalRouteParams }
    })
}

export { preparePageChangeHandler }